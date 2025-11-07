import google.generativeai as genai
import pathlib
import textwrap
from dotenv import load_dotenv
load_dotenv()
import os
from IPython.display import display, Markdown

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))