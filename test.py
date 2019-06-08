import search, extract, pickle
read = search.read("test.txt")
# search = search.search(read)
# ex = extract.text(search)
with open("ex","rb") as f:
    ex = pickle.load(f)
print(extract.preprocess(extract.normalize(ex)))
print(len(ex),"texts")
print("Ready")