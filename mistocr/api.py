"""
API module for mistocr.

Handles communication with the Mistral AI OCR API.
"""

import os
import requests
from typing import Dict, List, Optional, Any


MISTRAL_API_URL = "https://api.mistral.ai/v1/ocr"
DEFAULT_MODEL = "mistral-large-pdf"  # Use an appropriate model


def upload_file_to_mistral(file_path: str, api_key: str) -> Optional[str]:
    """
    Upload a file to Mistral API to get a document URL.
    
    Args:
        file_path: Path to the file to upload
        api_key: Mistral API key
        
    Returns:
        str: Document ID if successful, None otherwise
    """
    files_api_url = "https://api.mistral.ai/v1/files"
    
    try:
        with open(file_path, "rb") as f:
            file_content = f.read()
        
        filename = os.path.basename(file_path)
        files = {"file": (filename, file_content)}
        headers = {"Authorization": f"Bearer {api_key}"}
        
        response = requests.post(
            files_api_url,
            headers=headers,
            files=files
        )
        
        if response.status_code == 200:
            file_data = response.json()
            return file_data.get("id")
        else:
            print(f"Error uploading file: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"Error uploading file: {str(e)}")
        return None


def process_document(
    file_path: str,
    api_key: str,
    pages: Optional[List[int]] = None,
    include_images: bool = False,
) -> Dict[str, Any]:
    """
    Process a document with the Mistral OCR API.
    
    Args:
        file_path: Path to the document to process
        api_key: Mistral API key
        pages: Specific pages to process (None for all)
        include_images: Whether to include images in the response
        
    Returns:
        Dict containing the OCR results
    """
    file_id = upload_file_to_mistral(file_path, api_key)
    
    if not file_id:
        raise Exception("Failed to upload file")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": DEFAULT_MODEL,
        "document": {
            "type": "document_url",
            "document_url": file_id,
            "document_name": os.path.basename(file_path)
        },
        "include_image_base64": include_images,
    }
    
    if pages is not None:
        payload["pages"] = pages
    
    try:
        response = requests.post(
            MISTRAL_API_URL,
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return {"error": response.text}
    except Exception as e:
        return {"error": str(e)} 