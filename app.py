# we will be using Google Gemini Pro

import streamlit as st
from dotenv import load_dotenv
load_dotenv()                            #load all the environment variables
import os 
import google.generativeai as genai
#print(dir(genai))

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
#models = genai.list_models()
#for model in models:
#    print(model.name)
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🎥 YouTube Video Summarizer</h1>", unsafe_allow_html=True)
st.sidebar.header("📌 Input Video URL")
youtube_link = st.sidebar.text_input("Enter YouTube Video Link:")

prompt="""You are Youtube video summarizer. You will be taking the transcript 
text and summarizing the entire video and providing the important summary in points within 250 words. 
Please provide the summary of the text given here: """

## getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)
        transcript = "".join([i["text"] for i in transcript_text])
        #for i in transcript_text:
        #   transcript += " " + i["text"]
        return transcript

    except Exception as e:
        st.sidebar.error("❌ Could not retrieve transcript!")
        return None


## getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text, prompt):
    model=genai.GenerativeModel("gemini-1.5-flash")
    response=model.generate_content(prompt+transcript_text)
    return response.text


## creating streamlit app
#st.title("YouTube Transcript to Detailed Notes Converter")
#youtube_link = st.text_input("Enter Youtube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)

if st.sidebar.button("🎬 Generate Summary"):
    transcript_text = extract_transcript_details(youtube_link)

#if st.button("Get Detailed Notes"):
#    transcript_text=extract_transcript_details(youtube_link)

    if transcript_text:
        with st.spinner("Generating Summary... Please wait!"):
            summary=generate_gemini_content(transcript_text,prompt)
        
        st.subheader("🔍 Summary:")
        st.success(summary)
