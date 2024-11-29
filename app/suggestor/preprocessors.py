import re
import string

import numpy as np
import pandas as pd

# from nltk.corpus import stopwords
import spacy
from lxml import html
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import FunctionTransformer
from spacy.lang.en import stop_words


class TagsTransformer:
    def __init__(self):
        # t1 = time.perf_counter()
        self.replacements = {
            'c#': 'c_sharp',
            'f#': 'f_sharp',
            'c++': 'c_plusplus',
            'h++': 'h_plusplus',
            'obj-c++': 'obj_c_plusplus',
            'objective-c++': 'objective_c_plusplus',
            ' .net': ' dot_net'
        }
        # Create reverse replacements for unfiltering
        self.reverse_replacements = {v: k for k, v in self.replacements.items()}

    def filter_c_family(self, _data: str) -> str:
        #         t1 = time.perf_counter()
        for pattern, replacement in self.replacements.items():
            _data = re.sub(re.escape(pattern), replacement, _data)
        #             print('__init__ ', f"{time.perf_counter() - t1:.1f}")
        return _data

    def unfilter_c_family(self, _tags: list) -> list:
        #         t1 = time.perf_counter()

        def replace_tags(text):
            #             t1 = time.perf_counter()
            for pattern, replacement in self.reverse_replacements.items():
                text = re.sub(re.escape(pattern), replacement, text)
            #                 print('filter_c_family ', f"{time.perf_counter() - t1:.1f}")
            return text

        _data = pd.Series(_tags).map(lambda x: " ".join(x))
        _data = _data.map(replace_tags)
        #         print('unfilter_c_family ', f"{time.perf_counter() - t1:.1f}")
        return [x.split(" ") for x in _data]

    def compute_tags(self, _tags) -> pd.Series:
        #         t1 = time.perf_counter()
        """ Transforme les Tags en liste séparé par un espace
        :param _data_source: DataFrame source contenant les Tags
        :return: Un vecteur contenant les Tags
        """
        _tags = _tags.iloc[:, 0]
        _tags = _tags.astype(str)
        _tags = _tags.str.lower()
        _tags = _tags.map(lambda x: re.sub('><', ' ', x))
        _tags = _tags.map(lambda x: re.sub('<|>', '', x))
        _tags = _tags.map(lambda x: self.filter_c_family(x))
        _tags = _tags.map(lambda x: x.split(" "))
        #         print('replace_tags ', f"{time.perf_counter() - t1:.1f}")
        return _tags


#         print('compute_tags ', f"{time.perf_counter() - t1:.1f}")
# return _tags.values.reshape(-1, 1)


# tags_transformer.filter_c_family("c++ f#")
#
# tags_transformer.unfilter_c_family([["c_plusplus", "f_sharp"]])

lem_allowed_postags_NV = ['NOUN', 'VERB']
lem_allowed_postags_N = ['NOUN']
tags_transformer = TagsTransformer()


class TextPreprocessor:
    def __init__(self):
        #         t1 = time.perf_counter()
        self.lem_allowed_postags = lem_allowed_postags_N
        self.stop_words = stop_words.STOP_WORDS
        self.lem_model = spacy.load("en_core_web_md", disable=['parser', 'ner'])

    #         print('TextPreprocessor __init__ ', f"{time.perf_counter() - t1:.1f}")

    def extract_sentences_from_body_transformer(self, _df: np.array):
        #         t1 = time.perf_counter()
        _df = _df.map(lambda x: self.extract_sentences_from_body(str(x)))
        #         print('extract_sentences_from_body_transformer ', f"{time.perf_counter() - t1:.1f}")
        return _df.values.reshape(-1, 1)

    def extract_sentences_from_body(self, _data: str) -> str:
        #         t1 = time.perf_counter()
        doc = html.fromstring(_data)
        paragraphes = doc.cssselect('p')
        if len(paragraphes) == 0:
            #             print('extract_sentences_from_body ', f"{time.perf_counter() - t1:.1f}")
            return ""
        #         print('extract_sentences_from_body ', f"{time.perf_counter() - t1:.1f}")
        return " ".join([p.text_content() for p in paragraphes if p.text_content() is not None])

    def clean_sentence_transformer(self, _df: np.array) -> pd.DataFrame:
        #         t1 = time.perf_counter()
        _df = pd.DataFrame(_df)
        _df = _df.iloc[:, 0]
        _df = _df.map(lambda x: self.clean_sentence(str(x)))
        _df = _df.values.reshape(-1, 1)
        #         print('clean_sentence_transformer ', f"{time.perf_counter() - t1:.1f}")
        return _df

    def clean_sentence(self, sentence: str) -> str:
        #         t1 = time.perf_counter()
        # Convert to lowercase
        sentence_cleaned = sentence.lower()

        # Combine multiple regex substitutions into one
        sentence_cleaned = re.sub(
            r'[^\x00-\x7F]+|'  # Non-ASCII characters
            r'\s[0-9]+|'  # Numbers preceded by whitespace
            r'(&*;)|'  # HTML entities
            r'(<code.*code>)|'  # Code tags
            r'https?:\/\/.*[\r\n]*|'  # URLs
            r'\S*@\S*\s?|'  # Email addresses
            r'\n',  # Newlines
            ' ',
            sentence_cleaned
        )

        # Apply custom transformation
        sentence_cleaned = tags_transformer.filter_c_family(sentence_cleaned)

        # Remove punctuation (except underscores) and extra spaces
        sentence_cleaned = re.sub(
            rf"[{string.punctuation.replace('_', '')}]|\s+",
            ' ',
            sentence_cleaned
        ).strip()

        #         print('clean_sentence ', f"{time.perf_counter() - t1:.1f}")
        return sentence_cleaned

    def tokenize_for_bow(self, sentence: str) -> str:
        #         t1 = time.perf_counter()
        # Define the set of useless words for faster lookup
        useless_words_set = {"use", "get", "create", "way", "find", "return", "add", "work", "error", "issue", "file",
                             "code", "try", "want", "follow", "need", "run", "problem", "know", "value", "make", "fix"}
        # # Split the sentence into words
        # words = sentence.split()
        # Filter out stop words
        filtered_words = [word for word in sentence if word not in self.stop_words]
        # Lemmatize the filtered words
        doc = self.lem_model(" ".join(filtered_words))
        # Filter lemmatized words based on part of speech and other criteria
        processed_words = [
            token.lemma_ for token in doc
            if token.pos_ in self.lem_allowed_postags and
               token.lemma_ not in useless_words_set and
               2 <= len(token.lemma_) <= 200
        ]
        # Join the processed words into a single string
        processed_words = ' '.join(processed_words)
        #         print('tokenize_for_bow ', f"{time.perf_counter() - t1:.1f}")
        return processed_words

    def vectorize(self, _data):
        import joblib
        vectorizer = joblib.load('./artifacts/cv.pkl')
        transformer = joblib.load('./artifacts/tfidf.pkl')
        #         t1 = time.perf_counter()
        _data = _data.split(" ")
        _data_vect = vectorizer.transform(_data)
        _data_vect = transformer.transform(_data_vect)
        #         print('vectorize ', f"{time.perf_counter() - t1:.1f}")
        return _data_vect

    def get_pipeline(self):
        #         t1 = time.perf_counter()
        # Clean Title
        title_transformer = FunctionTransformer(self.clean_sentence_transformer, validate=False)

        # Clean Body
        body_transformer = make_pipeline(
            FunctionTransformer(self.extract_sentences_from_body_transformer, validate=False),
            FunctionTransformer(self.clean_sentence_transformer, validate=False),
        )

        # Preprocess Title + Body
        _preprocessor = ColumnTransformer([
            ('title_transformer', title_transformer, 'Title'),
            ('body_transformer', body_transformer, 'Body')
        ])

        def combine_fn(_data: np.ndarray):
            #             t1 = time.perf_counter()
            _data = [' '.join(map(str, row)) for row in _data]
            #             print('combine_fn ', f"{time.perf_counter() - t1:.1f}")
            return _data

        # Combine Title + Body
        combine_transformer = FunctionTransformer(
            combine_fn
            # lambda x: [' '.join(map(str, row)) for row in x]
        )

        # Tokenize Title + Body
        tokenize_transformer = FunctionTransformer(self.tokenize_for_bow, validate=False)

        # Vectorize Title + Body
        vectorize_transformer = FunctionTransformer(self.vectorize, validate=False)

        # Final pipeline
        pipeline_x = Pipeline([
            ("preprocess", _preprocessor),
            ("combine", combine_transformer),
            ("tokenize", tokenize_transformer),
            ("vectorize", vectorize_transformer),
        ])

        #         print('get_pipeline ', f"{time.perf_counter() - t1:.1f}")
        return pipeline_x

    def preprocess_text(self, _title: str, _body: str) -> pd.DataFrame:
        #         t1 = time.perf_counter()
        x_texts = pd.DataFrame([[_title, _body]], columns=["Title", "Body"])
        texts_preprocessed = self.get_pipeline().fit_transform(x_texts)
        #         print('preprocess_text ', f"{time.perf_counter() - t1:.1f}")
        return texts_preprocessed

#
# if __name__ == '__main__':
#     preprocessor = TextPreprocessor()
#     pipeline = preprocessor.get_pipeline()
#     title = "Why am I seeing Flutter EGL_emulation app_time_stats in the log when running on an Android 12 emulator?"
#     body = ("<p>When testing a Android Flutter app on an emulator running Android 12, "
#             "I'm seeing lines like these in the logs at regular intervals "
#             "(approximately every second):</p> <pre><code>D/EGL_emulation(32175): "
#             "app_time_stats: avg=312.93ms min=133.69ms max=608.57ms count=4 </code></pre> "
#             "<p>What do they mean, and how do I turn them off? I've never seen them on Android "
#             "11 emulators, so I'm guessing it has something to do with Android 12?</p>")
#     x_preprocessed_test = preprocessor.preprocess_text(title, body)
#     print(x_preprocessed_test)
#
#     # Charge modele fitted
#     loaded_model = joblib.load("./artifacts/model_supervise_proba.pkl")
#     y_proba = loaded_model.predict_proba(x_preprocessed_test[0])
#     all_tags = pd.read_csv('./artifacts/all_tags.csv', index_col=0)['0'].tolist()
#     y_proba_df = pd.DataFrame(y_proba, columns=all_tags)
#
#     tags = y_proba_df.iloc[0].sort_values(ascending=False).head(5).reset_index().rename(
#         columns={'index': 'tag', 0: 'proba'})
#     tags.proba = tags.proba.astype(float)
#     tags = tags[tags.proba > .1].head(5)
#
#     print(y_proba_df)
#     print(tags)
