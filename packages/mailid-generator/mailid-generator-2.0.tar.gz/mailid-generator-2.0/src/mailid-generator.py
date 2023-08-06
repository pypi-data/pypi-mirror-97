import random
import string
def rand_email_id():
    letters = list(string.ascii_lowercase[:26])
    s=''
    for i in range(4):
        s=s+letters[random.randint(0,25)]
    for k in range(3):
        n=random.randint(0,9)
        s=s+str(n)
    return (s+"@gmail.com")


