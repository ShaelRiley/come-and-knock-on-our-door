"""Non-GUI launcher checks only; no campaign, hardware, or audio acceptance."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("cakood_launcher", ROOT / "player-package" / "launcher.py")
launcher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(launcher)


class LauncherChecks(unittest.TestCase):
    def test_empty_or_relative_xdg_data_home_uses_home(self):
        manifest = {"save_lineage": "TEST_FIXTURE_NOT_A_GAME"}
        for invalid in ("", "relative-folder"):
            with self.subTest(value=invalid), patch.dict(os.environ, {"XDG_DATA_HOME": invalid}):
                self.assertTrue(launcher.default_data(manifest).is_relative_to(Path.home() / ".local" / "share"))
        with patch.dict(os.environ, {"XDG_DATA_HOME": "/custom/user-data"}):
            self.assertTrue(launcher.default_data(manifest).is_relative_to(Path("/custom/user-data")))

    def test_flatpak_command_confines_access_and_disables_own_joystick(self):
        package, data = Path("/tmp/package with spaces"), Path("/tmp/private saves")
        command = launcher.game_command(["/usr/bin/flatpak", "run", "--command=scummvm", launcher.APP], True, package, data)
        self.assertEqual(command[command.index(launcher.APP) + 1], "--config=/tmp/private saves/scummvm.ini")
        self.assertIn("--filesystem=/tmp/package with spaces:ro", command)
        self.assertIn("--filesystem=/tmp/private saves:rw", command)
        self.assertIn("--joystick=-1", command)
        self.assertIn("--env=SDL_VIDEO_X11_XINPUT2=0", command)
        self.assertIn("--env=SDL_APP_NAME=" + launcher.AUDIO_APP_NAME, command)
        self.assertIn("--no-fullscreen", command)
        self.assertNotIn("--filesystem=home", command)
        self.assertNotIn("override", command)

        # Exercise the real main -> exec environment boundary with all external
        # effects mocked. Existing mute/volume/driver preferences stay untouched.
        original_environment = {"SDL_APP_NAME": "SDL Application", "PULSE_PROP": "fixture-preserve",
                                "SDL_AUDIO_DRIVER": "fixture-driver", "PULSE_SINK": "fixture-sink"}
        for flatpak in (False, True):
            base = ["/usr/bin/flatpak", "run", "--command=scummvm", launcher.APP] if flatpak else ["/usr/bin/scummvm"]
            with self.subTest(flatpak=flatpak), patch.dict(os.environ, original_environment), \
                    patch.object(launcher, "verify_package", return_value={"save_lineage": "TEST_FIXTURE_NOT_A_GAME"}), \
                    patch.object(launcher, "runtime_base", return_value=(base, flatpak)), \
                    patch.object(launcher, "verify_runtime"), patch.object(launcher, "prepare_data"), \
                    patch.object(launcher.os, "execvpe") as execute:
                launcher.main([])
                execute.assert_called_once()
                actual_command, environment = execute.call_args.args[1:]
                self.assertEqual(environment["SDL_APP_NAME"], "Come and Knock on Our Door")
                for key in ("PULSE_PROP", "SDL_AUDIO_DRIVER", "PULSE_SINK"):
                    self.assertEqual(environment[key], original_environment[key])
                self.assertEqual(os.environ["SDL_APP_NAME"], "SDL Application")
                if flatpak:
                    self.assertIn("--env=SDL_APP_NAME=Come and Knock on Our Door", actual_command)

    def test_own_configuration_preserves_preferences(self):
        config = launcher.configuration(Path("/new/package"), Path("/own/data"),
            "[scummvm]\nmusic_volume=87\nfullscreen=true\n[other-game]\npath=/personal\n[cakood]\nvoice_volume=69\n")
        self.assertEqual(config["scummvm"]["music_volume"], "87")
        self.assertEqual(config["scummvm"]["fullscreen"], "true")
        self.assertEqual(config["other-game"]["path"], "/personal")
        self.assertEqual(config["cakood"]["voice_volume"], "69")
        self.assertEqual(config["cakood"]["music_driver"], "fluidsynth")
        self.assertEqual(config["cakood"]["joystick_num"], "-1")

    def test_existing_saves_survive_repeat_setup_and_wrong_lineage_refused(self):
        with tempfile.TemporaryDirectory(dir=ROOT, prefix="launcher-fixture-") as directory:
            data = Path(directory) / "data"
            manifest = {"save_lineage": "TEST_FIXTURE_NOT_A_GAME", "source_commit": "a" * 40}
            launcher.prepare_data(Path("/package"), data, manifest)
            save = data / "saves" / "genuine-save.dat"
            save.write_bytes(b"preserve exact existing bytes")
            launcher.prepare_data(Path("/relocated-package"), data, manifest)
            self.assertEqual(save.read_bytes(), b"preserve exact existing bytes")
            with self.assertRaisesRegex(ValueError, "another build"):
                launcher.prepare_data(Path("/package"), data, dict(manifest, save_lineage="WRONG_FIXTURE"))
            self.assertEqual(save.read_bytes(), b"preserve exact existing bytes")

    def test_unidentified_saves_refused(self):
        with tempfile.TemporaryDirectory(dir=ROOT, prefix="launcher-fixture-") as directory:
            data = Path(directory)
            (data / "saves").mkdir()
            (data / "saves" / "old-save.dat").write_bytes(b"keep")
            with self.assertRaisesRegex(ValueError, "no release identity"):
                launcher.prepare_data(Path("/package"), data, {"save_lineage": "TEST_FIXTURE", "source_commit": "a" * 40})
            self.assertFalse((data / "SAVE-LINEAGE.json").exists())

    def test_release_manifest_rejects_candidate_and_changed_game(self):
        with tempfile.TemporaryDirectory(dir=ROOT, prefix="launcher-fixture-") as directory:
            package = Path(directory)
            (package / "game").mkdir()
            resource = package / "game" / "resource.map"
            resource.write_bytes(b"fixture bytes only, never a playable build")
            font = package / "runtime" / "FluidR3_GM.sf2"
            font.parent.mkdir()
            font.write_bytes(b"fixture font only")
            files = {resource.name: {"bytes": resource.stat().st_size, "sha256": launcher.sha(resource)}}
            manifest = {"status": "PASS_NATIVE_ACCEPTED_PLAYER_RELEASE", "native_acceptance": True,
                        "genuine_campaign_acceptance": True, "release_eligible": True, "source_commit": "a" * 40,
                        "save_lineage": "TEST_FIXTURE_NOT_A_GAME", "files": files,
                        "accepted_game_file_map_sha256": launcher.map_sha(files)}
            path = package / "GAME-MANIFEST.json"
            path.write_text(json.dumps(dict(manifest, native_acceptance=False)))
            with self.assertRaisesRegex(ValueError, "not an accepted"):
                launcher.verify_package(package)
            path.write_text(json.dumps(manifest))
            with patch.object(launcher, "SOUNDFONT_SHA", launcher.sha(font)):
                self.assertEqual(launcher.verify_package(package)["save_lineage"], "TEST_FIXTURE_NOT_A_GAME")
                resource.write_bytes(b"changed game data")
                with self.assertRaisesRegex(ValueError, "Game file differs"):
                    launcher.verify_package(package)


if __name__ == "__main__":
    unittest.main(verbosity=2)
