from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Gemeni pro vision
model = genai.GenerativeModel('gemini-pro-vision')

def get_gemeni_response(input,image,prompt):
    response  = model.generate_content([input,image[0],prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        #read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file was uploaded")

## initialize our streamlit app

st.set_page_config(page_title="Multi Language NID Extractor")
st.header("Multi Language NID Extractor")
input = st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image of your National ID card...", type=["jpg","jpeg","png"])

image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)


submit = st.button("Extract Information")
input_prompt = """
You are an expert in extracting information from ID cards.

Only provide the specefic information that is asked for in the prompt.
don't provide the whole and additional information in one go.
If you can't find any asked information then give a response like "I can't find the information".

"""

if submit:
    image_data = input_image_details(uploaded_file)
    input = input + " in the card."
    response = get_gemeni_response(input,image_data,input_prompt)
    st.subheader("The response is : ")
    st.write(response)