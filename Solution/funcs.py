import re
import requests
from nltk.tokenize import sent_tokenize
import nltk
from bs4 import BeautifulSoup
# nltk.download('punkt')


def create_txt(url, url_id):
    """Extract the article text and save the extracted article in a text file with URL_ID as it's file name"""
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
    }

    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.content, 'html.parser')
    file = open(f"./data/{url_id}.txt", "w", encoding="utf-8")
    text = ""
    for node in soup.findAll(['h1', 'strong', 'p']):
        text += " "
        text += ''.join(node.findAll(text=True))
    file.writelines(text)


def count_syllables(word):
    """Function to count the number of syllables in a given word"""
    VOWEL_RUNS = re.compile("[aeiouy]+", flags=re.I)
    EXCEPTIONS = re.compile(
        # fixes trailing e issues:
        # smite, scared
        "[^aeiou]e[sd]?$|"
        # fixes adverbs:
        # nicely
        + "[^e]ely$",
        flags=re.I
    )
    ADDITIONAL = re.compile(
        # fixes incorrect subtractions from exceptions:
        # smile, scarred, raises, fated
        "[^aeioulr][lr]e[sd]?$|[csgz]es$|[td]ed$|"
        # fixes miscellaneous issues:
        # flying, piano, video, prism, fire, evaluate
        + ".y[aeiou]|ia(?!n$)|eo|ism$|[^aeiou]ire$|[^gq]ua",
        flags=re.I
    )
    vowel_runs = len(VOWEL_RUNS.findall(word))
    exceptions = len(EXCEPTIONS.findall(word))
    additional = len(ADDITIONAL.findall(word))
    return max(1, vowel_runs - exceptions + additional)


def num_sent(text):
    """Function to count the number of sentences in a given text"""
    number_of_sentences = sent_tokenize(str(text))
    return len(number_of_sentences)


def regex_prp(text):
    """Function to count the Personal Pronouns in a given text"""
    text_str = ""
    for word in text:
        words = word.split()
    for word in words:
        text_str += word + " "

    regex = r"\bI\b|\bwe\b|\bmy\b|\bours\b|\bus\b|\bWe\b|\bMy\b|\bOurs\b|\bUs\b"
    matches = re.findall(regex, text_str)
    return len(matches)
