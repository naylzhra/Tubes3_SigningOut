'''
Implementasi Allgoritma Levenshtein Distance
'''

threshold = 0.5

def levenshtein_distance(data : list, keyword : list) -> map :
    res = {key: 0 for key in keyword}
    for word in data:
        for key in keyword:
            dist = levenshtein_calculation(word, key)
            if is_pass(word, key, dist):
                res[key] += 1
    return res

def is_pass(string1 : str, string2 : str, dist: int) -> bool :
    m = max(len(string1), len(string2))
    sim = 1 - (dist / m)
    return sim > threshold

def levenshtein_calculation(string1 : str, string2 : str) -> int :
    
    m = max(len(string1), len(string2))
    n = min(len(string1), len(string2))
    longer = string1
    shorter = string2
    if (m != len(string1)):
        longer = string2
        shorter = string1

    # jika string1 or string2 is empty, maka ld = panjang string tidak kosong
    if m == 0:
        return n
    if n == 0:
        return m
    
    # membuat prev dan curr untuk mengecek perbedaan kedua string
    prev = [i for i in range(m+1)]
    curr = [0 for i in range(m+1)]
    
    # iterate untuk setiap character di shorter string
    for j in range(1, n +1):
        curr[0] = j
        # iterate untuk setiap character di longer string
        for k in range(1, m+1):
            if longer[k - 1] == shorter[j - 1]:
                curr[k] = prev[k - 1] # jika karakter sama, tidak ada biaya tambahan dari perhitungan sblmnya
            else:
                # cek minimum cost antara insert, remove, replace
                curr[k] = 1 + min(
                    curr[k - 1], # insert, cek dari biaya sejauh ini (pake curr)
                    prev[k],     # remove, cek biaya dari prev untuk dpt cost sampai curr char (jika di-remove)
                    prev[k - 1]  # replace, cek dari biaya prev (pengecekan terakhir sblm curr char di-replace)
                )
        # update prev dengan curr
        prev = curr.copy()
        
    # last index dari curr adalah nilai akhir levensh dist
    return curr[m]

# # driver
# if __name__ == "__main__":
#     with open('data/dummy.txt', 'r') as file:
#         line = file.readline().strip()
#         words = line.split(' ')
    
#         keywords = ['kook', 'coos', 'computer']

#         # Function call to calculate Levenshtein distance
#         result = levenshtein_distance(words, keywords)
#         print(result)