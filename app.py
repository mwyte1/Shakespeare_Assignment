import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import glob, nltk, os, re
from nltk.corpus import stopwords 
from nltk import FreqDist
nltk.download('stopwords')
nltk.download('punkt')

st.markdown('''
# Analyzing Shakespeare Texts
''')

# Create a dictionary (not a list)
books = {" ":" ","A Mid Summer Night's Dream":"data/summer.txt","The Merchant of Venice":"data/merchant.txt","Romeo and Juliet":"data/romeo.txt"}

# Sidebar
st.sidebar.header('Word Cloud Settings')
max_word = st.sidebar.slider("Max Words",min_value=10, max_value=200, value=100, step=10)
size_of_largest_word = st.sidebar.slider("Size of Largest Word", min_value=50, max_value=350, value=200, step=10)
image_width = st.sidebar.slider("Image Width", min_value=100, max_value=800, value=450, step=10)
random_state = st.sidebar.slider("Random State", min_value=20, max_value=100, value=60, step=2)
remove_stop_words = st.sidebar.checkbox("Remove Stop Words?",value=True)
st.sidebar.header('Word Count Settings')
min_count_of_words = st.sidebar.slider("Minimum Count of Words", min_value=5, max_value=100, value=48, step=5)

## Select text files
image = st.selectbox("Choose a text file", books.keys())

## Get the data file from folder by asking Python to 'get' the selected title.
image = books.get(image)

if image != " ":
    #Create stop_words variable
    stop_words = []
    #open(file, "r") asks Python to open the file for reading
    #open().read() asks Python to actually read the file
    #.lower() justs asks that Python return all of the items in lowercase form
    raw_text = open(image,"r").read().lower()
    #list of english stopwords; nltk_stop_words is the list of stop words
    nltk_stop_words = stopwords.words('english')

    if remove_stop_words:
        #Convert any of the iterable terms to a sequence of iterable elements with distinct elements
        stop_words = set(nltk_stop_words)
        #Inserts specified items into the dictionary
        stop_words.update(['us', 'one', 'though','will', 'said', 'now', 'well', 'man', 'may',
        'little', 'say', 'must', 'way', 'long', 'yet', 'mean',
        'put', 'seem', 'asked', 'made', 'half', 'much',
        'certainly', 'might', 'came','thou'])
        # These are all lowercase
    #converts the words in word_tokens to lower case and then checks whether they are present in stop_words or not
    #aka create a new list without the stop_words
    tokens = nltk.word_tokenize(raw_text)
    #Removes lower case conversion
    filtered_text = [t for t in tokens if not t.lower() in stop_words]
    filtered_text = []
    for t in tokens:
        if t not in stop_words:
            filtered_text.append(t)



tab1, tab2, tab3 = st.tabs(['Word Cloud', 'Bar Chart', 'View Text'])

with tab1:
    if image != " ":
        def create_wordcloud(raw_text):
            wordcloud = WordCloud(max_words=max_word,
                                  max_font_size=size_of_largest_word, 
                                  width=image_width,
                                  random_state=random_state,
                                  stopwords=stop_words
                                  ).generate(raw_text)
            return wordcloud
        wordcloud = create_wordcloud(raw_text)
        fig, ax = plt.subplots(figsize = (12, 8))
        ax.imshow(wordcloud)
        plt.axis("off")
        st.pyplot(fig)

    else:
        st.write(" ")

with tab2:
    if image != " ":
       freqdist = nltk.FreqDist(filtered_text)
       freqdist = pd.DataFrame(list(freqdist.items()), columns=['Word', 'Count'])
       freqdist = freqdist[freqdist['Count']>=min_count_of_words]
       bar = alt.Chart(freqdist).mark_bar().encode(
           x=alt.X('Count', axis=alt.Axis(title="count")),
           y=alt.Y('Word', axis=alt.Axis(title="word"))    
       ).properties(
           width=image_width,
           height=400
       )
       st.altair_chart(bar, use_container_width=True)
    else:
        st.write(" ")

with tab3:
    if image != " ":
        raw_text = open(image,"r").read().lower()
        st.write(raw_text)
