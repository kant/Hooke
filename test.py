import search, extract, pickle, compare
read = search.read("test.txt")
read = extract.preprocess(extract.normalize(read))[0]
search = search.search(read)
ex = extract.text(search)
texts = extract.preprocess(extract.normalize(ex))
ohNo= compare.compare(read, texts, threshold=1,length=5)
for upsie in ohNo:
    match, index, text = upsie
    (start, end, diff) = match
    x = texts[index]
    y = x[start:end]
    print(y, "IS CLOSE TO",text,"BY",diff)
print(len(ohNo),"matches")
print(len(ohNo)>10)