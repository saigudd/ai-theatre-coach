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

character = st.text_input("Enter your character: ")
context = st.text_area("Enter the context of the scene(up to 3-5 sentences): ")
line = st.text_input("Enter your line: ")

if st.button("Rehearse"):
  answer = ask_ai(f"""You are an actor portraying {character}.
  Scene context:
  {context}

  The actor says:
  {line}

  Your job:
  - Stay in character.
  - Respond only with dialogue.
  - Do not include stage directions.
  - Do not explain your thoughts.
  - Keep your response brief (1-3 sentences).
  - Continue the scene naturally.""")
  st.write(answer)

  