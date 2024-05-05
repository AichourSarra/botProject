
import streamlit as st
import os
import google.generativeai as genai
import pandas as pd
from fuzzywuzzy import fuzz

# Load environment variables from .env file


# Configure GenerativeAI with Google API key
genai.configure(api_key=os.getenv("AIzaSyBVM7enBvs-oDfl_3zr86SYtF60pW7ebBQ"))

# Load the Gemini model
model = genai.GenerativeModel("gemini-pro")

# Read the CSV file containing questions and answers
file_path = r"C:\Users\Mustapha\Downloads\chnse (2)\chnse\file.csv"
knowledge_df = pd.read_csv(file_path)

# Function to get response from Gemini model
def get_gemini_response(question):
    chat = model.start_chat(history=[])
    response = chat.send_message(question, stream=True)
    return response

# Function to find the most relevant answer based on the user's question
def find_answer(question, knowledge_df):
    max_similarity = -1
    best_answer = None
    for index, row in knowledge_df.iterrows():
        similarity = fuzz.token_sort_ratio(question.lower(), row['Question'].lower())
        if similarity > max_similarity:
            max_similarity = similarity
            best_answer = row['Answer']
    return best_answer

# Set page configuration and styling
st.set_page_config(page_title="Q&A Demo", page_icon=":robot_face:", layout="wide")



# Set header and title
st.title("Welcome Student!")

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Display input field and submit button
input_question = st.text_input("Input your question:")
submit_button = st.button("Ask the question")

# Handle form submission
if submit_button and input_question:
    # Find the most relevant answer from the CSV file
    answer = find_answer(input_question, knowledge_df)
    if answer:
        with st.chat_message(name="assistant"): 
         st.write(answer)
    else:
        # If no relevant answer found in the CSV file, use Gemini model
        response = get_gemini_response(input_question)
        st.subheader("The response is")
        for chunk in response:
            st.write(chunk.text)
    # Add user query and response to session chat history
    with st.sidebar:
     st.session_state['chat_history'].append(("You", input_question))
     st.session_state['chat_history'].append(("Bot", answer if answer else response))
    
    # Display chat history
     st.subheader("Chat History")
     for role, text in st.session_state['chat_history']:
         st.write(f"{role}: {text}")
