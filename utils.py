import re
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter

stop_words = stopwords.words('english')
normalizer = WordNetLemmatizer()


def preprocess_text(text):
  # remove urls
  # here's an explanation for the regex pattern:
  # (https?:\/\/) matches http:// or https://
  # (\s)* optional whitespaces
  # (www\.)? optionally matches www.
  # (\s)* optionally matches whitespaces
  # ((\w|\s)+\.)* matches 0 or more of one or more word characters followed by a period
  # ([\w\-\s]+\/)* matches 0 or more of one or more words(or a dash or a space) followed by '\'
  # ([\w\-]+) any remaining path at the end of the url followed by an optional ending
  # ((\?)?[\w\s]*=\s*[\w\%&]*)* matches ending query params (even with white spaces,etc)
  no_urls = re.sub(r'(https?:\/\/)(\s)*(www\.)?(\s)*((\w|\s)+\.)*([\w\-\s]+\/)*([\w\-]+)((\?)?[\w\s]*=\s*[\w\%&]*)*', ' ', text)

  # remove twitter handles from data
  no_handles = re.sub(r'@[\w]*', ' ', no_urls)

  # remove non-alphabetic characters
  cleaned = re.sub(r'\W+', ' ', no_handles).lower()

  # tokenize cleaned text
  tokenized = word_tokenize(cleaned)

  # lemmatize tokens
  # by default lemmatizer treats every word as a noun so we get the
  # actual part of speech with  the function 'get_part_of_speech" defined
  # below
  normalized = [normalizer.lemmatize(token, get_part_of_speech(token)) for token in tokenized]

  # remove stop words like 'is', 'are' etc. 
  filtered = [word for word in normalized if word not in stop_words]

  # return tokens 
  return filtered




# this function helps with the lemmatization process
# it uses nltk's part of speech tagging function to specify 
# what part of speech a word is so it knows how best to 
# reduce the word to it's base form. 
# We're able to normalize our data more accurately than a stemming algorithm. 
# Think a blunt axe versus a scalpel
def get_part_of_speech(word):
  probable_part_of_speech = wordnet.synsets(word)
  pos_counts = Counter()
  pos_counts["n"] = len(
      [item for item in probable_part_of_speech if item.pos() == "n"])
  pos_counts["v"] = len(
      [item for item in probable_part_of_speech if item.pos() == "v"])
  pos_counts["a"] = len(
      [item for item in probable_part_of_speech if item.pos() == "a"])
  pos_counts["r"] = len(
      [item for item in probable_part_of_speech if item.pos() == "r"])
  most_likely_part_of_speech = pos_counts.most_common(1)[0][0]
  return most_likely_part_of_speech

# this creates the features dictionary that is used to make
# our bag of words vectors for both our training data and 
# the data we'd like to classify
def create_features_dictionary(documents):
    features_dictionary = {}
    merged = " ".join(documents)
    tokens = preprocess_text(merged)
    index = 0
    for token in tokens:
        if token not in features_dictionary:
            features_dictionary[token] = index
            index += 1
    return features_dictionary, tokens

# this function creates our bag of words (bow) vector that 
# acts as the independent variable (x-axis) for our model
# when predicting data our labels form our output/dependent variable (y-axis)
def text_to_bow_vector(some_text, features_dictionary):
    bow_vector = len(features_dictionary) * [0]
    tokens = preprocess_text(some_text)

    for token in tokens:
        features_index = features_dictionary[token]
        bow_vector[features_index] += 1

    return bow_vector, tokens

    # after we run the predict function, we get a list of results that correspond to
# the different categories of sentiment.
# 0 is for neutral 
# -1 is for negative
# 1 is for positive 
# We want
# to collate the results to find how many are in each class
def number_of_positive_tweets(labels):
    counter = 0
    for result in labels: 
        if result == 1: 
            counter += 1
    return counter

# see comment for function "count_number_of_positive_tweets" above
def number_of_negative_tweets(labels):
    counter = 0
    for result in labels:
        if result == -1: 
            counter += 1
    return counter