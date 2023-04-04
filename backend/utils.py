import os
import json
import csv
from pyxpdf import Document, Page, Config
from pyxpdf.xpdf import TextControl

def to_csv(response, title):
    if type(response) == str:
        filename = 'outputs/{}.csv'.format(title)
        with open(filename, 'w') as file:
            file.write(response)
        return filename
    elif type(response) == list:
        i = 1
        filenames = []
        for item in response:
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

def from_csv(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
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
