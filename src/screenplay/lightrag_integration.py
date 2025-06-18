#!/usr/bin/env python3
"""
LightRAG + Screenplay Integration
Proper implementation following project plan
"""
import os
import sys
from pathlib import Path
from datetime import datetime

# Test LightRAG availability
try:
    from lightrag import LightRAG, QueryParam
    LIGHTRAG_AVAILABLE = True
    print("âœ… LightRAG imported successfully")
except ImportError as e:
    LIGHTRAG_AVAILABLE = False
    print(f"âŒ LightRAG import failed: {e}")
    print("ðŸ’¡ Solution: Run 'pip install git+https://github.com/HKUDS/LightRAG.git'")

# Test Screenplay Engine availability
try:
    from screenplay_engine import ScreenplayIntelligence
    SCREENPLAY_AVAILABLE = True
    print("âœ… Screenplay engine available")
except ImportError as e:
    SCREENPLAY_AVAILABLE = False
    print(f"âŒ Screenplay engine import failed: {e}")

class FilmCreativeRAG:
    """Main Film Creative RAG System - LightRAG + Screenplay Integration"""
    
    def __init__(self, working_dir="./film_rag_storage"):
        print("\nðŸŽ¬ Initializing Film Creative RAG System")
        print("=" * 50)
        
        self.working_dir = Path(working_dir)
        self.working_dir.mkdir(exist_ok=True)
        
        # Initialize components
        self.screenplay_engine = None
        self.rag = None
        self.system_ready = False
        
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize all system components"""
        
        # Initialize Screenplay Engine
        if SCREENPLAY_AVAILABLE:
            try:
                self.screenplay_engine = ScreenplayIntelligence()
                print("âœ… Screenplay engine initialized")
            except Exception as e:
                print(f"âŒ Screenplay engine failed: {e}")
        
        # Initialize LightRAG
        if LIGHTRAG_AVAILABLE:
            try:
                self.rag = LightRAG(working_dir=str(self.working_dir))
                print("âœ… LightRAG initialized")
                print(f"ðŸ“ Storage: {self.working_dir}")
            except Exception as e:
                print(f"âŒ LightRAG initialization failed: {e}")
                print(f"ðŸ’¡ Check: {e}")
        
        # System readiness check
        if self.screenplay_engine and self.rag:
            self.system_ready = True
            print("ðŸš€ Film Creative RAG System: READY")
        else:
            print("âš ï¸  System partially ready - some components missing")
    
    def analyze_screenplay(self, content, title="Untitled"):
        """Complete screenplay analysis with AI enhancement"""
        print(f"\nðŸŽ¯ Analyzing: {title}")
        print("=" * 40)
        
        results = {"title": title, "timestamp": datetime.now().isoformat()}
        
        # Basic screenplay analysis
        if self.screenplay_engine:
            print("ðŸ“Š Running basic screenplay analysis...")
            basic_analysis = self.screenplay_engine.analyze_screenplay(content, title)
            results["basic_analysis"] = basic_analysis
            print("âœ… Basic analysis complete")
        else:
            print("âš ï¸  Basic analysis skipped (engine not available)")
        
        # AI-enhanced analysis with LightRAG
        if self.rag:
            print("ðŸ§  Running AI-enhanced analysis...")
            try:
                # Insert screenplay into knowledge graph
                self.rag.insert(content)
                print("âœ… Screenplay added to knowledge graph")
                
                # Generate AI insights
                ai_insights = self._generate_ai_insights()
                results["ai_insights"] = ai_insights
                print("âœ… AI insights generated")
                
            except Exception as e:
                print(f"âŒ AI analysis failed: {e}")
                results["ai_error"] = str(e)
        else:
            print("âš ï¸  AI analysis skipped (LightRAG not available)")
        
        # Display results summary
        self._display_summary(results)
        
        return results
    
    def _generate_ai_insights(self):
        """Generate AI-powered insights using LightRAG"""
        insights = {}
        
        queries = [
            ("character_analysis", "Who are the main characters and what are their motivations?"),
            ("theme_analysis", "What are the central themes and emotional arcs?"),
            ("structure_analysis", "How is the story structured and paced?"),
            ("production_insights", "What are the key production considerations?")
        ]
        
        for insight_type, query in queries:
            try:
                response = self.rag.query(query, param=QueryParam(mode="hybrid"))
                insights[insight_type] = response
                print(f"   âœ… {insight_type}")
            except Exception as e:
                insights[insight_type] = f"Error: {e}"
                print(f"   âŒ {insight_type}: {e}")
        
        return insights
    
    def _display_summary(self, results):
        """Display analysis summary"""
        print(f"\nðŸŽ¬ ANALYSIS SUMMARY: {results['title']}")
        print("=" * 50)
        
        if "basic_analysis" in results:
            basic = results["basic_analysis"]
            meta = basic.get("metadata", {})
            print(f"ðŸ“Š Duration: {meta.get('estimated_duration_minutes', 'N/A')} minutes")
            print(f"ðŸŽ­ Scenes: {meta.get('total_scenes', 'N/A')}")
            print(f"ðŸ‘¥ Characters: {meta.get('total_characters', 'N/A')}")
            print(f"âš¡ Complexity: {meta.get('complexity_score', 'N/A')}")
        
        if "ai_insights" in results:
            print(f"\nðŸ§  AI INSIGHTS AVAILABLE:")
            for insight_type in results["ai_insights"]:
                print(f"   âœ… {insight_type.replace('_', ' ').title()}")
        
        print(f"\nâœ… Analysis complete at {results['timestamp'][:19]}")
    
    def query(self, question):
        """Query the system with natural language"""
        if not self.rag:
            return "âŒ LightRAG not available for queries"
        
        try:
            response = self.rag.query(question, param=QueryParam(mode="hybrid"))
            return response
        except Exception as e:
            return f"âŒ Query failed: {e}"
    
    def get_system_status(self):
        """Get detailed system status"""
        status = {
            "screenplay_engine": "âœ… Available" if self.screenplay_engine else "âŒ Not Available",
            "lightrag": "âœ… Available" if self.rag else "âŒ Not Available", 
            "storage_dir": str(self.working_dir),
            "system_ready": self.system_ready
        }
        return status

def run_comprehensive_test():
    """Run comprehensive system test"""
    print("ðŸ§ª COMPREHENSIVE SYSTEM TEST")
    print("=" * 50)
    
    # Initialize system
    system = FilmCreativeRAG()
    
    # Display system status
    print(f"\nðŸ“Š SYSTEM STATUS:")
    status = system.get_system_status()
    for component, state in status.items():
        print(f"   {component}: {state}")
    
    # Test with sample screenplay
    sample_screenplay = """
Title: System Test Screenplay
Author: Film Creative RAG

FADE IN:

INT. TECH LAB - DAY

ALICE (30), brilliant researcher, works on an AI system.

ALICE
Finally, a system that understands creativity!

BOB (35), skeptical filmmaker, watches over her shoulder.

BOB
But can it really help artists?

ALICE
Let's find out.

She runs the analysis.

FADE OUT.

THE END
"""
    
    print(f"\nðŸŽ¬ TESTING WITH SAMPLE SCREENPLAY")
    print("=" * 40)
    
    # Run analysis
    results = system.analyze_screenplay(sample_screenplay, "System Test")
    
    # Test querying if available
    if system.rag:
        print(f"\nðŸ¤– TESTING AI QUERIES")
        print("=" * 30)
        
        test_questions = [
            "Who are the main characters?",
            "What is this story about?",
            "What mood does this screenplay convey?"
        ]
        
        for question in test_questions:
            print(f"\nQ: {question}")
            answer = system.query(question)
            print(f"A: {answer[:100]}..." if len(str(answer)) > 100 else f"A: {answer}")
    
    print(f"\nðŸŽ¯ TEST RESULTS")
    print("=" * 20)
    print(f"âœ… System initialized: {system.system_ready}")
    print(f"âœ… Analysis completed: {'ai_insights' in results}")
    print(f"âœ… Storage working: {system.working_dir.exists()}")
    
    return system, results

if __name__ == "__main__":
    print("ðŸŽ¬ Film Creative RAG - LightRAG Integration Test")
    print("=" * 60)
    
    # Run comprehensive test
    system, results = run_comprehensive_test()
    
    print(f"\nðŸš€ INTEGRATION TEST COMPLETE!")
    print("=" * 40)
    
    if system.system_ready:
        print("âœ… LightRAG + Screenplay integration: SUCCESS")
        print("ðŸŽ¯ Ready for Phase 3: Mood Board Processing")
    else:
        print("âš ï¸  Integration partially working")
        print("ðŸ’¡ Check component status above for issues")
    
    print(f"\nðŸ“ Files created in: {system.working_dir}")
    print("ðŸŽ¬ Film Creative RAG System ready for filmmakers!")
