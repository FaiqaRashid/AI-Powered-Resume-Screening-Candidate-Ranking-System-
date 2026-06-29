# 📄 AI-Powered Resume Screening & Ranking System

> Automate your recruitment workflow with intelligent, semantic-based resume matching powered by AI.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Latest-green.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](#license)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

---

## 🚀 Quick Start

```bash
# 1. Clone repository
git clone https://github.com/yourusername/resume-screener.git
cd resume-screener

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup environment variables
cp .env.example .env
# Edit .env with your API keys

# 4. Run the app
streamlit run app.py
```

---

## 📋 Table of Contents

- [Features](#-features)
- [Problem Statement](#-problem-statement)
- [How It Works](#-how-it-works)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Database Schema](#-database-schema)
- [Contributing](#-contributing)
- [License](#-license)

---

## ⭐ Features

✅ **PDF Resume Parsing** - Automatically extracts text from uploaded PDF resumes  
✅ **Semantic AI Matching** - Uses Gemini 2.5 Flash LLM for intelligent, context-aware candidate evaluation  
✅ **Structured Data Extraction** - Extracts candidate name, email, skills, and experience using Pydantic validation  
✅ **Smart Scoring Algorithm** - Calculates match scores (0-100) with detailed strength/weakness analysis  
✅ **Cloud Database Persistence** - Auto-saves all candidate evaluations to Supabase  
✅ **HCI-Optimized Dashboard** - Beautiful Streamlit UI with high-contrast colors and intuitive layout  
✅ **Ranked Leaderboard** - Instant sorting of candidates by match score  
✅ **Production-Ready** - Clean code, security best practices, environment separation  

---

## 🎯 Problem Statement

Traditional recruitment workflows suffer from:
- ❌ Manual resume screening (time-consuming and error-prone)
- ❌ Simple keyword matching (misses qualified but differently-worded candidates)
- ❌ No structured data extraction (duplicate work)
- ❌ Lost candidate history (no persistence)

**Our Solution:** Intelligent AI-powered matching that understands *context*, not just keywords.

---

## 🧠 How It Works

### 1. **Resume Text Extraction**
```
PDF Upload → PyPDF Parser → Raw Text
```
Extracts all text content from uploaded PDF resumes.

### 2. **Semantic Analysis (NER + Matching)**
```
Resume + Job Description → Gemini 2.5 Flash LLM → Structured JSON
```
The LLM performs:
- Named Entity Recognition (NER) to extract: Name, Email, Skills, Experience
- Semantic matching against job requirements
- Contextual overlap evaluation (e.g., "Database Management" ≈ "SQL")

### 3. **Scoring & Evaluation**
```
LLM Output (Pydantic-validated) → Score (0-100) + Strengths/Weaknesses + Summary
```
- **Scoring Logic:** Evaluates how well candidate aligns with JD
- **Low Temperature (T=0.1):** Prevents hallucinations, ensures consistency
- **Output:** Match score, key strengths, identified gaps, 2-line summary

### 4. **Cloud Persistence**
```
Evaluated Candidate → Supabase Cloud Database → Stored for future reference
```
All candidate profiles are automatically saved to PostgreSQL-backed Supabase.

### 5. **Dashboard Ranking**
```
Multiple Candidates → Sorted by Match Score (Descending) → Live Leaderboard
```
Recruiters see an instant ranked list of best-fit candidates.

---

## 🛠 Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend Logic** | Python 3.9+ | Core application logic |
| **LLM Integration** | Google GenAI (Gemini 2.5 Flash) | Semantic understanding & NER |
| **Frontend** | Streamlit | Web dashboard & UI |
| **PDF Processing** | PyPDF | Resume text extraction |
| **Data Validation** | Pydantic | Structured output schemas |
| **Cloud Database** | Supabase (PostgreSQL) | Persistent candidate storage |
| **Config Management** | python-dotenv | Secure API key handling |

---

## 📦 Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Git

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/resume-screener.git
cd resume-screener
```

### Step 2: Create Virtual Environment (Optional but Recommended)
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**Dependencies:**
```
streamlit==1.28.0
pypdf==4.0.0
google-genai==0.3.0
pydantic==2.5.0
supabase==2.3.0
python-dotenv==1.0.0
```

---

## 🔐 Configuration

### Step 1: Create Environment File
```bash
cp .env.example .env
```

### Step 2: Add Your API Keys
Edit `.env` with:
```env
# Google Gemini API
GEMINI_API_KEY=your_actual_gemini_api_key_here

# Supabase Cloud Database
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your_supabase_anon_or_service_role_key_here
```

**How to get API keys:**

**Google Gemini API:**
1. Go to [Google AI Studio](https://ai.google.dev/)
2. Click "Get API Key" → Create new API key
3. Copy and paste into `.env`

**Supabase:**
1. Go to [Supabase](https://supabase.com/)
2. Create new project
3. Copy `Project URL` and `Anon Key` from Settings → API
4. Paste into `.env`

### Step 3: Setup Database Table
Inside your Supabase SQL Editor, run:
```sql
create table candidates (
  id bigint generated always as identity primary key,
  name text,
  email text,
  skills text,
  experience_years int,
  match_score int,
  summary text,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);
```

---

## 🎮 Usage

### Run the Application
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

### Step-by-Step Workflow

1. **Enter Job Description**
   - Paste the full job requirements, responsibilities, and qualifications
   - Be as detailed as possible for better matching

2. **Upload Resumes**
   - Click "Browse files" or drag-and-drop PDF resumes
   - Can upload 1 or multiple resumes at once

3. **Run Screening**
   - Click "⚡ Run Screening & Rank Candidates"
   - Wait for AI analysis (usually 10-30 seconds depending on resume complexity)

4. **View Results**
   - See ranked leaderboard sorted by match score (highest first)
   - Candidates automatically saved to Supabase

5. **Export Data** (Optional)
   - Download table as CSV via Streamlit's export feature
   - Query Supabase directly for historical data

---

## 📂 Project Structure

```
resume-screener/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template (no secrets)
├── .gitignore                 # Git ignore rules (includes .env)
├── README.md                  # This file
├── LICENSE                    # MIT License
└── docs/
    ├── ARCHITECTURE.md        # Detailed technical architecture
    └── EXAMPLES.md            # Sample usage & outputs
```

---

## 💾 Database Schema

### `candidates` Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | bigint (PK) | Auto-generated unique identifier |
| `name` | text | Candidate's full name |
| `email` | text | Candidate's email address |
| `skills` | text | Comma-separated list of skills |
| `experience_years` | int | Years of professional experience |
| `match_score` | int | AI-calculated match score (0-100) |
| `summary` | text | 2-line evaluation summary |
| `created_at` | timestamp | Auto-recorded timestamp |

**Sample Query:**
```sql
-- View top 10 candidates by match score
SELECT name, email, match_score, summary 
FROM candidates 
ORDER BY match_score DESC 
LIMIT 10;
```

---

## 🧪 Example Outputs

### Input
```
Job Description: Senior Full-Stack Engineer (5+ years, Python, React, AWS)
Resume: Sarah Johnson - 6 years exp, Python, JavaScript, React, AWS certified
```

### Output
```json
{
  "profile": {
    "name": "Sarah Johnson",
    "email": "sarah@email.com",
    "skills": ["Python", "JavaScript", "React", "AWS"],
    "experience_years": 6
  },
  "evaluation": {
    "matching_score": 92,
    "strengths": [
      "Exceeds experience requirement (6 vs 5 years)",
      "Strong full-stack background (Python + React)",
      "AWS certified aligns with cloud requirement"
    ],
    "weaknesses": [
      "No Java/Go experience (optional skills)"
    ],
    "summary": "Strong technical fit with seniority match. Ready for immediate impact."
  }
}
```

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** changes (`git commit -m 'Add amazing feature'`)
4. **Push** to branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Checklist
- [ ] Code follows PEP 8 standards
- [ ] Added comments for complex logic
- [ ] Tested with multiple resume formats
- [ ] Updated README if adding features
- [ ] No hardcoded API keys in code

---

## 🐛 Troubleshooting

### Issue: "API Key Invalid"
**Solution:** Check that `GEMINI_API_KEY` in `.env` is correct and hasn't expired.

### Issue: "Supabase Connection Error"
**Solution:** Verify `SUPABASE_URL` and `SUPABASE_KEY` in `.env`. Database table may not exist—run the SQL schema query.

### Issue: "PDF Text Extraction Empty"
**Solution:** Some PDFs are image-based (scanned). This tool requires text-based PDFs.

### Issue: "Streamlit App Won't Start"
**Solution:** 
```bash
# Clear Streamlit cache
streamlit cache clear

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Try again
streamlit run app.py
```

---

## 📈 Performance & Scaling

- **Single Resume:** ~3-5 seconds
- **10 Resumes:** ~30-50 seconds
- **100 Resumes:** ~5-10 minutes (depends on resume length)

**Optimization Tips:**
- Use shorter job descriptions (reduces token count)
- Upload resumes in batches if handling 100+

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 👩‍💻 Author

**Faiqa Rashid**  
AI Engineer Intern | June 2026  
[LinkedIn](https://linkedin.com/in/faiqa-rashid) | [GitHub](https://github.com/yourusername)

---

## 🙏 Acknowledgments

- Google GenAI (Gemini 2.5 Flash) for intelligent NER & matching
- Streamlit for beautiful, interactive dashboards
- Supabase for seamless cloud database integration
- PyPDF for robust PDF parsing

---

## 📧 Support

Have questions? Found a bug? 
- **Open an Issue:** [GitHub Issues](https://github.com/yourusername/resume-screener/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/resume-screener/discussions)

---

**⭐ If this project helped you, please star it on GitHub!**
