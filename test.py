import search, extract

read = search.read("test.txt")
search = search.search(read)
extract = extract.text(search)
for x in extract:
    print(x)
print(len(extract),"texts")
