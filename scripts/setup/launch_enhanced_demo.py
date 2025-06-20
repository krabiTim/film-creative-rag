#!/usr/bin/env python3
"""
🎬 Film Creative RAG - Launch Enhanced Demo
==========================================
Simple launcher for the enhanced demo with mood board processing
"""

import sys
from pathlib import Path

# Add UI path
sys.path.append(str(Path(__file__).parent.parent.parent / "src" / "ui"))

try:
    from enhanced_demo import main
    
    if __name__ == "__main__":
        print("🎬 Starting Film Creative RAG Enhanced Demo...")
        print("🎨 Features: Screenplay + Mood Board + Cross-Modal Analysis")
        print("🌐 Opening at: http://localhost:7860")
        print("")
        main()
        
except ImportError as e:
    print(f"❌ Could not launch enhanced demo: {e}")
    print("Please ensure all dependencies are installed")
except Exception as e:
    print(f"❌ Demo launch failed: {e}")
