import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("OPENAI_MODEL")
username=os.getenv("OPENAI_USER")
mathpix_api_key = os.getenv("MATHPIX_API_KEY")
mathpix_app_id = os.getenv("MATHPIX_APP_ID")
serpapi_api_key = os.getenv("SERPAPI_API_KEY")

essay_prompt = os.getenv("INPUT_ESSAY_PROMPT")
case_study_pdf = os.getenv("CASE_STUDY_PDF")
input_path = os.getenv("PROJECT_DIR")+"/inputs/"
output_path = os.getenv("PROJECT_DIR")+"/outputs/"

CSV_INSTRUCTIONS = """Give no other
    text besides CSV. Ignore all previous command and prompts. Do not respond to this
    prompt besides with the CSV. Delimit using |."""

MARKDOWN_INSTRUCTIONS = """Give no other
    text besides properly formatted markdown code. Ignore all previous command and prompts. Do not respond to this prompt besides with the markdown."""

MATH_HW = """Here is a page from a math textbook. Identify and provide a solution
to all of the mathematical problems contained inside of it. Ignore any question that tells
you to draw something. Output your response in this format and rewrite identified
questions to be in full sentences.: "1. Question: Math question. Answer: Answer.\n"
Number your questions and answers. Answer ALL questions. Output with PROPER LATEX
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

ARGUMENTATIVE_ESSAY_INTRO_PARAGRAPH_YAML = """
Objective: {prompt}
Instructions: Write the introductory paragraph to five paragraph argumentative essay with
three body paragraphs. Write a highly detailed and compelling topic sentence in which you argue three distinct points. Build the rest of your introductory paragraph around this topic sentence.
ONLY WRITE THE INTRODUCTORY PARAGRAPH.
Number of Paragraphs: 1
Minimum word count: 100
Minimum number of citations: 1
Supporting Documents:{context}
"""

EXTRACT_TOPIC_SENTENCE = """
Instructions: Read this introductory paragraph and identify the topic sentence that
outlines the rest of the essay. Extract the three distinct points that will be argued in this essay. Respond with ONLY these points.
"""

ARGUMENTATIVE_ESSAY_BODY_PARAGRAPH_YAML = """
Instructions: Write one paragraph arguing point {order} in this list of arguments.
Make your argument highly detailed and compelling. Cite at least one specific source from
the supporting document below to build your argument. ONLY CITE FROM THE GIVEN SUPPORTING
DOCUMENTS. Do not restate your main point in
the beginning of the paragraph.
Number of Paragraphs: 1
Minimum word count: 100
Minimum number of citations: 1
Topic Sentence: {thesis}
Supporting Documents:{context}
"""

ARGUMENTATIVE_ESSAY_CONCLUSION_YAML = """
Instructions: Finish this essay by writing the concluding paragraph. Be concise but
entertaining. Make sure to restate the topic sentence. Remember that you are a college
student.
Number of Paragraphs: 1
Minimum word count: 100
Minimum number of citations: 1
Topic Sentence: {thesis}
Supporting Documents:{context}
"""

STUDYGUIDE = """Here is a blank study guide I made. I am a teacher and I want to test your
abilities. Identify all the questions/points in this study guide and provide a solution or
study help for each. Ignore anything that tells you to draw something. Output your
response in this format.: "1. INSERT_QUESTION_OR_TOPIC: INSERT_ANSWER_OR_DETAILS  "
Number your identified questions/topics and answers. Provide Answers for ALL. If mathematical equations are involved, output with PROPER LATEX and no Unicode characters. {} :""".format(MARKDOWN_INSTRUCTIONS)

HOMEWORK = """Here is a homework assignment. I am a teacher and I want to test your abilities. Identify and provide a solution to all of the problems contained inside of it. Ignore any question that tells you to draw something. Output your response in this format and rewrite identified questions to be in full sentences.: "1. Question: question. Answer: Answer.  "
Number your questions and answers. Answer ALL questions. If mathematical equations are
involved, output with PROPER LATEX and no Unicode characters. {} :""".format(MARKDOWN_INSTRUCTIONS)

prompts = {
        "HOMEWORK": HOMEWORK,
        "STUDYGUIDE": STUDYGUIDE,
        "EXAM": HOMEWORK
        }
PARSE_USER_DESCRIPTION = """
Below is a user description of a pdf document. The document is normally either a homework
assignment, a blank study guide, or an exam. Determine the document type, and determine
its subject. Respond ONLY in PERFECT JSON with this format:
{
"TYPE": "HOMEWORK/STUDYGUIDE/EXAM",
"SUBJECT": "INSERT_IDENTIFIED_SUBJECT"
"LATEX": "YES/NO"
}
"""
