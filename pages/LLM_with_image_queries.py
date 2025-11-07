from dotenv import load_dotenv
load_dotenv()   #loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#function to load gemini model and get responses
model = genai.GenerativeModel('gemini-2.5-flash-lite')

def get_gemini_response(input,image):
    if input != "":
        response = model.generate_content([input,image])
    else:
        response = model.generate_content(image)
    return response.text

st.set_page_config(page_title="LLM Gemini")
st.header("Gemini LLM Application")
input = st.text_input("Input:",key="input")

upload_img = st.file_uploader("Choose an image..",type=['jpg','jpeg','png'])
image = ""
if upload_img is not None:
    image = Image.open(upload_img)
    st.image(image,caption="Uploaded Image.", use_container_width=True)
submit = st.button("Ask the Question")

#When submit is clicked

if submit:
    response = get_gemini_response(input,image)
    st.subheader("Your Response is:")
    st.write(response)

