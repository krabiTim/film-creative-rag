#!/bin/bash
# Easy Git Push Script for Film Creative RAG

cd ~/film-creative-rag

echo "ðŸ™ Film Creative RAG - Git Push"
echo "==============================="

echo ""
echo "ðŸ“Š Current status:"
git status --short

echo ""
echo "ðŸ“ Adding changes..."
git add .

echo ""
echo "ðŸ’¾ Committing changes..."
read -p "Enter commit message (or press Enter for default): " commit_msg

if [ -z "$commit_msg" ]; then
    commit_msg="Update Film Creative RAG system - $(date '+%Y-%m-%d %H:%M')"
fi

git commit -m "$commit_msg"

echo ""
echo "ðŸš€ Pushing to remote repository..."
git push origin main

echo ""
echo "âœ… Git push completed!"
echo ""
echo "ðŸ“Š Latest commits:"
git log --oneline -3

echo ""
echo "ðŸŽ¬ Film Creative RAG repository updated!"
