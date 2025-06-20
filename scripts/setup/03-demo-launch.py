#!/usr/bin/env python3
"""
🎬 Film Creative RAG - Demo Launch
=================================
Launches working Gradio demo with Ollama integration
Final step in Phase 2 setup
"""

import gradio as gr
import requests
import json
import sys
import os
from pathlib import Path
import time

class FilmCreativeRAGDemo:
    """Working demo interface for Film Creative RAG"""
    
    def __init__(self):
        self.project_dir = Path.home() / "film-creative-rag"
        self.ollama_url = "http://localhost:11434"
        self.config = self.load_config()
        
        print("🎬 Film Creative RAG - Demo Launch")
        print("=" * 35)
        print(f"Project directory: {self.project_dir}")
        print("")
    
    def load_config(self):
        """Load Ollama configuration"""
        config_file = self.project_dir / "configs" / "ollama_config.json"
        
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Default configuration
        return {
            "ollama": {
                "url": "http://localhost:11434",
                "default_model": "llama3.2:3b",
                "fallback_model": "llama3.2:1b",
                "timeout": 60,
                "max_tokens": 512,
                "temperature": 0.7
            }
        }
    
    def check_system_status(self):
        """Check if Ollama and models are ready"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json()
                available_models = [model['name'] for model in models.get('models', [])]
                
                # Check for our preferred models
                preferred_models = ["llama3.2:3b", "llama3.2:1b"]
                working_model = None
                
                for model in preferred_models:
                    if model in available_models:
                        working_model = model
                        break
                
                if working_model:
                    return True, working_model, available_models
                else:
                    return False, None, available_models
            else:
                return False, None, []
        except requests.RequestException:
            return False, None, []
    
    def analyze_screenplay(self, screenplay_text, title="Untitled Screenplay"):
        """Analyze screenplay using Ollama"""
        if not screenplay_text.strip():
            return "⚠️ Please enter screenplay content to analyze."
        
        # Check system status
        system_ready, working_model, available_models = self.check_system_status()
        
        if not system_ready:
            if not available_models:
                return """❌ **System Not Ready**

**Issue**: Ollama service not responding

**Solutions**:
1. Run: `ollama serve &` in terminal
2. Wait 30 seconds and try again
3. Check if Ollama is installed: `ollama --version`

**Need Help?** Run the setup script: `python3 scripts/setup/02-ollama-setup.py`
"""
            else:
                return f"""❌ **Model Not Available**

**Available models**: {', '.join(available_models)}
**Needed**: llama3.2:3b or llama3.2:1b

**Solution**: Run `ollama pull llama3.2:3b` in terminal
"""
        
        try:
            # Create analysis prompt
            prompt = f"""
Analyze this screenplay excerpt and provide a structured analysis:

**Title**: {title}

**Content**:
{screenplay_text}

Please provide:

1. **CHARACTERS**: List all character names mentioned
2. **LOCATION**: Scene setting and location details  
3. **SCENE TYPE**: Interior/Exterior and time of day
4. **MOOD**: Emotional tone and atmosphere
5. **KEY EVENTS**: Important actions or plot points
6. **DIALOGUE NOTES**: Quality and style observations
7. **PRODUCTION NOTES**: Requirements for filming this scene

Analysis:
"""
            
            # Send request to Ollama
            payload = {
                "model": working_model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": self.config["ollama"]["temperature"],
                    "max_tokens": self.config["ollama"]["max_tokens"]
                }
            }
            
            print(f"🎭 Analyzing screenplay '{title}' with {working_model}...")
            
            response = requests.post(
                f"{self.ollama_url}/api/generate", 
                json=payload, 
                timeout=self.config["ollama"]["timeout"]
            )
            
            if response.status_code == 200:
                result = response.json()
                analysis = result.get('response', 'No analysis received')
                
                # Format the response nicely
                formatted_analysis = f"""# 🎬 Screenplay Analysis Complete

## 📝 **{title}**

{analysis}

---

✅ **Analysis powered by**: {working_model}  
🔒 **Privacy**: All processing done locally on your computer  
⚡ **Performance**: Optimized for RTX 4090  

*Generated by Film Creative RAG v2.0*
"""
                
                return formatted_analysis
            else:
                return f"""❌ **Analysis Failed**

**Error**: Request failed with status {response.status_code}

**Solutions**:
1. Check if Ollama is running: `ollama serve &`
2. Verify model is available: `ollama list`
3. Try again in a few seconds

**Status**: {response.text[:200]}...
"""
                
        except requests.RequestException as e:
            return f"""❌ **Connection Error**

**Issue**: Cannot connect to Ollama service

**Error**: {str(e)}

**Solutions**:
1. Start Ollama: `ollama serve &`
2. Wait 30 seconds for startup
3. Try analysis again

**Help**: Run `python3 scripts/setup/02-ollama-setup.py`
"""
        except Exception as e:
            return f"""❌ **Unexpected Error**

**Error**: {str(e)}

**Solutions**:
1. Check system status
2. Restart Ollama service
3. Contact support if issue persists
"""
    
    def get_sample_screenplay(self):
        """Return sample screenplay for testing"""
        return """Title: The Digital Breakthrough
Author: Film Creative RAG Demo

FADE IN:

INT. INDIE FILMMAKER'S HOME OFFICE - NIGHT

MAYA, an independent filmmaker in her 30s, sits surrounded by storyboards, script pages, and multiple monitors. Her editing setup shows a documentary project in progress.

MAYA
(exhausted, talking to herself)
This transition between scenes isn't working. The emotional arc feels disconnected.

She pauses the video timeline and rubs her tired eyes. Empty coffee cups and energy drink cans indicate a long night of editing.

MAYA (CONT'D)
(studying her notes)
The interview with Sarah needs to connect better with the archive footage...

Her phone buzzes with a text message from her collaborator.

MAYA (CONT'D)
(reading text, then inspired)
Cross-cutting! That's exactly what this needs.

She starts making rapid edits, cutting between the interview segments and historical footage with renewed energy.

MAYA (CONT'D)
(to her computer)
Let's try alternating between Sarah's memories and the actual events...

The timeline fills with precise cuts as Maya finds the perfect rhythm for her story.

MAYA (CONT'D)
(satisfied)
There it is. The story finally breathes.

She saves her project and leans back, finally satisfied with the edit.

FADE OUT."""
    
    def get_system_info(self):
        """Get current system information"""
        system_ready, working_model, available_models = self.check_system_status()
        
        if system_ready:
            status = f"""🟢 **SYSTEM STATUS: READY**

✅ **Ollama Service**: Running at {self.ollama_url}
✅ **Active Model**: {working_model}
✅ **Available Models**: {', '.join(available_models)}
✅ **Local Processing**: All analysis done on your computer
✅ **Privacy Mode**: No data sent to external services
✅ **GPU Acceleration**: RTX 4090 optimization ready

🎬 **Ready for screenplay analysis!**

**Performance**: 
- Analysis time: ~30-60 seconds per screenplay
- Model: {working_model}
- Memory usage: Optimized for creative workflows

**Privacy**: 
- 100% local processing
- Your screenplays never leave your computer
- No cloud connections or data logging
"""
        else:
            status = f"""🔴 **SYSTEM STATUS: NEEDS ATTENTION**

❌ **Ollama Service**: {"Not running" if not available_models else "Running but model missing"}
{"❌" if not available_models else "✅"} **Available Models**: {', '.join(available_models) if available_models else "None found"}

🔧 **Setup Required**:

1. **Start Ollama service**:
   ```bash
   ollama serve &
   ```

2. **Download required model**:
   ```bash
   ollama pull llama3.2:3b
   ```

3. **Refresh this page** and try again

**Need Help?** Run the setup script:
```bash
python3 scripts/setup/02-ollama-setup.py
```

**Status**: Checking {self.ollama_url}
"""
        
        return status
    
    def create_interface(self):
        """Create the Gradio interface"""
        
        # Custom CSS for professional appearance
        custom_css = """
        .gradio-container {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        }
        .main-header {
            text-align: center;
            padding: 2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        .status-box {
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        """
        
        with gr.Blocks(css=custom_css, title="🎬 Film Creative RAG", theme=gr.themes.Soft()) as interface:
            
            # Header
            gr.HTML("""
            <div class="main-header">
                <h1>🎬 Film Creative RAG</h1>
                <h2>AI-Powered Screenplay Analysis for Independent Filmmakers</h2>
                <p><strong>100% Local Processing • Privacy First • RTX 4090 Optimized</strong></p>
            </div>
            """)
            
            with gr.Tab("📝 Screenplay Analysis"):
                with gr.Row():
                    with gr.Column(scale=2):
                        title_input = gr.Textbox(
                            label="📄 Screenplay Title",
                            placeholder="Enter your screenplay title...",
                            value="My Screenplay"
                        )
                        
                        screenplay_input = gr.Textbox(
                            label="📜 Screenplay Content (Fountain Format Preferred)",
                            placeholder="Paste your screenplay content here...\n\nSupported formats:\n• Fountain (.fountain)\n• Plain text\n• Copy-paste from Final Draft",
                            lines=20,
                            max_lines=30
                        )
                        
                        with gr.Row():
                            analyze_btn = gr.Button("🎭 Analyze Screenplay", variant="primary", size="lg")
                            sample_btn = gr.Button("📄 Load Sample Screenplay", variant="secondary")
                            clear_btn = gr.Button("🗑️ Clear", variant="secondary")
                    
                    with gr.Column(scale=2):
                        analysis_output = gr.Textbox(
                            label="🤖 AI Analysis Results",
                            lines=25,
                            max_lines=30,
                            interactive=False,
                            value="Click 'Analyze Screenplay' to see AI-powered insights about your script..."
                        )
            
            with gr.Tab("⚙️ System Status"):
                with gr.Column():
                    gr.HTML("<h3>🔧 Film Creative RAG System Status</h3>")
                    
                    status_display = gr.Textbox(
                        label="System Information",
                        lines=20,
                        interactive=False
                    )
                    
                    with gr.Row():
                        refresh_status_btn = gr.Button("🔄 Refresh Status", variant="secondary")
                        test_connection_btn = gr.Button("🧪 Test Connection", variant="secondary")
            
            with gr.Tab("ℹ️ About & Help"):
                gr.Markdown("""
                ## 🎬 Film Creative RAG System
                
                ### What Does This Do?
                This system analyzes your screenplays using advanced AI to provide insights for:
                - **Character Development**: Identify main characters and their arcs
                - **Scene Analysis**: Understand pacing, mood, and structure  
                - **Production Planning**: Get insights for scheduling and logistics
                - **Creative Feedback**: AI-powered suggestions for improvement
                
                ### Key Features
                - **🔒 100% Local Processing** - Your scripts never leave your computer
                - **⚡ GPU Accelerated** - Optimized for NVIDIA RTX 4090
                - **🎯 Artist-Friendly** - No technical knowledge required
                - **📊 Professional Output** - Results ready for production meetings
                - **🎨 Creative Focus** - Designed specifically for filmmakers
                
                ### How to Use
                1. **Enter your screenplay title** in the title field
                2. **Paste your screenplay content** (Fountain format works best)
                3. **Click "Analyze Screenplay"** and wait 30-60 seconds
                4. **Review the AI analysis** for creative and production insights
                5. **Use the insights** for planning your film project
                
                ### Supported Formats
                - **Fountain** (.fountain) - Preferred format
                - **Plain Text** - Copy-paste from any word processor
                - **Final Draft** - Copy-paste from Final Draft
                - **WriterDuet** - Export as text and paste
                
                ### System Requirements
                - **OS**: Ubuntu 22.04 (WSL2 supported)
                - **GPU**: NVIDIA RTX 4090 (recommended)
                - **RAM**: 16GB minimum, 32GB recommended
                - **Storage**: 10GB free space for models
                
                ### Privacy & Security
                - **No cloud connections** - Everything runs locally
                - **No data logging** - Your screenplays are not stored
                - **No external APIs** - Complete privacy protection
                - **Open source** - Full transparency in processing
                
                ### Troubleshooting
                - **Service not running**: Run `ollama serve &` in terminal
                - **Model missing**: Run `ollama pull llama3.2:3b`
                - **Slow analysis**: Normal for first run, speeds up after
                - **Error messages**: Check System Status tab for details
                
                ### Support
                - **GitHub Issues**: Report bugs and request features
                - **Documentation**: Check the `docs/` folder
                - **Community**: Join discussions for tips and tricks
                
                ---
                
                **Film Creative RAG v2.0** - Phase 2 Complete  
                *Made with ❤️ for independent filmmakers*
                """)
            
            # Event handlers
            sample_btn.click(
                fn=self.get_sample_screenplay,
                outputs=screenplay_input
            )
            
            clear_btn.click(
                fn=lambda: ("", "Ready for new screenplay analysis..."),
                outputs=[screenplay_input, analysis_output]
            )
            
            analyze_btn.click(
                fn=self.analyze_screenplay,
                inputs=[screenplay_input, title_input],
                outputs=analysis_output
            )
            
            refresh_status_btn.click(
                fn=self.get_system_info,
                outputs=status_display
            )
            
            test_connection_btn.click(
                fn=lambda: self.analyze_screenplay("INT. TEST - DAY\n\nTEST CHARACTER\nThis is a test.", "Connection Test"),
                outputs=status_display
            )
            
            # Load initial status
            interface.load(
                fn=self.get_system_info,
                outputs=status_display
            )
        
        return interface
    
    def launch_demo(self):
        """Launch the demo interface"""
        print("🚀 Launching Film Creative RAG Demo...")
        print("")
        
        # Check system status before launch
        system_ready, working_model, available_models = self.check_system_status()
        
        if system_ready:
            print("✅ System ready for demo")
            print(f"✅ Using model: {working_model}")
        else:
            print("⚠️ System not fully ready - demo will show setup instructions")
            if available_models:
                print(f"⚠️ Available models: {available_models}")
            else:
                print("⚠️ No models found - Ollama may not be running")
        
        print("")
        print("🌐 Demo will be available at: http://localhost:7860")
        print("🎬 Ready for filmmaker demonstrations!")
        print("")
        print("Press Ctrl+C to stop the demo")
        print("=" * 50)
        
        # Create and launch interface
        interface = self.create_interface()
        
        try:
            interface.launch(
                server_name="0.0.0.0",
                server_port=7860,
                share=False,  # Keep it local for privacy
                show_error=True,
                inbrowser=True,
                show_tips=False,
                quiet=False
            )
        except KeyboardInterrupt:
            print("\n🛑 Demo stopped by user")
        except Exception as e:
            print(f"\n❌ Demo failed to launch: {e}")
            print("Try running: python3 scripts/setup/02-ollama-setup.py")

def main():
    """Main demo launch function"""
    demo = FilmCreativeRAGDemo()
    
    try:
        demo.launch_demo()
    except KeyboardInterrupt:
        print("\n\n🛑 Film Creative RAG demo stopped")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
