# ✅ Getting Started Checklist

## GitHub Codespaces Setup - Step by Step

Follow this checklist to get the Virtue Foundation IDP Agent running in minutes!

---

## 📋 Pre-Setup Checklist

### Before You Start

- [ ] Have a GitHub account
- [ ] Have an Anthropic API key (or know how to get one)
- [ ] Have the dataset file: `Virtue_Foundation_Ghana_v0_3_-_Sheet1.csv`
- [ ] Basic understanding of running terminal commands

---

## 🚀 Part 1: Repository Setup (5 minutes)

### Step 1: Get the Code

**Option A: Use This Repository Directly**
- [ ] Fork this repository to your GitHub account
- [ ] Or clone it locally then push to your own repo

**Option B: Create New Repository**
- [ ] Create new repository on GitHub
- [ ] Upload all project files from the outputs folder
- [ ] Ensure folder structure matches `FOLDER_STRUCTURE.md`

### Step 2: Add the Dataset

- [ ] Place `Virtue_Foundation_Ghana_v0_3_-_Sheet1.csv` in the **root folder**
- [ ] NOT in any subfolder (data/, datasets/, etc.)
- [ ] Verify filename is exact (case-sensitive!)

**How to Add**:

**Option A: Via GitHub Web**
1. [ ] Go to your repository on GitHub
2. [ ] Click "Add file" → "Upload files"
3. [ ] Drag and drop the CSV file
4. [ ] Click "Commit changes"

**Option B: Via Git Command Line**
```bash
git add Virtue_Foundation_Ghana_v0_3_-_Sheet1.csv
git commit -m "Add Virtue Foundation dataset"
git push
```

### Step 3: Verify Repository Structure

Your repository should look like this:

```
✅ .devcontainer/devcontainer.json
✅ .gitignore
✅ .env.example
✅ Virtue_Foundation_Ghana_v0_3_-_Sheet1.csv  ← IMPORTANT!
✅ app.py
✅ agent.py
✅ rag_system.py
✅ visualizations.py
✅ mlflow_tracker.py
✅ models.py
✅ demo.py
✅ exploration.ipynb
✅ requirements.txt
✅ setup.sh
✅ README.md
✅ QUICK_START.md
✅ GITHUB_SETUP.md
✅ PROJECT_SUMMARY.md
✅ FOLDER_STRUCTURE.md
```

---

## 🔑 Part 2: API Key Setup (3 minutes)

### Step 1: Get Anthropic API Key

- [ ] Go to https://console.anthropic.com/
- [ ] Sign up or log in
- [ ] Navigate to "API Keys" section
- [ ] Click "Create Key"
- [ ] Copy your key (starts with `sk-ant-`)
- [ ] Save it somewhere safe temporarily

### Step 2: Add to Codespaces Secrets

- [ ] Go to https://github.com/settings/codespaces
- [ ] Scroll to "Codespaces secrets"
- [ ] Click "New secret"
- [ ] Name: `ANTHROPIC_API_KEY` (exact spelling!)
- [ ] Value: Paste your API key
- [ ] Select repository access (your repo or all repos)
- [ ] Click "Add secret"

**✅ Checkpoint**: You should see your secret listed

---

## 💻 Part 3: Launch Codespace (2 minutes)

### Step 1: Create Codespace

- [ ] Go to your repository on GitHub
- [ ] Click the green "Code" button
- [ ] Click "Codespaces" tab
- [ ] Click "Create codespace on main"

**Wait for setup** (2-3 minutes):
- [ ] Codespace container starts
- [ ] VS Code interface loads
- [ ] Dependencies install automatically (via `postCreateCommand`)

### Step 2: Verify Setup

Open the terminal in Codespaces and run:

```bash
# Check Python
python3 --version
# Should show: Python 3.11.x

# Check dependencies
pip list | grep anthropic
# Should show: anthropic

# Check dataset
ls -lh Virtue*.csv
# Should show: Virtue_Foundation_Ghana_v0_3_-_Sheet1.csv

# Check API key (first 10 chars only)
echo $ANTHROPIC_API_KEY | cut -c1-10
# Should show: sk-ant-api
```

**All checks passed?**
- [ ] ✅ Python 3.11+ installed
- [ ] ✅ Dependencies installed
- [ ] ✅ Dataset present in root
- [ ] ✅ API key set

---

## 🎮 Part 4: Run the Application (1 minute)

### Option A: Quick Test (No GUI)

Run the demo script first to verify everything works:

```bash
python3 demo.py
```

**Expected output**:
- [ ] RAG index builds successfully
- [ ] Search test returns results
- [ ] Medical desert detection works
- [ ] Facility validation completes
- [ ] Agent query processes (if API key is set)

### Option B: Full Application (Gradio UI)

Launch the main application:

```bash
python3 app.py
```

**Expected output**:
```
Initializing Virtue Foundation IDP Agent...
Building RAG index...
Index built with 1002 documents
Initializing AI agent...
Running on local URL:  http://127.0.0.1:7860
```

### Step 2: Access the Interface

In Codespaces, you'll see a notification:
- [ ] Look for popup: "Your application running on port 7860 is available"
- [ ] Click "Open in Browser" or "Open in Preview"

**Alternative**:
- [ ] Open "Ports" tab at the bottom of VS Code
- [ ] Find port 7860
- [ ] Click the globe icon 🌐
- [ ] Interface opens in new tab

---

## 🧪 Part 5: Test the Features (5 minutes)

### Test 1: AI Agent (Natural Language Queries)

- [ ] Go to "🤖 AI Agent" tab
- [ ] Try query: "Which regions lack cardiology services?"
- [ ] Wait 10-20 seconds for response
- [ ] Verify you get:
  - [ ] Natural language answer
  - [ ] Citations with row numbers
  - [ ] Reasoning steps shown
  - [ ] Agent execution steps visible

### Test 2: Medical Desert Detection

- [ ] Go to "🗺️ Medical Desert Detection" tab
- [ ] Enter specialty: `cardiology`
- [ ] Enter region: `Northern`
- [ ] Click "Detect Medical Deserts"
- [ ] Verify you get:
  - [ ] Analysis results with severity
  - [ ] List of available facilities
  - [ ] Heatmap visualization

### Test 3: Facility Validation

- [ ] Go to "✅ Facility Validation" tab
- [ ] Enter a facility name (e.g., "Korle Bu Teaching Hospital")
- [ ] Click "Validate Facility"
- [ ] Verify you get:
  - [ ] Completeness score
  - [ ] Missing fields list
  - [ ] Suspicious claims (if any)

### Test 4: Search

- [ ] Go to "🔍 Search Facilities" tab
- [ ] Search: "hospitals with emergency medicine"
- [ ] Click "Search"
- [ ] Verify you get:
  - [ ] Ranked results
  - [ ] Relevance scores
  - [ ] Citations with sources

### Test 5: Visualizations

- [ ] Go to "📊 Visualizations" tab
- [ ] Select "Facility Map"
- [ ] Click "Generate Visualization"
- [ ] Verify you get:
  - [ ] Interactive map
  - [ ] Facility markers
  - [ ] Hover tooltips

---

## 📊 Part 6: Explore MLflow (Optional - 2 minutes)

### Launch MLflow UI

In the terminal:

```bash
mlflow ui
```

- [ ] MLflow starts on port 5000
- [ ] Check "Ports" tab
- [ ] Click globe icon next to port 5000
- [ ] MLflow UI opens

### Verify Experiment Tracking

- [ ] See "virtue-foundation-idp" experiment
- [ ] View logged runs
- [ ] Check parameters (query, specialty, etc.)
- [ ] View artifacts (citations, responses)

---

## 🎯 Part 7: Success Criteria

### You're Successfully Running If:

**Core Functionality**
- [ ] ✅ Gradio interface loads without errors
- [ ] ✅ All 5 tabs are accessible
- [ ] ✅ Agent responds to natural language queries
- [ ] ✅ Medical desert detection works
- [ ] ✅ Search returns relevant results
- [ ] ✅ Visualizations display correctly

**Data & Citations**
- [ ] ✅ Dataset loads (1000+ facilities)
- [ ] ✅ Citations show row numbers
- [ ] ✅ Source URLs are present
- [ ] ✅ Reasoning steps are visible

**Performance**
- [ ] ✅ Search response < 1 second
- [ ] ✅ Agent response < 30 seconds
- [ ] ✅ Visualizations load < 3 seconds

---

## 🐛 Troubleshooting Checklist

### Problem: Codespace Won't Start

- [ ] Check GitHub service status
- [ ] Try creating in a different browser
- [ ] Clear browser cache and retry
- [ ] Check your GitHub quota (free tier = 60 hours/month)

### Problem: "Dataset not found"

- [ ] Verify CSV is in root folder: `ls *.csv`
- [ ] Check filename exactly: `Virtue_Foundation_Ghana_v0_3_-_Sheet1.csv`
- [ ] Re-upload if needed
- [ ] Restart Codespace

### Problem: "ANTHROPIC_API_KEY not set"

- [ ] Check secret name: Must be exactly `ANTHROPIC_API_KEY`
- [ ] Verify secret value starts with `sk-ant-`
- [ ] **Restart Codespace** (important!)
- [ ] Or set temporarily: `export ANTHROPIC_API_KEY='your-key'`

### Problem: Port Not Accessible

- [ ] Open "Ports" tab
- [ ] Right-click port 7860
- [ ] Select "Port Visibility" → "Public"
- [ ] Click globe icon to open
- [ ] Try in private/incognito browser window

### Problem: Dependencies Failed

```bash
# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### Problem: Agent Not Responding

- [ ] Verify API key is set: `echo $ANTHROPIC_API_KEY`
- [ ] Check Anthropic status: https://status.anthropic.com/
- [ ] Try simpler query first
- [ ] Check MLflow logs for errors

---

## 📚 Next Steps

### After Everything Works

**Learn More**:
- [ ] Read `README.md` for full documentation
- [ ] Open `exploration.ipynb` for code examples
- [ ] Review `PROJECT_SUMMARY.md` for architecture

**Customize**:
- [ ] Modify queries in `app.py`
- [ ] Add new visualizations in `visualizations.py`
- [ ] Extend agent logic in `agent.py`

**Deploy**:
- [ ] Make port 7860 public to share
- [ ] Deploy to Hugging Face Spaces
- [ ] Set up on cloud platform (GCP, AWS, Azure)

---

## 🎓 Learning Resources

- **Gradio**: https://gradio.app/docs/
- **LangGraph**: https://python.langchain.com/docs/langgraph
- **Anthropic**: https://docs.anthropic.com/
- **MLflow**: https://mlflow.org/docs/
- **FAISS**: https://github.com/facebookresearch/faiss

---

## ✅ Final Checklist

Before considering setup complete:

- [ ] Codespace running smoothly
- [ ] Dataset loaded (1000+ facilities)
- [ ] API key configured and working
- [ ] All 5 tabs in Gradio working
- [ ] Can query the agent successfully
- [ ] Visualizations display
- [ ] MLflow tracking works
- [ ] Understand basic troubleshooting

---

## 🎉 Congratulations!

You've successfully set up the Virtue Foundation IDP Agent!

**You can now**:
- 🔍 Search 1000+ healthcare facilities in Ghana
- 🗺️ Identify medical deserts automatically
- ✅ Validate facility claims and data quality
- 📊 Visualize healthcare infrastructure gaps
- 🤖 Ask natural language questions about healthcare access

**Next**: Start bridging medical deserts and saving lives! 🌍❤️

---

## 💬 Need Help?

1. **Check docs**: README.md, GITHUB_SETUP.md
2. **Run demo**: `python3 demo.py`
3. **Check logs**: Terminal output, MLflow UI
4. **Review code**: All files are well-commented

**Remember**: The goal is to reduce time to lifesaving treatment by 100×!