import os
import time
import json
import requests
import csv
import openai
import constants
import tiktoken
import pypdf
from datetime import datetime
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
from functools import partial


#PDF Style Sheet
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
styles.add(ParagraphStyle(name="Main Title",fontSize=36, leading=30, alignment=TA_CENTER, spaceAfter=20))
styles.add(ParagraphStyle(name="Sub Title",fontSize=20, leading=30, alignment=TA_CENTER, spaceAfter=20))

#Mathpix 
options = {
    "math_inline_delimiters": ["$", "$"],
    "rm_spaces": True
}
headers = {
        "app_id":  constants.mathpix_app_id,
        "app_key": constants.mathpix_api_key
}

def mathpix_post_local_file(filename,extension="", url="https://api.mathpix.com/v3/pdf"):
    pdf_id = requests.post(url,
            headers = headers,
            data={
            "options_json": json.dumps(options)
        },
        files={
            "file": open(filename+extension,"rb")
        }
    )
    pdf_id_text = json.loads(pdf_id.text.encode("utf8"))
    print(pdf_id_text)
    return pdf_id_text

def mathpix_pdf_to_mmd(filename, pdf_id=""):
    if pdf_id == "":
        pdf_id = mathpix_post_local_file(filename)['pdf_id']
    url = "https://api.mathpix.com/v3/pdf/" +pdf_id+ ".mmd"
    conversion_response = requests.get(url, headers=headers)
    while ('{"status":' in conversion_response.text):
        time.sleep(2)
        conversion_response = requests.get(url, headers=headers)
    final_converted_to_mmd = conversion_response.text
    with open(filename+".mmd","wb") as mathfile:
        mathfile.write(final_converted_to_mmd.encode("utf8"))
    return final_converted_to_mmd

def mathpix_img_to_txt(filename, img_id="", url="https://api.mathpix.com/v3/text"):
    img_id = mathpix_post_local_file(filename, extension=".png", url=url)
   # url = "https://api.mathpix.com/v3/ocr-results" +img_id+ ".mmd"
   # conversion_response = requests.get(url, headers=headers)
   # while ('{"status":' in conversion_response.text):
   #     time.sleep(2)
   #     conversion_response = requests.get(url, headers=headers)
   # final_converted_to_mmd = conversion_response.text
    print(img_id)
    with open(filename+".mmd","wb") as mathfile:
        mathfile.write(img_id.text)
    return img_id


def pandoc_pdf(_input, _output="", depth=1):
    print("running pandoc")
    def pandoc_error_handle(errormsg, depth=1):
        print("ERROR: Error with PDF format. Reformatting and trying again.")
        with open(_input, "r") as f:
            mmd = f.read()
        fixed = promptGPT("""Fix this markdown to ensure it can be converted to pdf by xelatex.
        The Error message is: {}, the document is below.""".format(errormsg), mmd,
        model="gpt-3.5-turbo")
        with open(_input, "w") as f:
            f.write(fixed)
        if depth < 3:
            pandoc_pdf(_input, _output, depth+1)
        else:
            return "PDF convert failed. Try again."

    if _output=="":
        command = "pandoc --pdf-engine=xelatex -s {}.md -o {}.pdf".format(_input, _input)
        output = os.system(command)
        if 'Error' in str(output):
            pandoc_error_handle(output, depth)
    else:
        command = "pandoc --pdf-engine=xelatex -s {}.md -o {}.pdf".format(_input, _output)
        output = os.system(command)
        if 'Error' in str(output):
            pandoc_error_handle(output, depth)

def to_md(buffer, title):
    if type(buffer) == str:
        filename = '{}.md'.format(title)
        with open(filename, 'w') as file:
            file.write(buffer)
        return filename
    elif type(buffer) == list:
        i = 1
        filenames = []
        for item in buffer:
            filename = '/{}/{}.md'.format(title, i)
            if not os.path.exists('/{}'.format(title)):
                os.makedirs('/{}'.format(title))
            with open(filename, 'w') as file:
                file.write(item)
            i+=1
            filenames.append(filename)
        return filenames
    else:
        raise ValueError("Buffer must be list or string")

def pdf_to_txt(_input, _output):
    if _input[-4] != ['.']:
        _input = _input+".pdf"
    if _output[-4] != ['.']:
        _output = _output+".txt"
    command = "pdftotext {} {}".format(_input, _output)
    print(os.system(command))

def to_csv(buffer, title):
    if type(buffer) == str:
        filename = '{}.csv'.format(title)
        with open(filename, 'w') as file:
            file.write(buffer)
        return filename
    elif type(buffer) == list:
        i = 1
        filenames = []
        for item in buffer:
            filename = '{}/{}.csv'.format(title, i)
            if not os.path.exists('{}'.format(title)):
                os.makedirs('{}'.format(title))
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
        filename += ".pdf"
    with open(filename, 'rb') as fp:
        reader = pypdf.PdfFileReader(fp)
        num_pages = reader.numPages
        txt = []
        for page_num in range(num_pages):
            page = reader.getPage(page_num)
            txt.append(page.extractText())
    return txt

def transcribe_audio(audiofile):
    audio_file= open(audiofile, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript

def num_tokens_from_messages(prompttext, model="gpt-3.5-turbo-0301"):
  """Returns the number of tokens used by a list of messages."""
  messages = [{"role":"user", "content":prompttext}]
  try:
      encoding = tiktoken.encoding_for_model(model)
  except KeyError:
      encoding = tiktoken.get_encoding("cl100k_base")
  if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
      num_tokens = 0
      for message in messages:
          num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
          for key, value in message.items():
              num_tokens += len(encoding.encode(value))
              if key == "name":  # if there's a name, the role is omitted
                  num_tokens += -1  # role is always required and always 1 token
      num_tokens += 2  # every reply is primed with <im_start>assistant
      return num_tokens
  else:
      raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
  See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")

def promptGPT_safe(messages, model="gpt-3.5-turbo-16k", function_call=None, functions=None):
    completion = 0
    i = 0
    while (completion == 0):
        completion = promptGPT(messages, function_call=function_call, functions=functions)
        if i == 30: #Arbitrarily chosen
            raise Exception("OpenAI Timeout Error.")
        i+=1
    return completion

def promptGPT(systemprompt, userprompt, model=constants.model, functions=None, function_call=None):
    """
    systemprompt: text
    userprompt: text
    functions: list of functions of form:
    {
        "name":,
        "description":,
        "parameters":{
                        "type":"object",
                        "properties": {"property name":{"type": "property type
                        (str,int,etc)","description":"description of property"}},
                        "required": [list of required properties by name]
                        }
    }
    function_call: {"name": "name of function from functions to call"}
    """
    print("""Inputting {} tokens into {}.""".format(num_tokens_from_messages(systemprompt+userprompt), model))
    if functions == None:
        response = openai.ChatCompletion.create(
          model=model,
          messages=[
            {"role": "system", "content": systemprompt},
            {"role": "user", "content": userprompt}])
        return response["choices"][0]["message"]["content"]
    else:
        response = openai.ChatCompletion.create(
          model=model,
          functions=functions,
          function_call=function_call,
          messages=[
            {"role": "system", "content": systemprompt},
            {"role": "user", "content": userprompt}])
        return str(response["choices"][0]["message"]["function_call"])

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

def default_pdf_doc(output_filename, fullname, pagesize=A4):
    doc = SimpleDocTemplate(output_filename, pagesize=pagesize)
    # Create a Frame to hold content
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
    # Create a custom PageTemplate with the onPage function
    page_template = PageTemplate(id='PageTemplate', frames=[frame],
            onPage=partial(create_header_footer, user_full_name=fullname))
    # Add the custom PageTemplate to the SimpleDocTemplate
    doc.addPageTemplates([page_template])
    return doc

def create_header_footer(canvas, doc, user_full_name):
    # Set font, font size, and font color
    canvas.setFont("Helvetica", 10)
    canvas.setFillColor(colors.grey)
    page_width, page_height = A4
    username = user_full_name#os.getenv("OPENAI_USER")
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

