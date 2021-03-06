'''
    Dictionary based WSD
    Author: Herat Gandhi
'''

import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer
import string
import re

def find_gloss_from_file(str):
    file = 'Dictionary.xml'
    content = open(file).read()
    l = re.compile('<lexelt item="'+str+'.[a-z]">(.*?)</lexelt>', re.DOTALL |  re.IGNORECASE).findall(content)
    if len(l) > 0 :
        return re.compile('gloss="(.*)"').findall(l[0])
    else:
        return -1
    
def remove_junk(string1,lines1):
    string1 = re.sub('[0-9]+','',string1)
    
    for punct in string.punctuation:
        string1 = string1.replace(punct,'')
    
    temp_l1 = string1.split()
    important_words1 = filter(lambda x: x not in stopwords.words('english'), temp_l1)
    important_words1 = filter(lambda x: x not in lines1, important_words1)
    return ' '.join(important_words1)
    
def find_word_sequences(s1):
    s1l = s1.split()    
    i = 0
    j = 0
    k = 1    
    new_s1l = []
    str = ''
    while k <= len(s1l):
        i = 0        
        while i < len(s1l)-k+1:
            j = i
            cnt = 0
            str = ''
            while j < k+i:
                if j == k+i-1:
                    str += s1l[i+cnt]
                else:
                    str += s1l[i+cnt]+ ' '
                j += 1
                cnt += 1
            i += 1
            new_s1l.append(str)            
        k += 1
    return new_s1l
    
def calculate_overall_score(s1,s2):
    seq1 = find_word_sequences(s1)
    total = 0
    for elem in seq1:
        if elem in s2:
            total += (elem.count(' ')+1) ** 2
    return total

'''
    Function to get context words from the given sample
    @param line: Sample from which we need to retrieve context words
    @param n: n context words we want to retrieve
    @return: Return list of n context words
'''
def get_sense_index(line,n,lines1,target):
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

    '''if len(important_words1) > n:
        temp_words1 = important_words1[len(important_words1)-n:]
    else:
        temp_words1 = important_words1
    temp_words2 = important_words2[:n]'''
    temp_words1 = important_words1
    temp_words2 = important_words2
    
    senses = []
    lmtzr = WordNetLemmatizer()
    
    for t in temp_words1:
        try:
            if 'VB' in t[1]:
                senses.append(wordnet.synsets(lmtzr.lemmatize(t[0],'v')))
            else:
                senses.append(wordnet.synsets(t[0]))
        except:
            pass
        
    for t in temp_words2:
        try:
            if 'VB' in t[1]:
                senses.append(wordnet.synsets(lmtzr.lemmatize(t[0],'v')))
            else:
                senses.append(wordnet.synsets(t[0]))
        except:
            pass    
    
    '''hypernyms = []
    for sense_l in senses:
        for s in sense_l:
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
            toponyms.append(s.part_holonyms())'''
            
    definitions = []
    for sense_l in senses:
        for s in sense_l:
            if find_gloss_from_file(s.name.split('.')[0]) != -1:
                definitions.append(' '.join(find_gloss_from_file(s.name.split('.')[0])))
            definitions.append(s.definition)
    
    '''for sense_l in hypernyms:
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
            definitions.append(s.definition)'''
    
    definitions = ' '.join(definitions)

    
    max_index = -1
    max = -1
    index = 1
    max_str = ''
        
    for s in find_gloss_from_file(target):
        stemmed1 = stem_funct(remove_junk(s.lower(),lines1))
        stemmed2 = stem_funct(remove_junk(definitions,lines1))
        temp_sc = calculate_overall_score(stemmed1, stemmed2)
        if temp_sc > max:
            max = temp_sc
            max_str = stemmed1
            max_index = index
        index += 1
    print(str(max_index) + " " + max_str+" "+str(max))
    return [max_index,len(find_gloss_from_file(target))]

def stem_funct(str):
    res = ''
    st = LancasterStemmer()
    for word in str.split(' '):
        res += ' ' + st.stem(word)
    return res

'''
    Function to perform WSD based on dictionaries
    @param filename: Filename to be used for testing
'''
def WSD_Dict(filename):
    fp = open(filename,'r')
    lines = fp.readlines()
    fp2 = open('words.txt','r')
    lines1 = fp2.read().splitlines()
    fpo = open('output.txt','w')
    
    for line in lines:
        at_p = line.find('@') #Find first occurance of @ that helps to identify where to break string
        starting = line [:at_p].split()
        strating_target = starting[0].split('.')[0] #Target word to be disambiguated
        form = starting[0].split('.')[1] #Target word form
        line = line[at_p+1:] #Get rest of the line
        target_in_sentence = line[line.find('@')+1:line.rfind('@')] #Target word in the sentence
        context_words = get_sense_index(line,5,lines1,strating_target)
        ind = 1
        op = '1\n'        
        while ind <= context_words[1]:
            if ind == context_words[0]:
                op += '1\n'
            else:
                op += '0\n'
            ind += 1
        fpo.write(op)
    
def main():
    filename = raw_input('Enter file name to test: ')
    WSD_Dict(filename)
    
main()