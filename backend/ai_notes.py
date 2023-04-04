# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import os
import openai
from utils import to_csv, from_csv
import constants
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet

def transcribe_audio(audiofile):
    audio_file= open(audiofile, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript

def create_quiz(initprompt, transcript):
    quiz = openai.ChatCompletion.create(
      model=constants.model,
      messages=[
        {"role": "user", "content": initprompt + "\n "+transcript["text"]}
      ])
    return quiz["choices"][0]["message"]["content"]

def generate_pdf(quiz_dict, output_filename="outputs/{}.pdf".format(os.getenv("LECTURE"))):
    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    styles = getSampleStyleSheet()

    content = []
    list_items = []
    for item in quiz_dict:
        for key,value in item.items():
            list_items.append(ListItem(Paragraph(f'<b>{key}</b>: <b>{value}</b>', styles['Normal'])))

    content.append(ListFlowable(list_items, bulletType='bullet'))

    doc.build(content)

if __name__ == '__main__':
    # Load your API key from an environment variable or secret management service
    defaultlecture=os.getenv("PWD")+"/audio/"+os.getenv("LECTURE")
    transcript = transcribe_audio(defaultlecture)
    quiz = create_quiz(constants.DEFAULT_QUIZ_PROMPT, transcript)
    filename = to_csv(quiz, os.getenv("LECTURE"))
    data = from_csv(filename)
    generate_pdf(data)
    print('PDF file generated: {}'.format(os.getenv("LECTURE")))
