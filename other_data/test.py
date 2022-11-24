import hashlib

file = ("TINF22CS1_test.ics")
BLOCK_SIZE = 65536

file_hash = hashlib.sha256()
with open(file, "rb") as f:
    fb = f.read(BLOCK_SIZE)
    while len(fb) > 0:
        file_hash.update(fb)
        fb = f.read(BLOCK_SIZE)

hash = file_hash.hexdigest()
print(hash) # for debugging

open("cal_hash.txt", "w").write(hash)