"""Check published paths, Markdown links, source syntax, hashes and ZIP integrity."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path, PurePosixPath
import posixpath
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def published_paths():
    result = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=ROOT, capture_output=True, check=True)
    return sorted(set(result.stdout.decode("utf-8").split("\0")) - {""})


def without_fences(text):
    return re.sub(r"^```.*?^```[^\n]*", "", text, flags=re.MULTILINE | re.DOTALL)


def heading_slugs(text):
    slugs, seen = set(), {}
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", without_fences(text), flags=re.MULTILINE):
        base = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        count = seen.get(base, 0)
        seen[base] = count + 1
        slugs.add(base if count == 0 else f"{base}-{count}")
    return slugs


def check_external(url):
    try:
        request = Request(url, headers={"User-Agent": "cybersecurity-operations-lab-link-check/1.0"})
        with urlopen(request, timeout=20) as response:
            return {"url": url, "status": response.status, "ok": 200 <= response.status < 400, "resolved_url": response.url}
    except Exception as error:
        return {"url": url, "ok": False, "error": str(error)}


def validate(external=False):
    paths = published_paths()
    path_set = set(paths)
    errors = []
    internal = 0
    external_urls = set()
    for name in paths:
        path = ROOT / name
        if not path.is_file():
            errors.append(f"Missing published file: {name}")
            continue
        if name.endswith(".py"):
            try:
                compile(path.read_bytes(), name, "exec")
            except (SyntaxError, UnicodeError) as error:
                errors.append(f"Syntax: {name}: {error}")
        if name.endswith(".md"):
            text = without_fences(path.read_text(encoding="utf-8"))
            for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", text):
                target = target.strip().strip("<>")
                parsed = urlsplit(target)
                if parsed.scheme in ("http", "https"):
                    external_urls.add(target)
                    continue
                if parsed.scheme:
                    errors.append(f"Unsupported link: {name}: {target}")
                    continue
                internal += 1
                joined = path.parent / unquote(parsed.path) if parsed.path else path
                resolved = joined.resolve()
                if not resolved.is_relative_to(ROOT):
                    errors.append(f"Link escapes repository: {name}: {target}")
                    continue
                relative = posixpath.normpath(posixpath.join(PurePosixPath(name).parent.as_posix(), unquote(parsed.path))) if parsed.path else name
                # Compare against Git's exact casing, even on Windows.
                if relative not in path_set:
                    errors.append(f"Missing or case-mismatched link: {name}: {target}")
                elif parsed.fragment:
                    if resolved.suffix != ".md" or unquote(parsed.fragment) not in heading_slugs(resolved.read_text(encoding="utf-8")):
                        errors.append(f"Unresolved fragment: {name}: {target}")

    hash_counts = {}
    for manifest, base in [(ROOT / "evidence/SOC-004/SHA256SUMS.txt", ROOT / "evidence/SOC-004"), (ROOT / "docs/historical-artifacts.sha256", ROOT)]:
        rows = manifest.read_text().splitlines()
        checked = 0
        for row in rows:
            if not row or row.startswith("#"):
                continue
            digest, name = row.split(maxsplit=1)
            target = base / name.strip()
            if not target.resolve().is_relative_to(ROOT) or not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != digest:
                errors.append(f"Hash mismatch: {manifest.relative_to(ROOT)}: {name}")
            else:
                checked += 1
        hash_counts[manifest.relative_to(ROOT).as_posix()] = checked
    if hash_counts["evidence/SOC-004/SHA256SUMS.txt"] != 10:
        errors.append("Original manifest must verify exactly ten artifacts")
    if hash_counts["docs/historical-artifacts.sha256"] != 32:
        errors.append("Historical publication inventory must verify exactly 32 artifacts")
    with zipfile.ZipFile(ROOT / "SOC-002-enhanced-original-evidence.zip") as archive:
        names = archive.namelist()
        expected = [f"evidence/SOC-002/{name}" for name in paths if name.startswith("SOC-002-0") and name.endswith(".png")]
        if sorted(names) != sorted(expected) or archive.testzip() is not None:
            errors.append("SOC-002 ZIP inventory or CRC failed")
        for member in names:
            if archive.read(member) != (ROOT / PurePosixPath(member).name).read_bytes():
                errors.append(f"ZIP member differs from root image: {member}")
    protected = json.loads((ROOT / "evidence/SOC-001/display-provenance.json").read_text())
    for key in ("source", "public_copy"):
        item = protected[key]
        if hashlib.sha256((ROOT / item["path"]).read_bytes()).hexdigest() != item["sha256"]:
            errors.append(f"Display provenance hash mismatch: {key}")
    unwanted = [name for name in paths if any(part in {"__pycache__", "private-evidence", "local-output", ".venv"} for part in PurePosixPath(name).parts) or name.endswith((".pyc", ".pcap", ".pcapng", ".journal"))]
    errors.extend(f"Publication hygiene: {name}" for name in unwanted)
    external_results = []
    if external:
        with ThreadPoolExecutor(max_workers=4) as pool:
            external_results = list(pool.map(check_external, sorted(external_urls)))
        errors.extend(f"External link unavailable: {item['url']}: {item.get('error', item.get('status'))}" for item in external_results if not item["ok"])
    return {"published_files": len(paths), "internal_link_occurrences": internal, "unique_external_urls": len(external_urls), "hash_counts": hash_counts, "soc002_zip_members": len(names), "python_syntax_files": sum(name.endswith(".py") for name in paths), "external_checks": external_results, "errors": errors, "status": "PASS" if not errors else "FAIL"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--external", action="store_true", help="Also issue read-only HTTP requests (network required)")
    parser.add_argument("--report", type=Path, help="Write a fresh JSON result outside historical evidence")
    args = parser.parse_args()
    result = validate(args.external)
    print(json.dumps(result, indent=2))
    if args.report:
        destination = args.report.resolve()
        historical = (ROOT / "evidence").resolve()
        if destination.is_relative_to(historical):
            parser.error("Reports must not be written into historical evidence")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    sys.exit(0 if result["status"] == "PASS" else 1)
