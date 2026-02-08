# Quick Start Guide 🚀

## Get Running in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt --break-system-packages
```

Or use the setup script:
```bash
chmod +x setup.sh
./setup.sh
```

### Step 2: Set Your API Key
```bash
export ANTHROPIC_API_KEY='your-anthropic-api-key-here'
```

Get your API key from: https://console.anthropic.com/

### Step 3: Launch the App
```bash
python app.py
```

The Gradio interface will open automatically in your browser at `http://localhost:7860`

---

## Alternative: Test Without GUI

Run the demo script to test functionality:
```bash
python demo.py
```

---

## Project Structure

```
.
├── app.py                  # ⭐ Main Gradio interface - START HERE
├── agent.py                # LangGraph agentic workflow
├── rag_system.py           # FAISS RAG + semantic search
├── visualizations.py       # Plotly charts and maps
├── mlflow_tracker.py       # Experiment tracking
├── models.py               # Data models and configs
├── demo.py                 # Testing script (no GUI)
├── exploration.ipynb       # Jupyter notebook examples
├── requirements.txt        # Python dependencies
├── setup.sh                # Automated setup script
├── README.md               # Full documentation
└── PROJECT_SUMMARY.md      # Challenge submission summary
```

---

## Usage Examples

### In the Gradio Interface

**Tab 1: AI Agent**
- Ask: "Which regions lack cardiology services?"
- Ask: "Find all facilities with emergency medicine"
- Ask: "Show me ophthalmology clinics in Ashanti"

**Tab 2: Medical Desert Detection**
- Specialty: "cardiology"
- Region: "Northern"
- Click "Detect Medical Deserts"

**Tab 3: Facility Validation**
- Enter a facility name from the dataset
- Click "Validate Facility"
- See completeness score and suspicious claims

**Tab 4: Search**
- Search: "hospitals with MRI equipment"
- Get ranked results with citations

**Tab 5: Visualizations**
- Choose visualization type
- Filter by specialty/region
- View interactive charts

---

## Key Features

✅ **Natural Language Queries**: Ask questions like you're talking to a person  
✅ **Medical Desert Detection**: Identify underserved regions automatically  
✅ **Facility Validation**: Check data quality and detect anomalies  
✅ **Full Citations**: Every claim backed by row-level sources  
✅ **Transparent Reasoning**: See how the AI makes decisions  
✅ **Interactive Maps**: Visualize facility distribution  
✅ **MLflow Tracking**: All experiments logged automatically  

---

## Troubleshooting

**Problem**: "ANTHROPIC_API_KEY not set"  
**Solution**: Export your API key: `export ANTHROPIC_API_KEY='sk-...'`

**Problem**: "Dataset not found"  
**Solution**: Ensure CSV is at `/mnt/user-data/uploads/Virtue_Foundation_Ghana_v0_3_-_Sheet1.csv`

**Problem**: "Module not found"  
**Solution**: Run `pip install -r requirements.txt --break-system-packages`

**Problem**: Port 7860 already in use  
**Solution**: Edit `app.py` and change `server_port=7860` to another port

---

## What Makes This Special?

1. **Agentic-Step Citations**: Not just what data was used, but WHEN and WHY in the reasoning process
2. **Medical Desert Severity Scoring**: Quantitative assessment (none/moderate/severe/critical)
3. **Real-Time Validation**: Automated data quality checks for healthcare data
4. **Accessible Interface**: No coding knowledge required - natural language only
5. **Production-Ready**: Full MLflow tracking, error handling, and scalability

---

## Next Steps

1. **Explore the Interface**: Try different queries in each tab
2. **Check MLflow**: Run `mlflow ui` to see experiment tracking
3. **Jupyter Notebook**: Open `exploration.ipynb` for code examples
4. **Read Documentation**: See `README.md` for full details
5. **Review Summary**: Check `PROJECT_SUMMARY.md` for challenge alignment

---

## Support

For questions or issues:
1. Check `README.md` for detailed documentation
2. Review `PROJECT_SUMMARY.md` for architecture details
3. Run `python demo.py` to test components individually
4. Examine MLflow logs for debugging

---

**Built for the Databricks Challenge to bridge medical deserts worldwide** 🌍

Goal: Reduce time to lifesaving treatment by 100× ✅