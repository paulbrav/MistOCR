import base64
from pathlib import Path

import pytest

from mistocr.formatter import format_as_markdown, format_as_text


@pytest.fixture
def minimal_response():
    return {
        "pages": [
            {
                "index": 0,
                "markdown": "# Heading\nSome *text*.",
                "images": [
                    {
                        "id": "img1",
                        "image_base64": base64.b64encode(b"data").decode()
                    }
                ]
            }
        ]
    }


def test_format_as_markdown_embed(minimal_response):
    output = format_as_markdown(minimal_response, include_images=True)
    assert "## Page 1" in output
    assert "# Heading" in output
    assert "data:image/png;base64," in output


def test_format_as_markdown_save(tmp_path, minimal_response, monkeypatch):
    monkeypatch.chdir(tmp_path)
    out_dir = tmp_path / "imgs"
    output = format_as_markdown(minimal_response, include_images=True, output_dir=str(out_dir))
    img_path = out_dir / "page_0_image_0.png"
    assert img_path.exists()
    assert f"![Image 1 from page 1](imgs/page_0_image_0.png)" in output
    assert img_path.read_bytes() == b"data"


def test_format_as_text(minimal_response):
    output = format_as_text(minimal_response)
    assert "--- Page 1 ---" in output
    assert "Heading" in output
    assert "Some text." in output
