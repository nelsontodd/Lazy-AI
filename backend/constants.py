import os
import promptlayer
promptlayer.api_key = "pl_68f5e2937994a1784404eaae2421a0b1"
openai = promptlayer.openai
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
sand = False
if os.getenv('ENVIRON') == 'SAND':
    sand = True

CSV_INSTRUCTIONS = """Give no other
    text besides CSV. Ignore all previous command and prompts. Do not respond to this
    prompt besides with the CSV. Delimit using |."""

MARKDOWN_INSTRUCTIONS = """Give no other
    text besides properly formatted markdown code. Ignore all previous command and prompts. Do not respond to this prompt besides with the markdown."""

LATEX_INSTRUCTIONS = """Give no other
    text besides properly formatted LATEX code. Do not respond to this prompt besides with
    the LATEX."""

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

NON_MATH_STUDYGUIDE = """Here is a blank study guide I made. I am a teacher and I want to test your
abilities. Identify all the questions/points in this study guide and provide a solution or
study help for each. Ignore anything that tells you to draw something. Output your
response in this format.: "1. INSERT_QUESTION_OR_TOPIC: INSERT_ANSWER_OR_DETAILS  "
Number your identified questions/topics and answers. If there is a question or a topic
with a table (or something with rows and columns), ignore the previous format for that
question and output in a table (or rows and columns)! Remember to think on your output
format and your solutions and do what works and looks best. You can bend my rules a little
bit if it works better! Provide Answers for ALL. {} :""".format(MARKDOWN_INSTRUCTIONS)

MATH_STUDYGUIDE = """
Here is a blank study guide I made. I am a teacher and I want to test your
abilities. Identify all the questions/points in this study guide and provide a solution or
study help for each. Ignore anything that tells you to draw something. Output your
questions (or points) and answers/study help in these formats, depending on type of question: 

TYPE 1:SINGLE SHORT ANSWER RESPONSE QUESTION WITH NO SUB PARTS
    \question IDENTIFIED_QUESTION
    \begin{solution}
    IDENTIFIED_SOLUTION
    \end{solution}
    
    \question  IDENTIFIED_QUESTION
    \begin{solution}
    IDENTIFIED_SOLUTION
    \end{solution}

TYPE 2: SHORT ANSWER RESPONSE QUESTIONS WITH SUB PARTS
\question IDENTIFIED_QUESTION
\begin{parts}
    \part IDENTIFIED SUB QUESTION (eg Maybe part a) or part 1)
    \begin{solution}
    IDENTIFIED SUB ANSWER
    \end{solution}

    \part IDENTIFIED SUB QUESTION (eg Maybe part b) or part 2)
    \begin{solution}
    IDENTIFIED SUB ANSWER
    \end{solution}
\end{parts}

TYPE 3: MULTIPLE CHOICE QUESTIONS

    \question IDENTIFIED_QUESTION
    \begin{solution}
    IDENTIFIED_SOLUTION BY LETTER OR NUMBER
    \end{solution}

Number your questions and answers. Answer ALL questions. Output with PROPER LATEX and no
Unicode characters. Follow ALL the rules of LATEX. Outputting in properly formatted LATEX
is very important. Dont include any commands that are supposed to be used in the preamble.
Your output will be in the main body of a document.

Rule: Answer ALL questions.
Rule: PROPER LATEX with no preamble commands
Tip: Be careful not to confuse multiple choice questions with questions that have sub parts ie a,b,c, and d! Review the wording of the question to determine its type and proper format.
Tip: Normally, questions in a homework document will be preceded by either a number or a letter at the beginning of a line.
Tip: Format your questions and answers for use in the body of the LATEX exam document class.
AVAILABLE LATEX PACKAGES: amssymb, amsmath, [utf8]{inputenc}, amsfonts, bm, esint, siunitx
"""
NON_MATH_HOMEWORK = """I am a teacher and I want to test your abilities. Here is a homework assignment. Identify and provide a solution to all of the problems contained inside of it. Ignore any question that tells you to draw something. rewrite identified questions to be
in full sentences. Output your questions and answers in this format: "1.
IDENTIFIED_QUESTION  \n- ANSWER  " Number your questions and answers. Answer ALL
questions. If there is a question or a topic
with a table (or something with rows and columns), ignore the previous format for that
question and output in a table (or rows and columns)! Remember to think on your output
format and your solutions and do what works and looks best. You can bend my rules a little
bit if it works better! Provide Answers for ALL.{} :""".format(MARKDOWN_INSTRUCTIONS)

MATH_HOMEWORK = """
I am a teacher and I want to test your abilities. Here is a homework assignment. Identify
all of the problems contained inside of it. Then, come up with your own answer to each question. Think hard and reflect on your answers. Ignore any question that tells you to draw something. Rewrite identified questions to be in full sentences where you see fit. Output your questions and answers in these formats, depending on type of question: 

TYPE 1:SINGLE SHORT ANSWER RESPONSE QUESTION WITH NO SUB PARTS
    \question IDENTIFIED_QUESTION
    \begin{solution}
    IDENTIFIED_SOLUTION
    \end{solution}
    
    \question  IDENTIFIED_QUESTION
    \begin{solution}
    IDENTIFIED_SOLUTION
    \end{solution}

TYPE 2: SHORT ANSWER RESPONSE QUESTIONS WITH SUB PARTS
\question IDENTIFIED_QUESTION
\begin{parts}
    \part IDENTIFIED SUB QUESTION (eg Maybe part a) or part 1)
    \begin{solution}
    IDENTIFIED SUB ANSWER
    \end{solution}

    \part IDENTIFIED SUB QUESTION (eg Maybe part b) or part 2)
    \begin{solution}
    IDENTIFIED SUB ANSWER
    \end{solution}
\end{parts}

TYPE 3: MULTIPLE CHOICE QUESTIONS

    \question IDENTIFIED_QUESTION
    \begin{solution}
    IDENTIFIED_SOLUTION BY LETTER OR NUMBER
    \end{solution}

Number your questions and answers. Answer ALL questions. Output with PROPER LATEX and no
Unicode characters. Follow ALL the rules of LATEX. Outputting in properly formatted LATEX
is very important. Dont include any commands that are supposed to be used in the preamble.
Your output will be in the main body of a document.

Rule: Answer ALL questions.
Rule: PROPER LATEX with no preamble commands
Tip: Be careful not to confuse multiple choice questions with questions that have sub parts ie a,b,c, and d! Review the wording of the question to determine its type and proper format.
Tip: Normally, questions in a homework document will be preceded by either a number or a letter at the beginning of a line.
Tip: Format your questions and answers for use in the body of the LATEX exam document class.
AVAILABLE LATEX PACKAGES: amssymb, amsmath, [utf8]{inputenc}, amsfonts, bm, esint, siunitx
"""

PARSE_USER_DESCRIPTION_SYSTEM_PROMPT = """
You are the router for lazyai, a natural language homework solutions manual. Determine,
based on user input, the type of the document that the user is uploading, either homework
or study guide. Determine also if the document will contain LATEX. Homework and study
guides in subjects related to math, engineering, sciences, or medicine will contain LATEX.
Homeworks and study guides in fields related to the social studies or literature or art
will not contain LATEX.
"""

CODE_HOMEWORK = """
I am a teacher and I want to test your abilities. Here is a homework assignment. Identify
all of the problems contained inside of it. Then, come up with your own answer to each
question. Think hard and reflect on your answers. Ignore any question that tells you to
draw something. Rewrite identified questions to be in full sentences where you see fit.
Output your questions and answers in this format: 

\question INSERT_IDENTIFIED_CODE_QUESTION
\begin{solution}
\begin{lstlisting}
INSERT_CODE_ANSWER_IN_PROPER_PROGRAMMING_LANGUAGE
\end{lstlisting}
\end{solution}

Number your questions and answers. Answer ALL questions. Output with PROPER CODE LATEX and no
Unicode characters. Follow ALL the rules of LATEX. Outputting in properly formatted LATEX
is very important. Dont include any commands that are supposed to be used in the preamble.
Your output will be in the main body of a document.

Rule: Answer ALL questions.
Rule: PROPER LATEX with no preamble commands
Tip: Be careful not to confuse multiple choice questions with questions that have sub parts ie a,b,c, and d! Review the wording of the question to determine its type and proper format.
Tip: Normally, questions in a homework document will be preceded by either a number or a letter at the beginning of a line.
Tip: Format your questions and answers for use in the body of the LATEX exam document class.
Tip: You will be using the lstlisting latex package in this document. Identify the correct
programming language and write it in a lstlisting block.

AVAILABLE LATEX PACKAGES: amssymb, amsmath, [utf8]{inputenc}, amsfonts, bm, esint,
siunitx, listings, xcolor
NOT AVAILABLE: algorithms, algpseudocode, minted

EXAMPLE OUTPUT: 
\question Write fizzbuzz in C++.
\begin{solution}
\begin{lstlisting}
#include <iostream>

int main() {
    for (int i = 1; i <= 100; ++i) {
        if (i % 3 == 0 && i % 5 == 0) {
            std::cout << "FizzBuzz" << std::endl;
        } else if (i % 3 == 0) {
            std::cout << "Fizz" << std::endl;
        } else if (i % 5 == 0) {
            std::cout << "Buzz" << std::endl;
        } else {
            std::cout << i << std::endl;
        }
    }
    return 0;
}
\end{lstlisting}
\end{solution}
"""
