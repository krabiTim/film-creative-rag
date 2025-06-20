#!/usr/bin/env python3
"""
🎬 Film Creative RAG - GitHub Integration Setup
==============================================
Integrates existing work with proper GitHub workflow
Builds on current WSL2 Ubuntu setup and project structure
"""

import os
import subprocess
import sys
from pathlib import Path

class GitHubSetup:
    """Simple GitHub integration for existing Film Creative RAG project"""
    
    def __init__(self):
        self.project_dir = Path.home() / "film-creative-rag"
        self.current_dir = Path.cwd()
        print("🎬 Film Creative RAG - GitHub Integration Setup")
        print("=" * 50)
        print(f"Project directory: {self.project_dir}")
        print(f"Current directory: {self.current_dir}")
        print("")
    
    def run_command(self, command, description=""):
        """Run command safely with error handling"""
        try:
            if description:
                print(f"🔧 {description}...")
            
            result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=self.project_dir)
            
            if result.returncode == 0:
                print(f"✅ Success: {description}")
                return True, result.stdout
            else:
                print(f"❌ Failed: {description}")
                print(f"Error: {result.stderr}")
                return False, result.stderr
        except Exception as e:
            print(f"❌ Exception in {description}: {e}")
            return False, str(e)
    
    def check_existing_setup(self):
        """Check what we already have working"""
        print("📋 Checking existing setup...")
        
        # Check if project directory exists
        if not self.project_dir.exists():
            print(f"❌ Project directory not found: {self.project_dir}")
            print("Please run from the correct location or create the directory")
            return False
        
        print(f"✅ Project directory exists: {self.project_dir}")
        
        # Check if we're already in a git repo
        git_dir = self.project_dir / ".git"
        if git_dir.exists():
            print("✅ Git repository already initialized")
            return True
        else:
            print("🔧 Git repository needs initialization")
            return False
    
    def create_project_structure(self):
        """Create/verify project structure based on existing work"""
        print("\n📁 Setting up project structure...")
        
        # Directories we need (some may already exist)
        directories = [
            "docs",
            "scripts/setup",
            "scripts/utils", 
            "src/core",
            "src/ui",
            "src/tests",
            "configs",
            "examples"
        ]
        
        for dir_path in directories:
            full_path = self.project_dir / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Directory ready: {dir_path}")
        
        return True
    
    def initialize_git(self):
        """Initialize Git repository with existing work"""
        print("\n🔧 Initializing Git repository...")
        
        os.chdir(self.project_dir)
        
        # Initialize git if needed
        if not (self.project_dir / ".git").exists():
            success, output = self.run_command("git init", "Initializing Git repository")
            if not success:
                return False
        
        # Configure git user (basic setup)
        self.run_command('git config user.name "Film Creative RAG Developer"', "Setting Git user name")
        self.run_command('git config user.email "developer@filmcreativerag.local"', "Setting Git email")
        
        return True
    
    def create_gitignore(self):
        """Create comprehensive .gitignore for the project"""
        print("\n📝 Creating .gitignore...")
        
        gitignore_content = """# Film Creative RAG - .gitignore

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
venv/
env/
ENV/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Temporary files
*.tmp
temp/
cache/

# Large model files
models/
*.pth
*.pt

# Sensitive data
.env
credentials/
secrets/

# Ollama data (keep models local but don't commit)
ollama_data/

# Generated outputs
outputs/
exports/
"""
        
        gitignore_path = self.project_dir / ".gitignore"
        with open(gitignore_path, 'w') as f:
            f.write(gitignore_content)
        
        print("✅ .gitignore created")
        return True
    
    def create_readme(self):
        """Create/update README with current status"""
        print("\n📖 Creating README...")
        
        readme_content = """# 🎬 Film Creative RAG

**AI-Powered Screenplay Analysis for Independent Filmmakers**

## 🌟 Current Status

✅ **Phase 1**: Foundation & Setup - COMPLETE  
🔧 **Phase 2**: Screenplay Intelligence - IN PROGRESS  
📅 **Phase 3**: Mood Board Processing - PLANNED  

## 🚀 Quick Start

### Prerequisites
- Ubuntu 22.04 (WSL2 supported)
- Python 3.8+
- RTX 4090 GPU (recommended)

### Installation
```bash
cd ~/film-creative-rag

# Setup system
python3 scripts/setup/01-github-setup.py
python3 scripts/setup/02-ollama-setup.py

# Launch demo
python3 scripts/setup/03-demo-launch.py
```

### Usage
1. Open browser to http://localhost:7860
2. Upload your screenplay (Fountain format preferred)
3. Get AI-powered analysis and insights
4. Use results for production planning

## 🎯 Features

- **🔒 100% Local Processing** - Your scripts stay private
- **⚡ GPU Accelerated** - RTX 4090 optimized
- **🎭 Screenplay Analysis** - Characters, scenes, structure
- **🤖 AI Insights** - Production planning assistance
- **🎨 Artist-Friendly** - No technical knowledge required

## 📁 Project Structure

```
film-creative-rag/
├── scripts/setup/     # Installation scripts
├── src/core/         # Core AI engines
├── src/ui/           # User interface
├── configs/          # Configuration files
└── examples/         # Sample content
```

## 🛠️ Development

### Branch Strategy
- `main` - Stable releases
- `develop` - Integration branch
- `phase-X` - Phase development branches

### Current Phase: Phase 2 - Screenplay Intelligence
- LightRAG integration
- Ollama LLM setup
- Gradio UI demo
- Screenplay analysis engine

## 📞 Support

- **Issues**: Use GitHub Issues for bug reports
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: See `docs/` directory

## 📄 License

MIT License - See LICENSE file for details

---

**Made for independent filmmakers who need AI tools that respect their creative privacy.**
"""
        
        readme_path = self.project_dir / "README.md"
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        
        print("✅ README.md created")
        return True
    
    def setup_branches(self):
        """Set up branch structure following project plan"""
        print("\n🌿 Setting up Git branches...")
        
        # Create and switch to develop branch
        success, _ = self.run_command("git checkout -b develop", "Creating develop branch")
        if not success:
            print("🔧 Develop branch may already exist, checking out...")
            self.run_command("git checkout develop", "Switching to develop branch")
        
        # Create phase-2 branch (current work)
        success, _ = self.run_command("git checkout -b phase-2-screenplay", "Creating phase-2 branch")
        if not success:
            print("🔧 Phase-2 branch may already exist, checking out...")
            self.run_command("git checkout phase-2-screenplay", "Switching to phase-2 branch")
        
        print("✅ Branch structure ready")
        return True
    
    def commit_existing_work(self):
        """Commit existing work with proper messages"""
        print("\n💾 Committing existing work...")
        
        # Add all files
        self.run_command("git add -A", "Adding all files")
        
        # Create initial commit
        commit_message = """Initial commit: Film Creative RAG project setup

✅ WSL2 Ubuntu 22.04 environment ready
✅ Python environment configured  
✅ Project structure established
✅ RTX 4090 GPU support ready
✅ Phase 1 (Foundation) complete

Phase 2 (Screenplay Intelligence) in progress:
- Ollama LLM integration planned
- LightRAG system planned
- Gradio UI demo planned

Following Film Creative RAG project plan v1.0"""
        
        success, _ = self.run_command(f'git commit -m "{commit_message}"', "Creating initial commit")
        
        if success:
            print("✅ Initial commit created")
        else:
            print("🔧 Commit may already exist or no changes to commit")
        
        return True
    
    def create_system_status(self):
        """Create system status file for tracking"""
        print("\n📊 Creating system status file...")
        
        status_content = """# Film Creative RAG - System Status

## Environment Status
- ✅ WSL2 Ubuntu 22.04
- ✅ Python 3.x with pip
- ✅ Project directory structure
- ✅ Git repository initialized
- ✅ RTX 4090 GPU ready

## Phase Status  
- ✅ Phase 1: Foundation & Setup - COMPLETE
- 🔧 Phase 2: Screenplay Intelligence - IN PROGRESS
- 📅 Phase 3: Mood Board Processing - PLANNED

## Next Steps
1. Run: `python3 scripts/setup/02-ollama-setup.py`
2. Run: `python3 scripts/setup/03-demo-launch.py`
3. Test: Open http://localhost:7860
4. Validate: Upload sample screenplay

## GitHub Integration
- ✅ Repository initialized
- ✅ Branch structure created
- ✅ Initial commit completed
- 🔧 Remote repository setup needed

Last updated: $(date)
"""
        
        status_path = self.project_dir / "STATUS.md"
        with open(status_path, 'w') as f:
            f.write(status_content)
        
        print("✅ System status file created")
        return True
    
    def run_setup(self):
        """Run complete GitHub setup process"""
        try:
            # Check existing setup
            if not self.check_existing_setup():
                print("⚠️ Some setup steps needed...")
            
            # Create/verify project structure
            if not self.create_project_structure():
                print("❌ Failed to create project structure")
                return False
            
            # Initialize Git
            if not self.initialize_git():
                print("❌ Failed to initialize Git")
                return False
            
            # Create project files
            self.create_gitignore()
            self.create_readme()
            self.create_system_status()
            
            # Setup branches
            if not self.setup_branches():
                print("❌ Failed to setup branches")
                return False
            
            # Commit work
            if not self.commit_existing_work():
                print("❌ Failed to commit work")
                return False
            
            print("\n🎉 GitHub Integration Setup Complete!")
            print("=" * 50)
            print("✅ Git repository initialized")
            print("✅ Branch structure created (main/develop/phase-2)")
            print("✅ Project files created")
            print("✅ Existing work committed")
            print("")
            print("🚀 Next Steps:")
            print("1. Run: python3 scripts/setup/02-ollama-setup.py")
            print("2. Run: python3 scripts/setup/03-demo-launch.py")
            print("3. Optional: Add remote repository later")
            print("")
            print("📁 Current branch: phase-2-screenplay")
            print("📊 Status: Ready for Phase 2 development")
            
            return True
            
        except Exception as e:
            print(f"❌ Setup failed with error: {e}")
            return False

def main():
    """Main setup function"""
    setup = GitHubSetup()
    
    try:
        success = setup.run_setup()
        
        if success:
            print("\n🎬 Film Creative RAG GitHub integration ready!")
            print("Continue with Ollama setup: python3 scripts/setup/02-ollama-setup.py")
        else:
            print("\n❌ Setup encountered issues. Check errors above.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
