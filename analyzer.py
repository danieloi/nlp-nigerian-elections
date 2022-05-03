# INTERNAL DEPENDENCIES

# import json module for relating with json data
import json

# EXTERNAL DEPENDENCIES

# use MultinomialNB to classify new data
from sklearn.naive_bayes import MultinomialNB

# import functions for creating features dictionary and
# generating bag of words vector
from utils import create_features_dictionary, text_to_bow_vector, number_of_negative_tweets, number_of_positive_tweets, preprocess_text


# initialize the classifier
model = MultinomialNB()
print('Classifier initialized')

# with open('atiku-cleaned.json') as atiku_complete:
#     atiku_doc = json.load(atiku_complete)
# print("all tweets loaded")

with open('buhari-cleaned.json') as buhari_complete:
    buhari_doc = json.load(buhari_complete)
print("all tweets loaded")

# import classified tweets
with open('buhari-train.json') as buhari_train:
    buhari_training_doc = json.load(buhari_train)
print('training data loaded')

# import unclassified tweets
with open('buhari-unclassified.json') as buhari_unclassified:
    buhari_unclassified_doc = json.load(buhari_unclassified)

print('unclassified data loaded')

# generate training labels
training_labels = [tweet['sentiment'] for tweet in buhari_training_doc]

training_text = [tweet['text'] for tweet in buhari_training_doc]


unclassified_text = [tweet['text'] for tweet in buhari_unclassified_doc]

# create features dictionary with training
features_dictionary = create_features_dictionary(training_text)[0]
print('features dictionary created: ')
print(str(features_dictionary) + '\n')

# create training vector
training_vectors =  [text_to_bow_vector(text, features_dictionary)[0] for text in training_text]

# create vector for unclassified data
unclassified_vectors = [text_to_bow_vector(text, features_dictionary)[0] for text in unclassified_text]
print('training vectors created')

model.fit(training_vectors, training_labels)

predicted_labels = model.predict(unclassified_vectors)

total_tweets = len(buhari_doc)

positive = number_of_positive_tweets(predicted_labels)

negative = number_of_negative_tweets(predicted_labels)

print(total)

print(positive)

print(negative)