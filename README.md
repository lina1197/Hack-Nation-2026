# Hack-Nation-2026
# Virtue Foundation - Healthcare IDP Agent 🏥

## Bridging Medical Deserts with AI

An Intelligent Document Parsing (IDP) agent that identifies healthcare infrastructure gaps and connects medical expertise with communities in need across Ghana.

**Built for the Databricks Challenge**: Reduce time to lifesaving treatment by 100× using agentic AI.

---

## 🎯 Problem Statement

By 2030, the world will face a shortage of over 10 million healthcare workers — not because expertise doesn't exist, but because it is not intelligently coordinated. This system addresses this planetary-scale coordination failure by building an AI intelligence layer that can:

- ✅ Identify infrastructure gaps and medical deserts
- ✅ Detect incomplete or suspicious claims about hospital capabilities  
- ✅ Map where critical expertise is available — and where lives are at risk due to lack of access

---

## ✨ Features

### Core Features (MVP)

1. **Unstructured Feature Extraction** ✅
   - Process free-form text fields (procedures, equipment, capabilities)
   - Extract specific medical data from messy, unstructured sources
   - Intelligent synthesis with structured facility schemas

2. **Intelligent Synthesis** ✅
   - Combine unstructured insights with structured data
   - Provide comprehensive view of regional healthcare capabilities
   - Semantic search powered by FAISS and sentence transformers

3. **Planning System** ✅
   - Natural language interface accessible to all experience levels
   - Intuitive Gradio UI for NGO planners
   - No technical knowledge required

### Stretch Goals Implemented 🚀

1. **Citations** ✅
   - Row-level citations for all claims
   - Agentic-step level citations showing which data supported each reasoning step
   - Full transparency in agent decision-making

2. **Visualizations** ✅
   - Interactive maps showing facility locations
   - Medical desert heatmaps by specialty and region
   - Specialty distribution charts
   - Facility type breakdowns

3. **Real-Impact Features** ✅
   - Medical desert detection algorithm
   - Facility validation and anomaly detection
   - Regional coverage analysis
   - Gap identification for resource allocation

---

## 🏗️ Architecture

### Tech Stack

- **Agentic Orchestrator**: LangGraph
- **LLM**: Claude Sonnet 4 (via Anthropic API)
- **RAG**: FAISS + Sentence Transformers
- **ML Lifecycle**: MLflow
- **Visualizations**: Plotly
- **Interface**: Gradio
- **Data**: Virtue Foundation Ghana Dataset (1,000+ facilities)

### System Components

```
┌─────────────────────────────────────────────────┐
│              Gradio Interface                    │
│         (Natural Language Queries)               │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│          LangGraph Agent                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │ Classify │→ │ Retrieve │→ │   Analyze    │  │
│  │  Query   │  │ Context  │  │  & Respond   │  │
│  └──────────┘  └──────────┘  └──────────────┘  │
└────────────────┬────────────────────────────────┘
                 │
         ┌───────┴────────┐
         │                │
┌────────▼─────┐  ┌──────▼──────┐
│  FAISS RAG   │  │   Claude    │
│  (Semantic   │  │   Sonnet 4  │
│   Search)    │  │  (Reasoning) │
└──────────────┘  └─────────────┘
         │
         ▼
┌────────────────────────────────────────┐
│  MLflow Experiment Tracking            │
│  - Run logging                         │
│  - Citation tracking                   │
│  - Metrics & parameters                │
└────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Anthropic API key
- 4GB+ RAM (for FAISS indexing)

### Installation

1. **Clone or download the project files**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up your API key**:
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

4. **Run the application**:
```bash
python app.py
```

5. **Open your browser** to the URL shown (typically `http://localhost:7860`)

---

## 📊 Usage Examples

### 1. Medical Desert Detection

**Query**: "Which regions in Ghana lack cardiology services?"

**Agent Process**:
1. Classifies query as desert_detection
2. Retrieves all facilities with cardiology specialty
3. Analyzes regional distribution
4. Identifies gaps and provides recommendations

**Output**: 
- List of regions with limited cardiology access
- Heatmap showing severity
- Specific facility recommendations
- Citations to source data

### 2. Facility Validation

**Query**: "Validate the claims of Korle Bu Teaching Hospital"

**Agent Process**:
1. Retrieves facility data
2. Checks data completeness
3. Identifies suspicious claims (e.g., unrealistic capacity)
4. Flags missing critical fields

**Output**:
- Completeness score
- List of suspicious claims
- Missing fields
- Data quality issues

### 3. Semantic Search

**Query**: "Find all hospitals with MRI equipment in Greater Accra"

**Agent Process**:
1. Embeds query
2. Performs semantic search in FAISS index
3. Ranks results by relevance
4. Returns top matches with citations

**Output**:
- Ranked list of matching facilities
- Relevance scores
- Full facility details
- Source citations

---

## 📈 Evaluation Criteria Alignment

### Technical Accuracy (35%) ✅

- **Must-have queries**: Agent handles search, validation, and desert detection reliably
- **Anomaly detection**: Built-in validation checks for suspicious claims
- **Data quality**: Completeness scoring and missing field identification

### IDP Innovation (30%) ✅

- **Free-form text extraction**: Procedures, equipment, and capabilities parsed from unstructured data
- **Intelligent synthesis**: Combines structured and unstructured data seamlessly
- **Semantic search**: FAISS-powered RAG for intelligent document retrieval

### Social Impact (25%) ✅

- **Medical desert identification**: Automated detection of underserved regions
- **Gap analysis**: Specialty-specific and region-specific coverage assessment
- **Resource allocation guidance**: Actionable insights for NGO planners

### User Experience (10%) ✅

- **Natural language interface**: No technical knowledge required
- **Intuitive Gradio UI**: Clean, accessible design
- **Clear citations**: Transparency in data sources
- **Visual feedback**: Maps and charts for easy comprehension

---

## 🎓 Dataset

**Source**: Virtue Foundation Ghana v0.3  
**Records**: 1,000+ healthcare facilities and NGOs  
**Coverage**: All regions of Ghana  

**Fields Include**:
- Organization details (name, contact, location)
- Medical specialties
- Procedures offered
- Equipment available
- Capabilities (ICU, trauma levels, etc.)
- Free-form text fields with rich unstructured data

---

## 🔬 MLflow Tracking

All agent runs are logged to MLflow for reproducibility and analysis:

- **Parameters**: Query, query type, specialties, regions
- **Metrics**: Citation count, reasoning steps, completeness scores
- **Artifacts**: Full responses, citations, agent steps
- **Comparison**: Compare multiple runs to evaluate performance

Access MLflow UI:
```bash
mlflow ui
```

---

## 📝 Citations & Transparency

### Row-Level Citations
Every claim is backed by specific rows in the dataset:
```
Citation: Row 42, Source: https://example.com/facility-page
```

### Agentic-Step Citations
Each step in the agent's reasoning shows which data was used:
```
Step 1: Query Classification
- Input: "Find cardiology facilities"
- Output: "search"
- Data sources: None (classification step)

Step 2: Context Retrieval  
- Input: Query + embeddings
- Output: 5 relevant documents
- Data sources: Rows 23, 45, 67, 89, 102

Step 3: Analysis
- Input: Retrieved context
- Output: Synthesized findings
- Data sources: Same as step 2
```

---

## 🗺️ Visualizations

### 1. Facility Map
Interactive map showing all facilities with:
- Location markers
- Hover details (name, type, specialties)
- Filtering by region and specialty

### 2. Medical Desert Heatmap
Severity visualization by region for specific specialties:
- 🟢 Green: Good coverage (5+ facilities)
- 🟡 Orange: Moderate (3-4 facilities)
- 🔴 Red: Severe (<3 facilities)
- ⚫ Black: Critical (0 facilities)

### 3. Specialty Distribution
Bar chart showing availability of different medical specialties across Ghana

### 4. Facility Type Distribution
Pie chart breaking down hospitals, clinics, pharmacies, etc.

---

## 💡 Real-World Impact

This system enables the Virtue Foundation to:

1. **Identify Critical Gaps**: Automatically detect medical deserts requiring intervention
2. **Validate Facility Claims**: Ensure accurate information for patient routing
3. **Optimize Resource Allocation**: Direct medical expertise where it's needed most
4. **Accelerate Decision-Making**: Reduce research time from days to seconds
5. **Scale Coordination**: Enable planetary-scale healthcare coordination

**Goal**: Reduce time to lifesaving treatment by 100×

---

## 🔧 Customization

### Adding New Specialties
Edit `models.py` to add specialties to `MEDICAL_HIERATCHY`

### Modifying Agent Workflow
Edit `agent.py` to customize the LangGraph workflow

### Custom Visualizations
Add new visualization functions in `visualizations.py`

### MLflow Configuration
Adjust tracking in `mlflow_tracker.py`

---

## 🐛 Troubleshooting

**Issue**: Agent not responding  
**Solution**: Check that `ANTHROPIC_API_KEY` is set correctly

**Issue**: FAISS index build fails  
**Solution**: Ensure you have sufficient RAM (4GB+ recommended)

**Issue**: Visualizations not showing  
**Solution**: Check that Plotly is installed correctly

**Issue**: MLflow UI not accessible  
**Solution**: Run `mlflow ui` in the project directory

---

## 📚 Code Structure

```
.
├── app.py                  # Gradio interface
├── agent.py                # LangGraph agentic workflow
├── rag_system.py           # FAISS RAG implementation
├── visualizations.py       # Plotly charts and maps
├── mlflow_tracker.py       # MLflow experiment tracking
├── models.py               # Pydantic models and configs
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

---

## 🌟 Future Enhancements

- [ ] Real-time data updates from facility websites
- [ ] Multi-country support
- [ ] Patient routing recommendations
- [ ] Doctor-facility matching
- [ ] Predictive analytics for future healthcare needs
- [ ] Integration with telehealth platforms
- [ ] Mobile app for field workers

---

## 📄 License

This project is built for the Databricks challenge in collaboration with the Virtue Foundation.

---

## 🙏 Acknowledgments

- **Virtue Foundation** for providing real-world healthcare data
- **Databricks** for sponsoring the challenge
- **Anthropic** for Claude Sonnet 4 API
- **LangChain/LangGraph** for agentic orchestration framework

---

## 📧 Contact

For questions about this implementation, please open an issue or contact the development team.

---

**Built with ❤️ to save lives and bridge medical deserts worldwide** 🌍