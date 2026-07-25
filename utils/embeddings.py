from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load model only once
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text):
    """
    Generate embedding for text.
    """
    return model.encode(text)


def calculate_similarity(job_description, resume_skills):
    """
    Compare Job Description with Resume.
    Returns similarity score (0-100).
    """

    jd_embedding = generate_embedding(job_description)

    resume_embedding = generate_embedding(resume_skills)

    similarity = cosine_similarity(
        [jd_embedding],
        [resume_embedding]
    )[0][0]

    return round(similarity * 100, 2)

