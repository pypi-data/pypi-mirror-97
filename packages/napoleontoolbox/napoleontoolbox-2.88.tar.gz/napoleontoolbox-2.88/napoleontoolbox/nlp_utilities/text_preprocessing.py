import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
import itertools


def sentence_tokenizer(text):
    tokens = [word_tokenize(t) for t in sent_tokenize(text)]
    return tokens

def lemmatize_sentence(tokens):
    lemmatizer = WordNetLemmatizer()
    lemmatized_sentence = []
    for word, tag in pos_tag(tokens):
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))
    return lemmatized_sentence

def pre_cleaning_sentences(text=''):


    #Lowercasing
    lower_text = text.lower()
    # Tokenize
    tokens = sentence_tokenizer(lower_text)

    # Lemmatizing
    lemma_text = [lemmatize_sentence(token) for token in tokens]
    lemma_text = list(itertools.chain.from_iterable(lemma_text))

    # Removing stop words
    tokens_without_sw = [word for word in lemma_text if not word in stopwords.words()]

    # Removing special characters
    alnum_token_list = [''.join(e for e in S if e.isalnum()) for S in tokens_without_sw]

    processed_tokens = list(filter(lambda a: a != '', alnum_token_list))
    return processed_tokens