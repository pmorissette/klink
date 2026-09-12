"""Build a Sphinx site using each installed distribution outside the checkout."""

import os
import subprocess
import sys
import venv
from pathlib import Path
from tempfile import TemporaryDirectory


def main():
    dist = Path("dist")
    wheels = sorted(dist.glob("*.whl"))
    sdists = sorted(dist.glob("*.tar.gz"))
    if not wheels or not sdists:
        raise SystemExit("Build both wheel and sdist with make dist first")

    for archive in wheels + sdists:
        with TemporaryDirectory(prefix="klink-dist-") as directory:
            root = Path(directory)
            environment = root / "venv"
            venv.EnvBuilder().create(environment)
            python = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
            subprocess.run(
                [sys.executable, "-m", "uv", "pip", "install", "--python", str(python), str(archive.resolve())],
                check=True,
                cwd=directory,
            )
            source = root / "source"
            source.mkdir()
            (source / "conf.py").write_text(
                "from importlib.metadata import version as _distribution_version\nimport klink\n"
                "assert klink.__version__ == _distribution_version('klink')\n"
                "project = 'Distribution test'\nhtml_theme = 'klink'\n",
                encoding="utf-8",
            )
            (source / "index.rst").write_text("Distribution test\n=================\n", encoding="utf-8")
            subprocess.run(
                [str(python), "-I", "-m", "sphinx", "-W", "-b", "html", str(source), str(root / "html")],
                check=True,
                cwd=directory,
            )
            assert "css/klink.css" in (root / "html" / "index.html").read_text(encoding="utf-8")
            for asset in ("css/klink.css", "fonts/fontawesome-webfont.woff", "img/logo.png"):
                assert (root / "html" / "_static" / asset).is_file(), asset
        print(f"Passed: {archive}", flush=True)


if __name__ == "__main__":
    main()
