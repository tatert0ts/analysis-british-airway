import pandas as pd
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import string
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

df = pd.read_csv('data\British_Airway_Review_cleaned.csv')

stop_words = set(STOPWORDS)
stop_words.update(['ba', 'flight', 'flights', 'british', 'airway', 'airways'])

def extractwords(df):
    # into a single string text, with each review separated by a space
    text = " ".join(review for review in df.cleaned_reviews)
    # remove all punctuation characters from the text
    text = text.translate(str.maketrans('', '', string.punctuation))
    # removing any extra whitespace and ensuring that the list only contains non-empty words
    cleaned_words = [word for word in text.split() if word.strip()]
    # convert into lowercase
    # checking words against stopwords
    cleaned_words = [word.lower() for word in cleaned_words if word.lower() not in stop_words]
    word_freq = pd.Series(cleaned_words).value_counts()
    df_word_freq = word_freq.reset_index()
    df_word_freq.columns = ['Word', 'Frequency']
    return df_word_freq

df_yes = pd.DataFrame(df[df['recommended'] == 'Yes']['cleaned_reviews'])
df_no = pd.DataFrame(df[df['recommended'] == 'No']['cleaned_reviews'])

df_concatenated = pd.concat([extractwords(df_yes), extractwords(df_no)], keys=['Yes', 'No'])
df_concatenated['Reccomended'] = df_concatenated.index.get_level_values(0)
df_concatenated = df_concatenated.reset_index(drop=True) # remove keys

topwords = extractwords(df).head(50).Word 
df_topwords = df_concatenated[df_concatenated['Word'].isin(topwords.values)]

# Plot the treemap
fig_wr = px.treemap(df_topwords, path=['Word', 'Reccomended']
                 , values='Frequency', title='Most Frequent Words')
fig_wr.update_layout(title_x = 0.5, 
                  margin = dict(l = 50, r = 40, t = 50, b = 30)
                  )

# Plot the treemap
fig_rw = px.treemap(df_topwords, path=['Reccomended','Word']
                 , values='Frequency', title='Most Frequent Words',
                 color = 'Reccomended',
                 color_discrete_map={'No':'red', 'Yes':'green'})
fig_rw.update_layout(title_x = 0.5, 
                  margin = dict(l = 50, r = 40, t = 50, b = 30)
                  )


# word cloud
# fig_wc = WordCloud(background_color='white',max_words=100,max_font_size=300,width=1600,height=800, stopwords=stop_words)
# fig_wc.generate(" ".join(cleaned_words))
# plt.imshow(fig_wc)
# plt.tight_layout()
# plt.axis('off')