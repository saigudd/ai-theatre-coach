import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def ask_ai(prompt):
  response = client.responses.create(
    model="gpt-4o-mini",
    input=prompt
  )
  return response.output_text

st.title("AI Line Partner")

line = st.text_input("Enter your line: ")

if st.button("Rehearse"):
  answer = ask_ai(f"""You are an acting partner.
    The user is rehearsing a scene. 
    Respond naturally as the other character. 
    Actor line: {line})""")
  st.write(answer)

  