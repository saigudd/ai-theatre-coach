"""Manual, billable API experiment: python -m tests.openai_test.

Importing this module (including pytest collection) makes no API calls.
"""


def main():
  from openai import OpenAI
  from dotenv import load_dotenv

  load_dotenv()

  with OpenAI() as client:
    response = client.responses.create(
      model="gpt-4o-mini",
      input="Write a verse about attachment and work that Krishna said in the Gita that is similar to the Stotism Meditations by Marcus Aurelius"
    )
    print(response.output_text)


if __name__ == "__main__":
  main()
