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
        pass ## Posible Future Use

    def download_pdf(url):
        '''Download PDFs (Not working properly)'''
        wget.download(url, "temp/temp.pdf", None)
        parsed = parser.from_file("temp/temp.pdf")['content']
        os.remove("temp/temp.pdf")
        return parsed.replace("\n\n","\n").replace("\n"," ").replace("\r","").replace("\t"," ").replace("  "," ")

    def text(self, url, timeout = 30, stika = True):
        '''Downloads text from the urls'''
        try:
            if ".pdf" in url and stika:
                return download_pdf(url)
            elif ".pdf" in url and not stika:
                return ""
            else:
                html = urllib.request.urlopen(url, timeout=timeout).read().decode()
                if html[:5] == "%PDF-":
                    if stika:
                        return download_pdf(url)
                    return ""
                soup = BeautifulSoup(html,"lxml")
                [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
                return soup.getText().replace("\n\n","\n").replace("\n"," ").replace("\r","").replace("\t"," ").replace("  "," ")
        except:
            return ""

    def normalize(self, x):
        '''Lowers, eliminates punctuation and strips text'''
        y = ""
        for z in x:
            y = y + z + " "
        output = y.lower()
        output = output.translate(str.maketrans("","", string.punctuation))
        output = output.strip()
        return word_tokenize(output)

    def doall(self, url, timeout, pdfsupport):
        '''Does all (Makes it easier to multithread)'''
        raw = self.text(url, timeout, pdfsupport)
        nor = self.normalize(raw.split())
        return nor