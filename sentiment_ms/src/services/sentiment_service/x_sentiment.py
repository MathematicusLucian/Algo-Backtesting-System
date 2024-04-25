import os
import csv
import urllib.request
from torch import AnyType
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TFAutoModelForSequenceClassification, BertTokenizer, BertForSequenceClassification, pipeline
import numpy as np
from scipy.special import softmax
from src.utils.utils import get_root_dir

class XSentimentService:
    def __init__(self, is_financial=False):
        self.is_financial = is_financial

    @property
    def is_financial(self) -> bool:
        return self._is_financial

    @is_financial.setter
    def is_financial(self, value: bool):
        self._is_financial: bool = value

    def display_info(self) -> str:
        return f"is_financial: {self._is_financial}"

    def get_model_for_classification(self, llm_model: str):
        if(llm_model=="roberta-base"):
            return AutoModelForSequenceClassification.from_pretrained(llm_model)
        elif(llm_model=="finbert-tone"):
            return BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone',num_labels=3)

    def determine_model(self) -> str:
        return "finbert-tone" if self._is_financial else "roberta-base"

    def save_model(self, model_for_classification, llm_model):
        model_for_classification.save_pretrained(llm_model)

    def get_tokenizer_path(self, model, is_local: bool, task: str) -> str:
        if is_local:
            llm_model = os.path.join(get_root_dir(), f"cardiffnlp/twitter-roberta-base-{task}")
        else:
            llm_model = 'yiyanghkust/finbert-tone' if model=="finbert-tone" else f"cardiffnlp/twitter-roberta-base-{task}"
        return llm_model

    def get_tokenizer(self, model, task: str, is_local: bool = False):
        model_path = self.get_tokenizer_path(model, is_local, task)
        if(model=="roberta-base"):
            return AutoTokenizer.from_pretrained(model_path)
        elif(model=="finbert-tone"):
            return BertTokenizer.from_pretrained(model_path)

    def generate_labels(self, task: str) -> list:
        mapping_link = f"https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/{task}/mapping.txt"
        with urllib.request.urlopen(mapping_link) as f:
            html = f.read().decode('utf-8').split("\n")
            csvreader = csv.reader(html, delimiter='\t')
        return [row[1] for row in csvreader if len(row) > 1]

    def get_tweets(self) -> list | str:
        return ["there is a shortage of capital, and we need extra financing",  
            "growth is strong and we have plenty of liquidity", 
            "there are doubts about our finances", 
            "profits are flat"] if self._is_financial else """
            Marsian spacecraft land in New York, and advance towards the White House. 
            Lockdown. Shops closed. Estimated 2 million human fatalities.
            President of the USA may be dead."""

    def extract_words_from_tweet(self, tweet_content: list | str) -> str:
        tweet_words = []
        for t in tweet_content.split(" "):
            t = '@user' if t.startswith('@') and len(t) > 1 else t
            t = 'http' if t.startswith('http') else t
            tweet_words.append(t)
        return " ".join(tweet_words)

    def get_scores(self, output) -> AnyType:
        return softmax(output[0][0].detach().numpy())

    def get_ranking(self, scores) -> np.ndarray[np.intp]:
        return np.argsort(scores)[::-1]

    def print_several_sentiments(self, output: list, labels: list):
        scores = self.get_scores(output)
        ranking = self.get_ranking(scores)
        for i in range(scores.shape[0]):
            print(f"{i+1}) {labels[ranking[i]]} {np.round(float(scores[ranking[i]]), 4)}")

    def determine_sentiment(self, tweet_content: str|list) -> list:
        task="sentiment"
        llm_model = self.determine_model()
        model_for_classification = self.get_model_for_classification(llm_model)
        tokenizer = self.get_tokenizer(llm_model, task, False)
        if self._is_financial:
            nlp = pipeline("sentiment-analysis", model=model_for_classification, tokenizer=tokenizer)
            return nlp(tweet_content)  
        else:
            tweet_words = self.extract_words_from_tweet(tweet_content)
            encoded_tweet = tokenizer(tweet_words, return_tensors='pt')
            return model_for_classification(**encoded_tweet)
        
    def print_sentiment(self, sentiment: str|list):
        labels = self.generate_labels("sentiment")
        print(sentiment) if self._is_financial else self.print_several_sentiments(sentiment, labels)