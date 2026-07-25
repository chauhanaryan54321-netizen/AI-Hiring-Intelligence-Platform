import pandas as pd

skills_df = pd.read_csv("data/skills.csv")

SKILLS = set(
    skills_df["skill"]
    .dropna()
    .str.lower()
)


def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        if skill in text:

            found_skills.append(skill)

    return sorted(list(set(found_skills)))

#Matching Skills
def compare_skills(job_skills, resume_skills):
    
    matched = sorted(
        list(
            set(job_skills) &
            set(resume_skills)
        )
    )

    missing = sorted(
        list(
            set(job_skills) -
            set(resume_skills)
        )
    )

    if len(job_skills) == 0:

        score = 0

    else:

        score = round(
            len(matched) / len(job_skills) * 100,
            2
        )

    return {

        "matched": matched,

        "missing": missing,

        "score": score

    }