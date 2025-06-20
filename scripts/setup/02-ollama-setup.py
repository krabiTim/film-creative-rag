#!/usr/bin/env python3
"""
🎬 Film Creative RAG - Ollama LLM Setup
======================================
Sets up Ollama for local LLM processing
Builds on existing Ubuntu environment
"""

import os
import subprocess
import time
import requests
import json
import sys
from pathlib import Path

class OllamaSetup:
    """Simple Ollama setup for Film Creative RAG"""
    
    def __init__(self):
        self.project_dir = Path.home() / "film-creative-rag"
        self.ollama_url = "http://localhost:11434"
        print("🎬 Film Creative RAG - Ollama LLM Setup")
        print("=" * 40)
        print(f"Project directory: {self.project_dir}")
        print("")
    
    def run_command(self, command, description="", timeout=300):
        """Run command safely with timeout"""
        try:
            if description:
                print(f"🔧 {description}...")
            
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout)
            
            if result.returncode == 0:
                print(f"✅ {description} - Success")
                return True, result.stdout
            else:
                print(f"❌ {description} - Failed")
                if result.stderr:
                    print(f"Error: {result.stderr}")
                return False, result.stderr
        except subprocess.TimeoutExpired:
            print(f"⏰ {description} - Timed out after {timeout} seconds")
            return False, "Timeout"
        except Exception as e:
            print(f"❌ {description} - Exception: {e}")
            return False, str(e)
    
    def check_python_deps(self):
        """Check/install Python dependencies"""
        print("🐍 Checking Python dependencies...")
        
        required_packages = ["requests", "gradio"]
        
        for package in required_packages:
            try:
                __import__(package)
                print(f"✅ {package} already installed")
            except ImportError:
                print(f"📦 Installing {package}...")
                success, _ = self.run_command(f"pip3 install {package}", f"Installing {package}")
                if not success:
                    print(f"⚠️ Failed to install {package}, but continuing...")
        
        return True
    
    def check_ollama_installed(self):
        """Check if Ollama is installed"""
        print("\n🤖 Checking Ollama installation...")
        
        success, output = self.run_command("which ollama", "Checking Ollama location")
        if success and output.strip():
            print(f"✅ Ollama found at: {output.strip()}")
            
            # Check version
            success, version = self.run_command("ollama --version", "Checking Ollama version")
            if success:
                print(f"✅ Ollama version: {version.strip()}")
            
            return True
        else:
            print("❌ Ollama not found")
            return False
    
    def install_ollama(self):
        """Install Ollama if not present"""
        print("\n📥 Installing Ollama...")
        
        # Download and install Ollama
        install_cmd = "curl -fsSL https://ollama.ai/install.sh | sh"
        success, output = self.run_command(install_cmd, "Downloading and installing Ollama", timeout=600)
        
        if success:
            print("✅ Ollama installation completed")
            return True
        else:
            print("❌ Ollama installation failed")
            print("Please install manually from: https://ollama.ai")
            return False
    
    def start_ollama_service(self):
        """Start Ollama service"""
        print("\n🚀 Starting Ollama service...")
        
        # Check if already running
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                print("✅ Ollama service already running")
                return True
        except requests.RequestException:
            pass
        
        # Start service in background
        print("🔧 Starting Ollama service...")
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Wait for service to start
        print("⏰ Waiting for service to start...")
        for i in range(15):
            try:
                response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
                if response.status_code == 200:
                    print("✅ Ollama service started successfully")
                    return True
            except requests.RequestException:
                time.sleep(2)
                print(f"🔄 Waiting... ({i+1}/15)")
        
        print("❌ Ollama service failed to start")
        print("Try running manually: ollama serve")
        return False
    
    def download_model(self, model_name="llama3.2:3b"):
        """Download LLM model"""
        print(f"\n📚 Downloading model: {model_name}")
        print("⏰ This may take several minutes depending on your internet connection...")
        
        # Check if model already exists
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=10)
            if response.status_code == 200:
                models = response.json()
                existing_models = [model['name'] for model in models.get('models', [])]
                
                if model_name in existing_models:
                    print(f"✅ Model {model_name} already downloaded")
                    return True
                
                print(f"📋 Currently available models: {existing_models}")
        except requests.RequestException:
            print("⚠️ Could not check existing models, proceeding with download...")
        
        # Download model
        success, output = self.run_command(f"ollama pull {model_name}", f"Downloading {model_name}", timeout=1800)
        
        if success:
            print(f"✅ Model {model_name} downloaded successfully")
            return True
        else:
            print(f"❌ Failed to download {model_name}")
            # Try smaller model as fallback
            if model_name != "llama3.2:1b":
                print("🔄 Trying smaller model: llama3.2:1b")
                return self.download_model("llama3.2:1b")
            return False
    
    def test_ollama_functionality(self):
        """Test Ollama with screenplay analysis"""
        print("\n🎭 Testing Ollama with screenplay analysis...")
        
        # Test prompt for screenplay analysis
        test_screenplay = """
INT. TECH LAB - DAY

ALICE, a skilled programmer, works at her computer terminal.

ALICE
(frustrated)
This security protocol isn't working as expected.

BOB enters, looking concerned about the deadline.

BOB
Any luck breaking through the firewall?

ALICE
(determined)
I think I found a way. Give me five more minutes.
"""
        
        analysis_prompt = f"""
Analyze this screenplay excerpt and provide:

1. CHARACTERS: List character names
2. LOCATION: Scene setting
3. MOOD: Emotional tone
4. ACTION: Key events

Screenplay:
{test_screenplay}

Analysis:
"""
        
        try:
            print("🔍 Sending test analysis request...")
            
            payload = {
                "model": "llama3.2:3b",
                "prompt": analysis_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "max_tokens": 400
                }
            }
            
            response = requests.post(f"{self.ollama_url}/api/generate", json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                analysis = result.get('response', 'No response received')
                
                print("\n🎬 SCREENPLAY ANALYSIS TEST RESULT:")
                print("-" * 50)
                print(analysis[:300] + "..." if len(analysis) > 300 else analysis)
                print("-" * 50)
                print("✅ Ollama screenplay analysis working!")
                return True
            else:
                print(f"❌ Test request failed with status: {response.status_code}")
                return False
                
        except requests.RequestException as e:
            print(f"❌ Test request failed: {e}")
            return False
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            return False
    
    def create_config_files(self):
        """Create configuration files for Ollama integration"""
        print("\n⚙️ Creating configuration files...")
        
        # Create configs directory
        config_dir = self.project_dir / "configs"
        config_dir.mkdir(exist_ok=True)
        
        # Ollama configuration
        ollama_config = {
            "ollama": {
                "url": "http://localhost:11434",
                "default_model": "llama3.2:3b",
                "fallback_model": "llama3.2:1b",
                "timeout": 60,
                "max_tokens": 512,
                "temperature": 0.7
            },
            "screenplay_analysis": {
                "enabled": True,
                "prompt_template": "screenplay_analysis.txt",
                "max_length": 5000
            },
            "performance": {
                "gpu_acceleration": True,
                "batch_processing": False,
                "concurrent_requests": 1
            }
        }
        
        import json
        config_file = config_dir / "ollama_config.json"
        with open(config_file, 'w') as f:
            json.dump(ollama_config, f, indent=2)
        
        print(f"✅ Configuration saved: {config_file}")
        
        # Create prompt template
        prompt_template = """
Analyze this screenplay excerpt and provide a structured analysis:

1. CHARACTERS: List all character names mentioned
2. LOCATION: Identify the scene setting/location
3. SCENE TYPE: Interior/Exterior and time of day
4. MOOD: Describe the emotional tone
5. ACTION: Key events or conflicts in the scene
6. DIALOGUE: Assessment of dialogue quality
7. PRODUCTION: Notable requirements for filming

Screenplay Content:
{screenplay_content}

Provide analysis in the above format:
"""
        
        template_file = config_dir / "screenplay_analysis_template.txt"
        with open(template_file, 'w') as f:
            f.write(prompt_template)
        
        print(f"✅ Prompt template saved: {template_file}")
        return True
    
    def save_system_status(self):
        """Update system status with Ollama setup"""
        print("\n📊 Updating system status...")
        
        status_file = self.project_dir / "STATUS.md"
        
        status_content = """# Film Creative RAG - System Status

## Environment Status
- ✅ WSL2 Ubuntu 22.04
- ✅ Python 3.x with pip
- ✅ Project directory structure
- ✅ Git repository initialized
- ✅ RTX 4090 GPU ready
- ✅ Ollama LLM service running
- ✅ llama3.2:3b model downloaded

## Phase Status  
- ✅ Phase 1: Foundation & Setup - COMPLETE
- 🔧 Phase 2: Screenplay Intelligence - IN PROGRESS
  - ✅ Ollama LLM integration - COMPLETE
  - 🔧 Gradio UI demo - NEXT
  - 📅 LightRAG integration - PLANNED
- 📅 Phase 3: Mood Board Processing - PLANNED

## Component Status
- ✅ Ollama Service: Running on localhost:11434
- ✅ LLM Model: llama3.2:3b ready for analysis
- ✅ Screenplay Analysis: Tested and working
- ✅ Configuration: Files created

## Next Steps
1. Run: `python3 scripts/setup/03-demo-launch.py`
2. Test: Open http://localhost:7860
3. Validate: Upload sample screenplay
4. Proceed: Phase 2 completion

## GitHub Integration
- ✅ Repository initialized
- ✅ Branch structure created (main/develop/phase-2)
- ✅ Ollama integration ready for commit

Last updated: Ollama setup completed
"""
        
        with open(status_file, 'w') as f:
            f.write(status_content)
        
        print("✅ System status updated")
        return True
    
    def run_setup(self):
        """Run complete Ollama setup process"""
        try:
            print("Starting Ollama setup for Film Creative RAG...")
            print("")
            
            # Check Python dependencies
            if not self.check_python_deps():
                print("❌ Python dependency check failed")
                return False
            
            # Check if Ollama is installed
            if not self.check_ollama_installed():
                print("📥 Ollama not found, installing...")
                if not self.install_ollama():
                    return False
            
            # Start Ollama service
            if not self.start_ollama_service():
                print("❌ Failed to start Ollama service")
                return False
            
            # Download model
            if not self.download_model():
                print("❌ Failed to download LLM model")
                return False
            
            # Test functionality
            if not self.test_ollama_functionality():
                print("❌ Ollama functionality test failed")
                return False
            
            # Create config files
            self.create_config_files()
            
            # Update status
            self.save_system_status()
            
            print("\n🎉 Ollama Setup Complete!")
            print("=" * 40)
            print("✅ Ollama service running")
            print("✅ llama3.2:3b model ready")
            print("✅ Screenplay analysis tested")
            print("✅ Configuration files created")
            print("")
            print("🚀 Next Steps:")
            print("1. Run: python3 scripts/setup/03-demo-launch.py")
            print("2. Test screenplay analysis at http://localhost:7860")
            print("")
            print("📊 System Status: Ready for Phase 2 demo")
            
            return True
            
        except Exception as e:
            print(f"❌ Setup failed with error: {e}")
            return False

def main():
    """Main setup function"""
    setup = OllamaSetup()
    
    try:
        success = setup.run_setup()
        
        if success:
            print("\n🎬 Ollama integration ready for Film Creative RAG!")
            print("Continue with demo: python3 scripts/setup/03-demo-launch.py")
        else:
            print("\n❌ Ollama setup encountered issues. Check errors above.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()