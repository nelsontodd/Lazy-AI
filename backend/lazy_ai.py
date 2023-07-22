import os
from typing import List
import constants
import utils
import json
from pydantic_types import Route
from pypdf import PdfReader, PdfWriter
from reportlab.platypus import Spacer

class LazyAI:
    def __init__(self, input_pdf, output_pdf, document_description, username,
            user_full_name, document_title="", latex=True):
        self.document_description = document_description
        self.document_title = document_title
        self.username = username
        self.full_name = user_full_name

        self.input_pdf = input_pdf
        self.abs_path_input_pdf = self.input_rel_path(input_pdf)

        self.output_pdf = output_pdf
        self.abs_path_output_pdf = self.output_rel_path(output_pdf)
        self.latex = latex
        self.model="gpt-4-0613"

    def output_rel_path(self, filename, extension=""):
        os.makedirs(constants.output_path+self.username, exist_ok=True)
        return constants.output_path+self.username+"/"+filename+extension

    def input_rel_path(self, filename, extension=""):
        os.makedirs(constants.input_path+self.username, exist_ok=True)
        return constants.input_path+self.username+"/"+filename+extension

    def extract_text_from_pdf(self, pdf_id=""):
        if self.latex == True:
            pdf_mmd = utils.mathpix_pdf_to_mmd(self.abs_path_input_pdf, pdf_id=pdf_id)
            return pdf_mmd
        else:
            text = utils.read_pdf(self.abs_path_input_pdf)
            return text

    def determine_prompt_from_description(self):
        descrip_JSON = json.loads(utils.promptGPT(constants.PARSE_USER_DESCRIPTION_SYSTEM_PROMPT, self.document_description,function_call={"name":Route.openai_schema["name"]}, functions=[Route.openai_schema]))
        descrip_JSON['arguments'] = json.loads(descrip_JSON['arguments'])
        if descrip_JSON["arguments"]["LATEX"] == False:
            self.Latex = False
        return constants.prompts[descrip_JSON["arguments"]["TYPE"]]

    def build_pdf_page(self, _items, page_filename):
        doc = utils.default_pdf_doc(self.output_rel_path(page_filename,".pdf"),
                self.full_name)
        doc.build(_items)
        return page_filename

    def write_answers_to_pdf(self, text):
        answers_pdf = "{}_answers".format(self.input_pdf)
        solutions = utils.promptGPT(self.determine_prompt_from_description(),
                text, self.model)
        utils.to_md(solutions, self.output_rel_path(answers_pdf))
        utils.pandoc_pdf(self.output_rel_path(answers_pdf),
                self.output_rel_path(answers_pdf))
        return answers_pdf

    def merge(self, reportlabfile, answersfile):
        output_pdf = PdfWriter()
        reportlab_pdf = PdfReader(self.output_rel_path(reportlabfile) + ".pdf")
        pandoc_pdf = PdfReader(self.output_rel_path(answersfile) + ".pdf")
        for page_num in range(len(reportlab_pdf.pages)):
            output_pdf.add_page(reportlab_pdf.pages[page_num])
        for page_num in range(len(pandoc_pdf.pages)):
            output_pdf.add_page(pandoc_pdf.pages[page_num])
        with open(self.abs_path_output_pdf+".pdf", "wb") as merged_file:
            output_pdf.write(merged_file)

    def solutions_pdf(self) -> str:
        _items = [utils.pdf_title(self.document_title), Spacer(1, 24)]
        titlepagename = self.build_pdf_page(_items, "{}_titlepage".format(self.input_pdf))
        answersfilename = self.write_answers_to_pdf(self.extract_text_from_pdf())
        self.merge(titlepagename, answersfilename)
        return self.abs_path_output_pdf
