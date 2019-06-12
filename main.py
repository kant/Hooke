import search, extract, compare

##vars
inp = "test.txt"
nort = 1
norl = 7
pret = 0
prel = 10
timeout = 10
lang = "english"
##/vars

extract = extract.ExtractC()

read = search.read(inp)
searches = search.div(read)
print(read)
norread = extract.normalize(read)
preread = extract.preprocess(norread)
print(norread, preread, searches)
# search = search.search(read)
# ex = extract.text(search, timeout=timeout)
# nortexts = extract.normalize(ex)
# pretext = extract.preprocess(nortexts)
# norcom = compare.compare(norread, nortexts, threshold=nort,length=norl)
# precom = compare.compare(preread, pretext, threshold=pret, length=prel)

# print(norcom, precom)