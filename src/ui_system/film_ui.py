#!/usr/bin/env python3
"""
Film Creative RAG - UI System
============================
Complete Gradio interface integrating all systems
"""

import gradio as gr
import asyncio
import sys
from pathlib import Path

# Add project paths
sys.path.append(str(Path(__file__).parent.parent))

try:
    from rag_core.film_rag_engine import FilmRAGCore
    from upload_system.file_uploader import FilmUploadSystem
    from chat_system.film_chat import FilmChatSystem
except ImportError:
    print("⚠️ Some modules not available - using mock implementations")
    
    class FilmRAGCore:
        async def add_screenplay(self, content, title):
            return {"chunks": 5}
        async def query(self, query):
            return f"Mock response to: {query}"
    
    class FilmUploadSystem:
        def process_upload(self, file_path, project_name=None):
            return {"upload_id": "test123", "file_type": "screenplay"}
    
    class FilmChatSystem:
        def __init__(self, rag_engine):
            pass
        async def chat(self, message, context=None):
            return {"content": f"Mock chat: {message}", "status": "success"}

class FilmCreativeRAGUI:
    """Complete UI for Film Creative RAG"""
    
    def __init__(self):
        # Initialize systems
        self.rag_engine = FilmRAGCore()
        self.upload_system = FilmUploadSystem()
        self.chat_system = FilmChatSystem(self.rag_engine)
        
        # State
        self.current_project = None
        
        print("🎬 Film Creative RAG UI initialized")
    
    def upload_file(self, file, project_name):
        """Handle file upload"""
        if not file:
            return "Please select a file to upload."
        
        if not project_name.strip():
            project_name = "Default_Project"
        
        try:
            # Process upload
            result = self.upload_system.process_upload(file.name, project_name)
            
            if "error" in result:
                return f"❌ Upload failed: {result['error']}"
            
            # Update current project
            self.current_project = project_name
            
            # If screenplay, add to RAG
            if result["file_type"] == "screenplay":
                # This would run in background
                pass
            
            return f"""# 📁 Upload Successful
            
**File**: {result['original_name']}  
**Type**: {result['file_type']}  
**Project**: {project_name}  
**Upload ID**: {result['upload_id']}  

✅ Ready for analysis and chat!
"""
            
        except Exception as e:
            return f"❌ Upload error: {str(e)}"
    
    async def chat_with_project(self, message, chat_history):
        """Chat about current project"""
        if not message.strip():
            return chat_history, ""
        
        try:
            response = await self.chat_system.chat(message)
            chat_history.append([message, response["content"]])
            return chat_history, ""
        except Exception as e:
            chat_history.append([message, f"Error: {str(e)}"])
            return chat_history, ""
    
    def get_project_status(self):
        """Get current project status"""
        if not self.current_project:
            return "No active project. Upload files to get started."
        
        return f"""# 📊 Project Status

**Active Project**: {self.current_project}

**Available Features**:
- 💬 **Chat**: Ask questions about your project
- 📝 **Analysis**: Get detailed insights
- 🎨 **Cross-modal**: Compare screenplay and visuals

**Chat Examples**:
- "Analyze the main characters"
- "What mood do the visuals convey?"
- "How do the colors support the story?"
"""
    
    def create_interface(self):
        """Create Gradio interface"""
        with gr.Blocks(title="🎬 Film Creative RAG", theme=gr.themes.Soft()) as interface:
            
            gr.HTML("""
            <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; margin-bottom: 2rem;">
                <h1>🎬 Film Creative RAG</h1>
                <h2>Modular AI System for Independent Filmmakers</h2>
                <p><strong>Upload • Process • Chat • Analyze</strong></p>
            </div>
            """)
            
            with gr.Tab("📁 Upload"):
                with gr.Row():
                    with gr.Column():
                        project_name = gr.Textbox(label="Project Name", value="My_Film_Project")
                        file_upload = gr.File(label="Upload File")
                        upload_btn = gr.Button("🚀 Upload & Process", variant="primary")
                    
                    with gr.Column():
                        upload_output = gr.Textbox(label="Upload Results", lines=10, interactive=False)
            
            with gr.Tab("💬 Chat"):
                with gr.Row():
                    with gr.Column(scale=3):
                        chatbot = gr.Chatbot(label="Chat with your project", height=400)
                        
                        with gr.Row():
                            chat_input = gr.Textbox(label="Message", scale=4)
                            send_btn = gr.Button("Send", variant="primary", scale=1)
                    
                    with gr.Column(scale=1):
                        project_status = gr.Textbox(label="Project Status", lines=15, interactive=False)
                        refresh_btn = gr.Button("🔄 Refresh")
            
            # Event handlers
            upload_btn.click(
                self.upload_file,
                inputs=[file_upload, project_name],
                outputs=upload_output
            )
            
            send_btn.click(
                self.chat_with_project,
                inputs=[chat_input, chatbot],
                outputs=[chatbot, chat_input]
            )
            
            refresh_btn.click(
                self.get_project_status,
                outputs=project_status
            )
            
            # Load initial status
            interface.load(self.get_project_status, outputs=project_status)
        
        return interface
    
    def launch(self):
        """Launch the interface"""
        print("🚀 Launching Film Creative RAG...")
        print("🌐 Opening at: http://localhost:7860")
        
        interface = self.create_interface()
        
        try:
            interface.launch(
                server_name="0.0.0.0",
                server_port=7860,
                share=False,
                show_error=True,
                inbrowser=True
            )
        except KeyboardInterrupt:
            print("\n🛑 UI stopped")
        except Exception as e:
            print(f"\n❌ UI error: {e}")

def main():
    """Main UI function"""
    ui = FilmCreativeRAGUI()
    ui.launch()

if __name__ == "__main__":
    main()
