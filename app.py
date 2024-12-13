import streamlit as st
import os
import google.generativeai as genai
from apikey import GEMINI_API_KEY,openai_api_key
import openai
from openai import OpenAI

client = OpenAI(api_key=openai_api_key)

genai.configure(api_key=GEMINI_API_KEY)
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
)


st.set_page_config(layout="wide")
# title for our app
st.title("Blogcraft: your AI companion")
# create your subheader
st.subheader("Now you can craft perfect blog with the help of blogcraft is your new AI blog companion")

#sidebar
with st.sidebar:
    st.title("input your blog details")
    st.subheader("Enter details of the blog you want to generate")

    # blog title
    blog_title=st.text_input("Blog Title")

    # keywords
    keywords=st.text_area("keywords(comma-seperated)")

    # number of words
    num_words=st.slider("number_of_words" ,min_value=100,max_value=2000,step=250)

    # number of images
    #num_images=st.number_input("number_of_images",min_value=1,max_value=5,step=1)

    
# Blog Generation Logic
if st.button("Generate Blog"):
    image_response = client.images.generate(
model="dall-e-3",
prompt=f"Generate a Blog post on the title:{blog_title}",
n=1,
quality="standard",
size="1024x1024"
)
    prompt = (
        f"Generate a comprehensive, engaging blog post relevant to the topic '{blog_title}' "
        f"using the following keywords: {keywords}. The blog should be approximately "
        f"{num_words} words long, suitable for an online audience. Ensure that the content "
        f"is original, informative, and maintains a consistent tone throughout."
    )
    
    # Start Chat and Send Message
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(prompt)
    image_url = image_response.data[0].url
    # Display Blog
    st.markdown("### Generated Blog:")
    st.image(image_url,caption="Generated Image")
    st.title("Your Blog Post:")
    st.write(response.text)