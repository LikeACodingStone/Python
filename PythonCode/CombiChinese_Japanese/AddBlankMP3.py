import os
from pydub import AudioSegment

blank = "E:\Temp_Files\Japanese\Blank.mp3"
blankMp3 = AudioSegment.from_mp3(blank)


folder3 = "E:\Temp_Files\Japanese\COMBI"
for rot, dirs, files in os.walk(folder3):
    for file in files:
        absP = rot + os.sep + file
        absP3 = AudioSegment.from_mp3(absP)
        outMP3 = absP3 + blankMp3
        outMP3.export(absP,format='mp3')
        
        
