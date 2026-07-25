import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


lemmatizer = WordNetLemmatizer()

stop_words = set(stopwords.words("english"))


def preprocess_nlp(text):
    """
    Performs NLP preprocessing on cleaned text.
    """

    # Tokenization
    tokens = word_tokenize(text)

    # Lowercase
    tokens = [word.lower() for word in tokens]

    # Remove stopwords
    tokens = [word for word in tokens if word not in stop_words]

    # Remove short words
    tokens = [word for word in tokens if len(word) > 2]

    # Lemmatization
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    return tokens