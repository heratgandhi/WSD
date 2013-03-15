import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer
import string
import re

dict_file = open('Dictionary.xml').read()

train = open('Training.data').read().splitlines()

train_dict = dict()

for line in train:
        at_p = line.find('@') #Find first occurance of @ that helps to identify where to break string
        starting = line [:at_p].split()
        starting_target = starting[0].split('.')[0] #Target word to be disambiguated
        form = starting[0].split('.')[1] #Target word form
        line = line[at_p+1:] #Get rest of the line
        target_in_sentence = line[line.find('@')+1:line.rfind('@')] #Target word in the sentence
        
        bits = starting[1:]
        
        if bits[0] == '0':
            if starting_target+' '+str(bits.index('1')) in train_dict.keys():
                train_dict[starting_target+' '+str(bits.index('1'))].update(set(line.split()))
            else:
                train_dict[starting_target+' '+str(bits.index('1'))] = set(line.split())


test = open('test.data').read().splitlines()
fpo = open('output.txt','w')
lineno = 0

for line in test:
        at_p = line.find('@') #Find first occurance of @ that helps to identify where to break string
        starting = line [:at_p].split()
        starting_target = starting[0].split('.')[0] #Target word to be disambiguated
        form = starting[0].split('.')[1] #Target word form
        line = line[at_p+1:] #Get rest of the line
        target_in_sentence = line[line.find('@')+1:line.rfind('@')] #Target word in the sentence
        
        max = -1
        max_i = -1
        max_cnt = 0
        
        total_keys = len(train_dict.keys())
        un_keys = 0
        
        for key in train_dict.keys():
            if starting_target in key:
                max_cnt += 1
                intersect_ss = train_dict[key].intersection(set(line.split()))
                if len(intersect_ss) > max:
                    max = len(intersect_ss)
                    max_i = key.split()[1]
            else:
                un_keys += 1
        
        ind = 1
        op = '0\n'
        #lineno += 1        
        while ind <= max_cnt:
            if ind == int(max_i):
                op += '1\n'
                #lineno += 1
            else:
                op += '0\n'
                #lineno += 1
            ind += 1
        fpo.write(op)
        
        print(max_i,max_cnt,total_keys,un_keys,op)#,lineno)