"""
Demo script to test the IDP agent functionality without the GUI.
Run this to verify the system is working correctly.
"""

import os
import sys
from RagSystem import DocumentRAG
from Agent import HealthcareIDPAgent
import json

# Dataset path (looks in root folder first)
import os
if os.path.exists("/workspaces/Hack-Nation-2026/Virtue Foundation Ghana v0.3 - Sheet1.csv"):
    DATASET_PATH = "/workspaces/Hack-Nation-2026/Virtue Foundation Ghana v0.3 - Sheet1.csv"
else:
    DATASET_PATH = "Virtue_Foundation_Ghana_v0_3_-_Sheet1.csv"  # Assume it's in root

def test_rag_system():
    """Test the RAG system."""
    print("\n" + "="*60)
    print("Testing RAG System")
    print("="*60)
    
    # Initialize RAG
    print("\n1. Initializing RAG system...")
    rag = DocumentRAG(DATASET_PATH)
    print(f"   ✓ Index built with {len(rag.document_chunks)} documents")
    
    # Test search
    print("\n2. Testing semantic search...")
    query = "cardiology facilities in Greater Accra"
    results = rag.search(query, top_k=3)
    print(f"   Query: '{query}'")
    print(f"   ✓ Found {len(results)} results:")
    for i, result in enumerate(results, 1):
        print(f"      {i}. {result['name']} (relevance: {result['relevance_score']:.3f})")
        print(f"         Citation: Row {result['row_idx']}")
    
    # Test medical desert detection
    print("\n3. Testing medical desert detection...")
    desert_analysis = rag.detect_medical_deserts(specialty="cardiology", region="Northern")
    print(f"   Specialty: cardiology, Region: Northern")
    print(f"   ✓ Facilities found: {desert_analysis.get('specialty_facilities', 0)}")
    print(f"   ✓ Medical desert: {desert_analysis['is_medical_desert']}")
    print(f"   ✓ Severity: {desert_analysis['desert_severity']}")
    
    # Test facility validation
    print("\n4. Testing facility validation...")
    # Get a facility name from the dataset
    facility_name = rag.df.iloc[0]['name']
    validation = rag.validate_facility_claims(facility_name)
    print(f"   Facility: {facility_name}")
    print(f"   ✓ Completeness score: {validation.get('completeness_score', 0)}%")
    print(f"   ✓ Suspicious claims: {len(validation.get('suspicious_claims', []))}")
    
    return rag


def test_agent(rag):
    """Test the agent system."""
    print("\n" + "="*60)
    print("Testing Agent System")
    print("="*60)
    
    # Check for API key
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("\n   ⚠️  WARNING: ANTHROPIC_API_KEY not set")
        print("   Skipping agent tests")
        print("   To test the agent, set your API key:")
        print("   export ANTHROPIC_API_KEY='your-key-here'")
        return
    
    # Initialize agent
    print("\n1. Initializing agent...")
    agent = HealthcareIDPAgent(rag, api_key)
    print("   ✓ Agent initialized")
    
    # Test query
    print("\n2. Running agent query...")
    query = "Are there any ophthalmology services in the Ashanti region?"
    print(f"   Query: '{query}'")
    print("   Processing... (this may take 10-20 seconds)")
    
    result = agent.run(query)
    
    print("\n   ✓ Agent response generated")
    print(f"   ✓ Citations: {len(result.get('citations', []))}")
    print(f"   ✓ Reasoning steps: {len(result.get('reasoning_steps', []))}")
    print(f"   ✓ Agent steps: {len(result.get('agent_steps', []))}")
    
    print("\n   Response preview:")
    response_lines = result['response'].split('\n')
    for line in response_lines[:10]:  # Show first 10 lines
        print(f"   {line}")
    if len(response_lines) > 10:
        print(f"   ... ({len(response_lines) - 10} more lines)")
    
    print("\n   Agent steps:")
    for i, step in enumerate(result.get('agent_steps', []), 1):
        print(f"   {i}. {step.get('step', 'Unknown')}")
        print(f"      Reasoning: {step.get('reasoning', 'N/A')[:80]}...")
    
    print("\n   Citations:")
    for i, citation in enumerate(result.get('citations', [])[:5], 1):
        print(f"   {i}. {citation.get('name', 'Unknown')} (Row {citation.get('row', 'N/A')})")


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("Virtue Foundation IDP Agent - Demo & Test Script")
    print("="*60)
    
    # Check dataset exists
    if not os.path.exists(DATASET_PATH):
        print(f"\n❌ ERROR: Dataset not found at {DATASET_PATH}")
        print("Please ensure the CSV file is in the correct location.")
        sys.exit(1)
    
    print(f"\n✓ Dataset found: {DATASET_PATH}")
    
    # Test RAG system
    rag = test_rag_system()
    
    # Test Agent system
    test_agent(rag)
    
    print("\n" + "="*60)
    print("Demo Complete!")
    print("="*60)
    print("\nTo launch the full Gradio interface, run:")
    print("  python app.py")
    print("\n")


if __name__ == "__main__":
    main()