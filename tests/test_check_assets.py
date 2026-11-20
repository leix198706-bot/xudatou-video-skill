import base64
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import wave


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "skills/xudatou-handdrawn-video/scripts/check_assets.py"
PIXEL_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jBFsAAAAASUVORK5CYII="
)


class CheckAssetsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        self.persona = self.project / "人物项目"

    def check(self, *options):
        return subprocess.run(
            [sys.executable, str(CHECKER), *options],
            cwd=self.project, capture_output=True, text=True,
        )

    def make_path(self, relative):
        path = self.persona / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    def make_wav(self, relative):
        path = self.make_path(relative)
        with wave.open(str(path), "wb") as sample:
            sample.setparams((1, 2, 8000, 0, "NONE", "not compressed"))
            sample.writeframes(bytes(200))
        return path

    def test_missing_folder_reports_both_inputs(self):
        result = self.check()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("缺少人物参考", result.stdout)
        self.assertIn("缺少音色", result.stdout)

    def test_renamed_text_files_do_not_count_as_assets(self):
        self.make_path("人物参考/占位.png").write_text("占位", encoding="utf-8")
        self.make_path("音色/占位.wav").write_text("占位", encoding="utf-8")
        result = self.check()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("缺少人物参考", result.stdout)
        self.assertIn("缺少音色", result.stdout)

    def test_real_assets_are_found_in_nested_folders(self):
        self.make_path("人物参考/基准/全身.PNG").write_bytes(PIXEL_PNG)
        self.make_wav("音色/样音.WAV")
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("按需补充 水印、片尾、封面参考", result.stdout)

    def test_explicit_file_paths_can_reuse_an_existing_layout(self):
        self.make_path("我的图.png").write_bytes(PIXEL_PNG)
        voice = self.make_wav("我的音色.wav")
        result = self.check(str(self.persona), "--character", "我的图.png", "--voice", str(voice))
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
