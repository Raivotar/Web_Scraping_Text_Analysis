from bs4 import BeautifulSoup
import pandas as pd
import requests
from funcs import create_txt
from funcs import count_syllables
from funcs import num_sent
from funcs import regex_prp

urls = pd.read_excel("Input.xlsx")
urls.set_index("URL_ID", inplace=True)


# ID 44 is missing so I had to add one more to the count
# for i in range(1, len(urls["URL"])+2):
#     try:
#         url = urls.loc[i].values[0]
#         create_txt(url, i)
#     except KeyError:
#         continue

# Parser.csv was created by running generic.py and lm.py from "https://sraf.nd.edu/textual-analysis/code/""
parser = pd.read_csv("Parser.csv")
parser["file name"] = parser["file name"].str[7:]
parser["file name"] = parser["file name"].str[:-4]

parser = parser.astype(int)
parser = parser.sort_values("file name")
parser["URL_ID"] = parser["file name"]
parser.drop("file name", axis=1, inplace=True)
parser.set_index("URL_ID", inplace=True)

output = pd.read_excel("Output.xlsx")
output = output.sort_values("URL_ID")
output.set_index("URL_ID", inplace=True)

output["POSITIVE SCORE"] = parser["% positive"]
output["NEGATIVE SCORE"] = parser["% negative"]
output["WORD COUNT"] = parser["number of words"]
output["POLARITY SCORE"] = (output["POSITIVE SCORE"] - output["NEGATIVE SCORE"]) / \
    (output["POSITIVE SCORE"] + output["NEGATIVE SCORE"])
output["SUBJECTIVITY SCORE"] = (
    output["POSITIVE SCORE"] + output["NEGATIVE SCORE"]) / (output["WORD COUNT"] + 0.000001)

pp_list = []
sent_list = []
sylla_list = []
for i in range(1, 172):
    try:
        with open(f"./data/{i}.txt", "r", encoding='utf-8') as file:
            text = file.readlines()
            pp_list.append(regex_prp(text))
            sent_list.append(num_sent(text))
            sylla_file = 0
            for word in text:
                words = word.split()
            for word in words:
                if count_syllables(word) > 2:
                    sylla_file += 1
        sylla_list.append(sylla_file)
    except FileNotFoundError:
        continue

output["AVG SENTENCE LENGTH"] = output["WORD COUNT"] / sent_list
output["AVG NUMBER OF WORDS PER SENTENCE"] = output["WORD COUNT"] / sent_list
output["COMPLEX WORD COUNT"] = sylla_list
output["PERCENTAGE OF COMPLEX WORDS"] = (
    output["COMPLEX WORD COUNT"] / output["WORD COUNT"])
output["FOG INDEX"] = 0.4 * \
    (output["AVG SENTENCE LENGTH"] + output["PERCENTAGE OF COMPLEX WORDS"])
output["SYLLABLE PER WORD"] = parser["avg # of syllables per word"]
output["PERSONAL PRONOUNS"] = pp_list
output["AVG WORD LENGTH"] = parser["average word length"]

output.to_excel("final_output.xlsx")
