import os            #os is a built-in Python module used to interact with the operating system

import google.generativeai as genai

from dotenv import load_dotenv    #python-dotenv is a library that loads the variables from the .env file into your Python program

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-3.5-flash"
)


def generate_feedback(job_description, resume):

    prompt = f"""
You are an experienced HR Recruiter.

Job Description:

{job_description}

Candidate Resume:

{resume["cleaned_text"]}

Matched Skills:

{", ".join(resume["matched_skills"])}

Missing Skills:

{", ".join(resume["missing_skills"])}

Skill Match:

{resume["skill_score"]}%

Semantic Match:

{resume["semantic_score"]}%

Final ATS Score:

{resume["final_score"]}%

Generate:

1. Candidate Summary

2. Strengths

3. Missing Skills

4. Resume Improvements

5. Interview Readiness

6. Hiring Recommendation

Keep the answer professional and concise.
"""

    response = model.generate_content(prompt)

    return response.text