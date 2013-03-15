'''
    Dictionary based WSD
    Author: Herat Gandhi, Jyoti Pandey, Saikiran, Vinayaka Dattatraya
'''

import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer
import string
import re

#Read dictionary file in the memory so that we don't have to load file again and again
dict_file = open('Dictionary.xml').read()

'''
    Find Glosses from XML file
    @param string: word for which we want to find senses
    @return: all definitions of a gloss and if word is not in XML then return -1
'''
def find_gloss_from_file(str):
    global dict_file
    content = dict_file
    #Parse using regex
    l = re.compile('<lexelt item="' + str + '.[a-z]">(.*?)</lexelt>', re.DOTALL |  re.IGNORECASE).findall(content)
    if len(l) > 0 :
        #return all the glosses
        return re.compile('gloss="(.*)"').findall(l[0])
    else:
        return -1

'''
    Remove junk content that is numbers and stopwords from the string
    @param string1: string from which we want to remove junk
    @param lines1: lines from which we want to ignore words
    @return: Clean string with no junk parts
'''
def remove_junk(string1,lines1):
    #Regex for numbers
    string1 = re.sub('[0-9]+','',string1)
    #Remove punctuations
    for punct in string.punctuation:
        string1 = string1.replace(punct,'')
    #Remove Stopwords and unimportant words
    temp_l1 = string1.split()
    important_words1 = filter(lambda x: x not in stopwords.words('english'), temp_l1)
    important_words1 = filter(lambda x: x not in lines1, important_words1)
    return ' '.join(important_words1)


'''
    Function to find all sub-sequences from a string
    @param s1: String for which we want to find sub-sequences
    @return List: List of all sub-sequences of the input string 
'''    
def find_word_sequences(s1):
    s1l = s1.split()    
    i = 0
    j = 0
    k = 1    
    new_s1l = []
    str = ''
    #Iterate through string and find the subsequences of k lengths
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
    @param s1,s2: Strings for which we want to find overlaps
    @return total: Integer representing weighted overlap score  
'''    
def calculate_overall_score(s1,s2):
    #Find sub-sequences of a string
    seq1 = find_word_sequences(s1)
    total = 0
    #Check whether we find a sub-string in a string or not
    for elem in seq1:
        if elem in s2:
            #if we found a match then check its length and take its square
            total += (elem.count(' ')+1) ** 2
    return total

'''
    Get bag of senses for a list of words
    @param temp_words1: Words for which we want to find bag of senses
    @return definitions: Definitions of context words also include hypernyms and hyponyms
'''
def get_bag_of_senses(temp_words1):
    senses = []
    lmtzr = WordNetLemmatizer()
    temp_words1 = nltk.pos_tag(temp_words1.split())
    #Find the synsets
    for t in temp_words1:
        try:
            if 'VB' in t[1]:
                senses.append(wordnet.synsets(lmtzr.lemmatize(t[0],'v')))
            else:
                senses.append(wordnet.synsets(t[0]))
        except:
            pass
    #Find hypernyms' synsets    
    hypernyms = []
    for sense_l in senses:
        for s in sense_l:
            hypernyms.append(s.hypernyms())
    #Find hyponyms' synsets
    hyponyms = []
    for sense_l in senses:
        for s in sense_l:
            hyponyms.append(s.hyponyms())
            
    definitions = []
    for sense_l in senses:
        for s in sense_l:
            definitions.append(s.definition)
    
    for sense_l in hypernyms:
        for s in sense_l:
            definitions.append(s.name)
   
    for sense_l in hyponyms:
        for s in sense_l:
            definitions.append(s.name)
    
    definitions = ' '.join(definitions)
    return definitions

'''
    Get bag of senses for target word
    @param list: List of senses of a target word
    @return string: String containing all the senses
'''
def get_minibag_of_senses(temp_words1):
    senses = []
    lmtzr = WordNetLemmatizer()
    temp_words1 = nltk.pos_tag(temp_words1.split())
    #Find the synsets
    for t in temp_words1:
        try:
            if 'VB' in t[1]:
                senses.append(wordnet.synsets(lmtzr.lemmatize(t[0],'v')))
            else:
                senses.append(wordnet.synsets(t[0]))
        except:
            pass    
    #Find senses
    definitions = []
    for sense_l in senses:
        for s in sense_l:
            definitions.append(s.name)
            
    definitions = ' '.join(definitions)
    return definitions

'''
    Stemming function
    @param string: String which we want to stem
    @return string: String with stemmed words
'''
def stem_funct(str):
    res = ''
    #Use NLTK's stemmer
    st = LancasterStemmer()
    #Stem each word and append the result in the string
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
    #Use regex to remove numbers
    temp = re.sub('[0-9]+','',temp)
    
    #Get context and target word
    first_at = temp.find('@')
    last_at = temp.rfind('@')+1
    
    temp1 = temp[:first_at]
    temp2 = temp[last_at:]
    #Remove junk from context words
    important_words1 = remove_junk(temp1, lines1)
    important_words2 = remove_junk(temp2, lines1)
    
    definitions = ''
    #Get senses for the context words
    definitions += ' ' + get_bag_of_senses(important_words1)
    definitions += ' ' + get_bag_of_senses(important_words2)
    
    max_index = -1
    max = -1
    index = 1
    max_str = ''
    #For all the senses find the perfect sense
    val = []    
    for s in find_gloss_from_file(target):
        bag2 = get_minibag_of_senses(remove_junk(s.lower(), lines1))
        #Stem the string
        stemmed1 = stem_funct(remove_junk(bag2, lines1))
        #Stem the string        
        stemmed2 = stem_funct(definitions)
        #Find the overlapping score        
        temp_sc = calculate_overall_score(stemmed1, stemmed2) * 1.00 / len(stemmed1)
        #Append the score in the list
        val.append(temp_sc)
        #Find the maximum value
        if temp_sc > max:
            max = temp_sc
            max_str = stemmed1
            max_index = index
        
        index += 1
    #Return the length and sense indexe/s
    return [max_index,len(find_gloss_from_file(target))]

'''
    Function to perform WSD based on dictionaries
    @param filename: Filename to be used for testing
    Writes output to output.txt
'''
def WSD_Dict(filename):
    fp = open(filename,'r') #Open file for reading
    lines = fp.readlines() #Get lines
    fp2 = open('words.txt','r') #Open words from which we ignore unimportant words
    lines1 = fp2.read().splitlines() #Lines from unimportant file
    fpo = open('output.txt','w') #Output file
    
    for line in lines:
        at_p = line.find('@') #Find first occurance of @ that helps to identify where to break string
        starting = line [:at_p].split()
        strating_target = starting[0].split('.')[0] #Target word to be disambiguated
        form = starting[0].split('.')[1] #Target word form
        line = line[at_p+1:] #Get rest of the line
        target_in_sentence = line[line.find('@')+1:line.rfind('@')] #Target word in the sentence
        
        context_words = get_sense_index(line,10,lines1,strating_target) #Get sense from the context
        if context_words[0] != -1: #If -1 is returned then we have multiple sense predictions
            ind = 1
            op = '0\n'        
            while ind <= context_words[1]:
                if ind == context_words[0]:
                    op += '1\n'
                else:
                    op += '0\n'
                ind += 1
            fpo.write(op)
        else:
            ind = 1
            op = '1\n'        
            while ind <= context_words[1]:
                op += '0\n'
                ind += 1
            fpo.write(op) #Write binary string to the file
    
def main():
    filename = raw_input('Enter file name to test: ')
    WSD_Dict(filename)
    
main()