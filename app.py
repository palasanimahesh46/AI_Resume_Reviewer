from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
from PIL import Image
import io
import pdf2image
import base64

import google.generativeai as genai

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert PDF to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        # Take the first page for simplicity, or loop through images for all pages
        first_page = images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")


st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF...",type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Upladed Successfully")


submit1 = st.button("Tell Me About the Resume")

#submit2 = st.button("How Can I Improvise my Skills")

#submit3 = st.button("What are the Keywords That are Missing")

submit3 = st.button("Percentage Match")

input_prompt1 = """
You are an experienced HR With Tech Experience in the filed of any one job role from Data Science,Full stack Web development,Big Data Engineering,DEVOPS,Data Analyst,your task is to review the provided resume against the job description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with it
Highlight the strengths and weaknesses of the applicant in relation to the specified job role
"""



input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of any one job role  Data Science, Web development,Big Data Engineering,DEVOPS,Data Analyst and deep ATS functionality,
your task is to evaluate the resume against the provided job description. give me the percentage alignment with the job description. First the output should come as percentage and then keywords missing aligned with
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("the response is")
        st.write(response)
    else:
        st.write("please upload the resume")

if submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("the response is")
        st.write(response)
    else:
        st.write("please upload the resume")
