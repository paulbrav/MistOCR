"""
Formatter module for mistocr.

Converts OCR API responses to various output formats.
"""

import os
import base64
from pathlib import Path
from typing import Dict, List, Any, Optional


def format_as_markdown(
    ocr_response: Dict[str, Any],
    include_images: bool = True,
    output_dir: Optional[str] = None
) -> str:
    """
    Format the OCR response as markdown.
    
    Args:
        ocr_response: Response from the Mistral OCR API
        include_images: Whether to include images
        output_dir: Directory to save extracted images (if None, images are embedded)
        
    Returns:
        str: Markdown formatted text
    """
    if "error" in ocr_response:
        return f"Error: {ocr_response['error']}"
    
    pages = ocr_response.get("pages", [])
    if not pages:
        return "No content found in document."
    
    markdown_content = []
    
    for page in pages:
        page_index = page.get("index", 0)
        page_content = page.get("markdown", "")
        
        # Add page header
        markdown_content.append(f"## Page {page_index + 1}\n")
        
        # Add page content
        markdown_content.append(page_content)
        
        # Process images if present and requested
        if include_images and "images" in page and page["images"]:
            images = page["images"]
            for i, image in enumerate(images):
                image_id = image.get("id", f"image_{i}")
                
                if output_dir and "image_base64" in image:
                    # Save image to file
                    img_dir = Path(output_dir)
                    img_dir.mkdir(parents=True, exist_ok=True)
                    
                    img_filename = f"page_{page_index}_image_{i}.png"
                    img_path = img_dir / img_filename
                    
                    try:
                        with open(img_path, "wb") as f:
                            f.write(base64.b64decode(image["image_base64"]))
                        
                        # Add image reference to markdown
                        rel_path = os.path.relpath(img_path, os.getcwd())
                        markdown_content.append(f"\n![Image {i+1} from page {page_index+1}]({rel_path})\n")
                    except Exception as e:
                        markdown_content.append(f"\n[Error saving image: {str(e)}]\n")
                elif "image_base64" in image:
                    # Embed image directly in markdown
                    img_data = image["image_base64"]
                    markdown_content.append(f"\n![Image {i+1} from page {page_index+1}](data:image/png;base64,{img_data})\n")
        
        # Add a separator between pages
        markdown_content.append("\n---\n")
    
    return "\n".join(markdown_content)


def format_as_text(ocr_response: Dict[str, Any]) -> str:
    """
    Format the OCR response as plain text.
    
    Args:
        ocr_response: Response from the Mistral OCR API
        
    Returns:
        str: Plain text content
    """
    if "error" in ocr_response:
        return f"Error: {ocr_response['error']}"
    
    pages = ocr_response.get("pages", [])
    if not pages:
        return "No content found in document."
    
    text_content = []
    
    for page in pages:
        page_index = page.get("index", 0)
        # Remove markdown formatting for plain text
        page_content = page.get("markdown", "")
        
        # Simple markdown to text conversion
        # This is a basic implementation; could be enhanced
        page_content = page_content.replace("#", "").replace("*", "")
        
        text_content.append(f"--- Page {page_index + 1} ---\n")
        text_content.append(page_content)
        text_content.append("\n\n")
    
    return "\n".join(text_content) 