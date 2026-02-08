import gradio as gr
import os
from RagSystem import DocumentRAG
from Agent import HealthcareIDPAgent
from Visualizations import HealthcareVisualizer
from MlflowTracker import IDPExperimentTracker
import json
import pandas as pd


# Initialize systems
print("Initializing Virtue Foundation IDP Agent...")

import os
import urllib.request

# Local filename
DATASET_LOCAL = "Virtue_Foundation_Ghana_v0_3_-_Sheet1.csv"

# GitHub raw URL
DATASET_URL = "https://raw.githubusercontent.com/lina1197/Hack-Nation-2026/main/Virtue%20Foundation%20Ghana%20v0.3%20-%20Sheet1.csv"

# Download CSV if not already present
if not os.path.exists(DATASET_LOCAL):
    print("Downloading dataset from GitHub...")
    urllib.request.urlretrieve(DATASET_URL, DATASET_LOCAL)
    print("Dataset downloaded.")

# Set path for RAG system
DATASET_PATH = DATASET_LOCAL



# Initialize RAG system
print("Building RAG index...")
rag = DocumentRAG(DATASET_PATH)

# Initialize agent (requires ANTHROPIC_API_KEY environment variable)
print("Initializing AI agent...")
api_key = os.getenv('ANTHROPIC_API_KEY')
if not api_key:
    print("WARNING: ANTHROPIC_API_KEY not set. Agent functionality will be limited.")
    agent = None
else:
    agent = HealthcareIDPAgent(rag, api_key)

# Initialize visualizer
viz = HealthcareVisualizer(rag)

# Initialize experiment tracker
tracker = IDPExperimentTracker()


def query_agent(user_query: str, enable_mlflow: bool = True):
    """Process user query through the agent."""
    if not agent:
        return (
            "Error: Agent not initialized. Please set ANTHROPIC_API_KEY environment variable.",
            "No citations available",
            "No reasoning available",
            "No agent steps available"
        )
    
    try:
        # Run agent
        result = agent.run(user_query)
        
        # Log to MLflow if enabled
        if enable_mlflow:
            tracker.log_agent_run(user_query, result)
        
        # Format response
        response_text = result['response']
        
        # Format citations
        citations = result.get('citations', [])
        citations_text = "### Citations\n\n"
        for i, citation in enumerate(citations, 1):
            citations_text += f"{i}. **{citation.get('name', 'Unknown')}** (Row {citation.get('row', 'N/A')})\n"
            citations_text += f"   Source: {citation.get('source', 'N/A')}\n\n"
        
        # Format reasoning steps
        reasoning_steps = result.get('reasoning_steps', [])
        reasoning_text = "### Reasoning Process\n\n"
        for i, step in enumerate(reasoning_steps, 1):
            reasoning_text += f"{i}. {step}\n"
        
        # Format agent steps
        agent_steps = result.get('agent_steps', [])
        agent_steps_text = "### Agent Execution Steps\n\n"
        for i, step in enumerate(agent_steps, 1):
            agent_steps_text += f"**Step {i}: {step.get('step', 'Unknown')}**\n"
            agent_steps_text += f"- Reasoning: {step.get('reasoning', 'N/A')}\n"
            if 'data_sources' in step and step['data_sources']:
                agent_steps_text += f"- Data sources: {len(step['data_sources'])} citations\n"
            agent_steps_text += "\n"
        
        return response_text, citations_text, reasoning_text, agent_steps_text
        
    except Exception as e:
        return f"Error: {str(e)}", "No citations", "No reasoning", "No steps"


def detect_medical_desert(specialty: str, region: str, enable_mlflow: bool = True):
    """Detect medical deserts for a given specialty and region."""
    try:
        analysis = rag.detect_medical_deserts(
            specialty=specialty if specialty else None,
            region=region if region else None
        )
        
        # Log to MLflow if enabled
        if enable_mlflow:
            tracker.log_desert_detection(specialty, region, analysis)
        
        # Format response
        response = f"## Medical Desert Analysis\n\n"
        response += f"**Specialty**: {specialty or 'All'}\n"
        response += f"**Region**: {region or 'All regions'}\n\n"
        response += f"**Total facilities in dataset**: {analysis['total_facilities']}\n"
        
        if 'regional_facilities' in analysis:
            response += f"**Facilities in region**: {analysis['regional_facilities']}\n"
        
        if 'specialty_facilities' in analysis:
            response += f"**Facilities with this specialty**: {analysis['specialty_facilities']}\n"
        
        response += f"\n**Medical Desert Status**: {'⚠️ YES' if analysis['is_medical_desert'] else '✓ NO'}\n"
        response += f"**Severity**: {analysis['desert_severity'].upper()}\n\n"
        
        if analysis['available_facilities']:
            response += "### Available Facilities\n\n"
            for fac in analysis['available_facilities'][:10]:
                response += f"- **{fac['name']}** - {fac['location']} (Row {fac['row_idx']})\n"
        else:
            response += "### ⚠️ No facilities found with this specialty in the specified region\n"
        
        # Create visualization
        if specialty:
            fig = viz.create_medical_desert_heatmap(specialty)
        else:
            fig = viz.create_facility_map(region=region)
        
        return response, fig
        
    except Exception as e:
        return f"Error: {str(e)}", None


def validate_facility(facility_name: str, enable_mlflow: bool = True):
    """Validate a facility's claims."""
    try:
        validation = rag.validate_facility_claims(facility_name)
        
        if 'error' in validation:
            return f"Error: {validation['error']}"
        
        # Log to MLflow if enabled
        if enable_mlflow:
            tracker.log_validation_run(facility_name, validation)
        
        # Format response
        response = f"## Facility Validation Report: {facility_name}\n\n"
        response += f"**Completeness Score**: {validation['completeness_score']}%\n\n"
        
        if validation['missing_critical_fields']:
            response += "### ⚠️ Missing Critical Fields\n"
            for field in validation['missing_critical_fields']:
                response += f"- {field}\n"
            response += "\n"
        
        if validation['suspicious_claims']:
            response += "### 🔍 Suspicious Claims\n"
            for claim in validation['suspicious_claims']:
                response += f"- {claim}\n"
            response += "\n"
        
        if validation['data_quality_issues']:
            response += "### ⚠️ Data Quality Issues\n"
            for issue in validation['data_quality_issues']:
                response += f"- {issue}\n"
            response += "\n"
        
        if not validation['suspicious_claims'] and not validation['data_quality_issues']:
            response += "### ✓ No major issues detected\n"
        
        response += f"\n**Citation**: Row {validation['citation']['row']}, Source: {validation['citation']['source']}\n"
        
        return response
        
    except Exception as e:
        return f"Error: {str(e)}"


def search_facilities(search_query: str):
    """Search for facilities."""
    try:
        results = rag.search(search_query, top_k=10)
        
        response = f"## Search Results for: '{search_query}'\n\n"
        response += f"Found {len(results)} relevant facilities:\n\n"
        
        for i, result in enumerate(results, 1):
            response += f"### {i}. {result['name']}\n"
            response += f"**Relevance Score**: {result['relevance_score']:.3f}\n"
            response += f"**Type**: {result['organization_type']}\n"
            response += f"**Location**: {result['full_data'].get('address_city', 'N/A')}, {result['full_data'].get('address_stateOrRegion', 'N/A')}\n"
            
            # Get specialties
            try:
                specialties = json.loads(result['full_data'].get('specialties', '[]'))
                if specialties:
                    response += f"**Specialties**: {', '.join(specialties[:5])}\n"
            except:
                pass
            
            response += f"**Citation**: Row {result['row_idx']}, Source: {result['source_url']}\n\n"
        
        return response
        
    except Exception as e:
        return f"Error: {str(e)}"


def show_visualizations(viz_type: str, specialty: str = None, region: str = None):
    """Generate visualizations."""
    try:
        if viz_type == "Facility Map":
            return viz.create_facility_map(region=region, specialty=specialty)
        elif viz_type == "Medical Desert Heatmap":
            if not specialty:
                specialty = "cardiology"  # Default
            return viz.create_medical_desert_heatmap(specialty)
        elif viz_type == "Specialty Distribution":
            return viz.create_specialty_distribution()
        elif viz_type == "Facility Types":
            return viz.create_facility_type_pie()
        else:
            return None
    except Exception as e:
        print(f"Visualization error: {e}")
        return None


# Build Gradio interface
with gr.Blocks(title="Virtue Foundation - Healthcare IDP Agent", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🏥 Virtue Foundation - Intelligent Document Parsing Agent
    
    ## Bridging Medical Deserts with AI
    
    This AI agent helps identify healthcare infrastructure gaps and connects medical expertise with communities in need.
    Built for the Databricks challenge to reduce time to lifesaving treatment by 100×.
    
    ### Features:
    - 🔍 **Intelligent Search**: Find facilities and medical services using natural language
    - 🗺️ **Medical Desert Detection**: Identify gaps in healthcare coverage
    - ✅ **Facility Validation**: Verify claims and detect data anomalies
    - 📊 **Visualizations**: Interactive maps and analytics
    - 📝 **Citations**: Full transparency with row-level data sources
    - 🔬 **MLflow Tracking**: Experiment logging for reproducibility
    """)
    
    with gr.Tabs():
        # Tab 1: AI Agent
        with gr.Tab("🤖 AI Agent"):
            gr.Markdown("### Ask questions in natural language about healthcare infrastructure in Ghana")
            
            with gr.Row():
                query_input = gr.Textbox(
                    label="Your Question",
                    placeholder="e.g., 'Are there any cardiology facilities in the Greater Accra region?' or 'Which regions lack ophthalmology services?'",
                    lines=3
                )
            
            mlflow_checkbox = gr.Checkbox(label="Log to MLflow", value=True)
            query_button = gr.Button("Ask Agent", variant="primary")
            
            response_output = gr.Markdown(label="Agent Response")
            
            with gr.Accordion("📚 Citations", open=False):
                citations_output = gr.Markdown()
            
            with gr.Accordion("🧠 Reasoning Process", open=False):
                reasoning_output = gr.Markdown()
            
            with gr.Accordion("🔧 Agent Steps (with data sources)", open=True):
                steps_output = gr.Markdown()
            
            query_button.click(
                query_agent,
                inputs=[query_input, mlflow_checkbox],
                outputs=[response_output, citations_output, reasoning_output, steps_output]
            )
            
            gr.Examples(
                examples=[
                    "Which regions in Ghana lack cardiology services?",
                    "Show me all facilities with emergency medicine capabilities",
                    "Are there any medical deserts for pediatric care?",
                    "What facilities offer ophthalmology in the Ashanti region?",
                    "Find hospitals with ICU capabilities"
                ],
                inputs=query_input
            )
        
        # Tab 2: Medical Desert Detection
        with gr.Tab("🗺️ Medical Desert Detection"):
            gr.Markdown("### Identify regions with limited access to specific medical specialties")
            
            with gr.Row():
                specialty_input = gr.Textbox(
                    label="Medical Specialty",
                    placeholder="e.g., cardiology, pediatrics, ophthalmology",
                    value="cardiology"
                )
                region_input = gr.Textbox(
                    label="Region (optional)",
                    placeholder="e.g., Greater Accra, Ashanti"
                )
            
            mlflow_desert_checkbox = gr.Checkbox(label="Log to MLflow", value=True)
            desert_button = gr.Button("Detect Medical Deserts", variant="primary")
            
            desert_output = gr.Markdown(label="Analysis Results")
            desert_viz = gr.Plot(label="Visualization")
            
            desert_button.click(
                detect_medical_desert,
                inputs=[specialty_input, region_input, mlflow_desert_checkbox],
                outputs=[desert_output, desert_viz]
            )
        
        # Tab 3: Facility Validation
        with gr.Tab("✅ Facility Validation"):
            gr.Markdown("### Verify facility capabilities and detect suspicious claims")
            
            facility_input = gr.Textbox(
                label="Facility Name",
                placeholder="Enter exact facility name from dataset"
            )
            
            mlflow_validation_checkbox = gr.Checkbox(label="Log to MLflow", value=True)
            validate_button = gr.Button("Validate Facility", variant="primary")
            
            validation_output = gr.Markdown(label="Validation Report")
            
            validate_button.click(
                validate_facility,
                inputs=[facility_input, mlflow_validation_checkbox],
                outputs=validation_output
            )
        
        # Tab 4: Search
        with gr.Tab("🔍 Search Facilities"):
            gr.Markdown("### Semantic search across all facilities")
            
            search_input = gr.Textbox(
                label="Search Query",
                placeholder="e.g., 'hospitals with MRI equipment' or 'maternity care in Kumasi'",
                lines=2
            )
            
            search_button = gr.Button("Search", variant="primary")
            search_output = gr.Markdown(label="Search Results")
            
            search_button.click(
                search_facilities,
                inputs=search_input,
                outputs=search_output
            )
        
        # Tab 5: Visualizations
        with gr.Tab("📊 Visualizations"):
            gr.Markdown("### Interactive maps and analytics")
            
            with gr.Row():
                viz_type = gr.Dropdown(
                    choices=["Facility Map", "Medical Desert Heatmap", "Specialty Distribution", "Facility Types"],
                    label="Visualization Type",
                    value="Facility Map"
                )
            
            with gr.Row():
                viz_specialty = gr.Textbox(label="Filter by Specialty (optional)", placeholder="e.g., cardiology")
                viz_region = gr.Textbox(label="Filter by Region (optional)", placeholder="e.g., Greater Accra")
            
            viz_button = gr.Button("Generate Visualization", variant="primary")
            viz_output = gr.Plot(label="Visualization")
            
            viz_button.click(
                show_visualizations,
                inputs=[viz_type, viz_specialty, viz_region],
                outputs=viz_output
            )
    
    gr.Markdown("""
    ---
    ### About the Data
    - **Dataset**: Virtue Foundation Ghana Healthcare Facilities (v0.3)
    - **Records**: 1,000+ facilities and NGOs
    - **Coverage**: All regions of Ghana
    - **Features**: Specialties, equipment, procedures, capabilities, and contact information
    
    ### Tech Stack
    - **RAG**: FAISS + Sentence Transformers
    - **Agent**: LangGraph + Claude Sonnet 4
    - **Tracking**: MLflow
    - **Visualization**: Plotly
    - **Interface**: Gradio
    
    Built for the Databricks challenge by leveraging agentic AI to bridge medical deserts. 🌍
    """)

# Launch

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))  # Uses cloud-assigned PORT if available
    demo.launch(server_name="0.0.0.0", server_port=port, share=True)
