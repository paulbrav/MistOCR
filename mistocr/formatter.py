"""
Formatter module for mistocr.

Converts OCR API responses to various output formats.
"""

import os
import base64
import io
from pathlib import Path
from typing import Dict, List, Any, Optional
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from PIL import Image


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


def format_as_pdf(
    ocr_response: Dict[str, Any],
    output_path: str,
    include_images: bool = True
) -> None:
    """
    Format the OCR response as a PDF document.
    
    Args:
        ocr_response: Response from the Mistral OCR API
        output_path: Path to save the PDF file
        include_images: Whether to include images
        
    Returns:
        None
    """
    if "error" in ocr_response:
        raise ValueError(f"Error in OCR response: {ocr_response['error']}")
    
    pages = ocr_response.get("pages", [])
    if not pages:
        raise ValueError("No content found in document.")
    
    # Create a PDF document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    normal_style = styles['Normal']
    
    # Create a custom style for page headers
    page_header_style = ParagraphStyle(
        'PageHeader',
        parent=styles['Heading2'],
        textColor=colors.darkblue,
        spaceAfter=12
    )
    
    # Build document content
    content = []
    
    for page in pages:
        page_index = page.get("index", 0)
        page_content = page.get("markdown", "")
        
        # Add page header
        content.append(Paragraph(f"Page {page_index + 1}", page_header_style))
        content.append(Spacer(1, 0.2 * inch))
        
        # Convert markdown to paragraphs (simple conversion)
        # For a more complete markdown to PDF conversion, consider using a dedicated library
        paragraphs = page_content.split('\n\n')
        for para in paragraphs:
            if para.strip().startswith('#'):
                # Handle headers
                header_level = 0
                while para.strip()[header_level] == '#':
                    header_level += 1
                
                header_text = para.strip()[header_level:].strip()
                if header_level == 1:
                    content.append(Paragraph(header_text, styles['Heading1']))
                elif header_level == 2:
                    content.append(Paragraph(header_text, styles['Heading2']))
                else:
                    content.append(Paragraph(header_text, styles['Heading3']))
            else:
                # Regular paragraph
                content.append(Paragraph(para, normal_style))
                content.append(Spacer(1, 0.1 * inch))
        
        # Process images if present and requested
        if include_images and "images" in page and page["images"]:
            images = page["images"]
            for i, image in enumerate(images):
                if "image_base64" in image:
                    try:
                        # Decode base64 image
                        img_data = base64.b64decode(image["image_base64"])
                        img_io = io.BytesIO(img_data)
                        img = RLImage(img_io, width=6*inch, height=4*inch, kind='proportional')
                        
                        # Add image caption
                        content.append(Spacer(1, 0.2 * inch))
                        content.append(img)
                        content.append(Paragraph(f"Image {i+1} from page {page_index+1}", styles['Italic']))
                        content.append(Spacer(1, 0.2 * inch))
                    except Exception as e:
                        content.append(Paragraph(f"Error processing image: {str(e)}", styles['Italic']))
        
        # Add page separator
        content.append(Spacer(1, 0.5 * inch))
    
    # Build the PDF
    doc.build(content) 