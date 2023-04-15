#!/usr/bin/env python
import os
import time
import utils
import constants
from PyPDF2 import PdfReader, PdfWriter
from reportlab.platypus import SimpleDocTemplate, Paragraph, ListFlowable, ListItem
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


if __name__ == '__main__':
    hwdir, hw_file_name = "inputs/", "poorly_formatted_math"
    hw_mmd = utils.mathpix_pdf_to_mmd(hw_file_name, pdf_id="2023_04_10_88d52bf6ed7bb2cb3e1eg")
    solutions = utils.promptGPT(constants.MATH_HW, hw_mmd, "gpt-4")
    utils.to_md(solutions, hw_file_name)
    utils.pandoc_pdf(constants.output_path+hw_file_name,
            constants.output_path+"hw_answer_sheet_temp")
    print("Prompted gpt-4.")

    reportlab_temp_pdf=constants.output_path+"{}.pdf".format("hw_reportlab_temp")
    doc = utils.default_pdf_doc(reportlab_temp_pdf)
    _items = [utils.pdf_title("Calculus Homework"), Spacer(1, 24)]
    doc.build(_items)
    # Merge the ReportLab document and the Pandoc-generated PDF
    output_pdf = PdfWriter()
    reportlab_pdf = PdfReader(reportlab_temp_pdf)
    pandoc_pdf = PdfReader(constants.output_path+"{}.pdf".format("hw_answer_sheet_temp"))

    for page_num in range(len(reportlab_pdf.pages)):
        output_pdf.add_page(reportlab_pdf.pages[page_num])

    for page_num in range(len(pandoc_pdf.pages)):
        output_pdf.add_page(pandoc_pdf.pages[page_num])

    with open(constants.output_path+"{}.pdf".format(hw_file_name), "wb") as merged_file:
        output_pdf.write(merged_file)

    print('Answer key generated for file: {}'.format(hw_file_name))
