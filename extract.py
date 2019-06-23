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
            if ".pdf" in url and stika:
                return download_pdf(url)
            elif ".pdf" in url and not stika:
                return ""
            else:
                html = urllib.request.urlopen(url, timeout=timeout).read()
                if html[:5] == b"%PDF-":
                    if stika:
                        return download_pdf(url)
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
        output = y.lower()
        output = output.translate(str.maketrans("","", string.punctuation))
        output = output.strip()
        return word_tokenize(output)

    def preprocess(self, x):
        # Preprocesses using nltk stopwords and lemmatizer
        out = []
        tem = [i for i in x if not i in self.stop_words]
        for word in tem:
            out.append(  self.lemmatizer.lemmatize(word)  )
        return out

    def doall(self, url, timeout, pdfsupport):
        # Does all (Makes it easier to multithread)
        raw = self.text(url, timeout, pdfsupport)
        nor = self.normalize(raw.split())
        pre = self.preprocess(nor)
        return nor, pre