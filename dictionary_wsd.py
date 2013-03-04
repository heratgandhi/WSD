'''
    Dictionary based WSD
    Author: Herat Gandhi
'''

'''
    Function to perform WSD based on dictionaries
    @param filename Filename to be used for testing
'''
def WSD_Dict(filename):
    fp = open(filename,'r')
    lines = fp.readlines()
    for line in lines:
        at_p = line.find('@') #Find first occurance of @ that helps to identify where to break string
        starting = line [:at_p].split()
        strating_target = starting[0].split('.')[0] #Target word to be disambiguated
        form = starting[0].split('.')[1] #Target word form
        line = line[at_p+1:] #Get rest of the line
        target_in_sentence = line[line.find('@')+1:line.rfind('@')] #Target word in the sentence
        #line = line.replace('@','')

    
def main():
    filename = input('Enter file name to test: ')
    WSD_Dict(filename)
    
main()