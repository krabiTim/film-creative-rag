#!/usr/bin/env python3
"""
Film Creative RAG - PDF Mood Board Extractor
============================================
Extracts images and text from PDF mood boards
"""

import fitz  # PyMuPDF
import os
from pathlib import Path
from PIL import Image
import json

class MoodBoardExtractor:
    """Extract images and text from PDF mood boards"""
    
    def __init__(self, output_dir="outputs/extracted_images"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.extracted_data = {
            "images": [],
            "text_annotations": [],
            "metadata": {}
        }
    
    def extract_from_pdf(self, pdf_path, project_name="mood_board"):
        """Extract all images and text from PDF mood board"""
        try:
            print(f"🎨 Processing mood board: {pdf_path}")
            
            # Open PDF
            pdf_document = fitz.open(pdf_path)
            
            # Create project directory
            project_dir = self.output_dir / project_name
            project_dir.mkdir(exist_ok=True)
            
            total_images = 0
            
            # Process each page
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                
                # Extract images from page
                image_list = page.get_images(full=True)
                
                if image_list:
                    print(f"📄 Page {page_num + 1}: Found {len(image_list)} images")
                    
                    for img_index, img in enumerate(image_list):
                        # Extract image data
                        xref = img[0]
                        base_image = pdf_document.extract_image(xref)
                        image_bytes = base_image["image"]
                        image_ext = base_image["ext"]
                        
                        # Save image
                        image_filename = f"page_{page_num+1}_image_{img_index+1}.{image_ext}"
                        image_path = project_dir / image_filename
                        
                        with open(image_path, "wb") as image_file:
                            image_file.write(image_bytes)
                        
                        self.extracted_data["images"].append({
                            "filename": image_filename,
                            "page": page_num + 1,
                            "path": str(image_path)
                        })
                        
                        total_images += 1
                
                # Extract text annotations from page
                text_blocks = page.get_text("dict")
                annotations = []
                
                for block in text_blocks["blocks"]:
                    if "lines" in block:
                        for line in block["lines"]:
                            for span in line["spans"]:
                                text = span["text"].strip()
                                if text and len(text) > 3:
                                    annotations.append({
                                        "text": text,
                                        "font": span.get("font", "unknown"),
                                        "size": span.get("size", 0)
                                    })
                
                if annotations:
                    self.extracted_data["text_annotations"].extend(annotations)
            
            # Save metadata
            self.extracted_data["metadata"] = {
                "source_pdf": str(pdf_path),
                "project_name": project_name,
                "total_pages": len(pdf_document),
                "total_images": total_images,
                "extraction_complete": True
            }
            
            # Save extraction report
            report_path = project_dir / "extraction_report.json"
            with open(report_path, 'w') as f:
                json.dump(self.extracted_data, f, indent=2)
            
            pdf_document.close()
            
            print(f"✅ Extraction complete: {total_images} images extracted")
            print(f"📊 Report saved: {report_path}")
            
            return self.extracted_data
            
        except Exception as e:
            print(f"❌ PDF extraction failed: {e}")
            return None

def test_pdf_extraction():
    """Test PDF extraction"""
    print("🧪 Testing PDF mood board extraction...")
    extractor = MoodBoardExtractor()
    print("📋 PDF extraction engine ready for testing")
    return True

if __name__ == "__main__":
    test_pdf_extraction()
