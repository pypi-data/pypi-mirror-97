import random
import string
letters=list(string.ascii_lowercase[:26])
def rand_email_id(l):
    s=''
    for i in range(4):
        s=s+l[random.randint(0,25)]
    for k in range(3):
        n=random.randint(0,9)
        s=s+str(n)
    return (s+"@gmail.com")
print(rand_email_id(letters))

