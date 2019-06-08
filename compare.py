from fuzzysearch import find_near_matches

def compare(input, texts,length, threshold):
    matches = []
    query = []
    for n in range((len(input) - length + 1)):
        query.append(input[n:n+length])
    for q in query:
        for index, t in enumerate(texts):
            for x in find_near_matches(q,t,max_l_dist=threshold):
                matches.append((x,index))
    return matches
