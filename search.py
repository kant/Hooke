import textract
from google import google


def read(file, every=16, length=32):
    print("Reading...")
    raw = textract.process(file)
    words = raw.split()
    count = 0
    run = True
    search = []

    while run:
        current = b""
        for x in range(count * every, count * every + length):
            try:
                current = current + b" " + words[x]
            except:
                run = False
        search.append(current.decode())
        count += 1
    return search

def search(searches, results=1):
    print("Searching", len(searches),"queries...")
    list = []
    for x in searches:
        for element in google.search(x, results):
            url = element.link
            if url not in list:
                list.append(url)
    return list

#Old
#import googlesearch
#
# def search(searches, results=1, pause = 5):
#     print("Searching", len(searches),"queries...")
#     list = []
#     for x in searches:
#         for url in googlesearch.search(x, num=results, pause=pause):
#             if url not in list:
#                 list.append(url)
#     return list
