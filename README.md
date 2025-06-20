# 🎬 Film Creative RAG

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
