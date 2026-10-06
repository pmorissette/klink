import re
import subprocess
import sys
from pathlib import Path

import pytest

import klink

THEME = Path(klink.__file__).parent


def build(tmp_path, logo):
    source = tmp_path / "source"
    source.mkdir()
    theme_path = str(THEME.parent)
    (source / "conf.py").write_text(f"html_theme = 'klink'\nhtml_theme_path = [{theme_path!r}]\nhtml_theme_options = {{'logo': {logo!r}}}\n")
    (source / "index.rst").write_text("Home\n====\n\nText.\n")
    result = subprocess.run(
        [sys.executable, "-m", "sphinx", "-b", "html", str(source), str(tmp_path / "html")],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return (tmp_path / "html" / "index.html").read_text()


@pytest.mark.parametrize("logo", ["", "logo.png"])
def test_head_and_logo_spacing(tmp_path, logo):
    html = build(tmp_path, logo)
    assert "http://fonts.googleapis.com" not in html
    assert "https://fonts.googleapis.com/css?family=Open+Sans" in html
    assert "maximum-scale" not in html
    assert ('<body class="klink-has-logo">' in html) == bool(logo)


def test_styles():
    for asset in ("less/klink.less", "static/css/klink.css"):
        styles = (THEME / asset).read_text()
        assert "div#searchbox" not in styles
        assert "#searchbox {" in styles
        assert ".klink-has-logo div.documentwrapper" in styles

    css = (THEME / "static/css/klink.css").read_text()
    code = re.search(r"\.highlight pre \{([^}]*)\}", css).group(1)
    assert "white-space: pre;" in code
    assert "overflow-x: auto;" in code
    nested = re.search(r"\.klink-sidebar > ul > li ul \{([^}]*)\}", css).group(1)
    assert "list-style: none;" in nested
