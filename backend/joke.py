from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, validator
from typing import List
import os
import openai
import constants
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
from langchain.chat_models import ChatOpenAI
# Define your desired data structure.
class DomainName(BaseModel):
    domain: str = Field(description="Domain Name")
    extension: str = Field(description="Extension")

# And a query intented to prompt a language model to populate the data structure.
domain_query = """Come up with with an extremely fun and creative short AI assistant related
domain name using extension .io or .ai. The website is about helping students do their
homework."""

# Set up a parser + inject instructions into the prompt template.
parser = PydanticOutputParser(pydantic_object=DomainName)

prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

model_name = 'gpt-3.5-turbo'
temperature = 1.0
model = OpenAI(model_name=model_name, temperature=temperature)
_input = prompt.format_prompt(query=domain_query)
names = []
for i in range(25):
    output = model(_input.to_string())
    names.append(parser.parse(output))
    print(output)
