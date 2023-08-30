import re
import spacy  # conda install -c conda-forge spacy-model-fr_core_news_md
from spacy.language import Language
from spacy.tokens import Doc

spacy.prefer_gpu()

from spellchecker import SpellChecker

spell = SpellChecker(language="fr")


@Language.component("remove_punctuation")
def remove_punctuation(doc: Doc):
    """
    Function that takes a string and remove all punctuations
        --> requirements :
            import re

    :param doc: Doc object that need to be cleaned (Doc object)
    :return: string cleaned
    """
    text_cleaned = re.sub(r'[^\w\s]', ' ', doc.text)  # remove punctuation
    text_cleaned = re.sub(r'\d+', ' ', text_cleaned)  # remove numbers
    text_cleaned = re.sub(r'_', ' ', text_cleaned)  # remove "_"
    text_cleaned = re.sub(r'\s+', ' ', text_cleaned)  # remove additional space

    return Doc(doc.vocab, words=text_cleaned.lower().split())


@Language.component("remove_stopwords")
def remove_stopwords_spacy(doc: Doc) -> Doc:
    """
    Function that removes stopwords from a text using SpaCy

    :param doc: string that need to be cleaned (Doc object)
    :return: string without stopwords
    """

    text = [token.text for token in doc if token.is_stop is False and len(token.text) > 2]

    return Doc(doc.vocab, words=text)


@Language.component("spellcheck_SpellChecker")
def spellcheck(doc: Doc) -> Doc:
    """
    Function that corrects the spelling of the words using Levenshtein distance (distance=2)
        -> documentation : https://pypi.org/project/pyspellchecker/
        -> https://ansegura7.github.io/NLP/support/pyspellchecker_manual.pdf

    :param doc: text that wants to be spellchecked
    :return: Doc with corrected misspelled words.
    """

    tokens = [token.text for token in doc]
    tokens_in_dict = spell.known(tokens)
    tokens_misspelled = spell.unknown(tokens)

    tokens_corrected = []
    for word in tokens_misspelled:
        check_spelling = spell.correction(word)
        if check_spelling is not None:
            tokens_corrected.append(check_spelling)
        else:
            tokens_corrected.append(word)

    print("number of misspelled words corrected :", len(tokens_corrected))
    tokens_corrected.extend(list(tokens_in_dict))

    return Doc(doc.vocab, words=tokens_corrected)


@Language.component("lemmatize_words")
def lemmatize_words_spacy(doc: Doc) -> Doc:
    """
    Function that stem words using Spacy

    :param doc: text in which we want to stem the words
    :return: text with words stemmed
    """

    # on supprime les mots qui n'ont qu'un seul charactère après le stemming
    text_lemma = [token.lemma_ for token in doc if len(token.lemma_) > 2]

    return Doc(doc.vocab, words=text_lemma)


# pip install spacy-lookups-data
nlp = spacy.blank('fr')
nlp.add_pipe("remove_punctuation", first=True)
nlp.add_pipe("remove_stopwords")
nlp.add_pipe("spellcheck_SpellChecker")
nlp.add_pipe("lemmatizer", config={"mode": "lookup"})
nlp.add_pipe("lemmatize_words")
nlp.initialize()

# --- Testing the Pipeline
# print(nlp.pipeline)
# print("text after preprocessing ->",
#       nlp("Binpjur .. helooo jouer jouons jouez joucnkdhfzef § eeeee e u toi le les des !!").text)
