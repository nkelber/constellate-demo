"""
# Word Frequencies Demo

"""

import streamlit as st
import numpy as np
import pandas as pd

# Import modules and libraries
import constellate
import pandas as pd
from pathlib import Path
import csv
from collections import Counter

# For making wordclouds
from wordcloud import WordCloud
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from PIL import Image
import urllib.request

def gather_unigrams():
    word_freq = Counter()
    for document in constellate.dataset_reader(dataset_file):
        unigrams = document.get("unigramCount", [])
        for gram, count in unigrams.items():
            clean_gram = gram.lower()
            if clean_gram in stop_words:
                continue
            if not clean_gram.isalpha():
                continue
            if len(clean_gram) < 4:
                continue
            word_freq[clean_gram] += count
            return word_freq
        
# Load the NLTK stopwords list
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
stop_words = stopwords.words('english')

st.markdown('# Exploring Word Frequencies')

dataset_id = st.text_input('Constellate Dataset ID')
info = constellate.get_description(dataset_id)

# # Check to see if a dataset file exists
# # If not, download a dataset using the Constellate Client
# # The default dataset is Shakespeare Quarterly, 1950-present
# dataset_id = "7e41317e-740f-e86a-4729-20dab492e925"
if 'search_description' in info:
    st.write(info['search_description'])
    st.write('1500 documents sample of ', str(info['num_documents']), ' documents.')
    st.divider()
    with st.spinner(text='Downloading...'):
        dataset_file = constellate.get_dataset(dataset_id)
    
    
    word_frequency = Counter()
    with st.spinner(text='Counting words...'):
        for document in constellate.dataset_reader(dataset_file):
            unigrams = document.get("unigramCount", [])
            for gram, count in unigrams.items():
                clean_gram = gram.lower()
                if clean_gram in stop_words:
                    continue
                if not clean_gram.isalpha():
                    continue
                if len(clean_gram) < 4:
                    continue
                word_frequency[clean_gram] += count
    
    st.markdown(' ## Most Common Words')
    for gram, count in word_frequency.most_common(10):
        st.write(gram.ljust(20), count)
    else:
        pass
    st.markdown('## Wordcloud')

    ### Download cloud image for our word cloud shape ###
    # It is not required to have a shape to create a word cloud
    download_url = 'https://ithaka-labs.s3.amazonaws.com/static-files/images/tdm/tdmdocs/sample_cloud.png'
    urllib.request.urlretrieve(download_url, 'sample_cloud.png')

    # Create a wordcloud from our data

    # Adding a mask shape of a cloud to your word cloud
    # By default, the shape will be a rectangle
    # You can specify any shape you like based on an image file
    cloud_mask = np.array(Image.open('sample_cloud.png'))  # Specifies the location of the mask shape
    cloud_mask = np.where(cloud_mask > 3, 255,
                        cloud_mask)  # this line will take all values greater than 3 and make them 255 (white)

    ### Specify word cloud details
    wordcloud = WordCloud(
        width=800,  # Change the pixel width of the image if blurry
        height=600,  # Change the pixel height of the image if blurry
        background_color="white",  # Change the background color
        colormap='viridis',  # The colors of the words, see https://matplotlib.org/stable/tutorials/colors/colormaps.html
        max_words=150,  # Change the max number of words shown
        min_font_size=4,  # Do not show small text

        # Add a shape and outline (known as a mask) to your wordcloud
        contour_color='blue',  # The outline color of your mask shape
        mask=cloud_mask,  #
        contour_width=1
    ).generate_from_frequencies(word_frequency)

    mpl.rcParams['figure.figsize'] = (20, 20)  # Change the image size displayed
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.pyplot(plt.gcf())
else:
    pass



