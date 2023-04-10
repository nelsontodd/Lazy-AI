import os
import utils
import csv
import constants
import openai
from io import StringIO, BytesIO
from xhtml2pdf import pisa
from PyPDF2 import PdfReader, PdfWriter
from reportlab.platypus import SimpleDocTemplate, Paragraph, ListFlowable, ListItem
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import markdown2
from xhtml2pdf import pisa
from io import StringIO, BytesIO


# Create a PDF from the HTML using ReportLab's pisa (HtmlToPdf)


if __name__ == '__main__':
    hwdir, inputhw = "hw/", "non_math_hw"
    hwpdf = utils.read_pdf(hwdir+inputhw)
    output_filename="outputs/{}.pdf".format(inputhw)
    doc = utils.default_pdf_doc("outputs/temp_qualitative_hw.pdf")
    _items = [utils.pdf_title("SLP Homework"), Spacer(1, 24)]
    i = 0
    hwresponse = ""
    for page in hwpdf:
        hwresponse += utils.promptGPT(constants.NON_MATH_HW, page, "gpt-4")
    utils.to_md(hwresponse, inputhw)
    utils.pandoc_pdf("outputs/{}".format(inputhw), "outputs/{}".format(inputhw))
    doc.build(_items)

    output_pdf = PdfWriter()
    reportlab_pdf = PdfReader("outputs/temp_qualitative_hw.pdf")
    pandoc_pdf = PdfReader("outputs/{}.pdf".format(inputhw))

    for page_num in range(len(reportlab_pdf.pages)):
        output_pdf.add_page(reportlab_pdf.pages[page_num])

    for page_num in range(len(pandoc_pdf.pages)):
        output_pdf.add_page(pandoc_pdf.pages[page_num])

    with open("outputs/{}.pdf".format(inputhw), "wb") as merged_file:
        output_pdf.write(merged_file)
    print('Notes file generated for file: {}'.format(inputhw))
