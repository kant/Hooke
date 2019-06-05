import urllib.request
from bs4 import BeautifulSoup

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

