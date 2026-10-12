# Evidence handling and publication

## Provenance categories

Reports label original supplied journal excerpts, user-reported observations, transcriptions, processed photographs, detector-derived output, synthetic fixtures, and AI illustrations separately. Synthetic timestamps and outputs belong to tests; they do not prove historical activity. Hash agreement proves byte agreement with a stated reference, not authentic acquisition or an uninterrupted chain of custody.

Historical evidence files, both historical detector sources, the original SOC-004 manifest, both validation JSON records, and the reported checksum transcript remain unchanged. The separate [historical artifact inventory](historical-artifacts.sha256) records 32 non-Markdown artifacts as published at main `2728239bf6f4dd942baf855ef6a9120e9959a256`. It adds byte-integrity coverage for existing photographs and the ZIP without extending or replacing the original ten-file manifest. It is a new publication snapshot, not a historical collection manifest. New tests and the accurately named MPO copy are outside both manifests; copy hashes are recorded separately.

## SOC-001 format and metadata

The [legacy original](../SOC-001-authentication-evidence.png) contains JPEG/MPO bytes despite its `.png` name. It has a color terminal frame and a second grayscale frame. Both decode; a suffix mismatch alone does not prove that browser display is broken.

The [accurately named MPO copy](../evidence/SOC-001/SOC-001-terminal-original.mpo) reuses the existing original repository blob. Its bytes, both frames and metadata are identical to the legacy file; no image processing or metadata stripping is performed. The [copy provenance record](../evidence/SOC-001/display-provenance.json) records both paths and hashes, detected format and frame dimensions. The case report displays the established legacy image path and provides the correctly suffixed copy for download. This addresses the format mismatch while preserving the original link and bytes.

The existing public original retains camera/device/software and capture-time metadata. No GPS EXIF fields were found in either frame during the audit or remediation inspection. Its metadata is not used to infer the journal timezone. Both public copies retain metadata and visible host/account information. Preserving the original public bytes also preserves metadata in current files and Git history; this sprint does not claim to remove it retroactively. A future metadata-stripped derivative would need a separate documented conversion and publication review.

The [archived AI illustration](../SOC-001-illustrative-reconstruction.png) is retained for historical transparency, with its `dodo[6559]` transcription error documented in the case report. It has no embedded illustration label and must stay accompanied by the provenance caption. It is removed from the report's evidence display.

## Future collections

Store raw journals, private PCAPs and unedited original photographs outside the repository. Record the actual tool/package versions, absolute start/end time and offset, commands, exit statuses, acquisition operator, and SHA256 values at acquisition. Preserve package verification stdout/stderr, version, and exit status; an empty display alone is not sufficient. For a private PCAP, an accurately labeled collection hash can be documented without publishing the capture itself. Do not invent missing historical values from a new collection.

Use separate public derivatives with documented processing and metadata review. Check visible content and every image frame for credentials, tokens, keys, personal/device metadata, addresses, account names and packet payloads. Publish only reviewed material in the authorized scope. The current SOC-002/SOC-003 PNGs are enhanced photographs; unedited originals and historical acquisition records are unavailable here. The SOC-003 PCAP remains private, with no historical hash or absolute collection timestamp supplied.

## Publication checklist

- Identify provenance and limitations for every new artifact; distinguish newly proposed commands from actual execution.
- Keep collection outputs in `private-evidence/` or outside the checkout. `.gitignore` reduces accidental publication; it does not sanitize a file or untrack an existing file.
- Review staged paths and contents, including all binary frames and archive members. Do not use `git add -f` to bypass the private-output rules.
- Run the [SOC-004 tests](../tests/SOC-004/README.md) and [repository validator](../scripts/validate_repository.py). Preserve original bytes and both manifests.
- Review external link checks separately from local path/fragment checks. An available URL does not authenticate its content.
- Open a draft PR and hold it for user review. No merge authorization for this remediation has been given.

See the [reproduction guide](reproduction.md) for future collection examples and the [remediation record](documentation-remediation.md) for known gaps.
