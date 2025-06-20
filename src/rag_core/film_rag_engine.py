#!/usr/bin/env python3
"""
Film Creative RAG - Core RAG Engine
==================================
Modular RAG implementation with chunking and embedding
"""

import asyncio
import json
from pathlib import Path
from typing import List, Dict, Any
import requests

class FilmRAGCore:
    """Core RAG functionality for Film Creative RAG"""
    
    def __init__(self, working_dir="data/vector_store"):
        self.working_dir = Path(working_dir)
        self.working_dir.mkdir(parents=True, exist_ok=True)
        self.ollama_url = "http://localhost:11434"
        self.model_name = "llama3.2:3b"
        
        # Initialize embedding model
        try:
            from sentence_transformers import SentenceTransformer
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            print("✅ Embedding model loaded")
        except ImportError:
            print("⚠️ Sentence transformers not available")
            self.embedding_model = None
        
        # Knowledge storage
        self.knowledge_store = {
            "screenplays": {},
            "mood_boards": {},
            "relationships": []
        }
    
    def chunk_screenplay(self, content: str, title: str) -> List[Dict]:
        """Chunk screenplay content intelligently"""
        chunks = []
        lines = content.split('\n')
        
        current_scene = ""
        current_chunk = ""
        current_characters = set()
        scene_count = 0
        
        for line in lines:
            line = line.strip()
            
            # Scene break detection
            if line.startswith(('INT.', 'EXT.', 'FADE IN', 'FADE OUT')):
                if current_chunk.strip():
                    chunks.append({
                        "content": current_chunk.strip(),
                        "scene_header": current_scene,
                        "characters": list(current_characters),
                        "scene_number": scene_count,
                        "chunk_type": "scene"
                    })
                
                current_scene = line
                current_chunk = line + "\n"
                current_characters = set()
                scene_count += 1
            
            # Character detection (ALL CAPS lines)
            elif line.isupper() and len(line.split()) <= 3 and line:
                current_characters.add(line)
                current_chunk += line + "\n"
            
            else:
                current_chunk += line + "\n"
        
        # Add final chunk
        if current_chunk.strip():
            chunks.append({
                "content": current_chunk.strip(),
                "scene_header": current_scene,
                "characters": list(current_characters),
                "scene_number": scene_count,
                "chunk_type": "scene"
            })
        
        return chunks
    
    def extract_entities(self, chunks: List[Dict]) -> Dict:
        """Extract characters and locations from chunks"""
        entities = {"characters": {}, "locations": {}}
        
        for chunk in chunks:
            # Process characters
            for character in chunk.get("characters", []):
                if character not in entities["characters"]:
                    entities["characters"][character] = {
                        "mentions": 0,
                        "scenes": []
                    }
                entities["characters"][character]["mentions"] += 1
                entities["characters"][character]["scenes"].append(chunk.get("scene_number", 0))
            
            # Process locations from scene headers
            scene_header = chunk.get("scene_header", "")
            if scene_header:
                location = scene_header.replace("INT.", "").replace("EXT.", "").split("-")[0].strip()
                if location and location not in entities["locations"]:
                    entities["locations"][location] = {
                        "type": "location",
                        "scenes": [chunk.get("scene_number", 0)]
                    }
        
        return entities
    
    async def add_screenplay(self, content: str, title: str) -> Dict:
        """Add screenplay to knowledge store"""
        print(f"📝 Processing screenplay: {title}")
        
        # Chunk content
        chunks = self.chunk_screenplay(content, title)
        
        # Extract entities
        entities = self.extract_entities(chunks)
        
        # Store in knowledge store
        self.knowledge_store["screenplays"][title] = {
            "content": content,
            "chunks": chunks,
            "entities": entities,
            "metadata": {
                "total_chunks": len(chunks),
                "total_characters": len(entities["characters"]),
                "total_locations": len(entities["locations"])
            }
        }
        
        # Save to file
        self.save_knowledge_store()
        
        print(f"✅ Screenplay processed: {len(chunks)} chunks, {len(entities['characters'])} characters")
        return self.knowledge_store["screenplays"][title]["metadata"]
    
    async def add_mood_board(self, visual_data: Dict, project_name: str) -> Dict:
        """Add mood board to knowledge store"""
        print(f"🎨 Processing mood board: {project_name}")
        
        self.knowledge_store["mood_boards"][project_name] = {
            "visual_data": visual_data,
            "metadata": {
                "images_count": visual_data.get("images_found", 0),
                "color_palettes": len(visual_data.get("color_palettes", [])),
                "style_elements": len(visual_data.get("style_elements", []))
            }
        }
        
        self.save_knowledge_store()
        
        print(f"✅ Mood board processed: {project_name}")
        return self.knowledge_store["mood_boards"][project_name]["metadata"]
    
    async def query(self, query: str, context: str = "") -> str:
        """Query the knowledge store with LLM"""
        try:
            # Build context from knowledge store
            context_info = self.build_context_for_query(query)
            
            # Create enhanced prompt
            prompt = f"""Based on the following film project information, answer the user's question:

{context_info}

User Question: {query}

Provide a helpful, specific answer based on the project information:"""
            
            # Send to Ollama
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "max_tokens": 512
                }
            }
            
            response = requests.post(f"{self.ollama_url}/api/generate", json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "No response generated")
            else:
                return f"Error querying LLM: {response.status_code}"
                
        except Exception as e:
            return f"Query error: {str(e)}"
    
    def build_context_for_query(self, query: str) -> str:
        """Build relevant context from knowledge store"""
        context_parts = []
        
        # Add screenplay information
        for title, screenplay in self.knowledge_store["screenplays"].items():
            context_parts.append(f"Screenplay '{title}':")
            context_parts.append(f"- Characters: {list(screenplay['entities']['characters'].keys())[:5]}")
            context_parts.append(f"- Total scenes: {len(screenplay['chunks'])}")
        
        # Add mood board information
        for name, mood_board in self.knowledge_store["mood_boards"].items():
            context_parts.append(f"Mood Board '{name}':")
            context_parts.append(f"- Images: {mood_board['metadata']['images_count']}")
            context_parts.append(f"- Visual elements analyzed")
        
        return "\n".join(context_parts)
    
    def save_knowledge_store(self):
        """Save knowledge store to file"""
        store_file = self.working_dir / "knowledge_store.json"
        with open(store_file, 'w') as f:
            json.dump(self.knowledge_store, f, indent=2)
    
    def load_knowledge_store(self):
        """Load knowledge store from file"""
        store_file = self.working_dir / "knowledge_store.json"
        if store_file.exists():
            try:
                with open(store_file, 'r') as f:
                    self.knowledge_store = json.load(f)
                print("✅ Knowledge store loaded")
            except Exception as e:
                print(f"⚠️ Could not load knowledge store: {e}")

async def test_rag_core():
    """Test RAG core functionality"""
    print("🧪 Testing RAG Core...")
    
    rag = FilmRAGCore()
    
    # Test screenplay processing
    sample_screenplay = """
INT. TECH LAB - DAY

ALICE works at her computer.

ALICE
This code needs to be perfect.

BOB enters.

BOB
How's the progress?
"""
    
    result = await rag.add_screenplay(sample_screenplay, "Test Script")
    print(f"📊 Processing result: {result}")
    
    # Test query
    query_result = await rag.query("Who are the main characters?")
    print(f"💬 Query result: {query_result}")
    
    print("✅ RAG Core test completed")

if __name__ == "__main__":
    asyncio.run(test_rag_core())
