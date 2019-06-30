from fuzzysearch import find_near_matches
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 


def compare(input, texts,length=5, threshold=1):
    '''Uses fizzysearch´s Levenshtein search to find matches in n length'''
    matches = []
    query = []
    for n in range((len(input) - length + 1)):
        query.append(input[n:n+length])
    for q in query:
        for index, t in enumerate(texts, start=0):
            for x in find_near_matches(q,t,max_l_dist=threshold):
                matches.append((x,index,q))
    return matches

class nlp:
    '''Used for NLP
    Inits with a language, picks stop words and then compares
    '''
    def __init__(self, lang = "english"):
        '''Inits to specific language'''
        self.lem = WordNetLemmatizer()
        self.stopwords = set(stopwords.words('english')) 


    def preprocess(self, input):
        '''Stop word removal and preprocessing'''
        output = []
        dic = []
        for index, x in enumerate(input):
            if x not in self.stopwords:
                output.append(self.lem.lemmatize(x))
                dic.append(index)
        return output, dic
    

# from nltk.tokenize import word_tokenize 
# x = nlp("english")
# ink = word_tokenize("This is how we are making our processed content more efficient by removing words that do not contribute to any future operations This article is contributed by Pratima Upadhyay If you like GeeksforGeeks and would like to contribute you can also write an article using")
# y, dic = x.preprocess(ink)
# print(y)
# print(dic)