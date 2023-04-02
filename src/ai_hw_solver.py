import os
from utils import to_csv, from_csv, read_pdf
import constants
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet
import openai

def hw_solutions_to_pdf(json_data, output_filename="outputs/{}.pdf".format("hw")):
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
          model=constants.model,
          messages=[
            {"role": "user", "content": prompt + page}
          ])
        solutions.append(solution["choices"][0]["message"]["content"])
    return solutions

if __name__ == '__main__':
    hwdir = "hw/"
    hwtitle = "hw1"
    hwpages = read_pdf(hwdir+hwtitle)
    solutions = solve(hwpages, constants.DEFAULT_HW_PROMPT)
    filenames = to_csv(solutions, hwtitle)
    i = 0
    for file in filenames:
        solution_csv = from_csv(file)
        hw_solutions_to_pdf(solution_csv, hwtitle+str(i))
        i+=1
