from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import stopwords
import random
import sqlite3

query = input("Jarvis online!\n")
greeting_list = ["hello", "Hello", "hi", "Hi", "greetings", "sup", "what's up", "yo"]
greeting_responses = ["'sup", "hey", "*nods*"]
responses = ["What can I do for you?", "How can I help?", "What can I help you with?"]
weather_list = ["climate", "weather", "forecast"]


def index():
    return query


def check_for_greeting(query_tag, count):
    # count = 0
    for word, pos in query_tag:
        # count = count + 1
        # print(type(word))
        # print(word)
        if (word == 'jarvis' or 'Jarvis') and count == 1:
            print(random.choice(greeting_responses) + " " + random.choice(responses))

        elif word in greeting_list:
            print(word)
            print(random.choice(greeting_responses) + " " + random.choice(responses))
            break


