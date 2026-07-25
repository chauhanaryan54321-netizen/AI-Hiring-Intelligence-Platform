def calculate_final_score(skill_score, semantic_score):
    """
    Combine Skill Score and Semantic Score.
    """

    final_score = (
        skill_score * 0.40 +
        semantic_score * 0.60
    )

    return round(final_score, 2)


def rank_candidates(resumes):
    """
    Rank candidates according to Final ATS Score.
    """

    resumes.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    rank = 1

    for resume in resumes:

        resume["rank"] = rank

        rank += 1

    return resumes