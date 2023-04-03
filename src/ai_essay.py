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

os.environ["SERPAPI_API_KEY"] = "ab9f6989f1bca1e2a64b472ac9e999fa8939cd291fa4673bb0a045476fe29277"
wikipedia = WikipediaAPIWrapper()
loader = TextLoader("bkk-case-analysis.txt")
def get_github_docs(repo_owner, repo_name):
    with tempfile.TemporaryDirectory() as d:
        subprocess.check_call(
            f"git clone --depth 1 https://github.com/{repo_owner}/{repo_name}.git .",
            cwd=d,
            shell=True,
        )
        git_sha = (
            subprocess.check_output("git rev-parse HEAD", shell=True, cwd=d)
            .decode("utf-8")
            .strip()
        )
        repo_path = pathlib.Path(d)
        markdown_files = list(repo_path.glob("*/*.md")) + list(
            repo_path.glob("*/*.mdx")
        )
        for markdown_file in markdown_files:
            with open(markdown_file, "r") as f:
                relative_path = markdown_file.relative_to(repo_path)
                github_url = f"https://github.com/{repo_owner}/{repo_name}/blob/{git_sha}/{relative_path}"
                yield Document(page_content=f.read(), metadata={"source": github_url})

sources = loader.load()#get_github_docs("yirenlu92", "deno-manual-forked")

source_chunks = []
splitter = CharacterTextSplitter(separator=" ", chunk_size=1024, chunk_overlap=0)
for source in sources:
    for chunk in splitter.split_text(source.page_content):
        source_chunks.append(Document(page_content=chunk, metadata=source.metadata))
search_index = Chroma.from_documents(source_chunks, OpenAIEmbeddings(model="text-embedding-ada-002"))

from langchain.chains import LLMChain

essay_prompt = """This case assignment will explore some of the challenges of taking a new
product to market. Your role in this case analysis is to develop your own perspective on
whether you would advocate to bring BKK to market, which of the three options are best,
and would BKK be successful. Your submitted analysis should detail your position. Write
a detailed and methodical introductory paragraph for an essay that will include three body
paragraphs of each at least three sentences. Make sure your introductory paragraph has a
topic sentence outlining the three paragraphs of your essay. Make your introduction paragraph a minimum of 100 words. Only respond with your introduction paragraph."""
prompt_template = """ You are a helpful essay writer with great knowledge of the
pharmaceutical industry and you only are able to write one paragraph responses. Use the context below.
    Context: {context}
    Prompt: {topic}
    Essay: """

essay_intro_prompt = PromptTemplate(
    template=prompt_template, input_variables=["context", "topic"]
)

llm = OpenAI(temperature=0, max_tokens=-1, )

chain = LLMChain(llm=llm, prompt=essay_intro_prompt)

def gen_introduction(topic):
    docs = search_index.similarity_search(topic, k=1)
    print(len(docs))
    inputs = [{"context": doc.page_content, "topic": topic} for doc in docs]
    return chain.apply(inputs)

with open("introduction.txt", 'w') as f:
    introduction = gen_introduction(essay_prompt)[0]["text"]
    f.write(introduction)

body_paragraph_template = """ You are a highly professional and helpful essay writer with
great knowledge of the pharmaceutical industry. Argue, in one paragraph, the first idea
stated in the introduction paragraph given below. Ensure your paragraph is 200 words minimum. Only write One paragraph.
    Context: {context}
    Introduction: {introduction}
    Essay: """
paragraph_1 = PromptTemplate(
    template=body_paragraph_template, input_variables=["context", "introduction"]
)
chain1 = LLMChain(llm=llm, prompt=paragraph_1)
def generate_body(topic):
    docs = search_index.similarity_search(topic, k=1)
    print(len(docs))
    inputs = [{"context": doc.page_content, "introduction": introduction} for doc in docs]
    return chain1.apply(inputs)

with open("body_1.txt", 'w') as f:
    body_1 = generate_body(introduction)[0]["text"]
    f.write(body_1)

body_paragraph_template = """ You are a highly professional and helpful essay writer with
great knowledge of the pharmaceutical industry. Argue, in one paragraph, the second idea
stated in the introduction paragraph given below. Ensure your paragraph is 200 words
minimum. Only write ONE paragraph or else you DIE.
    Context: {context}
    Introduction: {introduction}
    Essay: """
paragraph_2 = PromptTemplate(
    template=body_paragraph_template, input_variables=["context", "introduction"]
)
chain2 = LLMChain(llm=llm, prompt=paragraph_2)
def generate_body(topic):
    docs = search_index.similarity_search(topic, k=1)
    print(len(docs))
    inputs = [{"context": doc.page_content, "introduction": introduction} for doc in docs]
    return chain2.apply(inputs)

with open("body_2.txt", 'w') as f:
    body_2 = generate_body(introduction)[0]["text"]
    f.write(body_2)

body_paragraph_template = """ You are a highly professional and helpful essay writer with
great knowledge of the pharmaceutical industry. Argue, in one paragraph, the third idea
stated in the introduction paragraph given below. Ensure your paragraph is 200 words
minimum. Only write ONE paragraph or ELSE YOU WILL DIE.
    Context: {context}
    Introduction: {introduction}
    Essay: """
paragraph_3 = PromptTemplate(
    template=body_paragraph_template, input_variables=["context", "introduction"]
)
chain3 = LLMChain(llm=llm, prompt=paragraph_3)
def generate_body(topic):
    docs = search_index.similarity_search(topic, k=1)
    print(len(docs))
    inputs = [{"context": doc.page_content, "introduction": introduction} for doc in docs]
    return chain3.apply(inputs)

with open("body_3.txt", 'w') as f:
    body_3 = generate_body(introduction)[0]["text"]
    f.write(body_3)

conclusion_template = """ You are a highly professional and helpful essay writer with
great knowledge of the pharmaceutical industry. Given the introduction paragraph below,
Remember to make a recommendation. write the conclusion paragraph. Ensure your paragraph
is 200 words minimum. Only write One paragraph.
    Context: {context}
    Introduction: {introduction}
    Essay: """
paragraph_2 = PromptTemplate(
    template=body_paragraph_template, input_variables=["context", "introduction"]
)
chain = LLMChain(llm=llm, prompt=paragraph_2)
def generate_body(topic):
    docs = search_index.similarity_search(topic, k=1)
    print(len(docs))
    inputs = [{"context": doc.page_content, "introduction": introduction} for doc in docs]
    return chain.apply(inputs)

with open("conclusion.txt", 'w') as f:
    conclusion = generate_body(introduction)[0]["text"]
    f.write(conclusion)

with open("essay.txt", 'w') as f:
    f.write(introduction)
    f.write("\n")
    f.write(body_1)
    f.write("\n")
    f.write(body_2)
    f.write("\n")
    f.write(body_3)
    f.write("\n")
    f.write(conclusion)

essay = introduction + "\n" + body_1 + "\n" + body_2 + "\n" + body_3 + "\n" + conclusion
llm = OpenAI(model_name="gpt-4", max_tokens=-1)
intro_gpt = llm("""Rewrite this essay to be more professional and compelling. You are an
expert consultant and are making your arguments more clear. Don't just use big words, stress
logical coherence and creativity. Minimum 800 words. : {}""""".format(essay))
with open("essay-200-iq.txt", 'w') as f:
    f.write(intro_gpt)
