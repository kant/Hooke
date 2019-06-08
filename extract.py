import urllib.request
from bs4 import BeautifulSoup
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer


def text(urls):
    print("Extracting text from", len(urls),"URLs....")
    text = []
    for url in urls:
        try:
            print("Downloading text from",url)
            html = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(html,"lxml")
            [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
            text.append(soup.getText().replace("\n\n","\n").replace("\n"," ").replace("\r","").replace("  "," "))
        except:
            text.append("")
            pass
    return text

def normalize(input):
    print("Normalizing...")
    output = input.lower()
    output = output.translate(str.maketrans("","", string.punctuation))
    output = output.strip()
    output = word_tokenize(output)
    return output

def preprocess(input, lang="english"):
    print("Preprocessing")
    stop_words = set(stopwords.words(lang))
    output = []
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    for x in input:
        out = []
        tem = [i for i in x if not i in stop_words]
        for word in tem:
            out.append(  lemmatizer.lemmatize(stemmer.stem(word))  )
        output.append(out)
    return output


