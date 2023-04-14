import os
import openai
import constants
import utils
from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
from langchain.indexes import VectorstoreIndexCreator
from langchain.utilities import WikipediaAPIWrapper
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.llms import OpenAI
from langchain.docstore.document import Document
import requests
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import PromptTemplate
import pathlib
import subprocess
import tempfile
from reportlab.pdfgen import canvas
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

os.environ["SERPAPI_API_KEY"] = "ab9f6989f1bca1e2a64b472ac9e999fa8939cd291fa4673bb0a045476fe29277"
wikipedia = WikipediaAPIWrapper()
loader = TextLoader("bkk-case-analysis.txt")

sources = loader.load()#get_github_docs("yirenlu92", "deno-manual-forked")

source_chunks = []
splitter = CharacterTextSplitter(separator=" ", chunk_size=1024, chunk_overlap=0)
for source in sources:
    for chunk in splitter.split_text(source.page_content):
        source_chunks.append(Document(page_content=chunk, metadata=source.metadata))
search_index = Chroma.from_documents(source_chunks, OpenAIEmbeddings(model="text-embedding-ada-002"))

llm = OpenAI(temperature=0, max_tokens=-1, )

essay_prompt = """This case assignment will explore some of the challenges of taking a new
product to market. Your role in this case analysis is to develop your own perspective on
whether you would advocate to bring BKK to market, which of the three options are best,
and would BKK be successful. Your submitted analysis should detail your position. """

essay_intro_prompt = PromptTemplate(
    template=constants.ARGUMENTATIVE_ESSAY_INTRO_PARAGRAPH_YAML, input_variables=[ "prompt", "context"]
)

body_paragraph = PromptTemplate(
    template=constants.ARGUMENTATIVE_ESSAY_BODY_PARAGRAPH_YAML, input_variables=["order",       "thesis","context"]
)
conclusion_paragraph = PromptTemplate(template=constants.ARGUMENTATIVE_ESSAY_CONCLUSION_YAML,
        input_variables=["thesis", "context"])

intro_chain = LLMChain(llm=llm, prompt=essay_intro_prompt)
body_chain = LLMChain(llm=llm, prompt=body_paragraph)
conclusion_chain = LLMChain(llm=llm, prompt=conclusion_paragraph)

def gen_introduction(prompt):
    docs = search_index.similarity_search(prompt, k=1)
    inputs = [{"context": doc.page_content, "prompt": prompt} for doc in docs]
    return intro_chain.apply(inputs)

def gen_body(order, thesis):
    docs = search_index.similarity_search(thesis, k=1)
    inputs = [{"order": order, "thesis": thesis, "context": doc.page_content} for doc in docs]
    return body_chain.apply(inputs)

def gen_conclusion(thesis):
    docs = search_index.similarity_search(thesis, k=1)
    inputs = [{"thesis": thesis, "context": doc.page_content} for doc in docs]
    return conclusion_chain.apply(inputs)

introduction = gen_introduction(essay_prompt)[0]["text"]
thesis = utils.promptGPT(constants.EXTRACT_TOPIC_SENTENCE, introduction)
print(thesis)
with open("essay.txt", 'w') as f:
    f.write(introduction)
    f.write("\n")
    f.write(gen_body("1", thesis)[0]["text"])
    f.write("\n")
    f.write(gen_body("2", thesis)[0]["text"])
    f.write("\n")
    f.write(gen_body("3", thesis)[0]["text"])
    f.write("\n")
    f.write(gen_conclusion(thesis)[0]["text"])
