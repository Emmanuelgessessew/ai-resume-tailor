import re

def match_keywords(resume_text, job_text):
    """
    Compare job description keywords with resume text.
    Returns two lists: found_keywords, missing_keywords.
    """

    # Clean up text (lowercase, remove punctuation)
    resume_text_clean = re.sub(r'[^a-zA-Z0-9\s]', '', resume_text.lower())
    job_text_clean = re.sub(r'[^a-zA-Z0-9\s]', '', job_text.lower())

    resume_words = set(resume_text_clean.split())
    job_words = set(job_text_clean.split())

    # Ignore short filler words like "a", "the", "is"
    job_keywords = {word for word in job_words if len(word) > 2}

    found = sorted([kw for kw in job_keywords if kw in resume_words])
    missing = sorted([kw for kw in job_keywords if kw not in resume_words])

    return found, missing
