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

dict_file = open('Dictionary.xml').read()

'''
    Find Glosses from XML file
    @return: all definitions of a gloss and if word is not in XML then return -1
'''
def find_gloss_from_file(str):
    global dict_file
    content = dict_file
    l = re.compile('<lexelt item="' + str + '.[a-z]">(.*?)</lexelt>', re.DOTALL |  re.IGNORECASE).findall(content)
    if len(l) > 0 :
        return re.compile('gloss="(.*)"').findall(l[0])        
    else:
        return -1

'''
    Remove junk content that is numbers and stopwords from the string
'''
def remove_junk(string1,lines1):
    string1 = re.sub('[0-9]+','',string1)
    
    for punct in string.punctuation:
        string1 = string1.replace(punct,'')
    
    temp_l1 = string1.split()
    important_words1 = filter(lambda x: x not in stopwords.words('english'), temp_l1)
    important_words1 = filter(lambda x: x not in lines1, important_words1)
    
    return ' '.join(important_words1)


'''
    Function to find all sub-sequences from a string
'''    
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

'''
    Find total overlap
'''    
def calculate_overall_score(s1,s2):
    seq1 = find_word_sequences(s1)
    total = 0
    for elem in seq1:
        if elem in s2:
            total += (elem.count(' ')+1) ** 2
    return total

'''
    Get bag of senses for a list of words
'''
def get_bag_of_senses(temp_words1):
    senses = []
    lmtzr = WordNetLemmatizer()
    temp_words1 = nltk.pos_tag(temp_words1.split())
    
    for t in temp_words1:
        try:
            if 'VB' in t[1]:
                senses.append(wordnet.synsets(lmtzr.lemmatize(t[0],'v')))
            else:
                senses.append(wordnet.synsets(t[0]))
        except:
            pass
        
    hypernyms = []
    for sense_l in senses:
        for s in sense_l:
            hypernyms.append(s.hypernyms())
    
    hyponyms = []
    for sense_l in senses:
        for s in sense_l:
            hyponyms.append(s.hyponyms())
            
    '''meronyms = []
    for sense_l in senses:
        for s in sense_l:
            meronyms.append(s.part_meronyms())        
    
    toponyms = []
    for sense_l in senses:
        for s in sense_l:
            toponyms.append(s.part_holonyms())'''
    
    definitions = []
    for sense_l in senses:
        if len(sense_l) > 1:
            for s in sense_l:
                definitions.append(s.definition)
    
    for sense_l in hypernyms:
        if len(sense_l) > 1:
            for s in sense_l:
                definitions.append(s.definition)
   
    for sense_l in hyponyms:
        if len(sense_l) > 1:
            for s in sense_l:
                definitions.append(s.definition)
    
    '''for sense_l in meronyms:
        for s in sense_l:
            definitions.append(s.name)
            
    for sense_l in toponyms:
        for s in sense_l:
            definitions.append(s.name)'''
                    
    definitions = ' '.join(definitions)
    return definitions

'''
    Get bag of senses for a list of words
'''
def get_minibag_of_senses(temp_words1):
    senses = []
    lmtzr = WordNetLemmatizer()
    temp_words1 = nltk.pos_tag(temp_words1.split())
    
    for t in temp_words1:
        try:
            if 'VB' in t[1]:
                senses.append(wordnet.synsets(lmtzr.lemmatize(t[0],'v')))
            else:
                senses.append(wordnet.synsets(t[0]))
        except:
            pass
    
    definitions = []
    for sense_l in senses:
        for s in sense_l:
            definitions.append(s.name)
            
    definitions = ' '.join(definitions)
    return definitions

def stem_funct(str):
    res = ''
    st = LancasterStemmer()
    for word in str.split(' '):
        res += ' ' + st.stem(word)
    return res

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
    
    important_words1 = remove_junk(temp1, lines1)
    important_words2 = remove_junk(temp2, lines1)
    
    '''if len(important_words1) > n:
        important_words1 = important_words1[len(important_words1)-n:]
    else:
        important_words1 = important_words1
    important_words2 = important_words2[:n]'''
    
    definitions = ''
    
    definitions += ' ' + get_bag_of_senses(important_words1)
    definitions += ' ' + get_bag_of_senses(important_words2)
    
    max_index = -1
    max = -1
    index = 1
    max_str = ''
    val = dict()    
    for s in find_gloss_from_file(target):
        bag2 = get_minibag_of_senses(remove_junk(s.lower(), lines1))#s.lower()#get_bag_of_senses(remove_junk(s.lower(), lines1).split(' '))
        stemmed1 = stem_funct(remove_junk(bag2, lines1))#stem_funct(remove_junk(bag2, lines1))
        stemmed2 = stem_funct(definitions)#stem_funct(definitions)
        
        temp_sc = calculate_overall_score(stemmed1, stemmed2)
        
        val[temp_sc] = index
        if temp_sc > max:
            max = temp_sc
            max_str = stemmed1
            max_index = index
            
        index += 1    
    
    val = sorted(val.items())
    print(val)
    return [[val[-2],val[-1]],len(find_gloss_from_file(target))]

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
        
        context_words = get_sense_index(line,3,lines1,strating_target)
        
        if context_words[0][1][0] - context_words[0][0][0] > 10:
            print(context_words[0][1][1])
            ind = 1
            op = '0\n'        
            while ind <= context_words[1]:
                if ind == context_words[0][1][1]:
                    op += '1\n'
                else:
                    op += '0\n'
                ind += 1
            fpo.write(op)
        else:
            ind = 1
            op = '0\n'      
            print(context_words[0][1][1],context_words[0][0][1])  
            while ind <= context_words[1]:
                if ind == context_words[0][1][1] or ind == context_words[0][0][1]:
                    op += '1\n'
                else:
                    op += '0\n'
                ind += 1
            fpo.write(op)
    
def main():
    filename = raw_input('Enter file name to test: ')
    WSD_Dict(filename)
    
main()