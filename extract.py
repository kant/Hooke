import urllib.request
from bs4 import BeautifulSoup
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

class ExtractC():
    def __init__(self, lang = "english"):
        self.stop_words = set(stopwords.words(lang))
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()

    def text(self, url, timeout = 30):
        try:
            print("Downloading text from",url)
            html = urllib.request.urlopen(url, timeout=timeout).read()
            soup = BeautifulSoup(html,"lxml")
            [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
            return soup.getText().replace("\n\n","\n").replace("\n"," ").replace("\r","").replace("\t"," ").replace("  "," ")
        except:
            return ""
            pass

    def normalize(self, x):
        y = ""
        for z in x:
            y = y + z + " "
        print("Normalizing...")
        output = y.lower()
        output = output.translate(str.maketrans("","", string.punctuation))
        output = output.strip()
        return word_tokenize(output)

    def preprocess(self, x, stop_words):
        print("Preprocessing...")
        print(x)
        out = []
        tem = [i for i in x if not i in stop_words]
        for word in tem:
            out.append(  self.lemmatizer.lemmatize(self.stemmer.stem(word))  )
        return out

