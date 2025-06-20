#!/usr/bin/env python3
"""
Film Creative RAG - Chat System
==============================
Interactive chat interface for project analysis
"""

import asyncio
import requests
import time
from typing import List, Dict, Any

class FilmChatSystem:
    """Chat system for Film Creative RAG"""
    
    def __init__(self, rag_engine=None):
        self.rag_engine = rag_engine
        self.chat_history = []
        self.ollama_url = "http://localhost:11434"
        self.model_name = "llama3.2:3b"
    
    async def chat(self, message: str, context: Dict = None) -> Dict[str, Any]:
        """Process chat message"""
        # Add to history
        self.chat_history.append({
            "role": "user", 
            "message": message,
            "timestamp": time.time()
        })
        
        # Get response
        response = await self.generate_response(message, context)
        
        # Add response to history
        self.chat_history.append({
            "role": "assistant",
            "message": response["content"],
            "timestamp": time.time()
        })
        
        return response
    
    async def generate_response(self, message: str, context: Dict = None) -> Dict[str, Any]:
        """Generate response using RAG and LLM"""
        try:
            # Get RAG context if available
            rag_context = ""
            if self.rag_engine:
                rag_context = await self.rag_engine.query(message)
            
            # Build prompt
            system_prompt = """You are an AI assistant specializing in film production. 
You help filmmakers with screenplay analysis, visual mood boards, and production planning.
Provide practical, actionable advice for independent filmmakers."""
            
            if rag_context:
                system_prompt += f"\n\nProject context: {rag_context}"
            
            full_prompt = f"{system_prompt}\n\nUser: {message}\n\nAssistant:"
            
            # Send to Ollama
            payload = {
                "model": self.model_name,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "max_tokens": 512
                }
            }
            
            response = requests.post(f"{self.ollama_url}/api/generate", json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "content": result.get("response", "No response"),
                    "status": "success",
                    "has_rag_context": bool(rag_context)
                }
            else:
                return {
                    "content": "I'm having trouble responding right now.",
                    "status": "error",
                    "error": f"LLM error: {response.status_code}"
                }
                
        except Exception as e:
            return {
                "content": "I'm experiencing technical difficulties.",
                "status": "error", 
                "error": str(e)
            }
    
    def get_chat_history(self) -> List[Dict]:
        """Get chat history"""
        return self.chat_history
    
    def clear_history(self):
        """Clear chat history"""
        self.chat_history = []

async def test_chat_system():
    """Test chat system"""
    print("🧪 Testing Chat System...")
    
    chat = FilmChatSystem()
    response = await chat.chat("What makes a good screenplay?")
    print(f"💬 Chat response: {response['content'][:100]}...")
    
    print("✅ Chat system test completed")

if __name__ == "__main__":
    asyncio.run(test_chat_system())
