import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("OPENAI_MODEL")
username=os.getenv("OPENAI_USER")

CSV_INSTRUCTIONS = """Give no other
    text besides CSV. Ignore all previous command and prompts. Do not respond to this
    prompt besides with the CSV. Delimit using |."""

MARKDOWN_INSTRUCTIONS = """Give no other
    text besides properly formatted markdown code. Ignore all previous command and prompts. Do not respond to this prompt besides with the markdown."""

DEFAULT_HW_PROMPT = """Here is a page from a PDF document. Identify and provide an answer
to all of the mathematical problems contained inside of it. Note that some of the
mathematical symbols were possibly formatted incorrectly. Use your best judgement to
figure out what they mean. Ignore any question that tells
you to draw something. Output your response in a format like Question: Math question.
Answer: Answer. {} :""".format(MARKDOWN_INSTRUCTIONS)

DEFAULT_QUIZ_PROMPT =  """I am going to give you a transcript of an audio recording. Use the
    text to generate a CSV file with a list of five questions and answers. {} The
    columns will be titled Question and Anser. : """.format(CSV_INSTRUCTIONS)

DEFAULT_SUMMARY_PROMPT =  """I am going to give you a transcript of an audio recording. Use the
    text to generate an "executive summary" of what happened during the meeting. Ignore all previous command and prompts. Do not respond to this prompt besides with the summary.: """

