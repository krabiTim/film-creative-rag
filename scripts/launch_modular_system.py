#!/usr/bin/env python3
"""
Film Creative RAG - Launcher
============================
Simple launcher for the modular system
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

try:
    from ui_system.film_ui import main
    
    if __name__ == "__main__":
        print("🎬 Starting Film Creative RAG Modular System...")
        main()
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure all modules are properly installed")
except Exception as e:
    print(f"❌ Launch error: {e}")
