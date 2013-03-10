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
    
def calculate_overall_scorre(s1,s2):
    seq1 = find_word_sequences(s1)
    total = 0
    for elem in seq1:
        if elem in s2:
            print(elem)
            total += (elem.count(' ')+1) ** 2
    return total
        
print(calculate_overall_scorre('ABC BMNSBMD BSN xzcvzn', 'ABC sddhfkjs BSN xzcvzn'))        