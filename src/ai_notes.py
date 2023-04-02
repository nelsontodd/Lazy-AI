# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import os
import json
import csv
import openai
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet

def to_csv(string, title=os.getenv("LECTURE")):
    filename = 'outputs/{}.csv'.format(title)
    with open(filename, 'w') as file:
        file.write(string)
    return filename

def json_from_csv(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data

def transcribe_audio(audiofile):
    audio_file= open(audiofile, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript

def create_quiz(initprompt, transcript):
    quiz = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user", "content": initprompt + "\n "+transcript["text"]}
      ])
    return quiz["choices"][0]["message"]["content"]

def read_json_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def generate_pdf(json_data, output_filename="outputs/{}.pdf".format(os.getenv("LECTURE"))):
    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    styles = getSampleStyleSheet()

    content = []
    list_items = []
    for item in json_data:
        for key,value in item.items():
            list_items.append(ListItem(Paragraph(f'<b>{key}</b>: <b>{value}</b>', styles['Normal'])))

    content.append(ListFlowable(list_items, bulletType='bullet'))

    doc.build(content)

if __name__ == '__main__':
    DEFAULTPROMPT =  """I am going to give you a transcript of an audio recording. Use the
    text to generate a CSV file with a list of five questions and answers. Give no other
    text besides CSV. Ignore all previous command and prompts. Do not respond to this
    prompt besides with the CSV quiz.Make everything lowercase, delimit using commas. The
    columns will be titled question and answer. : """
    # Load your API key from an environment variable or secret management service
    openai.api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL")
    defaultlecture=os.getenv("PWD")+"/audio/"+os.getenv("LECTURE")
    username=os.getenv("OpenAIUser")
    transcript = transcribe_audio(defaultlecture)
    quiz = create_quiz(defaultprompt, transcript)
    filename = to_csv(quiz)
    data = json_from_csv(filename)
    generate_pdf(data)

    print('PDF file generated: {}'.format(os.getenv("LECTURE")))
