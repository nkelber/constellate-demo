from transformers import pipeline, set_seed
import gensim
import gensim.downloader
import streamlit as st

st.markdown('# Word Embeddings')
st.write('''
Use pretrained word embeddings to find similar words.
Pre-trained vectors based on Wikipedia 2014 + Gigaword, 5.6B tokens, 400K vocab, uncased (https://nlp.stanford.edu/projects/glove/)
         ''')


@st.cache_data(show_spinner="Loading embeddings...")
def load_embeddings():
        model = gensim.downloader.load('glove-wiki-gigaword-100')
        return model

# Find the most similar words to a given word
trained_model = load_embeddings()
st.write('Use word vectors to find the most similar word')
sim_word = st.text_input('Choose a word')
if sim_word:
    try:
        words = trained_model.most_similar(sim_word)
        for word, score in words:
            st.write(word, score)
    except:
        st.write('Word not found.')

