import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from quiry import check_for_greeting
from quiry import index
import requests
import re
import json

api_key_weather = "f008574df2dfaee547da4e4dd339685f"
country_code = ""
city = ""
temp_c = temp_k = temp_f = 0
api_base_url_dict = "https://od-api.oxforddictionaries.com/api/v1"
app_id_dict = "ecdf5812"
app_key_dict = "a224b789697d483b87f2517f8e08b10b"

flag = 0
queri = index()
weather_list = ["climate", "weather", "forecast", "temperature"]
dictionary_list = ["define", "meaning", "means"]
run = 0
temp_word = ""


def api_calls(tag_query, flag_2):
    global api_key_weather, temp_c, temp_k, temp_f, api_base_url_dict, app_id_dict, app_key_dict
    # global flag
    # global run
    global temp_word

    for word, tag in tag_query:
        # print(word)
        # print("Flag:", flag_2)
        if flag_2 != 0:

            def weather_api(wrd):
                language = 'en'
                url = 'https://od-api.oxforddictionaries.com/api/v1/entries/' + language + '/' + wrd.lower()
                r = requests.get(url, headers={'app_id': app_id_dict, 'app_key': app_key_dict})
                json_object = r.json()
                print("code{}\n".format(r.status_code))
                # print(r.text)
                ans = json_object['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
                print(wrd, " : " + ans)

            if flag_2 == 1:  # check here
                # print(tag_query[-1][1])
                if tag_query[-1][1] != '.':
                    temp_word = tag_query[-1][0]
                    print("meaning iski nikalooio:", temp_word)
                    weather_api(temp_word)
                    break
                else:
                    temp_word = tag_query[-2][0]
                    print("meaning iski nikalosbhcbisb:", temp_word)
                    weather_api(temp_word)
                    break
            elif flag_2 == 2:
                temp_word = tag_query[0][0]
                print("meaning iski nikalo:", temp_word)
                weather_api(temp_word)
                break

        elif word in weather_list:
            for word_i, tag_j in tag_query:
                if tag_j == 'NNP' and word_i != 'Jarvis':
                    print(word_i)
                    r = requests.get(
                        "http://api.openweathermap.org/data/2.5/weather?q=" + word_i + "&appid=" + api_key_weather)
                    json_object = r.json()
                    temp_k = float(json_object['main']['temp'])
                    # print("Temperature in kelvin:", (str(temp_k)))
                    temp_f = (temp_k - 273.15) * 1.8 + 32
                    # print("Temperature in fahrenheit:", str(temp_f))
                    temp_c = temp_k - 273.15
                    print("Temperature in Celsius:", temp_c)
                    weather_list1 = json_object['weather']
                    desc = weather_list1[0]['description']
                    print("Its gonna be", desc, "in " + word_i)


def processing(sentence, flag_1):
    # print(sentence)
    cnt = 1
    for i in sentence:
        if i == ' ':
            cnt = cnt + 1
    # print(cnt)
    words = word_tokenize(sentence)  # words = ['hi', 'bot']
    tagged_query = pos_tag(words)  # tagged_query = [('hi', 'NN'), ('bot', 'NN')]
    # print(tagged_query)
    check_for_greeting(tagged_query, cnt)
    api_calls(tagged_query, flag_1)


processing(queri, flag)


def diction(qry):
    global flag
    patFinder1 = re.compile('what is\s\w+\smeaning\s', re.IGNORECASE)
    patFinder2 = re.compile('Define\s', re.IGNORECASE)
    patFinder3 = re.compile('Explain\s', re.IGNORECASE)
    patFinder4 = re.compile('\w+\smeans', re.IGNORECASE)
    # findPat1 = re.search(patFinder1, sentence)
    # print(findPat1.group(0))
    if re.search(patFinder1, qry) or re.search(patFinder2, qry) or re.search(patFinder3, qry):
        flag = 1
        processing(qry, flag)
    elif re.search(patFinder4, qry):
        flag = 2
        processing(qry, flag)
        # api_calls(tagged_query)


diction(queri)
