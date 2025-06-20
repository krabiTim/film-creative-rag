#!/usr/bin/env python3
"""
Film Creative RAG - Upload System
================================
Handles file uploads with intelligent processing
"""

import os
import shutil
from pathlib import Path
from typing import Dict, Any
import mimetypes
import hashlib

class FilmUploadSystem:
    """Handle file uploads for Film Creative RAG"""
    
    def __init__(self, upload_dir="data/uploads"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        
        self.supported_formats = {
            "screenplay": [".fountain", ".fdx", ".txt", ".pdf"],
            "mood_board": [".pdf", ".zip"],
            "image": [".jpg", ".jpeg", ".png", ".bmp"]
        }
    
    def process_upload(self, file_path: str, project_name: str = None) -> Dict[str, Any]:
        """Process uploaded file"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            return {"error": f"File not found: {file_path}"}
        
        # Generate upload ID
        upload_id = self.generate_upload_id(file_path)
        
        # Detect file type
        file_type = self.detect_file_type(file_path)
        
        # Create project directory
        project_name = project_name or file_path.stem
        project_dir = self.upload_dir / project_name
        project_dir.mkdir(exist_ok=True)
        
        # Copy file
        destination = project_dir / file_path.name
        shutil.copy2(file_path, destination)
        
        # Process based on type
        if file_type == "screenplay":
            processing_result = self.process_screenplay(destination)
        elif file_type == "mood_board":
            processing_result = self.process_mood_board(destination)
        else:
            processing_result = {"processed": True, "type": "generic"}
        
        # Create upload record
        upload_record = {
            "upload_id": upload_id,
            "original_name": file_path.name,
            "file_type": file_type,
            "project_name": project_name,
            "stored_path": str(destination),
            "file_size": file_path.stat().st_size,
            "processing_result": processing_result
        }
        
        return upload_record
    
    def generate_upload_id(self, file_path: Path) -> str:
        """Generate unique upload ID"""
        content = f"{file_path.name}{file_path.stat().st_size}"
        return hashlib.md5(content.encode()).hexdigest()[:8]
    
    def detect_file_type(self, file_path: Path) -> str:
        """Detect file type from extension and content"""
        extension = file_path.suffix.lower()
        
        for file_type, extensions in self.supported_formats.items():
            if extension in extensions:
                return file_type
        
        return "unknown"
    
    def process_screenplay(self, file_path: Path) -> Dict[str, Any]:
        """Process screenplay file"""
        try:
            if file_path.suffix.lower() == '.pdf':
                content = self.extract_pdf_text(file_path)
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            
            # Basic analysis
            lines = content.split('\n')
            characters = set()
            scenes = 0
            
            for line in lines:
                line = line.strip()
                if line.startswith(('INT.', 'EXT.')):
                    scenes += 1
                elif line.isupper() and len(line.split()) <= 3 and line:
                    characters.add(line)
            
            return {
                "content_length": len(content),
                "characters_found": list(characters)[:10],
                "scenes_count": scenes,
                "preview": content[:200] + "..." if len(content) > 200 else content
            }
            
        except Exception as e:
            return {"error": f"Screenplay processing failed: {e}"}
    
    def process_mood_board(self, file_path: Path) -> Dict[str, Any]:
        """Process mood board file"""
        try:
            if file_path.suffix.lower() == '.pdf':
                return self.process_pdf_mood_board(file_path)
            else:
                return {"processed": True, "type": "mood_board"}
        except Exception as e:
            return {"error": f"Mood board processing failed: {e}"}
    
    def process_pdf_mood_board(self, file_path: Path) -> Dict[str, Any]:
        """Process PDF mood board"""
        try:
            import fitz  # PyMuPDF
            
            doc = fitz.open(str(file_path))
            images_count = 0
            annotations = []
            
            for page in doc:
                images = page.get_images()
                images_count += len(images)
                
                text = page.get_text()
                if text.strip():
                    annotations.append(text.strip())
            
            doc.close()
            
            return {
                "images_found": images_count,
                "annotations_count": len(annotations),
                "annotations_preview": annotations[:3]
            }
            
        except Exception as e:
            return {"error": f"PDF processing failed: {e}"}
    
    def extract_pdf_text(self, file_path: Path) -> str:
        """Extract text from PDF"""
        try:
            import fitz
            
            doc = fitz.open(str(file_path))
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            
            return text
        except Exception as e:
            return f"PDF text extraction failed: {e}"

def test_upload_system():
    """Test upload system"""
    print("🧪 Testing Upload System...")
    
    uploader = FilmUploadSystem()
    print("📁 Upload system ready")
    
    return True

if __name__ == "__main__":
    test_upload_system()
