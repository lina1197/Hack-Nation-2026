from typing import TypedDict, Annotated, List, Dict, Any
import operator
from langgraph.graph import StateGraph, END
from anthropic import Anthropic
import json
import os


class AgentState(TypedDict):
    """State for the agent workflow."""
    query: str
    query_type: str  # 'search', 'desert_detection', 'validation', 'general'
    context: List[Dict[str, Any]]
    analysis: Dict[str, Any]
    citations: List[Dict[str, Any]]
    response: str
    reasoning_steps: Annotated[List[str], operator.add]
    agent_steps: Annotated[List[Dict[str, Any]], operator.add]


class HealthcareIDPAgent:
    """
    Intelligent Document Parsing Agent for healthcare facility data.
    Uses LangGraph for agentic orchestration and Claude for reasoning.
    """
    
    def __init__(self, rag_system, api_key: str = None):
        """
        Initialize the IDP agent.
        
        Args:
            rag_system: DocumentRAG instance
            api_key: Anthropic API key
        """
        self.rag = rag_system
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        self.client = Anthropic(api_key=self.api_key)
        self.graph = self._build_graph()
        
    def _build_graph(self) -> StateGraph:
        """Build the agent workflow graph."""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("classify_query", self.classify_query)
        workflow.add_node("retrieve_context", self.retrieve_context)
        workflow.add_node("analyze", self.analyze)
        workflow.add_node("generate_response", self.generate_response)
        
        # Add edges
        workflow.set_entry_point("classify_query")
        workflow.add_edge("classify_query", "retrieve_context")
        workflow.add_edge("retrieve_context", "analyze")
        workflow.add_edge("analyze", "generate_response")
        workflow.add_edge("generate_response", END)
        
        return workflow.compile()
    
    def classify_query(self, state: AgentState) -> AgentState:
        """Classify the user query to determine the appropriate workflow."""
        query = state['query']
        
        # Use Claude to classify the query
        classification_prompt = f"""Classify this healthcare query into one of these categories:
- 'search': User wants to find specific facilities or information
- 'desert_detection': User wants to identify medical deserts or gaps in care
- 'validation': User wants to verify facility capabilities or detect anomalies
- 'general': General question about healthcare infrastructure

Query: {query}

Respond with only the category name."""
        
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=50,
            messages=[{"role": "user", "content": classification_prompt}]
        )
        
        query_type = response.content[0].text.strip().lower()
        state['query_type'] = query_type
        state['reasoning_steps'].append(f"Query classified as: {query_type}")
        state['agent_steps'].append({
            'step': 'query_classification',
            'input': query,
            'output': query_type,
            'reasoning': 'Classified query type to determine appropriate analysis workflow'
        })
        
        return state
    
    def retrieve_context(self, state: AgentState) -> AgentState:
        """Retrieve relevant context from the RAG system."""
        query = state['query']
        query_type = state['query_type']
        
        # Perform semantic search
        search_results = self.rag.search(query, top_k=5)
        
        state['context'] = search_results
        state['citations'].extend([r['citation'] for r in search_results])
        state['reasoning_steps'].append(f"Retrieved {len(search_results)} relevant documents")
        state['agent_steps'].append({
            'step': 'context_retrieval',
            'input': query,
            'output': f"Retrieved {len(search_results)} documents",
            'data_sources': [r['citation'] for r in search_results],
            'reasoning': 'Used semantic search to find relevant facility data'
        })
        
        return state
    
    def analyze(self, state: AgentState) -> AgentState:
        """Perform analysis based on query type."""
        query_type = state['query_type']
        query = state['query']
        context = state['context']
        
        analysis = {}
        
        if query_type == 'desert_detection':
            # Extract specialty and region from query using Claude
            extraction_prompt = f"""Extract the medical specialty and/or region from this query:
"{query}"

Respond in JSON format:
{{
  "specialty": "specialty name or null",
  "region": "region name or null"
}}"""
            
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=200,
                messages=[{"role": "user", "content": extraction_prompt}]
            )
            
            try:
                extraction = json.loads(response.content[0].text)
                specialty = extraction.get('specialty')
                region = extraction.get('region')
                
                # Perform medical desert analysis
                desert_analysis = self.rag.detect_medical_deserts(specialty, region)
                analysis['desert_detection'] = desert_analysis
                
                state['reasoning_steps'].append(
                    f"Analyzed medical desert for specialty={specialty}, region={region}"
                )
                state['agent_steps'].append({
                    'step': 'desert_analysis',
                    'input': {'specialty': specialty, 'region': region},
                    'output': desert_analysis,
                    'data_sources': desert_analysis.get('citations', []),
                    'reasoning': 'Identified facilities with specified specialty in region to assess coverage'
                })
            except Exception as e:
                analysis['error'] = str(e)
                
        elif query_type == 'validation':
            # Extract facility name from query
            extraction_prompt = f"""Extract the facility name from this query:
"{query}"

Respond with just the facility name."""
            
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=100,
                messages=[{"role": "user", "content": extraction_prompt}]
            )
            
            facility_name = response.content[0].text.strip()
            
            # Validate facility
            validation = self.rag.validate_facility_claims(facility_name)
            analysis['validation'] = validation
            
            state['reasoning_steps'].append(f"Validated facility: {facility_name}")
            state['agent_steps'].append({
                'step': 'facility_validation',
                'input': facility_name,
                'output': validation,
                'data_sources': [validation.get('citation', {})],
                'reasoning': 'Checked facility data completeness and identified suspicious claims'
            })
            
        else:  # search or general
            # Synthesize information from context
            analysis['search_results'] = context
            state['reasoning_steps'].append(f"Compiled {len(context)} search results")
            state['agent_steps'].append({
                'step': 'information_synthesis',
                'input': query,
                'output': f"Synthesized data from {len(context)} sources",
                'data_sources': [r['citation'] for r in context],
                'reasoning': 'Aggregated relevant facility information from multiple sources'
            })
        
        state['analysis'] = analysis
        return state
    
    def generate_response(self, state: AgentState) -> AgentState:
        """Generate final response using Claude."""
        query = state['query']
        analysis = state['analysis']
        context = state['context']
        reasoning_steps = state['reasoning_steps']
        
        # Prepare context for Claude
        context_text = "\n\n".join([
            f"[Source {i+1} - Row {r['row_idx']}]: {r['text']}"
            for i, r in enumerate(context[:5])
        ])
        
        analysis_text = json.dumps(analysis, indent=2)
        
        # Generate response
        prompt = f"""You are an expert healthcare infrastructure analyst helping the Virtue Foundation identify medical resource gaps.

User Query: {query}

Retrieved Context:
{context_text}

Analysis Results:
{analysis_text}

Reasoning Steps Taken:
{chr(10).join(f"{i+1}. {step}" for i, step in enumerate(reasoning_steps))}

Please provide a clear, actionable response that:
1. Directly answers the user's query
2. Highlights key findings and insights
3. Identifies any gaps or concerns in healthcare infrastructure
4. Provides specific recommendations if applicable
5. Cites specific data sources when making claims (reference row numbers)

Format your response in a professional yet accessible tone suitable for NGO planners."""
        
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        state['response'] = response.content[0].text
        state['agent_steps'].append({
            'step': 'response_generation',
            'input': 'Analysis synthesis',
            'output': 'Natural language response generated',
            'reasoning': 'Synthesized all findings into actionable recommendations with citations'
        })
        
        return state
    
    def run(self, query: str) -> Dict[str, Any]:
        """
        Run the agent on a query.
        
        Args:
            query: User query
            
        Returns:
            Complete agent response with citations and reasoning
        """
        initial_state = {
            'query': query,
            'query_type': '',
            'context': [],
            'analysis': {},
            'citations': [],
            'response': '',
            'reasoning_steps': [],
            'agent_steps': []
        }
        
        final_state = self.graph.invoke(initial_state)
        
        return {
            'query': query,
            'response': final_state['response'],
            'citations': final_state['citations'],
            'reasoning_steps': final_state['reasoning_steps'],
            'agent_steps': final_state['agent_steps'],
            'analysis': final_state['analysis']
        }