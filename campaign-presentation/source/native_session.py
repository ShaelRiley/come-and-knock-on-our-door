#!/usr/bin/env python3
"""Verify the frozen candidate and launch a private stock-ScummVM test session.

This does not automate gameplay, import saves, or establish native acceptance.
By default configuration, logs and saves stay in ignored build/native-sessions/.
"""
import argparse
import configparser
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import uuid

SOURCE = Path(__file__).resolve().parent
EXPECTED_VERSION = "2026.3.0"
EXPECTED_SOUNDFONT = "74594e8f4250680adf590507a306655a299935343583256f3b722c48a1bc1cb0"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_game(source=SOURCE):
    public = json.loads((source.parent / "PUBLIC-MANIFEST.json").read_text())
    profile = json.loads((source / "BUILD-PROFILE.json").read_text())
    receipt_path = source / "build/coherent/compile-receipt.json"
    require(sha(receipt_path) == public["compiled_receipt_sha256"],
            "Compile receipt differs from the checkpoint; rebuild the exact candidate.")
    receipt = json.loads(receipt_path.read_text())
    require(receipt["status"] == "PASS_FRESH_COMPILE" and
            receipt.get("complete_candidate") is True and
            receipt.get("diagnostic_traces") is False,
            "A complete candidate without diagnostic traces is required.")
    require(receipt["build_profile_sha256"] == sha(source / "BUILD-PROFILE.json"),
            "Build profile differs from the compiled candidate.")
    for row in receipt["modules"]:
        name = "main.sc" if row["module"] == 0 else f'module{row["module"]}.sc'
        require(sha(source / "src" / name) == row["source_sha256"],
                f"Source differs from the compiled candidate: {name}")
    stage = source / "stage"
    manifest = json.loads((stage / "GAME-MANIFEST.json").read_text())
    require(manifest["compile_sha256"] == public["compiled_receipt_sha256"],
            "Stage belongs to another compiled candidate.")
    require(profile["save_lineage"] == public["save_lineage"] and
            manifest["save_compatibility"].startswith(profile["save_lineage"] + ";"),
            "Stage save lineage differs from the checkpoint.")
    files = manifest["files"]
    map_sha = hashlib.sha256(json.dumps(files, sort_keys=True,
                                       separators=(",", ":")).encode()).hexdigest()
    require(map_sha == public["staged_game_file_map_sha256"],
            "Staged file map differs from the frozen candidate.")
    game = stage / "game"
    require({p.name for p in game.iterdir()} == set(files),
            "Game folder membership differs from the stage manifest.")
    for name, row in files.items():
        require(Path(name).name == name, "Invalid staged filename.")
        path = game / name
        require(path.is_file() and not path.is_symlink() and
                path.stat().st_size == row["bytes"] and sha(path) == row["sha256"],
                f"Game file differs from the frozen candidate: {name}")
    return {"game_path": str(game.resolve()),
            "compile_sha256": public["compiled_receipt_sha256"],
            "game_file_map_sha256": map_sha, "game_files": len(files),
            "save_lineage": profile["save_lineage"], "native_acceptance": False}


def probe(executable, option):
    result = subprocess.run([str(executable), option], capture_output=True,
                            text=True, timeout=20, check=False)
    require(result.returncode == 0, f"ScummVM capability check failed: {option}")
    return result.stdout + result.stderr


def verify_runtime(executable, soundfont):
    runtime = shutil.which(str(executable))
    require(runtime is not None, "ScummVM is unavailable; supply --scummvm PATH.")
    runtime = Path(runtime).resolve()
    version = probe(runtime, "--version")
    require(re.search(r"\bScummVM " + re.escape(EXPECTED_VERSION) + r"\b", version),
            f"Use stock ScummVM {EXPECTED_VERSION} for this frozen candidate.")
    engines = probe(runtime, "--list-engines")
    require(re.search(r"(?mi)^\s*sci\s", engines), "This ScummVM build lacks SCI.")
    devices = probe(runtime, "--list-audio-devices")
    require("fluidsynth" in devices.lower(), "This ScummVM build lacks FluidSynth.")
    require(soundfont is not None and soundfont.is_file(),
            "Supply the installed FluidR3_GM.sf2 with --soundfont PATH.")
    require(sha(soundfont) == EXPECTED_SOUNDFONT,
            "SoundFont differs from the FluidR3 GM used for this candidate.")
    return {"runtime_path": str(runtime), "runtime_sha256": sha(runtime),
            "runtime_version": version.strip(),
            "soundfont_path": str(soundfont.resolve()),
            "soundfont_sha256": EXPECTED_SOUNDFONT}


def create_session(session, identity):
    # Exclusive creation preserves every earlier test's saves and evidence.
    session.mkdir(parents=True, exist_ok=False)
    for name in ("saves", "screenshots"):
        (session / name).mkdir()
    config = configparser.ConfigParser(interpolation=None)
    config["scummvm"] = {"fullscreen": "false", "aspect_ratio": "true",
                          "music_driver": "fluidsynth",
                          "soundfont": identity["soundfont_path"],
                          "output_rate": "44100", "mute": "false",
                          "music_mute": "false", "music_volume": "192",
                          "sfx_volume": "192", "speech_volume": "192",
                          "autosave_period": "0"}
    config["cakood-native"] = {
        "description": "Come and Knock on Our Door (developer acceptance)",
        "engineid": "sci", "gameid": "sci-fanmade",
        "path": identity["game_path"], "savepath": str(session / "saves")}
    config_path = session / "scummvm.ini"
    with config_path.open("w") as stream:
        config.write(stream)
    record = dict(identity, created_utc=datetime.now(timezone.utc).isoformat(),
                  initial_save_files=0, config_sha256=sha(config_path),
                  status="PREPARED_NOT_LAUNCHED_NOT_ACCEPTED")
    (session / "SESSION.json").write_text(json.dumps(record, indent=2) + "\n")
    return record


def check_resume(session, identity):
    record = json.loads((session / "SESSION.json").read_text())
    for key, value in identity.items():
        require(record.get(key) == value, f"Session identity changed: {key}")
    require((session / "saves").is_dir(), "Session save folder is missing.")
    # ScummVM writes benign preferences on normal exit. Check effective launch
    # settings rather than rejecting those writes because the INI bytes changed.
    config = configparser.ConfigParser(interpolation=None)
    require(config.read(session / "scummvm.ini"), "Session configuration is missing.")
    expected = {"engineid": "sci", "gameid": "sci-fanmade",
                "path": identity["game_path"], "savepath": str(session / "saves")}
    for key, value in expected.items():
        require(config.get("cakood-native", key, fallback=None) == value,
                f"Session configuration changed: {key}")
    for key, value in {"music_driver": "fluidsynth",
                       "soundfont": identity["soundfont_path"],
                       "output_rate": "44100"}.items():
        actual = config.get("cakood-native", key,
                            fallback=config.get("scummvm", key, fallback=None))
        require(actual == value, f"Session audio configuration changed: {key}")
    for key in ("mute", "music_mute"):
        actual = config.get("cakood-native", key,
                            fallback=config.get("scummvm", key, fallback="false"))
        require(actual.lower() in ("false", "no", "0"), "Session audio is muted.")
    return record


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check-game", action="store_true",
                      help="verify candidate files without a native runtime")
    mode.add_argument("--launch", action="store_true",
                      help="launch stock ScummVM after all preflight checks")
    parser.add_argument("--scummvm", default="scummvm")
    parser.add_argument("--soundfont", type=Path)
    parser.add_argument("--session", type=Path)
    parser.add_argument("--resume", action="store_true",
                        help="reuse an identical existing session; load via the game UI")
    args = parser.parse_args(argv)
    try:
        require(args.launch or (args.session is None and not args.resume),
                "--session and --resume require --launch.")
        identity = verify_game()
        if args.check_game:
            print(json.dumps(dict(identity, status="PASS_EXACT_GAME_FILES_NOT_NATIVE")))
            return 0
        identity.update(verify_runtime(args.scummvm, args.soundfont))
        if not args.launch:
            print(json.dumps(dict(identity, status="PASS_PREFLIGHT_NOT_LAUNCHED")))
            return 0
        if sys.platform.startswith("linux"):
            require(bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")),
                    "Native launch needs a graphical desktop and visible app controls.")
        require(not args.resume or args.session is not None,
                "--resume requires the original --session PATH.")
        session = args.session
        if session is None:
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            session = SOURCE / "build/native-sessions" / (stamp + "-" + uuid.uuid4().hex[:8])
        session = session.resolve()
        if session.is_relative_to(SOURCE.parent.parent):
            require(session.is_relative_to(SOURCE / "build/native-sessions"),
                    "Keep repository-local native sessions under ignored build/native-sessions/.")
        if args.resume:
            check_resume(session, identity)
        else:
            create_session(session, identity)
        command = [identity["runtime_path"], f"--config={session / 'scummvm.ini'}",
                   f"--savepath={session / 'saves'}",
                   f"--screenshotpath={session / 'screenshots'}",
                   f"--logfile={session / 'scummvm.log'}", "cakood-native"]
        print("Native session:", session, flush=True)
        print("Use ordinary game controls; save through F2 and load through F3.", flush=True)
        print("Launching does not certify a complete campaign or native acceptance.", flush=True)
        return subprocess.run(command, check=False).returncode
    except (OSError, ValueError, KeyError, configparser.Error,
            subprocess.TimeoutExpired) as error:
        print(f"Native session blocked: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
