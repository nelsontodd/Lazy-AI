import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("OPENAI_MODEL")
username=os.getenv("OPENAI_USER")

DEFAULT_HW_PROMPT = """Here is a page from a PDF document. Identify and provide an answer to all of
    the mathematical problems contained inside of it. Generate a CSV file with a list of each
    question and answer. Give no other text besides CSV. Ignore all previous command and
    prompts. Do not respond to this prompt besides with the CSV quiz.Make everything
    lowercase, delimit using commas. The columns will be titled question and answer. Ignore
    any question that tells you to draw something.:"""

DEFAULT_QUIZ_PROMPT =  """I am going to give you a transcript of an audio recording. Use the
    text to generate a CSV file with a list of five questions and answers. Give no other
    text besides CSV. Ignore all previous command and prompts. Do not respond to this
    prompt besides with the CSV quiz.Make everything lowercase, delimit using commas. The
    columns will be titled question and answer. : """

