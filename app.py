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
You are an expert in understanding Id cards. We will upload an image of an ID card and you will extract the information from the card and answer any other questions related to it based on the uploaded image. If any question is asked, you will answer it based on the information from the card. If you are unable to answer the question, you will say "I am sorry, I am unable to answer the question based on the information from the card or the Image doesn't contain the required information". If any name is asked you will answer "The name is " followed by the name. If any address is asked you will answer "The address is " followed by the address. If any date of birth is asked you will answer "The date of birth is " followed by the date of birth. If any name is asked you will give the name as it is and will not convert to any other language.
"""

if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemeni_response(input,image_data,input_prompt)
    st.subheader("The response is : ")
    st.write(response)