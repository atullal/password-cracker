import os
import hashlib
import string

small_letters = [*string.ascii_lowercase]
capital_letters = [*string.ascii_uppercase]
all_letters = small_letters+capital_letters

file_hash_dict = {}

# newpath = r'./dictionary/small_a.txt' 
# if os.path.exists(newpath):
#     print("hello")
# print("world")


for l1 in all_letters:
    for l2 in all_letters:
        if 'A' <= l1 <= 'Z':
            prefix1 = "capital_"
        else:
            prefix1 = "small_"
        if 'A' <= l2 <= 'Z':
            prefix2 = "capital_"
        else:
            prefix2 = "small_"
        filename = prefix1+l1+prefix2+l2+".txt"
        file_hash_dict[filename] = hashlib.md5(open("./dictionary/"+filename,'rb').read()).hexdigest()

print(file_hash_dict)