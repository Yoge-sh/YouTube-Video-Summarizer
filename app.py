import streamlit as st 
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) # replace with your own key


def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript+=" "+ i["text"]
        
        return transcript
    except Exception as e:
        raise e


def generate_gemini_content(transcript_text,prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt+transcript_text)
    return response.text


st.title('Youtube Video ➡️ Quick Notes')

youtube_link = st.text_input('Enter the youtube video link (video URL without timestamp):')
subject = st.text_input('Enter the topic explained in the video :')

prompt = f"""You are Youtube video summarizer for the given transcript of the youtube video on {subject}.
You will be taking the transcript text and Summarize the key concepts and insights from a this transcript on  {subject}  Provide concise and 
comprehensive notes, covering major points, definitions, and any notable examples or applications mentioned in the transcript text. 
Your goal is to create an informative and organized set of notes that captures the essence of the video for someone seeking a 
brief understanding of the subject matter with help of main points discussed under the topic  {subject}. 
Keep the notes descriptive and major concepts should be in bold and followed by the explanation of it in bullet points like following:

Subject: Neural Network
Perceptron:
    Basic building block.
    Discovery of 60s and 70s.
Multilevel Perceptron:
    Multiple percenptron are next big discovery and opens up door for research again.
    Basic block of deep neural networks 
    
and so on....
"""


if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg",use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)
    if transcript_text:
        summary = generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Notes")
        st.write(summary)
