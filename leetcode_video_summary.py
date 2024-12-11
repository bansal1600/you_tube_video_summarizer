import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key="AIzaSyA3KwHZayd4cvwI29fOW7SMe_wuFwUMxV0")

prompt="""
"You are a YouTube video summarizer. Your task is to analyze the transcript provided and identify the following information:

Title: Provide a concise title reflecting the main topic of the video.
Leetcode Link: provide the leetcode question link of the video
Psudo Code: Write steps of algorithem to explain in step by step 
Code: provide a leet code solution described in the problem and write the code explained in video in Python" 
Time Complexity : provide the time complexity of solution
Space Complexity : provide the space complexity of solution
"""


## getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e
    
## getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text,prompt):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text

# Streamlit app layout
st.title("Leetcode YouTube Video Summarizer")

# Input text box for the video link
video_url = st.text_input("Enter YouTube Video URL:")

if st.button("Summarize"):
    # Get transcript and summarize it
    if video_url:
        with st.spinner('Fetching and summarizing...'):
            transcript = extract_transcript_details(video_url)
            if "Error" not in transcript:
                summary = generate_gemini_content(transcript, prompt)
                st.subheader("Summary")
                st.write(summary)
            else:
                st.error(transcript)
    else:
        st.warning("Please enter a YouTube video URL.")