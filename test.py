import search, extract

read = search.read("test.txt")
search = search.search(read)
ex = extract.text(search)
for x in ex:
    print( extract.preprocess(extract.normalize(x) ))
print(len(extract),"texts")
