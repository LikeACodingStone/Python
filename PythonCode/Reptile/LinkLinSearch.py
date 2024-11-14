import json
import requests
filePre = "cPlus3"
fileName = filePre + ".json"

content = ""
with open(fileName, "r", encoding="utf-8") as file:
    content = file.read()

data = json.loads(content)
jobLinks = []
for subData in data:
    jobLinks.append(subData["basecard_fulllink_链接"])

def check_keyword_in_web(url, keyword1, keyword2):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            if keyword1 in response.text and keyword2 in response.text:
                return True
            else:
                return False
    except requests.exceptions.RequestException as e:
        pass
    return False


fpCPlusKey = open(filePre + "_cPlusKey.txt","w",encoding='utf-8')
fpToeicKey = open(filePre + "_ToeicKey.txt","w", encoding='utf-8')
fpEnglishKey = open(filePre + "_EnglishKey.txt", "w", encoding='utf-8')

keywordCount = 0
for jobLink in jobLinks:
    if check_keyword_in_web(jobLink, "C++", ""):
        keywordCount += 1
        fpCPlusKey.write(jobLink + "\n")
        print(jobLink)
fpCPlusKey.close()

for jobLink in jobLinks:
    if check_keyword_in_web(jobLink, "C++", "Toeic"):
        fpToeicKey.write(jobLink + "\n")
fpToeicKey.close()

for jobLink in jobLinks:
    if check_keyword_in_web(jobLink, "C++", "English"):
        fpEnglishKey.write(jobLink + "\n")
fpToeicKey.close()

print("C++ Number=====>  " + str(keywordCount))
