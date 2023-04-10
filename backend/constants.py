import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("OPENAI_MODEL")
username=os.getenv("OPENAI_USER")
mathpix_api_key = os.getenv("MATHPIX_API_KEY")
mathpix_app_id = os.getenv("MATHPIX_APP_ID")

CSV_INSTRUCTIONS = """Give no other
    text besides CSV. Ignore all previous command and prompts. Do not respond to this
    prompt besides with the CSV. Delimit using |."""

MARKDOWN_INSTRUCTIONS = """Give no other
    text besides properly formatted markdown code. Ignore all previous command and prompts. Do not respond to this prompt besides with the markdown."""

MATH_HW = """Here is a page from a math textbook. Identify and provide an answer
to all of the mathematical problems contained inside of it. Note that it is formatted in
LATEX. Ignore any question that tells you to draw something. Output your response in this
format and rewrite identified questions to be in full sentences.: "1. Question: Math question.
Answer: Answer. Explanation: Simple intuitive explanation." Number your questions and answers. Answer ALL questions. Use proper LATEX
and no Unicode characters. {} :""".format(MARKDOWN_INSTRUCTIONS)

MATH_EXPLANATIONS = """Here is an answer key for a math assignment. For each
problem and corresponding solution provide a detailed 2-3 sentence explanation and/or
derivation. Note that the answer key is formatted in LATEX. Ignore any question that tells you to draw something. Output your response in this format.: "1. Question: Math question.
Answer: answer. Explanation: explanation" Number your questions and answers. Provide an
explanation for ALL answers. Use proper LATEX and no Unicode characters. {} :""".format(MARKDOWN_INSTRUCTIONS)

DEFAULT_QUIZ =  """I am going to give you a transcript of an audio recording. Use the
    text to generate a CSV file with a list of five questions and answers. {} The
    columns will be titled Question and Anser. : """.format(CSV_INSTRUCTIONS)

DEFAULT_SUMMARY =  """I am going to give you a transcript of an audio recording. Use the
    text to generate an "executive summary" of what happened during the meeting. Ignore all previous command and prompts. Do not respond to this prompt besides with the summary.: """

NON_MATH_HW = """Here is a page from a textbook. Identify and provide an answer
to all of the questions contained inside of it. Be insightful and creative! Ignore any question that tells you to draw something. Output your response in this format and rewrite identified questions to be in full sentences.: "1. Question: question. Answer: Answer." Number your questions and answers. Answer ALL questions. Use no Unicode characters. {} :""".format(MARKDOWN_INSTRUCTIONS)
