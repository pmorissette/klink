import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import klink


class SidebarTests(unittest.TestCase):
    def test_global_navigation_includes_hidden_and_visible_toctrees(self):
        for hidden in (False, True):
            with self.subTest(hidden=hidden), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                source = root / "source"
                source.mkdir()
                theme_path = str(Path(klink.__file__).parent.parent)
                (source / "conf.py").write_text(f"html_theme = 'klink'\nhtml_theme_path = [{theme_path!r}]\n")
                hidden_option = "   :hidden:\n" if hidden else ""
                (source / "index.rst").write_text(f"Home\n====\n\n.. toctree::\n{hidden_option}\n   guide\n   reference\n")
                (source / "guide.rst").write_text("Guide\n=====\n\nUsage.\n")
                (source / "reference.rst").write_text("Reference\n=========\n\nAPI.\n")

                result = subprocess.run(
                    [sys.executable, "-m", "sphinx", "-W", "-b", "html", str(source), str(root / "html")],
                    capture_output=True,
                    text=True,
                )

                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                for page in ("index", "guide"):
                    html = (root / "html" / f"{page}.html").read_text()
                    sidebar = re.search(r"<aside>(.*?)</aside>", html, re.DOTALL)
                    self.assertIsNotNone(sidebar)
                    self.assertIn('href="reference.html"', sidebar.group(1))
                    self.assertIn("Reference", sidebar.group(1))


if __name__ == "__main__":
    unittest.main()
