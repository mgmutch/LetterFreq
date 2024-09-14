
import string

left_column = []
right_column = []

def to6(x):
    if (int(x/6)):
        return to6(int(x/6))+str(x%6)
    return str(x%6)

nums = [1, 2, 3, 4, 6, 8]

for i in range(50000, 1, -1):
    x = "%06d" % int(to6(i))
    if (len(x) == 6) and (len(set(x)) == 6):
        ans = ""
        for a in x:
            ans += str(nums[int(a)])
        left_column.append(ans)

primes = [0, 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]
alphabets = list(string.ascii_lowercase)
for a in range(0,26):
    for p in range(0,26):
        right_column.append("(%d, %s)" % (primes[p], alphabets[a]))
for i in range(1,45):
    right_column.append(str(i))

for i in range(len(left_column)):
    print(left_column[i] , right_column[i])


