enc = "àÒÆÞ¦È¬ëÙ£ÖÓÚåÛÑ¢ÕÓÉÕËÆÒÇÚËí"
key = "picoctf"

res = ""
for i in range(len(enc)):
    res += chr((ord(enc[i]) - ord(key[i % len(key)]) + 256) % 256)

print(res)
