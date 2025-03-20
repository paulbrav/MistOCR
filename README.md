# mistocr

A command-line tool for OCR using the Mistral AI API, converting PDFs and PowerPoint files to markdown or text.

## Installation

### Install with `uv` (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver. If you don't have uv installed, you can install it with:

```bash
# Install uv
curl -fsSL https://astral.sh/uv/install.sh | sh
```

Then install mistocr globally:

```bash
# Clone the repository
git clone https://github.com/username/mistocr.git
cd mistocr

# Install mistocr globally with uv
uv pip install --system .
```

This will install the `mistocr` command globally on your system, making it available in your PATH so you can run it from anywhere.

### Verify Installation

After installation, verify that `mistocr` is correctly installed:

```bash
# Check the installed version
mistocr --version

# Check the location of the executable
which mistocr
```

### Alternative Installation Methods

If you don't want to use uv, you can install with standard pip:

```bash
pip install .
```

Or directly from GitHub:

```bash
pip install git+https://github.com/username/mistocr.git
```

## Requirements

- Python 3.7+
- Mistral AI API key (sign up at https://console.mistral.ai/)

## API Key Setup

On first run, you'll be prompted to enter your Mistral AI API key:

```bash
mistocr document.pdf -o output.md
# You'll see: "Mistral API key not found. You'll only need to enter this once."
```

The key will be stored securely using your system's keyring service, and you won't need to enter it again.

Alternatively, you can set the API key as an environment variable:

```bash
export MISTRAL_API_KEY=your_api_key_here
mistocr document.pdf -o output.md
```

## Usage

Basic usage:

```bash
mistocr document.pdf -o output.md
```

### Command Line Options

```
Usage: mistocr [OPTIONS] FILE

  Process documents using Mistral AI OCR API.

  FILE is the path to the document to process (PDF or PPTX).

Options:
  --version                       Show the version and exit.
  -o, --output PATH               Output file path. If not specified, output
                                  will be printed to stdout.
  -f, --format [markdown|text]    Output format (default: markdown)
  --pages TEXT                    Pages to process (e.g., "0,1,3-5"). Starts
                                  from 0.
  --images / --no-images          Include images in output (default: yes)
  --images-dir PATH               Directory to save extracted images instead of
                                  embedding them
  --help                          Show this message and exit.
```

### Examples

Process a PDF file and save the output as markdown:

```bash
mistocr document.pdf -o output.md
```

Process only specific pages:

```bash
mistocr presentation.pptx --pages "0,2-4" -o output.md
```

Extract images to a separate directory:

```bash
mistocr document.pdf --images-dir ./extracted_images -o output.md
```

Output plain text instead of markdown:

```bash
mistocr document.pdf -f text -o output.txt
```

## License

MIT License 