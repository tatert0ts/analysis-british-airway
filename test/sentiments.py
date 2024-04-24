import pandas as pd
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import string

from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


import matplotlib.pyplot as plt

df = pd.read_csv(r'C:\Users\niyai\git\british-analysis\British_Airway_Review_cleaned.csv')

text = " ".join(review for review in df.cleaned_reviews)
text = text.translate(str.maketrans('', '', string.punctuation))

stop_words = set(STOPWORDS)
stop_words.update(['ba', 'flight', 'flights', 'british', 'airway', 'airways'])

# Tokenize the text into words and remove empty strings
cleaned_words = [word for word in text.split() if word.strip()]

# convert into lowercase
# checking words against stopwords
cleaned_words = [word.lower() for word in cleaned_words if word.lower() not in stop_words]

word_freq = pd.Series(cleaned_words).value_counts()

df_word_freq = word_freq.reset_index()
df_word_freq.columns = ['Word', 'Frequency']

# Plot the treemap
fig_word_tm = px.treemap(df_word_freq.head(50), path=['Word'], values='Frequency', title='Most Frequent Words')
