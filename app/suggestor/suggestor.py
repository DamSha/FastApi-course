import time

import joblib
import pandas as pd

from app.suggestor.preprocessors import TextPreprocessor

preprocessor = TextPreprocessor()

# Charge modele fitted
model_supervise = joblib.load("./artifacts/model_supervise_proba.pkl")
all_tags = pd.read_csv('./artifacts/all_tags.csv', index_col=0)['0'].tolist()
# model_non_supervise = joblib.load("./artifacts/model_non_supervise.pkl")


class Suggestor:

    def preprocess(self, title: str, body: str):
        return preprocessor.preprocess_text(title, body)

    def predict(self, title: str, body: str, supervised: bool = False, threshold: float = 0.25):
        if supervised:
            # Preprocess
            x_preprocessed = self.preprocess(title, body)

            # Predit les Tags
            y_proba = model_supervise.predict_proba(x_preprocessed[0])

            # transformation en DataFrame
            y_proba_df = pd.DataFrame(y_proba, columns=all_tags)
            # Récupération des 5 meilleurs stats
            tags = y_proba_df.iloc[0].sort_values(ascending=False).head(5).reset_index().rename(
                columns={'index': 'tag', 0: 'proba'})
            tags.proba = tags.proba.astype(float)
            # Filtre sur le threshold
            tags = tags[tags.proba > threshold].head(5)

        else:  # Non supervisé
            x_preprocessed = f"{str(title)} {str(body)}"
            topics = pd.DataFrame({}, columns=['similar_topics', 'similarity'])
            topics.similar_topics, topics.similarity = \
                model_non_supervise.find_topics(x_preprocessed, top_n=5)
            topics = topics[topics.similarity > threshold]

            tags = pd.DataFrame({}, columns=['tag', 'proba'])

            for topic in topics.similar_topics:
                words = model_non_supervise.get_topic(topic)
                for word in words:
                    if float(word[1]) > threshold:
                        tags.loc[-1] = {"tag": word[0], "proba": word[1]}
                        tags.reset_index(drop=True, inplace=True)
            tags = tags.sort_values(by='proba',
                                    ascending=False).head(5).reset_index(drop=True)
        return tags
