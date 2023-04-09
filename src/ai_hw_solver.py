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
    hwdir, inputhw = "hw/", "hw1"
    hwpages = utils.read_pdf(hwdir+inputhw)
    output_filename="outputs/{}.pdf".format(inputhw)
    doc = utils.default_pdf_doc(output_filename)
    _items = [utils.pdf_title("Calculus Homework"), Spacer(1, 24)]
    i = 0
    for page in hwpages:
        i+=1
        hwresponse = utils.promptGPT(constants.DEFAULT_HW_PROMPT + page)
        formatted = utils.promptGPT("""Format all of the mathematical
        expressions in the following text with proper LATEX inline. Maintain the same
        markdown structure as before. {} :""".format(constants.MARKDOWN_INSTRUCTIONS) + hwresponse)
        print(formatted)
        utils.to_md(formatted, "{}_page_{}".format(inputhw,i))
        utils.pandoc_pdf("outputs/{}_page_{}".format(inputhw,i), "outputs/{}_page_{}".format(inputhw,i))
    doc.build(_items)
    print(i)
    # Merge the ReportLab document and the Pandoc-generated PDF
    output_pdf = PdfWriter()
    reportlab_pdf = PdfReader(output_filename)
    pandoc_pdf = PdfReader("outputs/{}_page_{}.pdf".format(inputhw,i))

    for page_num in range(len(reportlab_pdf.pages)):
        output_pdf.add_page(reportlab_pdf.pages[page_num])

    for page_num in range(len(pandoc_pdf.pages)):
        output_pdf.add_page(pandoc_pdf.pages[page_num])

    with open("outputs/{}.pdf".format(inputhw), "wb") as merged_file:
        output_pdf.write(merged_file)
    print('Notes file generated for file: {}'.format(inputhw))
