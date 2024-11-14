import os
from pydub import AudioSegment
import shutil

FileLength = 0
for root, dirs, files in os.walk("E:/Temp_Files/Japanese/Combi_Chinese_Japanese/Generated"):
    for file in files:
        if file.startswith("CH_EXP"):                
            FileLength =  FileLength + 1           
    
 
blank1s = "E:\Temp_Files\Japanese\Combi_Chinese_Japanese\Blank_1s.mp3"
blankMp3_1s = AudioSegment.from_mp3(blank1s)
blank2s = "E:\Temp_Files\Japanese\Combi_Chinese_Japanese\Blank_2s.mp3"
blankMp3_2s = AudioSegment.from_mp3(blank2s)
 
CH_JP_Len = 0
for root, dirs, files in os.walk("E:/Temp_Files/Japanese/Combi_Chinese_Japanese/CH_JP"):
    CH_JP_Len = len(files)
    
CH_JP_Test_Len = 0
for root, dirs, files in os.walk("E:/Temp_Files/Japanese/Combi_Chinese_Japanese/CH_JP_Test/CH"):
    CH_JP_Test_Len = len(files)
CH_JP_Test_Len = (int)(CH_JP_Test_Len / 2)

for index in range(FileLength):
    chMp3 = "E:/Temp_Files/Japanese/Combi_Chinese_Japanese/Generated/CH_EXP_" + str(index) + ".mp3"
    jpMp3 = "E:/Temp_Files/Japanese/Combi_Chinese_Japanese/Generated/JP_EXP_" + str(index) + ".mp3"
    chMp3File = AudioSegment.from_mp3(chMp3)
    jpMp3File = AudioSegment.from_mp3(jpMp3)
   
    chTestMp3 = "E:/Temp_Files/Japanese/Combi_Chinese_Japanese/CH_JP_Test/CH/CH_EXP_" + str(CH_JP_Test_Len) + ".mp3"
    jpTestMp3 = "E:/Temp_Files/Japanese/Combi_Chinese_Japanese/CH_JP_Test/JP/JP_EXP_" + str(CH_JP_Test_Len) + ".mp3"
    chTestMp3File = chMp3File + blankMp3_2s + blankMp3_2s
    jpTestMp3File = jpMp3File + blankMp3_2s + blankMp3_2s
    CH_JP_Test_Len = CH_JP_Test_Len + 1
    chTestMp3File.export(chTestMp3,format='mp3')
    jpTestMp3File.export(jpTestMp3,format='mp3')
    print(chTestMp3, CH_JP_Test_Len)
    
    
    outMp3File = chMp3File + blankMp3_1s + jpMp3File + blankMp3_2s
    outMp3 = "E:/Temp_Files/Japanese/Combi_Chinese_Japanese/CH_JP/CH_JP_" + str(CH_JP_Len) + ".mp3"
    CH_JP_Len = CH_JP_Len + 1
    outMp3File.export(outMp3,format='mp3')
    print(outMp3, index)
    
