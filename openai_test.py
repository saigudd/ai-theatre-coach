from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.responses.create(
      model="gpt-4o-mini",
      input="Write a verse about attachment and work that Krishna said in the Gita that is similar to the Stotism Meditations by Marcus Aurelius"
) 

print(response.output_text)