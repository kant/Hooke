import textract
from google import google

def read(file, every=16, length=32):
    # Reads from file
    print("Reading...")
    raw = textract.process(file)
    words = raw.decode().split()
    return words

def div(words, every=16, length=32):
    # Divides the text in google-friendly 32 word text in 16 word intervals
    search = []
    count = 0
    run = True
    while run:
        current = ""
        for x in range(count * every, count * every + length):
            try:
                current = current + " " + words[x]
            except:
                run = False
        search.append(current)
        count += 1
    return search

def search(searches, results=1):
    # Searches divided text in google
    print("Searching", len(searches),"queries...")
    list = []
    for x in searches:
        for element in google.search(x, results):
            url = element.link
            if url not in list:
                list.append(url)
    return list