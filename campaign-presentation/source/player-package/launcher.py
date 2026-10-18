#!/usr/bin/env python3
"""Launch the accepted player package with separate ScummVM settings and saves."""
import argparse
import configparser
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys

APP = "org.scummvm.ScummVM"
TARGET = "cakood"
AUDIO_APP_NAME = "Come and Knock on Our Door"
SOUNDFONT_SHA = "74594e8f4250680adf590507a306655a299935343583256f3b722c48a1bc1cb0"
RUNTIME_VERSION = "2026.3.0"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def map_sha(files):
    return hashlib.sha256(json.dumps(files, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def verify_package(package):
    manifest = json.loads((package / "GAME-MANIFEST.json").read_text())
    require(manifest.get("status") == "PASS_NATIVE_ACCEPTED_PLAYER_RELEASE"
            and manifest.get("native_acceptance") is True
            and manifest.get("genuine_campaign_acceptance") is True
            and manifest.get("release_eligible") is True,
            "This folder is not an accepted player release.")
    require(re.fullmatch(r"[0-9a-f]{40}", manifest["source_commit"]), "Invalid release source identity.")
    require(isinstance(manifest.get("save_lineage"), str) and manifest["save_lineage"], "Missing save lineage.")
    files = manifest["files"]
    require(map_sha(files) == manifest["accepted_game_file_map_sha256"], "Release game map identity differs.")
    game = package / "game"
    require({p.name for p in game.iterdir()} == set(files), "Game folder membership differs from this release.")
    for name, row in files.items():
        require(Path(name).name == name and name not in (".", ".."), "Invalid game filename.")
        path = game / name
        require(path.is_file() and not path.is_symlink() and path.stat().st_size == row["bytes"]
                and sha(path) == row["sha256"], "Game file differs: " + name)
    font = package / "runtime" / "FluidR3_GM.sf2"
    require(font.is_file() and not font.is_symlink() and sha(font) == SOUNDFONT_SHA,
            "The bundled FluidR3 GM SoundFont is missing or differs from the tested file.")
    return manifest


def runtime_base(executable=None):
    if executable:
        resolved = shutil.which(str(executable))
        require(resolved is not None, "ScummVM executable is unavailable: " + str(executable))
        return [str(Path(resolved).resolve())], False
    flatpak = shutil.which("flatpak")
    if flatpak:
        probe = subprocess.run([flatpak, "info", APP], capture_output=True, text=True, timeout=20)
        if probe.returncode == 0:
            return [flatpak, "run", "--command=scummvm", APP], True
    resolved = shutil.which("scummvm")
    require(resolved is not None, "Install ScummVM from Flathub: flatpak install flathub org.scummvm.ScummVM")
    return [str(Path(resolved).resolve())], False


def verify_runtime(base):
    outputs = {}
    for option in ("--version", "--list-engines", "--list-audio-devices"):
        result = subprocess.run(base + [option], capture_output=True, text=True, timeout=20)
        require(result.returncode == 0, "ScummVM capability probe failed: " + option)
        outputs[option] = result.stdout + result.stderr
    require(re.search(r"\bScummVM " + re.escape(RUNTIME_VERSION) + r"\b", outputs["--version"]),
            "This release was tested with stock ScummVM " + RUNTIME_VERSION + "; use that version.")
    require(re.search(r"(?mi)^\s*sci\s", outputs["--list-engines"]), "ScummVM lacks the SCI engine.")
    require("fluidsynth" in outputs["--list-audio-devices"].lower(), "ScummVM lacks FluidSynth music support.")


def default_data(manifest):
    configured = os.environ.get("XDG_DATA_HOME")
    base = Path(configured) if configured and Path(configured).is_absolute() else Path.home() / ".local" / "share"
    namespace = hashlib.sha256(manifest["save_lineage"].encode()).hexdigest()[:16]
    return base / "come-and-knock-on-our-door" / namespace


def configuration(package, data, existing=None):
    config = configparser.ConfigParser(interpolation=None)
    if existing is not None:
        config.read_string(existing)
    if "scummvm" not in config:
        config["scummvm"] = {"fullscreen": "false", "aspect_ratio": "true", "mute": "false",
                             "music_mute": "false", "music_volume": "192", "sfx_volume": "192",
                             "speech_volume": "192", "autosave_period": "0"}
    if TARGET not in config:
        config[TARGET] = {"description": "Come and Knock on Our Door", "engineid": "sci",
                          "gameid": "sci-fanmade"}
    # Change only this launcher's own target. Volume and presentation preferences survive.
    config[TARGET].update({"path": str(package / "game"), "savepath": str(data / "saves"),
                          "music_driver": "fluidsynth", "soundfont": str(package / "runtime" / "FluidR3_GM.sf2"),
                          "output_rate": "44100", "output_channels": "2", "joystick_num": "-1"})
    return config


def game_command(base, is_flatpak, package, data, fullscreen=False):
    command = list(base)
    if is_flatpak:
        command[-1:-1] = ["--socket=x11", "--nosocket=wayland", "--env=SDL_VIDEODRIVER=x11",
                           "--env=SDL_VIDEO_X11_XINPUT2=0", "--env=SDL_APP_NAME=" + AUDIO_APP_NAME,
                           "--filesystem=" + str(package) + ":ro",
                           "--filesystem=" + str(data) + ":rw"]
    command.extend(["--config=" + str(data / "scummvm.ini"), "--path=" + str(package / "game"),
                    "--savepath=" + str(data / "saves"), "--screenshotpath=" + str(data / "screenshots"),
                    "--logfile=" + str(data / "scummvm.log"), "--music-driver=fluidsynth",
                    "--soundfont=" + str(package / "runtime" / "FluidR3_GM.sf2"), "--output-rate=44100",
                    "--output-channels=2", "--joystick=-1", "--fullscreen" if fullscreen else "--no-fullscreen", TARGET])
    return command


def prepare_data(package, data, manifest):
    data.mkdir(parents=True, exist_ok=True)
    identity = data / "SAVE-LINEAGE.json"
    if identity.exists():
        require(json.loads(identity.read_text())["save_lineage"] == manifest["save_lineage"],
                "This save folder belongs to another build. Choose a separate --user-data folder.")
    else:
        require(not (data / "saves").exists() or not any((data / "saves").iterdir()),
                "Existing saves have no release identity. Choose an empty --user-data folder.")
        with identity.open("x") as stream:
            json.dump({"save_lineage": manifest["save_lineage"], "first_source_commit": manifest["source_commit"]}, stream, indent=2)
            stream.write("\n")
    for name in ("saves", "screenshots"):
        (data / name).mkdir(exist_ok=True)
    path = data / "scummvm.ini"
    config = configuration(package, data, path.read_text() if path.exists() else None)
    temporary = data / "scummvm.ini.pending"
    require(not temporary.exists(), "An earlier configuration write is pending: " + str(temporary))
    with temporary.open("x") as stream:
        config.write(stream)
    temporary.replace(path)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-only", action="store_true", help="verify package and runtime without launching or writing saves")
    parser.add_argument("--print-command", action="store_true", help="verify and show the launch command without starting the game")
    parser.add_argument("--user-data", type=Path, help="separate settings/saves folder (defaults to this release's user-data folder)")
    parser.add_argument("--scummvm", help="use a specific stock ScummVM executable instead of the installed Flatpak")
    parser.add_argument("--fullscreen", action="store_true", help="start full screen; windowed is the default")
    args = parser.parse_args(argv)
    try:
        package = Path(__file__).resolve().parent
        manifest = verify_package(package)
        base, is_flatpak = runtime_base(args.scummvm)
        verify_runtime(base)
        data = (args.user_data or default_data(manifest)).expanduser().resolve()
        require(not data.is_relative_to(package / "game"), "Keep saves outside the game data folder.")
        command = game_command(base, is_flatpak, package, data, args.fullscreen)
        if args.verify_only:
            print("PASS package identity and ScummVM SCI/FluidSynth requirements; no game launched.")
            return 0
        if args.print_command:
            print(shlex.join(command))
            return 0
        prepare_data(package, data, manifest)
        environment = dict(os.environ, SDL_VIDEO_X11_XINPUT2="0", SDL_APP_NAME=AUDIO_APP_NAME)
        os.execvpe(command[0], command, environment)
    except (OSError, ValueError, KeyError, configparser.Error, subprocess.TimeoutExpired) as error:
        print("Unable to launch: " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
