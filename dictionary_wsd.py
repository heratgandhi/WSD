'''
    Dictionary based WSD
    Author: Herat Gandhi
'''

import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
import string
import re
from bs4 import BeautifulSoup as Soup

'''
    Function to get context words from the given sample
    @param line: Sample from which we need to retrieve context words
    @param n: n context words we want to retrieve
    @return: Return list of n context words
'''
def get_context_words(line,n,lines1,target):
    temp = line.lower()
    temp = re.sub('[0-9]+','',temp)
    
    first_at = temp.find('@')
    last_at = temp.rfind('@')+1
    
    temp1 = temp[:first_at]
    temp2 = temp[last_at:]
    
    for punct in string.punctuation:
        temp1 = temp1.replace(punct,'')
        temp2 = temp2.replace(punct,'')
    
    temp_l1 = temp1.split()
    temp_l2 = temp2.split()
    
    important_words1 = filter(lambda x: x not in stopwords.words('english'), temp_l1)
    important_words1 = filter(lambda x: x not in lines1, important_words1)
    important_words2 = filter(lambda x: x not in stopwords.words('english'), temp_l2)
    important_words2 = filter(lambda x: x not in lines1, important_words2)
    
    important_words1 = nltk.pos_tag(important_words1)
    important_words2 = nltk.pos_tag(important_words2)

    if len(important_words1) > n:
        temp_words1 = important_words1[len(important_words1)-n:]
    else:
        temp_words1 = important_words1
    temp_words2 = important_words2[:n]
    
    senses = []
    lmtzr = WordNetLemmatizer()
    
    for t in temp_words1:
        try:
            if 'VB' in t[1]:
                senses.append(wordnet.synsets(lmtzr.lemmatize(t[0],'v')))
            else:
                senses.append(wordnet.synsets(t[0]))
        except:
            print('Ignored: '+t[0])
            pass
        
    for t in temp_words2:
        try:
            if 'VB' in t[1]:
                senses.append(wordnet.synsets(lmtzr.lemmatize(t[0],'v')))
            else:
                senses.append(wordnet.synsets(t[0]))
        except:
            print('Ignored:' + t[0])
            pass    
    
    hypernyms = []
    for sense_l in senses:
        for s in sense_l:
            #print(s.definition)
            hypernyms.append(s.hypernyms())
    
    hyponyms = []
    for sense_l in senses:
        for s in sense_l:
            hyponyms.append(s.hyponyms())
            
    meronyms = []
    for sense_l in senses:
        for s in sense_l:
            meronyms.append(s.part_meronyms())        
    
    toponyms = []
    for sense_l in senses:
        for s in sense_l:
            toponyms.append(s.part_holonyms())
            
    definitions = []
    for sense_l in senses:
        for s in sense_l:
            definitions.append(s.definition)
    
    for sense_l in hypernyms:
        for s in sense_l:
            definitions.append(s.definition)
   
    for sense_l in hyponyms:
        for s in sense_l:
            definitions.append(s.definition)
    
    for sense_l in meronyms:
        for s in sense_l:
            definitions.append(s.definition)
            
    for sense_l in toponyms:
        for s in sense_l:
            definitions.append(s.definition) 
    
    target_w_l = []
    for w in wordnet.synsets(target):
        target_w_l.append(w.definition)        
    
    definitions = ' '.join(definitions).split()
    definitions_s = set(definitions)
    
    max_index = -1
    max = -1
    index = 1
    max_str = ''
        
    file = 'Dictionary.xml'
    handler = open(file).read()
    soup = Soup(handler)
    for message in soup.dictmap.findAll('lexelt'):
        if target in message['item']:
            for s in message.findAll('sense'):
                temp_S = set(s['gloss'].split())
                
                print(temp_S & definitions_s)
                
                if len(temp_S & definitions_s) > max:
                    max = len(temp_S & definitions_s)
                    max_str = s['gloss']
                    max_index = index
                index += 1
    
    print( str(max_index) + ' ' + max_str )
    
    return ''

'''
    Function to perform WSD based on dictionaries
    @param filename: Filename to be used for testing
'''
def WSD_Dict(filename):
    fp = open(filename,'r')
    lines = fp.readlines()
    fp2 = open('words.txt','r')
    lines1 = fp2.read().splitlines()
    
    for line in lines:
        at_p = line.find('@') #Find first occurance of @ that helps to identify where to break string
        starting = line [:at_p].split()
        strating_target = starting[0].split('.')[0] #Target word to be disambiguated
        form = starting[0].split('.')[1] #Target word form
        line = line[at_p+1:] #Get rest of the line
        target_in_sentence = line[line.find('@')+1:line.rfind('@')] #Target word in the sentence
        #line = line.replace('@','')
        context_words = get_context_words(line,5,lines1,strating_target)
    
def main():
    filename = raw_input('Enter file name to test: ')
    WSD_Dict(filename)

main()