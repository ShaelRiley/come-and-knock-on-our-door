#!/usr/bin/env python3
"""Stream a publication payload and nested ZIP/tar archives for private material.

Reports locations and rule names only; never prints a suspected credential.
This is a bounded technical inspection, not a legal-clearance certificate.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import tarfile
import tempfile
import zipfile

RULES = {
    "private-key": rb"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----",
    "github-token": rb"(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})",
    "aws-access-key": rb"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b",
    "bearer-credential": rb"(?i)authorization[\"'\s:]+bearer\s+[A-Za-z0-9._~+/=-]{24,}",
    "url-credential": rb"(?i)https?://[^\s/<>\"':]{2,}:[^\s/<>\"']{4,}@",
    "literal-secret": rb"(?i)(?:api[_-]?key|client[_-]?secret|access[_-]?token|password|passwd)[\"'\s]*[:=][\s]*[\"'][^\r\n\"']{8,}[\"']",
}
PATTERNS = {name: re.compile(rule) for name, rule in RULES.items()}
PRIVATE_NAMES = re.compile(r"(?i)(?:^|/)(?:\.env(?:\.[^/]+)?|id_(?:rsa|ed25519)|scummvm\.ini|sci-fanmade\.[0-9]+)$")
ARCHIVES = (".zip", ".tar", ".tar.gz", ".tgz", ".tar.bz2", ".tbz2", ".tar.xz", ".txz")
UNSUPPORTED = (".7z", ".rar")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--git-tracked", action="store_true")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--max-bytes", type=int, default=4 * 1024**3)
    args = parser.parse_args()
    root = args.root.resolve()
    report = {"schema": "CAKOOD_RECURSIVE_PAYLOAD_REVIEW_V1", "status": "RUNNING",
              "scope": "technical pattern and private-file inspection; rights reviewed separately",
              "files": 0, "nested_members": 0, "archives": 0, "scanned_bytes": 0,
              "findings": [], "errors": [], "rules": list(PATTERNS), "sha256": {}}

    def problem(location, rule, offset=None):
        finding = {"location": location, "rule": rule}
        if offset is not None:
            finding["byte_offset"] = offset
        report["findings"].append(finding)

    def inspect(stream, location, name, depth=0, archive_size=None):
        if depth > 12:
            raise ValueError("nested archive depth exceeds 12")
        path = PurePosixPath(name)
        if path.is_absolute() or ".." in path.parts:
            problem(location, "unsafe-archive-path")
        if PRIVATE_NAMES.search(name):
            problem(location, "private-filename")
        lower = name.lower()
        if lower.endswith(UNSUPPORTED):
            raise ValueError("unsupported archive format")
        digest = hashlib.sha256()
        offset = 0
        previous = b""
        seen = set()
        with tempfile.TemporaryFile() as spool:
            is_archive = lower.endswith(ARCHIVES)
            while True:
                chunk = stream.read(1024 * 1024)
                if not chunk:
                    break
                report["scanned_bytes"] += len(chunk)
                if report["scanned_bytes"] > args.max_bytes:
                    raise ValueError("scan byte budget exhausted")
                digest.update(chunk)
                data = previous + chunk
                for rule, pattern in PATTERNS.items():
                    for match in pattern.finditer(data):
                        position = offset - len(previous) + match.start()
                        if (rule, position) not in seen:
                            seen.add((rule, position))
                            problem(location, rule, position)
                previous = data[-4096:]
                offset += len(chunk)
                if is_archive:
                    spool.write(chunk)
            report["sha256"][location] = digest.hexdigest()
            if not is_archive:
                return
            report["archives"] += 1
            spool.seek(0)
            if lower.endswith(".zip"):
                with zipfile.ZipFile(spool) as archive:
                    for member in archive.infolist():
                        if member.is_dir():
                            continue
                        if member.flag_bits & 1:
                            raise ValueError("encrypted archive member")
                        report["nested_members"] += 1
                        with archive.open(member) as child:
                            inspect(child, location + "!" + member.filename,
                                    member.filename, depth + 1, member.file_size)
            else:
                with tarfile.open(fileobj=spool, mode="r:*") as archive:
                    for member in archive:
                        if member.isdir():
                            continue
                        if not member.isfile():
                            problem(location + "!" + member.name, "archive-link-or-device")
                            continue
                        report["nested_members"] += 1
                        with archive.extractfile(member) as child:
                            inspect(child, location + "!" + member.name,
                                    member.name, depth + 1, member.size)

    if args.git_tracked:
        result = subprocess.run(["git", "ls-files", "-z"], cwd=root,
                                capture_output=True, check=True)
        paths = [root / s.decode() for s in result.stdout.split(b"\0") if s]
    elif root.is_file():
        paths = [root]
    else:
        paths = sorted(p for p in root.rglob("*") if p.is_file())
    for path in paths:
        location = path.name if root.is_file() else path.relative_to(root).as_posix()
        try:
            if path.is_symlink():
                problem(location, "filesystem-symlink")
                continue
            with path.open("rb") as stream:
                inspect(stream, location, location)
            report["files"] += 1
        except Exception as exc:
            report["errors"].append({"location": location, "error": type(exc).__name__ + ": " + str(exc)})
    report["status"] = "REVIEW_REQUIRED" if report["findings"] or report["errors"] else "PASS_TECHNICAL_SCAN"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "sha256"}))
    return 0 if report["status"] == "PASS_TECHNICAL_SCAN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
