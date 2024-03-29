import os
from typing import List
import constants
import utils
import json
from pydantic_types import Route
from pypdf import PdfReader, PdfWriter
from reportlab.platypus import Spacer

class LazyAI:
    def __init__(self, input_doc, output_pdf, document_description, username,
            user_full_name, document_title="", latex=True, programming_language="",assignment_type="HOMEWORK",
            extension=".pdf"):
        self.document_description = document_description
        self.document_title = document_title
        self.username = username
        self.full_name = user_full_name

        self.input_doc = input_doc
        self.abs_path_input_doc = self.input_rel_path(input_doc)

        self.output_pdf = output_pdf
        self.abs_path_output_pdf = self.output_rel_path(output_pdf)
        self.abs_path_output = self.output_rel_path("")
        self.abs_path_input  = self.input_rel_path("")
        self.latex = latex
        self.assignment_type= assignment_type
        self.model="gpt-4-0613"
        self.solutions = None
        self.extension=extension
        self.programming_language = programming_language
        if self.programming_language != "":
            self.latex = False

    def output_rel_path(self, filename, extension=""):
        os.makedirs(constants.output_path+self.username, exist_ok=True)
        return constants.output_path+self.username+"/"+filename+extension

    def input_rel_path(self, filename, extension=""):
        os.makedirs(constants.input_path+self.username, exist_ok=True)
        return constants.input_path+self.username+"/"+filename+extension

    def extract_text_from_inputfile(self, doc_id=""):
        if (self.extension==".pdf") or (self.extension=="pdf"):
            if (self.latex == True):
                pdf_mmd = utils.mathpix_pdf_to_mmd(self.abs_path_input_doc, pdf_id=doc_id)
                return pdf_mmd
            else:
                text = utils.read_pdf(self.abs_path_input_doc)
                return text
        else:
            image_mmd = utils.mathpix_img_to_mmd(self.abs_path_input_doc, img_id=doc_id)
            return image_mmd

    def determine_prompt_from_description(self):
        if self.assignment_type == "HOMEWORK" or self.assignment_type == "EXAM":
            if self.programming_language != "":
                return constants.NON_MATH_HOMEWORK + """NOTE: This is a programming
            assignment! Output your code in {}""".format(self.programming_language)
            if self.latex == True:
                return constants.MATH_HOMEWORK
            else:
                return constants.NON_MATH_HOMEWORK
        else:
            if self.programming_language != "":
                return constants.NON_MATH_STUDYGUIDE + """NOTE: This is a programming
            assignment! Output your code in {}""".format(self.programming_language)
            if self.latex == True:
                return constants.MATH_STUDYGUIDE
            else:
                return constants.NON_MATH_STUDYGUIDE

    def build_pdf_page(self, _items, page_filename):
        doc = utils.default_pdf_doc(self.output_rel_path(page_filename,".pdf"),
                self.full_name)
        doc.build(_items)
        return page_filename

    def write_answers_to_pdf(self, text):
        answers_pdf = "{}_answers".format(self.input_doc)
        if self.latex == True:
            document_class = "exam"
            document = "document"
            solutions = """
    \documentclass[answers]{{{}}}
    \\usepackage{{amssymb}}
    \\usepackage{{amsmath}}
    \\usepackage[utf8]{{inputenc}}
    \\usepackage{{amsfonts}}
    \\usepackage{{bm}}
    \\usepackage{{esint}}
    \\usepackage{{siunitx}}

    \\title{{{}}}
    \\author{{{}}}

    \\begin{{document}}
    \\maketitle
    \\section{{Solutions}}
    \\begin{{questions}}
            """.format(document_class, self.document_title, self.full_name)
            solutions += utils.promptGPT([{'role':'system',
                'content':self.determine_prompt_from_description()},
                {'role':'user', 'content':text}], self.model)
            solutions+="""

    \\end{questions}
    \end{document}
            """
        else:
            solutions = """
---
header-includes:
 - \\usepackage{fvextra}
 - \\DefineVerbatimEnvironment{Highlighting}{Verbatim}{breaklines,commandchars=\\\\\\{\\}}
---
"""
            solutions += utils.promptGPT([{'role':'system',
                'content':self.determine_prompt_from_description()},
                {'role':'user', 'content':text}], self.model)
        self.solutions = solutions
        utils.to_md(solutions, self.output_rel_path(answers_pdf))
        if self.latex == True:
            utils.pdflatex(self.output_rel_path(answers_pdf), output_path=self.abs_path_output)
        else:
            utils.pandoc_pdf(self.output_rel_path(answers_pdf))
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
        titlepagename = self.build_pdf_page(_items, "{}_titlepage".format(self.input_doc))
        answersfilename = self.write_answers_to_pdf(self.extract_text_from_inputfile())
        print(f"Answers file name: {answersfilename}")
        self.merge(titlepagename, answersfilename)
        return self.abs_path_output_pdf

    def explain_solution(self):
        pass

    def determine_cost(self):
        """
        GPT-4 .03/1k token input .06/1k token output
        OCR image: .025/page
        1k tokens ~ 750 words
        """
        cost = .3 #Guess
        if ".pdf" in self.input_doc:
            with open(self.abs_path_input_doc, 'rb') as fp:
                reader = PdfReader(fp)
                num_pages = len(reader.pages)
            if self.latex == True: #Have to use OCR
                cost += num_pages*.05
            cost+=utils.num_tokens_from_messages([{'role':'system','content':str(utils.read_pdf(self.abs_path_input_doc))}])*.00006
            if cost > 3:
                raise Exception("Pdf too large for context limit.")
        else:
            cost = 1.50
        if cost < 1:
            cost = 1
        return cost

