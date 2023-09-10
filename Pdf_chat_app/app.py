#Requirements - langchain, streamlit, streamlit-extras, faiss-cpu, PyPDF, python-dotenv.
import os
from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
import pickle
from pydantic.v1 import *
from streamlit_extras.add_vertical_space import add_vertical_space
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

#Sidebar
with st.sidebar:
    st.title("Pdf Chat App")
    st.markdown('''
                ## About
               LLM pdf chat APP.
            - [Streamlit](https://streamlit.io/) is used to build this app.
            - [Langchain](https://python.langchain.com/) is used to build the LLM model.
            - [OpenAI](https://openai.com/) is used to build the GPT-3 model.
            ''')
    add_vertical_space(5)
    st.write("Made by ❤ [Adithya S Nair](https://github.com/ADITHYASNAIR2021)")
    st.write("Source code available at Github")


def main():
    st.header("Pdf Chat App")
    load_dotenv()  
    #Upload PDF file
    pdf = st.file_uploader("Upload a PDF file", type=["pdf"])
    if pdf is not None:
        st.write(pdf.name)
        pdf_reader = PdfReader(pdf)
        st.write(pdf_reader)
        
        text =""
        for page in pdf_reader.pages:
            text += page.extract_text()
            
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap  = 200,
            length_function = len,
            is_separator_regex = False,
            )
        chunks = text_splitter.split_text(text= text)
        
        #Embedding
        
        store_name = pdf.name[:-4]
        
        if os.path.exists(f"{store_name}.pkl"):
            with open(f"{store_name}.pkl", "rb") as f:
                VectorStore = pickle.load(f)
            st.write("Embeddings loaded")
        else:
            embeddings = OpenAIEmbeddings()
            VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
            with open(f"{store_name}.pkl", "wb") as f:
                pickle.dump(VectorStore, f)
        


if __name__ == '__main__':
    main()