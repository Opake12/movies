import streamlit as st
import pinecone
from sentence_transformers import SentenceTransformer
from tqdm.auto import tqdm
import requests

import configparser

### api auth
config = configparser.ConfigParser()
config.read('./.config/config.ini')

api_key = config['api_key']['auth']
environment = config['environment']['server']

# cache
@st.experimental_singleton
def init_retriever():
    """
    init SentenceTransformer
    """
    pass

@st.experimental_singleton
def init_pinecone():
    # initialize connection to pinecone (get api key app.pinecone.io)
    pinecone.init(
        api_key=api_key,
        environment=environment
    )

    # connect to the index
    pass


def card(id_val, title, context):
    return f"""
    <div class="card" style="margin:1rem;">
        <div class="card-body">
            <h5 class="card-title">{title}</h5>
            <h6 class="card-subtitle mb-2 text-muted">{id_val}</h6>
            <p class="card-text">{context}</p>
        </div>
    </div>
    """


st.markdown("""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
""", , unsafe_allow_html=True)

st.write("""

# Movie recommendation

Which Movie would you like to watch
""")

# call the functions
model = init_retriever()
index = init_pinecone()

query = st.text_input('Search', '')


# Make a request to the FastAPI endpoint to retrieve the data
response = requests.get(f"http://localhost:8000/data/{query}")
data = response.json()

