from pydub import AudioSegment
import pydub
import audioread
import numpy as np
import os

def detect_silence(audio_file, threshold=-50, min_silence_duration=20):
    # 使用pydub加载音频文件
    audio = AudioSegment.from_file(audio_file, format="mp3")

    # 将pydub音频对象转换为numpy数组
    audio_data = np.array(audio.get_array_of_samples())

    # 将毫秒转换为采样点数
    min_silence_samples = int(min_silence_duration * audio.frame_rate / 1000)

    # 检测空白部分
    silence_ranges = pydub.silence.detect_silence(audio, silence_thresh=threshold, min_silence_len=min_silence_samples)
    print("over")
    # 打印空白部分的起始和结束时间
    
    index = 0
    voiceList = []
    voiceList.append(0)
    for start, end in silence_ranges:
        voiceList.append(start)
        voiceList.append(end)
    
    for tmIndex in  range(len(voiceList)):
        if(tmIndex % 2) != 0:
            continue
        exportName = "E:\Temp_Files\Japanese\Combi_Chinese_Japanese\Generated" + os.sep + "CH_EXP_" + str(index) + ".mp3"
        segment = audio[voiceList[tmIndex]:voiceList[tmIndex + 1]+650]
        segment.export(exportName, format="mp3")
        index = index + 1
        print("Silence range:", voiceList[tmIndex], "ms -", voiceList[tmIndex + 1], "ms")

# 音频文件路径
audio_file = "E:\Temp_Files\Japanese\Combi_Chinese_Japanese\chTest.mp3"

# 检测MP3音频中的空白
detect_silence(audio_file)