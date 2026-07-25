from PyPDF2 import PdfReader

# Mern stack developer
# python 
# c 
# java
# c++
# css
# javascript
# node
# react
# express

def extract_text_from_pdf(uploaded_file):
    """
    Reads a single PDF and returns all extracted text.
    """

    pdf = PdfReader(uploaded_file)

    text = ""

    for page in pdf.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text.strip()


def extract_multiple_resumes(uploaded_files):
    """
    Reads multiple uploaded PDF resumes.

    Returns a list like:

    [
        {
            "filename": "...",
            "text": "..."
        }
    ]
    """

    resumes = []

    for file in uploaded_files:

        resume_text = extract_text_from_pdf(file)

        resumes.append(
            {
                "filename": file.name,
                "text": resume_text
            }
        )

    return resumes