#!/usr/bin/env python3
"""Launcher guard checks. Runtime probes are fixtures, not native game evidence."""
import configparser
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import native_session as native


class NativeSessionChecks(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.session = self.root / "session"
        self.identity = {"game_path": str(self.root / "game"),
                         "compile_sha256": "unit-fixture",
                         "game_file_map_sha256": "unit-fixture",
                         "game_files": 1759, "save_lineage": "unit-fixture",
                         "native_acceptance": False,
                         "runtime_path": str(self.root / "scummvm"),
                         "runtime_sha256": "unit-fixture",
                         "runtime_version": "ScummVM 2026.3.0",
                         "soundfont_path": str(self.root / "FluidR3_GM.sf2"),
                         "soundfont_sha256": "unit-fixture"}

    def config(self):
        config = configparser.ConfigParser(interpolation=None)
        config.read(self.session / "scummvm.ini")
        return config

    def write_config(self, config):
        with (self.session / "scummvm.ini").open("w") as stream:
            config.write(stream)

    def test_exact_candidate_files(self):
        result = native.verify_game()
        self.assertEqual(result["game_files"], 1759)
        self.assertFalse(result["native_acceptance"])
        # Frozen R4 stage, independently recorded after the inline header repair.
        self.assertEqual(result["game_file_map_sha256"],
                         "1b705e851338597ba4ea3b5b811db90d12352379f5d232f3740eb09162e82017")

    def test_forged_stage_map_is_rejected(self):
        source = self.root / "campaign/source"
        source.mkdir(parents=True)
        shutil.copy(native.SOURCE.parent / "PUBLIC-MANIFEST.json", source.parent)
        shutil.copy(native.SOURCE / "BUILD-PROFILE.json", source)
        shutil.copytree(native.SOURCE / "src", source / "src")
        receipt = source / "build/coherent"
        receipt.mkdir(parents=True)
        shutil.copy(native.SOURCE / "build/coherent/compile-receipt.json", receipt)
        (source / "stage").mkdir()
        manifest = json.loads((native.SOURCE / "stage/GAME-MANIFEST.json").read_text())
        manifest["files"]["resource.map"]["sha256"] = "0" * 64
        (source / "stage/GAME-MANIFEST.json").write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, "file map differs"):
            native.verify_game(source)

    def test_existing_saves_and_configuration_are_preserved(self):
        record = native.create_session(self.session, self.identity)
        self.assertFalse(record["native_acceptance"])
        self.assertEqual(record["initial_save_files"], 0)
        marker = self.session / "saves/preservation-marker.txt"
        marker.write_bytes(b"opaque preservation sentinel")
        before = (self.session / "scummvm.ini").read_bytes()
        with self.assertRaises(FileExistsError):
            native.create_session(self.session, self.identity)
        self.assertEqual(marker.read_bytes(), b"opaque preservation sentinel")
        self.assertEqual((self.session / "scummvm.ini").read_bytes(), before)

    def test_resume_permits_benign_runtime_preferences(self):
        native.create_session(self.session, self.identity)
        config = self.config()
        config["scummvm"]["versioninfo"] = "2026.3.0"
        config["scummvm"]["lastselectedgame"] = "cakood-native"
        config["scummvm"]["fullscreen"] = "true"
        self.write_config(config)
        record = native.check_resume(self.session, self.identity)
        self.assertFalse(record["native_acceptance"])

    def test_resume_rejects_game_or_audio_changes(self):
        native.create_session(self.session, self.identity)
        for key, value, message in (("path", str(self.root / "another-game"), "path"),
                                    ("savepath", str(self.root / "old-saves"), "savepath"),
                                    ("music_driver", "adlib", "music_driver"),
                                    ("music_mute", "true", "muted")):
            config = self.config()
            config["cakood-native"][key] = value
            self.write_config(config)
            with self.assertRaisesRegex(ValueError, message):
                native.check_resume(self.session, self.identity)
            del config["cakood-native"][key]
            if key in ("path", "savepath"):
                config["cakood-native"][key] = (self.identity["game_path"] if key == "path"
                                                else str(self.session / "saves"))
            self.write_config(config)
        changed = dict(self.identity, game_file_map_sha256="another-candidate")
        with self.assertRaisesRegex(ValueError, "identity changed"):
            native.check_resume(self.session, changed)

    def test_runtime_capabilities_and_soundfont_are_required(self):
        runtime = self.root / "runtime-fixture"
        runtime.write_bytes(b"not a native runtime")
        font = self.root / "font-fixture.sf2"
        font.write_bytes(b"not a real soundfont")
        outputs = {"--version": "ScummVM 2026.3.0 (fixture)",
                   "--list-engines": "sci  SCI engine", "--list-audio-devices": "fluidsynth"}
        with patch.object(native.shutil, "which", return_value=str(runtime)), \
                patch.object(native, "probe", side_effect=lambda path, option: outputs[option]), \
                patch.object(native, "EXPECTED_SOUNDFONT", native.sha(font)):
            result = native.verify_runtime(runtime, font)
            self.assertEqual(result["runtime_sha256"], native.sha(runtime))
            for option, replacement, message in (("--version", "ScummVM 2.9.0", "stock ScummVM"),
                                                  ("--list-engines", "scumm  SCUMM engine", "lacks SCI"),
                                                  ("--list-audio-devices", "adlib", "lacks FluidSynth")):
                original = outputs[option]
                outputs[option] = replacement
                with self.assertRaisesRegex(ValueError, message):
                    native.verify_runtime(runtime, font)
                outputs[option] = original
            font.write_bytes(b"different font bytes")
            with self.assertRaisesRegex(ValueError, "SoundFont differs"):
                native.verify_runtime(runtime, font)


if __name__ == "__main__":
    unittest.main(verbosity=2)
