import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from pypdf import PdfReader
from google.genai import Client
from google.genai import types
from pydantic import BaseModel
from typing import List
import json
import os
from supabase import create_client, Client as SupabaseClient

# --- 1. INITIALIZE SUPABASE CLOUD DATABASE ---
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: SupabaseClient = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        st.error(f"Database connection error: {e}")

# --- 2. DESIGN THE OUTPUT FORMATS (The Blueprints) ---
class CandidateProfile(BaseModel):
    name: str
    email: str
    skills: List[str]
    experience_years: int

class MatchResult(BaseModel):
    matching_score: int
    strengths: List[str]
    weaknesses: List[str]
    summary: str

# --- 3. CUSTOM STYLING (Beige, Navy Blue, Teal, Wide Boxes) ---
st.markdown("""
  <style>
    /* 1. VISIBILITY & ACCESSIBILITY (HCI Rule: High Contrast & Consistency) */
    .stApp {
        background-color: #F7F5F0; /* Clean Beige Background */
        color: #1A365D;            /* Deep Navy Blue Text */
    }
    
    /* 2. TYPOGRAPHY HIERARCHY (HCI Rule: Clear Visual Hierarchy) */
    h1 {
        color: #1A365D !important;
        font-size: 42px !important;
        font-weight: 800 !important;
        margin-bottom: 12px !important;
    }
    h2, h3 {
        color: #1A365D !important;
        font-size: 26px !important;
        font-weight: 600 !important;
        margin-top: 22px !important;
    }
    .stMarkdown p {
        font-size: 18px !important;
        color: #2D3748;
    }
    .stTextInput > label, .stTextArea > label, .stFileUploader > label {
        color: #1A365D !important;
        font-size: 18px !important;
        font-weight: 600 !important;
    }

    /* 3. INPUT COMPONENT DESIGN (HCI Rule: Clear Interaction Boundaries) */
    .stTextArea textarea {
        background-color: #FFFFFF !important;
        color: #1A365D !important;
        font-size: 16px !important;
        padding: 15px !important;
        border: 2px solid #0D9488 !important; /* Teal border for active elements */
        border-radius: 10px !important;
        min-height: 200px !important;
    }
    
    /* 4. FIXING THE FILE UPLOADER & BUTTONS (HCI Rule: Error Prevention & Feedback) */
    .stFileUploader {
        border: 2px dashed #0D9488 !important;
        border-radius: 10px !important;
        padding: 25px !important;
        background-color: #FFFFFF !important;
    }
    
    /* TARGETING INTERNAL FILE BROWSE BUTTON FOR ACCESSIBILITY */
    .stFileUploader section button {
        background-color: #1A365D !important; /* Force Deep Navy Blue */
        color: #FFFFFF !important;             /* Force Clear White Text */
        font-size: 15px !important;
        font-weight: bold !important;
        border-radius: 6px !important;
        border: none !important;
        padding: 8px 16px !important;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1) !important;
    }
    
    .stFileUploader section button:hover {
        background-color: #0D9488 !important; /* Turns Teal on Hover */
        color: #FFFFFF !important;
    }

    /* 5. PRIMARY ACTION BUTTON (HCI Rule: Fitts's Law - Easy Target) */
    div.stButton > button:first-child {
        background-color: #0D9488 !important; /* Vibrant Teal */
        color: #FFFFFF !important;             /* Crisp White Text */
        font-size: 20px !important;
        font-weight: bold !important;
        padding: 14px 40px !important;
        border-radius: 10px !important;
        border: none !important;
        width: 100% !important;
        margin-top: 15px !important;
        transition: background-color 0.2s ease-in-out !important;
        box-shadow: 0px 4px 6px rgba(13, 148, 136, 0.2) !important;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #0F766E !important; /* Darker Teal on Hover */
    }
    
    /* 6. STATUS COMPONENT REFACTORING (HCI Rule: Emotional Design & Safety) */
    .stAlert {
        background-color: #E6FFFA !important;
        color: #0D9488 !important;
        border: 2px solid #0D9488 !important;
        border-radius: 10px !important;
        padding: 15px !important;
        font-size: 16px !important;
    }
    .stWarning {
        background-color: #FEF3C7 !important;
        color: #92400E !important;
        border: 2px solid #F59E0B !important;
        border-radius: 10px !important;
        padding: 15px !important;
        font-size: 16px !important;
    }
    
    /* 7. STRUCTURAL WRAPPERS */
    .stContainer {
        background-color: #FFFFFF;
        border-radius: 10px !important;
        padding: 20px !important;
        border: 1px solid #E0E0E0 !important;
    }
    .stDataFrame {
        border-radius: 10px !important;
        background-color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. CORE HELPER FUNCTIONS ---
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    extracted_text = ""
    for page in reader.pages:
        extracted_text += page.extract_text() + "\n"
    return extracted_text

def process_resume_and_match(raw_text, job_description):
    client = Client()
    
    prompt = f"""
    You are an expert technical recruiter. Analyze the following candidate text.
    First, extract the candidate's basic details.
    Second, evaluate how well they match the provided Job Description. 
    Calculate a score from 0-100, list strengths, weaknesses, and a 2-line summary.
    
    Candidate Text:
    {raw_text}
    Job Description:
    {job_description}
    """
    
    class FullEvaluation(BaseModel):
        profile: CandidateProfile
        evaluation: MatchResult

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.1,
            response_mime_type="application/json",
            response_schema=FullEvaluation,
        ),
    )
    return json.loads(response.text)

# --- 5. STREAMLIT USER INTERFACE ---
st.set_page_config(
    page_title="AI Resume Screener",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📄 AI-Powered Resume Screening & Ranking System")
st.write("Upload candidate resumes in PDF format and match them against your job descriptions instantly.")

# --- WIDE BOX FOR JOB DESCRIPTION ---
st.markdown("<h2 style='color: #1A365D; margin-top: 30px;'>📋 Job Description</h2>", unsafe_allow_html=True)
with st.container():
    job_desc_input = st.text_area(
        "Enter Job Description:", 
        placeholder="Paste the complete job requirements, responsibilities, and qualifications here...", 
        height=250,
        label_visibility="collapsed"
    )

# --- WIDE BOX FOR FILE UPLOAD ---
st.markdown("<h2 style='color: #1A365D; margin-top: 30px;'>📥 Upload Candidate Resumes</h2>", unsafe_allow_html=True)
with st.container():
    uploaded_files = st.file_uploader(
        "Upload Candidate Resumes (PDFs):", 
        type=["pdf"], 
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    
    if uploaded_files:
        st.info(f"✅ {len(uploaded_files)} resume(s) selected and ready for screening")

# --- SUBMIT BUTTON (FULL WIDTH) ---
submit_button = st.button("⚡ Run Screening & Rank Candidates", use_container_width=True)

# --- RESULTS SECTION ---
st.markdown("<h2 style='color: #1A365D; margin-top: 30px;'>🏆 Ranked Candidate Shortlist</h2>", unsafe_allow_html=True)

if submit_button and uploaded_files and job_desc_input:
    master_leaderboard = []
    
    with st.spinner("🔄 AI Intern is analyzing resumes and updating database..."):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for idx, file in enumerate(uploaded_files):
            status_text.text(f"Processing: {file.name} ({idx + 1}/{len(uploaded_files)})")
            
            raw_text = extract_text_from_pdf(file)
            result = process_resume_and_match(raw_text, job_desc_input)
            
            # Arrange data item
            candidate_data = {
                "Name": result["profile"]["name"],
                "Email": result["profile"]["email"],
                "Skills": ", ".join(result["profile"]["skills"]),
                "Experience (Yrs)": result["profile"]["experience_years"],
                "Match Score": result["evaluation"]["matching_score"],
                "Summary": result["evaluation"]["summary"]
            }
            
            master_leaderboard.append(candidate_data)
            
            # Save to Supabase Cloud Database if configured
            if supabase:
                try:
                    supabase.table("candidates").insert({
                        "name": candidate_data["Name"],
                        "email": candidate_data["Email"],
                        "skills": candidate_data["Skills"],
                        "experience_years": candidate_data["Experience (Yrs)"],
                        "match_score": candidate_data["Match Score"],
                        "summary": candidate_data["Summary"]
                    }).execute()
                except Exception as db_err:
                    pass  # Silently proceed if table isn't created yet
            
            # Update progress
            progress_bar.progress((idx + 1) / len(uploaded_files))
        
        status_text.empty()
        progress_bar.empty()
    
    # Sort the master list by Match Score (Highest to Lowest)
    master_leaderboard = sorted(master_leaderboard, key=lambda x: x["Match Score"], reverse=True)
    
    # Display the beautiful sorted table on the dashboard
    st.dataframe(master_leaderboard, use_container_width=True)
    
    st.success(f"✅ Successfully screened, ranked, and saved {len(uploaded_files)} candidates to cloud!")
    
elif submit_button:
    st.warning("⚠️ Please provide both a job description and at least one PDF resume.")