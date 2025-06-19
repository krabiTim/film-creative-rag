#!/bin/bash
# Git Pull Script for Film Creative RAG

cd ~/film-creative-rag

echo "ðŸ“¥ Film Creative RAG - Git Pull"
echo "==============================="

echo ""
echo "ðŸ“Š Current branch and status:"
git branch --show-current
git status --short

echo ""
echo "ðŸ”„ Fetching latest changes..."
git fetch origin

echo ""
echo "ðŸ“‹ Checking for updates..."
git log HEAD..origin/main --oneline

echo ""
echo "ðŸ”„ Pulling latest changes..."
git pull origin main

echo ""
echo "âœ… Git pull completed!"
echo ""
echo "ðŸ“Š Latest commits:"
git log --oneline -5

echo ""
echo "ðŸŽ¬ Film Creative RAG repository synchronized!"
