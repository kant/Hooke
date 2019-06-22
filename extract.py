import urllib.request
from bs4 import BeautifulSoup
from tika import parser
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import wget
import os


class ExtractC():
    def __init__(self, lang = "english"):
        #Initializes a extractor class, to set the stopwords and lenguaje just once
        self.stop_words = set(stopwords.words(lang))
        self.lemmatizer = WordNetLemmatizer()

    def download_pdf(url):
        #Download PDFs
        wget.download(url, "temp/temp.pdf", None)
        parsed = parser.from_file("temp/temp.pdf")['content']
        os.remove("temp/temp.pdf")
        return parsed.replace("\n\n","\n").replace("\n"," ").replace("\r","").replace("\t"," ").replace("  "," ")

    def text(self, url, timeout = 30, stika = True):
        #Downloads text from the urls
        try:
            print("Downloading text from",url)
            if ".pdf" in url and stika:
                return download_pdf(url)
            elif ".pdf" in url and not stika:
                return ""
            else:
                html = urllib.request.urlopen(url, timeout=timeout).read()
                if html[:5] == b"%PDF-" and stika:
                    return download_pdf(url)
                elif not stika:
                    return ""
                soup = BeautifulSoup(html,"lxml")
                [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
                return soup.getText().replace("\n\n","\n").replace("\n"," ").replace("\r","").replace("\t"," ").replace("  "," ")
        except:
            return ""

    def normalize(self, x):
        # Lowers, eliminates punctuation and strips text
        y = ""
        for z in x:
            y = y + z + " "
        print("Normalizing...")
        output = y.lower()
        output = output.translate(str.maketrans("","", string.punctuation))
        output = output.strip()
        return word_tokenize(output)

    def preprocess(self, x):
        # Preprocesses using nltk stopwords and lemmatizer
        print("Preprocessing...")
        out = []
        tem = [i for i in x if not i in self.stop_words]
        for word in tem:
            out.append(  self.lemmatizer.lemmatize(word)  )
        return out

