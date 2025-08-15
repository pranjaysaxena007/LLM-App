from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image 

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,image,prompt):
    model = genai.GenerativeModel("gemini-2.5-flash-lite")
    response = model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_image):
    if uploaded_image is not None:
        bytes_data = uploaded_image.getvalue()
        image_parts = [
            {
                "mime_type":uploaded_image.type,
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")
    
#streamlit app
st.set_page_config(page_title="Calorie Counter")
st.header("Gemini Calorie Counter")
input = st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Upload a file: ",type=['jpg','jpeg','png'])
image = "" 
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image",use_container_width=True)

submit = st.button("Tell me total calories")

input_prompt="""
    You are an expert nutritionist and you need to see the food items from the image and need to caclculate total calories intake.
    Also provide detailed calorie intake of every food item in below format.
    1. Item 1 : no. of calories
    2. Item 2 : no. of calories
    ----
    ----
"""

#If submit button clicked
if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Response is:")
    st.write(response)
