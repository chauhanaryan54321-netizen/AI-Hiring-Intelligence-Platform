import streamlit as st
from utils.pdf_reader import extract_multiple_resumes
from utils.preprocess import clean_text
from utils.nlp import preprocess_nlp
from utils.skill_extractor import (
    extract_skills,
    compare_skills
 )
from utils.embeddings import calculate_similarity
from utils.ranking import (
     calculate_final_score,
     rank_candidates
 )
from utils.feedback import generate_feedback
import pandas as pd
import matplotlib.pyplot as plt

# # Page Configuration

st.set_page_config(
    page_title="Smart Resume Screening System",
    page_icon="📄",
    layout="wide"
)

# Title

st.title("📄 Smart Resume Screening & Candidate Ranking Tool")

st.markdown("""
Analyze **multiple resumes** against a Job Description using AI.

Upload resumes, compare them with the Job Description, rank candidates,
and generate AI feedback.
""")

# # Sidebar

st.sidebar.title("Project Information")

st.sidebar.info("""
  Project:
  Smart Resume Screening Tool

Technology:

• Python

• Streamlit

• NLP

• Sentence Transformers

• LLM

• Candidate Ranking
""")

st.sidebar.success("GenAI Internship Project")

# Job Description

st.header("Job Description")

job_description = st.text_area(
    "Paste Job Description",
    height=250,
    placeholder="Paste complete Job Description here..."
 )


# Multiple Resume Upload

st.header("Upload Multiple Resume PDFs")

uploaded_files = st.file_uploader(
    "Choose Resume PDFs",
    type=["pdf"],
    accept_multiple_files=True
)


# # Resume Count

if uploaded_files:

    st.success(f"{len(uploaded_files)} Resume(s) Uploaded Successfully")


# Analyze Button

analyze = st.button("Analyze Resumes")


# Processing 

if analyze:
    
    if job_description == "":

        st.error("Please enter Job Description.")

    elif not uploaded_files:

        st.error("Please upload Resume PDFs.")

    else:

        with st.spinner("Reading Resume PDFs..."):

            resumes = extract_multiple_resumes(uploaded_files)

        st.success("All Resume PDFs Read Successfully!")

        st.write("### Resume Information")
        st.header("Cleaned Resume Preview")

        for resume in resumes:

            cleaned_resume = clean_text(resume["text"])

            resume["cleaned_text"] = cleaned_resume

            tokens = preprocess_nlp(cleaned_resume)

            resume["tokens"] = tokens

            st.subheader(resume["filename"])

            with st.expander("NLP Output"):

                st.write(tokens)

            job_skills = extract_skills(job_description)
                    
            st.header("Required Skills")
                    
            st.success(job_skills) 
            
            resume_skills = extract_skills(
                        cleaned_resume
                    )

            comparison = compare_skills(
                        job_skills,
                        resume_skills
                    )

            resume["resume_skills"] = resume_skills

            resume["matched_skills"] = comparison["matched"]

            resume["missing_skills"] = comparison["missing"]

            resume["skill_score"] = comparison["score"] 

            st.subheader(resume["filename"])

            st.write("Resume Skills")

            st.success(resume["resume_skills"])

            st.write("Matched Skills")

            st.info(resume["matched_skills"])

            st.write("Missing Skills")

            st.error(resume["missing_skills"])

            st.metric(
                "Skill Match %",
                f'{resume["skill_score"]}%'
                )   

            semantic_score = calculate_similarity(
                job_description,
                cleaned_resume
                )

            resume["semantic_score"] = semantic_score


            st.write("### ATS Analysis")

            resume["final_score"] = calculate_final_score(
                resume["skill_score"],
                resume["semantic_score"]
                )

            
            resumes = rank_candidates(resumes)

            st.subheader(
                f"Rank #{resume['rank']}"
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                "Final ATS Score",
                f"{resume['final_score']}%"
                )

            with col2:
                st.metric(
                "Skill Match",
                f"{resume['skill_score']}%"
                )

            with col3:
                st.metric(
                "Semantic Match",
                f"{resume['semantic_score']}%"
                )

            st.write("Resume:", resume["filename"])

            if resume["final_score"] >= 85:
                
                resume["status"] = "Highly Recommended"
            
            elif resume["final_score"] >= 70:
            
                resume["status"] = "Recommended"
            
            elif resume["final_score"] >= 50:
            
                resume["status"] = "Consider"
            
            else:
            
                resume["status"] = "Not Recommended"


            dashboard = []

            dashboard.append({

            "Rank": resume["rank"],

            "Candidate": resume["filename"],

            "Skill Score": resume["skill_score"],

            "Semantic Score": resume["semantic_score"],

            "ATS Score": resume["final_score"],

            "Status": resume["status"]

            })

            df = pd.DataFrame(dashboard)

            st.header("Candidate Ranking Dashboard")

            st.dataframe(
            df,
            use_container_width=True
            )    

            total = len(df)

            selected = len(
                df[df["Status"]=="Highly Recommended"]
            )

            recommended = len(
                df[df["Status"]=="Recommended"]
            )

            col1,col2,col3 = st.columns(3)

            with col1:
                st.metric(
                "Total Candidates",
                total
                )

            with col2:
               st.metric(
               "Highly Recommended",
               selected
               )

            with col3:
               st.metric(
               "Recommended",
               recommended
               )

            search = st.text_input(
                "Search Candidate"
                )

            if search:

                filtered = df[
                df["Candidate"].str.contains(
                search,
                case=False
                )
            ]

                st.dataframe(filtered)

            else:

                st.dataframe(df) 

                status = st.selectbox(

                    "Filter",

                    [

                    "All",

                    "Highly Recommended",

                    "Recommended",

                    "Consider",

                    "Not Recommended"

                    ]
                )  

            if status!="All":
    
                df = df[
                df["Status"]==status
                ]

            fig, ax = plt.subplots()

            ax.bar(

                df["Candidate"],

                df["ATS Score"]

            )

            ax.set_ylabel("ATS Score")

            ax.set_xlabel("Candidates")

            plt.xticks(rotation=45)

            st.pyplot(fig)   

            status_counts = df["Status"].value_counts()

            fig, ax = plt.subplots()

            ax.pie(

                status_counts,

                labels=status_counts.index,

                autopct="%1.1f%%"

            )

            st.pyplot(fig) 

            st.header("Top 5 Candidates")

            top = df.sort_values(

                "ATS Score",

                ascending=False

            ).head()

            st.table(top)

            candidate = st.selectbox(

                "Select Candidate",

                df["Candidate"]

            )

            selected = df[
                df["Candidate"]==candidate
            ]

            st.write(selected)

            csv = df.to_csv(index=False)

            st.download_button(

                label="Download Dashboard",

                data=csv,

                file_name="ATS_Report.csv",

                mime="text/csv"

            )

            st.divider()

            try:
                top_candidates = resumes[:10]

                for resume in top_candidates:
                 
                    resume["feedback"] = generate_feedback(
                    job_description,
                    resume
                    )
            except Exception:

                resume["feedback"] = "Unable to generate AI feedback."       

            st.subheader(
                f"AI Feedback - {resume['filename']}"
                )

            with st.expander("AI Generated Feedback"):
                st.write(resume["feedback"])

#REAL FUNCTIONING

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Uploaded Resumes", len(uploaded_files) if uploaded_files else 0)

with col2:
    st.metric("Selected Candidates", 0)

with col3:
    st.metric("Rejected Candidates", 0)


tab1, tab2, tab3 = st.tabs(
    [
        "Ranking",
        "Feedback",
        "Analytics"
    ]
)

with tab1:

    st.write("Candidate Ranking will appear here.")

with tab2:

    st.write("AI Feedback will appear here.")

with tab3:

    st.write("Charts and Statistics")

with st.expander("Preview Resume Text"):

    st.write("Resume content will appear here.")

#Download Resume

st.download_button(
    "Download Report",
    data="Candidate Ranking Report",
    file_name="report.txt"
)

