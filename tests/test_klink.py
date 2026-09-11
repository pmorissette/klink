from pathlib import Path
from unittest.mock import Mock

import pytest

import klink


def test_version_aliases():
    assert klink.__version_full__ == klink.__version__
    assert klink.VERSION == tuple(int(part) for part in klink.__version__.split("."))


def test_theme_setup():
    app = Mock()
    metadata = klink.setup(app)
    theme_directory = Path(klink.__file__).parent
    app.add_html_theme.assert_called_once_with("klink", theme_directory)
    assert metadata == {"parallel_read_safe": True, "parallel_write_safe": True}
    assert Path(klink.get_html_theme_path()) / "klink" == theme_directory
    for asset in ("theme.toml", "layout.html", "static/css/klink.css", "static/fonts/fontawesome-webfont.woff", "static/img/logo.png"):
        assert (theme_directory / asset).is_file()


@pytest.mark.parametrize("separator", ["/", "%5C"])
def test_convert_notebooks_preserves_outputs_and_styles(tmp_path, monkeypatch, separator):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "_static").mkdir()
    (tmp_path / "example.ipynb").write_text("{}")
    outputs = tmp_path / "example_files"
    outputs.mkdir()
    (outputs / "plot.png").write_bytes(b"saved notebook image")
    export = tmp_path / "example.rst"
    export.write_text(f".. image:: example_files{separator}plot.png\n\n.. parsed-literal::\n\n   saved output\n\n.. raw:: html\n\n   <div>table</div>\n")
    convert = Mock(return_value=0)
    monkeypatch.setattr(klink, "call", convert)

    klink.convert_notebooks()

    convert.assert_called_once_with(["jupyter", "nbconvert", "--to", "rst", "*.ipynb"])
    assert (tmp_path / "_static" / "plot.png").read_bytes() == b"saved notebook image"
    assert not outputs.exists()
    assert export.read_text() == (
        ".. image:: _static/plot.png\n   :class: pynb\n\n"
        ".. parsed-literal::\n   :class: pynb-result\n\n   saved output\n\n"
        '.. raw:: html\n\n   <div class="pynb-result">table</div>\n'
    )


def test_convert_notebooks_reports_failure(monkeypatch):
    monkeypatch.setattr(klink, "call", Mock(return_value=1))
    with pytest.raises(SystemError, match="Conversion failed! Status was 1"):
        klink.convert_notebooks()
