import os
absChName = []
for root, dirs, files in os.walk("E:/CombiMp3/ChJapanMp3"):
    for file in files:
        absDir = root + os.sep + file
        absChName.append(absDir)
        print(absDir)


from pydub import AudioSegment
mp3Blank = AudioSegment.from_mp3("blank.mp3")
for file in absChName:
    mp3Input = AudioSegment.from_mp3(file)
    
    tmBlank =len(mp3Blank)
    tmInput =len(mp3Input)

    outMP3 = mp3Input+mp3Blank
    outMP3.export(file,format='mp3')
    
