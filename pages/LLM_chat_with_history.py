from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

#function to load model

model = genai.GenerativeModel("gemini-2.5-flash-lite")
chat_model = model.start_chat(history=[])

def get_gemini_response(image,question):
    if question!="" and image!="":
        response = chat_model.send_message([question,image],stream = True)
    elif image=="":
        response = chat_model.send_message(question,stream=True)
    elif question=="":
        response = chat_model.send_message(image,stream=True)
    return response

#Initialize app

st.set_page_config("LLM Chat")
st.header("Gemini Chat LLM Application")

#Initialize ession state for chat history if not exists

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("Input:",key="input")
upload_img = st.file_uploader("Choose an image..",type=['jpg','jpeg','png'])
image = ""
if upload_img is not None:
    image = Image.open(upload_img)
    st.image(image,caption="Uploaded Image.", use_container_width=True)
submit = st.button("Ask the Question")

if submit:
    response = get_gemini_response(image,input)
    #Add user query and response to chat history
    st.session_state['chat_history'].append(("You",input))
    st.subheader("The Response is:")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot",chunk.text))

st.subheader("Chat History:")
for role,text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")

