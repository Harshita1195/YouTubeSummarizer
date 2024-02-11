#Import Libraries
from dotenv import load_dotenv
load_dotenv() ## load all the environemnt variables
import streamlit as st
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

## Configure Genai Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""You are YouTube video summarizer. You will be taking the transcript text and summarizing the entire video
and providing the important summary in points within 250 words. Please provide the summary of the text given here: """

def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript=""
        for i in transcript_text:
            transcript+=" "+i["text"]

        return transcript

    except Exception as e:
        raise e

def generate_gemini_content(transcript_text, prompt):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text

st.title("YouTube Transcript Summarizer")
youtube_link=st.text_input("Enter YouTube Video Link: ")

if youtube_link:
    video_id=youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Summary"):
    transcript_text=extract_transcript_details(youtube_link)

    if transcript_text:
        summary=generate_gemini_content(transcript_text, prompt)
        st.markdown("## Summary:")
        st.write(summary)