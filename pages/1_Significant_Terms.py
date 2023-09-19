"""
# Significant Terms Demo

"""
import streamlit as st
import constellate
from collections import defaultdict
from pathlib import Path
import gensim

# Define a function that will process individual tokens
# Only a token that passes through all three `if` 
# statements will be returned. A `True` result for
# any `if` statement does not return the token. 

def process_token(token):
    token = token.lower()
    if len(token) < 4: # If True, do not return token
        return None
    if not(token.isalpha()): # If True, do not return token
        return None
    return token # If all are False, return the lowercased token

@st.cache_data(show_spinner="Finding significant terms...")
def find_significant_terms():
    documents = [] # A list that will contain all of our unigrams
    document_ids = [] # A list that will contain all of our document ids
    document_titles = [] # A list that will contain all of our titles

    for document in constellate.dataset_reader(dataset_file):
        processed_document = [] # Temporarily store the unigrams for this document
        document_id = document['id'] # Temporarily store the document id for this document
        document_title = document['title'] # Temporarily store the document title for this document
        unigrams = document.get("unigramCount", [])
        for gram, count in unigrams.items():
            clean_gram = process_token(gram)
            if clean_gram is None:
                continue
            processed_document += [clean_gram] * count # Add the unigram as many times as it was counted
        if len(processed_document) > 0:
            document_ids.append(document_id)
            document_titles.append(document_title)
            documents.append(processed_document)
    
    # Create Gensim dictionary
    dictionary = gensim.corpora.Dictionary(documents)

    # Create a bag of words corpus
    bow_corpus = [dictionary.doc2bow(document) for document in documents]

    # Create our gensim TF-IDF model
    model = gensim.models.TfidfModel(bow_corpus) 

    # Create TF-IDF scores for the ``bow_corpus`` using our model
    corpus_tfidf = model[bow_corpus]

    # For each document, print the ID, most significant/unique word, and TF/IDF score

    n = 0

    for n, doc in enumerate(corpus_tfidf):
        if len(doc) < 1:
            continue
        word_id, score = max(doc, key=lambda x: x[1])
        


        # st.write(document_titles[n], document_ids[n], dictionary.get(word_id), score)
        st.write(f'[{document_titles[n]}]({document_ids[n]})', dictionary.get(word_id), score)

        if n >= 10:
            break

st.markdown('# Significant Terms')

dataset_id = st.session_state['dataset_id']
info = constellate.get_description(dataset_id)

# # Check to see if a dataset file exists
# # If not, download a dataset using the Constellate Client
# # The default dataset is Shakespeare Quarterly, 1950-present
# dataset_id = "7e41317e-740f-e86a-4729-20dab492e925"
if 'search_description' in info:
    st.write(info['search_description'])
    st.write('1500 documents sample of ', str(info['num_documents']), ' documents.')
    st.divider()
    
    dataset_file = constellate.get_dataset(dataset_id)
    st.session_state['dataset_file'] = dataset_file

    find_significant_terms()
else:
    st.markdown('*Enter Dataset ID to visualize*')