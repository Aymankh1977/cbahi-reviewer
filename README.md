# CBAHI Reviewer — DentEdTech™
### AI-Powered CBAHI Accreditation Intelligence Platform

---

## 📁 Project Structure

```
cbahi_reviewer_streamlit/
├── app.py                          ← Main Streamlit application
├── requirements.txt                ← Python dependencies
├── .gitignore                      ← Protects secrets from Git
├── .streamlit/
│   ├── config.toml                 ← Theme and server config
│   └── secrets.toml                ← API key (LOCAL ONLY — never commit)
└── utils/
    ├── __init__.py
    ├── cbahi_data.py               ← Standards reference data
    ├── ai_engine.py                ← Claude AI analysis engine
    └── report_generator.py         ← HTML report generator
```

---

## 🚀 Deployment to Streamlit Cloud (Free)

### Step 1 — Push to GitHub

```bash
cd cbahi_reviewer_streamlit

# Initialize git
git init
git add .
# Make sure secrets.toml is in .gitignore before this!
git commit -m "Initial commit — CBAHI Reviewer"

# Create a repo on github.com then:
git remote add origin https://github.com/YOUR_USERNAME/cbahi-reviewer.git
git push -u origin main
```

### Step 2 — Deploy on Streamlit Cloud

1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Sign in with GitHub
3. Click **"New app"**
4. Set:
   - Repository: `your-username/cbahi-reviewer`
   - Branch: `main`
   - Main file path: `app.py`
5. Click **"Advanced settings"**
6. Under **Secrets**, paste:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-your-actual-key-here"
   ```
7. Click **"Deploy!"**

Your app will be live at:
`https://your-username-cbahi-reviewer-app-XXXX.streamlit.app`

---

## 💻 Local Development

```bash
# 1. Clone your repo
git clone https://github.com/YOUR_USERNAME/cbahi-reviewer.git
cd cbahi-reviewer

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API key locally
# Edit .streamlit/secrets.toml — replace sk-ant-YOUR-KEY-HERE

# 5. Run
streamlit run app.py
```

App opens at: http://localhost:8501

---

## 🔑 API Key Security

| Environment     | How key is stored                          |
|-----------------|--------------------------------------------|
| Streamlit Cloud | Streamlit Secrets UI (encrypted, server-side) |
| Local dev       | `.streamlit/secrets.toml` (gitignored)    |

The key is **never** exposed in the browser, URL, or source code.

---

## 📋 Features

- **AI Analyzer** — Full compliance analysis with chapter scores, ESR status, gap identification, recommendations, and corrective action plan
- **Self-Assessment** — Interactive 0/1/2 scoring for all standards with real-time score calculation
- **Standards Explorer** — Browse all 3 CBAHI programs with ESR reference tables
- **Report Export** — Downloadable HTML report + JSON data

## ⚠️ Disclaimer

This platform is for educational and preparation purposes only.
Results are AI-generated and do not constitute an official CBAHI assessment.

---

**© 2025 DentEdTech™ — All rights reserved**
