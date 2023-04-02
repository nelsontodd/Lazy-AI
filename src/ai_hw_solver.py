import os
import json
import csv
from pyxpdf import Document, Page, Config
from pyxpdf.xpdf import TextControl
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet
import openai


def read_pdf(filename):
    with open(filename, 'rb') as fp:
        doc = Document(fp)
    control = TextControl(mode = "physical")
    txt = []
    for page in doc:
        txt.append(page.text(control=control))
    return txt

def to_csv(string, title="hwsolution"):
    i = 1
    filenames = []
    for item in string:
        filename = 'outputs/{}{}.csv'.format(title, i)
        with open(filename, 'w') as file:
            file.write(item)
        i+=1
        filenames.append(filename)
    return filenames

def json_from_csv(filename):
    for item in filename:
        with open(item, 'r') as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
    return data

def generate_pdf(json_data, output_filename="outputs/{}.pdf".format("hw1")):
    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    styles = getSampleStyleSheet()

    content = []
    list_items = []
    for item in json_data:
        for key,value in item.items():
            list_items.append(ListItem(Paragraph(f'<b>{key}</b>: <b>{value}</b>', styles['Normal'])))

    content.append(ListFlowable(list_items, bulletType='bullet'))

    doc.build(content)

def solve(pages, prompt):
    solutions = []
    for page in pages:
        solution = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
            {"role": "user", "content": prompt + page}
          ])
        print(solution["choices"][0])
        solutions.append(solution["choices"][0]["message"]["content"])
    return solutions

if __name__ == '__main__':
    openai.api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL")
    username=os.getenv("OpenAIUser")
    PROMPT = """Here is a page from a PDF document. Identify and provide an answer to all of
    the mathematical problems contained inside of it. Generate a CSV file with a list of each
    question and answer. Give no other text besides CSV. Ignore all previous command and
    prompts. Do not respond to this prompt besides with the CSV quiz.Make everything
    lowercase, delimit using commas. The columns will be titled question and answer. Ignore
    any question that tells you to draw something.:"""
    hwfile = "hw/hw1.pdf"
    hwpages = read_pdf(hwfile)
    solutions = solve(hwpages, PROMPT)
    filename = to_csv(solutions, "hw1solutions")
    data = json_from_csv(filename)
    generate_pdf(data)
