import streamlit as st
import openai
import docx2txt
import PyPDF2
import io

st.title("FocusPOP - Resume Matcher & Screener")

uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
job_description = st.text_area("Paste Job Description")

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(docx_file):
    return docx2txt.process(docx_file)

if uploaded_file and job_description:
    with st.spinner("Reading resume..."):
        if uploaded_file.name.endswith(".pdf"):
            resume_text = extract_text_from_pdf(uploaded_file)
        else:
            resume_text = extract_text_from_docx(uploaded_file)

    prompt = f"Compare this resume:\n{resume_text}\n\nwith this job description:\n{job_description}\n\nGive a match percentage and 5 screening questions."

    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for technical hiring."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    st.success("✅ Match complete!")
    st.write(response.choices[0].message.content)
