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

# Init ExtractC class
extract = extract.ExtractC()

read = search.read(inp)
searches = search.div(read)
norread = extract.normalize(read)
preread = extract.preprocess(norread)
searchurls = search.search(searches)
print(searchurls)
# ex = extract.text(search, timeout=timeout)
# nortexts = extract.normalize(ex)
# pretext = extract.preprocess(nortexts)
# norcom = compare.compare(norread, nortexts, threshold=nort,length=norl)
# precom = compare.compare(preread, pretext, threshold=pret, length=prel)

# print(norcom, precom)