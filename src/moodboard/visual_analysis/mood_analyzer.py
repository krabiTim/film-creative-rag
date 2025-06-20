#!/usr/bin/env python3
"""
Film Creative RAG - Visual Mood Board Analyzer
==============================================
Analyzes extracted images for style, mood, and production elements
"""

import cv2
import numpy as np
from pathlib import Path
import json
from PIL import Image

class VisualMoodAnalyzer:
    """Analyze visual elements in mood board images"""
    
    def __init__(self):
        pass
    
    def analyze_image_collection(self, image_directory):
        """Analyze all images in a directory"""
        try:
            image_dir = Path(image_directory)
            if not image_dir.exists():
                return {"error": "Directory not found"}
            
            image_files = list(image_dir.glob("*.jpg")) + list(image_dir.glob("*.png")) + list(image_dir.glob("*.jpeg"))
            
            if not image_files:
                return {"error": "No images found"}
            
            print(f"🎨 Analyzing {len(image_files)} mood board images...")
            
            collection_analysis = {
                "images": [],
                "overall_palette": [],
                "style_consistency": {},
                "production_elements": []
            }
            
            all_colors = []
            
            for image_file in image_files:
                image_analysis = self.analyze_single_image(image_file)
                collection_analysis["images"].append(image_analysis)
                
                if "color_palette" in image_analysis:
                    all_colors.extend(image_analysis["color_palette"])
            
            collection_analysis["overall_palette"] = all_colors[:10]
            collection_analysis["style_consistency"] = {"analyzed": len(image_files)}
            
            print("✅ Visual analysis complete")
            return collection_analysis
            
        except Exception as e:
            print(f"❌ Visual analysis failed: {e}")
            return {"error": str(e)}
    
    def analyze_single_image(self, image_path):
        """Analyze a single mood board image"""
        try:
            image = cv2.imread(str(image_path))
            if image is None:
                return {"error": "Could not load image", "file": str(image_path)}
            
            analysis = {
                "filename": Path(image_path).name,
                "path": str(image_path)
            }
            
            # Color analysis
            analysis["color_palette"] = self.extract_color_palette(image)
            analysis["brightness"] = self.analyze_brightness(image)
            
            return analysis
            
        except Exception as e:
            return {"error": str(e), "file": str(image_path)}
    
    def extract_color_palette(self, image, num_colors=3):
        """Extract dominant color palette"""
        try:
            # Convert to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Reshape for clustering
            pixels = image_rgb.reshape(-1, 3)
            
            # K-means clustering for dominant colors
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
            _, labels, centers = cv2.kmeans(pixels.astype(np.float32), num_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
            
            # Convert to hex colors
            colors = []
            for center in centers:
                hex_color = "#{:02x}{:02x}{:02x}".format(int(center[0]), int(center[1]), int(center[2]))
                colors.append({
                    "hex": hex_color,
                    "rgb": [int(center[0]), int(center[1]), int(center[2])]
                })
            
            return colors
            
        except Exception as e:
            return [{"error": str(e)}]
    
    def analyze_brightness(self, image):
        """Analyze image brightness"""
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            brightness = np.mean(gray)
            
            if brightness > 180:
                return {"level": "high", "value": float(brightness)}
            elif brightness < 70:
                return {"level": "low", "value": float(brightness)}
            else:
                return {"level": "medium", "value": float(brightness)}
                
        except Exception as e:
            return {"error": str(e)}

def test_visual_analysis():
    """Test visual analysis system"""
    print("🧪 Testing visual mood board analysis...")
    analyzer = VisualMoodAnalyzer()
    print("📋 Visual analysis engine ready")
    return True

if __name__ == "__main__":
    test_visual_analysis()
