import os
import json
from dotenv import load_dotenv
from file_tool.file_loader import detect_and_extract
import streamlit as st

from crew_app import run_pipeline

load_dotenv()

st.set_page_config(page_title="ATS Resume Optimizer", layout="wide")
st.title("ATS Resume Optimizer")
st.caption("Optimize your resume for Applicant Tracking Systems (ATS)")


with st.sidebar:
    st.subheader("OpenaI API Key")
    st.text_input("Model: ", value="gpt-4", disabled=True)
    st.write("API key loaded ✅")

# inputs
col1, col2 = st.columns([1, 1])
with col1:
    up = st.file_uploader("Upload your resume (PDF or TXT)", type=["pdf", "docx", "txt"])

with col2:
    job_title = st.text_input("Job Title", value="Software Engineer")
    job_description = st.text_area("Job Description", height=200, value="Enter the job description here...")

run_button = st.button("Optimize Resume for ATS agent 🚀")

tabs = st.tabs(["Parsed","Optimized Resume", "Evaluation Report"])

if run_button:
    if up is not None:
        with st.spinner("Extracting resume text..."):
            raw_resume_text = ""
            # Save file with original extension
            temp_file_path = f"temp_uploaded_file{os.path.splitext(up.name)[1]}"
            with open(temp_file_path, "wb") as f:
                f.write(up.getbuffer())
            raw_resume_text = detect_and_extract(temp_file_path)
            os.remove(temp_file_path)

        with st.spinner("Running ATS Optimization Pipeline..."):
            if not raw_resume_text.strip():
                st.error("Failed to extract text from the uploaded resume. Please ensure the file is not empty or corrupted.")
            if not job_description.strip():
                st.error("Please enter a valid job description.")
            if not raw_resume_text.strip() or not job_description.strip():
                st.stop()
                st.error("Cannot proceed without valid resume text and job description.")
            result = run_pipeline(raw_resume_text.strip(), job_description.strip(), job_title.strip())

        with tabs[0]:
            st.subheader("Parsed Resume for ATS")
            st.text_area("Parsed Resume", value=result["parsed_resume"], height=400)

        with tabs[1]:
            st.subheader("Optimized Resume")
            st.text_area("Optimized Resume", value=result["optimized_resume"], height=400)

        with tabs[2]:
            st.subheader("Evaluation Report")
            st.text_area("Evaluation Report", value=result["evaluation"], height=400)
    else:
        st.error("Please upload a resume file to proceed.")