# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import os
from io import StringIO
import openai
import csv
import utils
import constants
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER


if __name__ == '__main__':
    # Load your API key from an environment variable or secret management service
    defaultlecture=os.getenv("PWD")+"/audio/"+os.getenv("LECTURE")
    transcript = utils.transcribe_audio(defaultlecture)
    output_filename="outputs/{}.pdf".format(os.getenv("LECTURE"))
    doquiz = True
    dosummary= True
    doc = utils.default_pdf_doc(output_filename)
    _items = [utils.pdf_title("Zoom Meeting Summary"), Spacer(1, 24)]

    if dosummary == True:
        summaryresponse = utils.promptGPT(constants.DEFAULT_SUMMARY_PROMPT+ "\n "+transcript["text"])
        _items.append(utils.pdf_subtitle("Executive Summary"))
        _items.append(Spacer(1, 24))
        _items.append(utils.pdf_paragraph(summaryresponse))
        _items.append(Spacer(1, 24))
    if doquiz == True:
        quizresponse = utils.promptGPT(constants.DEFAULT_QUIZ_PROMPT+ "\n "+transcript["text"])
        quizdict = csv.DictReader(StringIO(quizresponse), delimiter="|")
        _items.append(utils.pdf_subtitle("Short Quiz"))
        _items.append(Spacer(1, 24))
        _items += utils.pdf_unordered_list(quizdict)
        _items.append(Spacer(1, 24))
    doc.build(_items)

    print('Notes file generated for file: {}'.format(os.getenv("LECTURE")))
