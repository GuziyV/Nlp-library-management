
import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import pandas as pd 
from sklearn.ensemble import RandomForestClassifier
from enum import Enum
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

class Command(Enum):
    AddBook = 1
    RemoveBook = 2
    AddComment = 3
    MyName = 4

def getCommand(text):
    training_set = [
        ["Hello, can you add a book", Command.AddBook.name],
        ["Add a book", Command.AddBook.name],
        ["Put a book", Command.AddBook.name],
        ["Please add a book", Command.AddBook.name],
        ["Add the book", Command.AddBook.name],
        ["Attach a book", Command.AddBook.name],

        ["Hello, can you remove a book", Command.RemoveBook.name],
        ["remove book", Command.RemoveBook.name],
        ["delete book", Command.RemoveBook.name],
        ["Please remove a book", Command.RemoveBook.name],
        ["Drop the book", Command.RemoveBook.name],
        ["Take out book", Command.RemoveBook.name],
        ["Pull out book", Command.RemoveBook.name],

        ["Add comment", Command.AddComment.name],
        ["Attach comment", Command.AddComment.name],
        ["Leave comment", Command.AddComment.name],
        ["Post comment", Command.AddComment.name],
        ["Drop a line about a book", Command.AddComment.name],
        ["Add remark", Command.AddComment.name],
        ["Comment", Command.AddComment.name],
        [text, "dummy"]
    ]

    training_set = pd.DataFrame(training_set, columns=['feature', 'label'])

    # Remove all redundant characters from the training set.
    def clean_up_training_set(trainingSet):
        processed_features = []
        for sentence in range(0, len(trainingSet)):
            # Remove all the special characters
            processed_feature = re.sub(r'\W', ' ', str(trainingSet[sentence]))

            # remove all single characters
            processed_feature= re.sub(r'\s+[a-zA-Z]\s+', ' ', processed_feature)

            # Remove single characters from the start
            processed_feature = re.sub(r'\^[a-zA-Z]\s+', ' ', processed_feature) 

            # Substituting multiple spaces with single space
            processed_feature = re.sub(r'\s+', ' ', processed_feature, flags=re.I)

            # Removing prefixed 'b'
            processed_feature = re.sub(r'^b\s+', '', processed_feature)

            # Converting to Lowercase
            processed_feature = processed_feature.lower()

            processed_features.append(processed_feature)

        return processed_features

    features = training_set.iloc[:, 0].values
    labels = training_set.iloc[:, 1].values

    cleaned_up_training_set = clean_up_training_set(features)

    vectorizer = TfidfVectorizer (max_features=1000, stop_words=stopwords.words('english'))
    processed_features = vectorizer.fit_transform(cleaned_up_training_set).toarray()

    X_train, X_test, y_train, y_test = train_test_split(processed_features[:-1], labels[:-1], test_size=0.2, random_state=0)

    text_classifier = RandomForestClassifier(n_estimators=30, random_state=0)
    text_classifier.fit(X_train, y_train)

    predictions = text_classifier.predict([processed_features[-1]])

    return predictions[0]






