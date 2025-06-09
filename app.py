import streamlit as st
import openai
import fitz  # PyMuPDF
import docx

st.set_page_config(page_title="FocusPOP - Resume Matcher", layout="centered")

st.title("📄 FocusPOP - Resume Matcher")
st.write("Upload a candidate's resume and paste a job description to see match % and screening questions.")

openai.api_key = st.secrets["OPENAI_API_KEY"]

def extract_text_from_pdf(file):
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        return " ".join([page.get_text() for page in doc])

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
job_description = st.text_area("Paste Job Description", height=200)

if st.button("Match Now"):
    if uploaded_file and job_description:
        with st.spinner("Reading resume..."):
            if uploaded_file.name.endswith(".pdf"):
                resume_text = extract_text_from_pdf(uploaded_file)
            else:
                resume_text = extract_text_from_docx(uploaded_file)

        prompt = f"Compare this resume:\n{resume_text}\n\nwith this job description:\n{job_description}\n\nGive a match percentage and 5 screening questions."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for technical hiring."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )

        st.success("✅ Match complete!")
        st.write(response["choices"][0]["message"]["content"])
    else:
        st.warning("Please upload a resume and paste a job description.")