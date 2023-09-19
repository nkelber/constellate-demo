"""
# NER

"""
import streamlit as st
from transformers import pipeline, set_seed
import pandas as pd

st.markdown('# Named Entity Recognition')
# Named Entity Recognition Pipeline
ner_tagger = pipeline("ner", aggregation_strategy="simple")


given_prompt = st.text_area('Enter text here', 
                             value='The United States of America includes Michigan, Hawaii, and Guam. The current president is Joe Biden. Mickey Mouse and Captain Planet are fictional characters. $100 was deposited in the Swiss bank account.',
                             max_chars=500
                             )

@st.cache_data(show_spinner="Finding entities...")
def extract_entities(prompt):
    output = ner_tagger(prompt)
    return pd.DataFrame(output)

output = extract_entities(given_prompt)

st.write(output)


