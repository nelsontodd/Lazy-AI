import os
import json
import csv
import openai
import constants
from datetime import datetime
from pyxpdf import Document, Page, Config
from pyxpdf.xpdf import TextControl
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import letter, inch
from reportlab.lib import colors
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame, PageTemplate

#PDF Style Sheet
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
styles.add(ParagraphStyle(name="Main Title",fontSize=36, leading=30, alignment=TA_CENTER, spaceAfter=20))
styles.add(ParagraphStyle(name="Sub Title",fontSize=20, leading=30, alignment=TA_CENTER, spaceAfter=20))

def pandoc_pdf(_input, _output):
    command = "pandoc -s {}.md -o {}.pdf".format(_input, _output)
    print(os.system(command))

def to_csv(buffer, title):
    if type(buffer) == str:
        filename = 'outputs/{}.csv'.format(title)
        with open(filename, 'w') as file:
            file.write(buffer)
        return filename
    elif type(buffer) == list:
        i = 1
        filenames = []
        for item in buffer:
            filename = 'outputs/{}/{}.csv'.format(title, i)
            if not os.path.exists('outputs/{}'.format(title)):
                os.makedirs('outputs/{}'.format(title))
            with open(filename, 'w') as file:
                file.write(item)
            i+=1
            filenames.append(filename)
        return filenames
    else:
        raise ValueError("Buffer must be list or string")

def to_md(buffer, title):
    if type(buffer) == str:
        filename = 'outputs/{}.md'.format(title)
        with open(filename, 'w') as file:
            file.write(buffer)
        return filename
    elif type(buffer) == list:
        i = 1
        filenames = []
        for item in buffer:
            filename = 'outputs/{}/{}.md'.format(title, i)
            if not os.path.exists('outputs/{}'.format(title)):
                os.makedirs('outputs/{}'.format(title))
            with open(filename, 'w') as file:
                file.write(item)
            i+=1
            filenames.append(filename)
        return filenames
    else:
        raise ValueError("Buffer must be list or string")

def from_csv(filename, delimiter="|"):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file, delimiter=delimiter)
        data = [row for row in reader]
    return data

def read_pdf(filename):
    if ".pdf" not in filename:
        filename+=".pdf"
    with open(filename, 'rb') as fp:
        doc = Document(fp)
    control = TextControl(mode = "physical")
    txt = []
    for page in doc:
        txt.append(page.text(control=control))
    return txt

def transcribe_audio(audiofile):
    audio_file= open(audiofile, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcriphw1t

def promptGPT(prompt, model=constants.model):
    response = openai.ChatCompletion.create(
      model=model,
      messages=[
        {"role": "user", "content": prompt}])
    return response["choices"][0]["message"]["content"]

def pdf_unordered_list(_dict, formatstyle=styles):
    _list = []
    list_items = []
    print(_dict)
    for item in _dict:
        for key,value in item.items():
            if key == None or value == None:
                print(f'<b>{key}</b>: <b>{value}</b>')
                pass
            if key == "" and value == "":
                print(f'<b>{key}</b>: <b>{value}</b>')
                pass
            if key == "-" or value == "-":
                print(f'<b>{key}</b>: <b>{value}</b>')
                pass
            else:
                list_items.append(ListItem(Paragraph(f'<b>{key}</b>: <b>{value}</b>', formatstyle['Normal'])))
    _list.append(ListFlowable(list_items, bulletType='bullet'))
    return _list

def pdf_paragraph(paragraph, formatstyle=styles):
    return Paragraph(paragraph, formatstyle['Justify'])

def pdf_subtitle(subtitle, formatstyle=styles):
    return Paragraph(subtitle, formatstyle['Sub Title'])

def pdf_title(title, formatstyle=styles):
    return Paragraph(title, formatstyle['Main Title'])

def default_pdf_doc(output_filename, pagesize=A4):
    doc = SimpleDocTemplate(output_filename, pagesize=A4)
    # Create a Frame to hold content
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
    # Create a custom PageTemplate with the onPage function
    page_template = PageTemplate(id='PageTemplate', frames=[frame],
            onPage=create_header_footer)
    # Add the custom PageTemplate to the SimpleDocTemplate
    doc.addPageTemplates([page_template])
    return doc

def create_header_footer(canvas, doc):
    # Set font, font size, and font color
    canvas.setFont("Helvetica", 10)
    canvas.setFillColor(colors.grey)
    page_width, page_height = A4
    username = os.getenv("OPENAI_USER")
    headernote = "{}".format(datetime.now().strftime("%m/%d/%Y"))
    print(username)
    text_width = canvas.stringWidth(username)
    
    # Calculate the x position for the right-aligned text
    page_width = letter[0]
    x = page_width - text_width - .75*cm
    y = doc.pagesize[1] - .35* cm
    canvas.drawString(x, y, username)
    canvas.drawString(page_width -  canvas.stringWidth(headernote) - .75*cm, y-.5*cm,
            headernote)

    # Draw a line
    canvas.setLineWidth(1)
    canvas.line(2 * cm, 1.5 * cm, page_width - 2 * cm, 1.5 * cm)
    # Page number
    page_number_text = f"Page {canvas.getPageNumber()}"
    y = 1 * cm
    x = page_width - 4 * cm
    canvas.drawString(x, y, page_number_text)

