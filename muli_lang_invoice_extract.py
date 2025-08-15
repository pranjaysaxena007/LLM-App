from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load gemini model
model = genai.GenerativeModel('gemini-2.5-flash-lite')

def get_gemini_response(input,image,prompt):
    response = model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        print(bytes_data)
        image_parts = [
            {
                "mime_type" : uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")

#streamlit setup
st.set_page_config(page_title ="Multi Language Invoice Extractor") 
st.header("Gemini Multi Language Invoice Extractor")
input = st.text_input("Input Prompt:",key="input")
upload_file = st.file_uploader("Choose an image of invoice...",type=['jpg','jpeg','png','wepm'])
image= ""
if upload_file is not None:
    image = Image.open(upload_file)
    st.image(image,caption="Uploaded Image",use_container_width=True)

submit = st.button("Tell me about the image")

input_prompt = """
You are an expert in understanding invoices. We will upload an image of an invoice.
You have to answer any question based on that uploaded image.
"""

#if submit button clicked
if submit:
    image_data = input_image_setup(upload_file)
    response = get_gemini_response(input_prompt,image_data,input)
    st.subheader("Response:")
    st.write(response)