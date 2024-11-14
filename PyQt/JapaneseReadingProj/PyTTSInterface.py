import pyttsx3
class PyTTSInterface:
    def __init__(self, language, rate = 100, volume = 1.0):
        self._language = language
        self._engine = pyttsx3.init()
        self._rate = rate
        self._volume = volume
        self.setRateAndVolume(self._engine, rate, volume)
        self.setLanguage(language, self._engine)
    def setRateAndVolume(self, engine, rate, volume):
        engine.setProperty('rate', rate)
        engine.setProperty('volume', volume)
    def setLanguage(self, language, engine):
        LanguageList = {}
        intKeyIndex = 0
        voices = engine.getProperty('voices')
        for voice in voices:
            if "English" in voice.name:
                LanguageList["English"] = intKeyIndex
            if "Chinese" in voice.name:
                LanguageList["Chinese"] = intKeyIndex
            if "Japanese" in voice.name:
                LanguageList["Japanese"] = intKeyIndex
            intKeyIndex = intKeyIndex + 1
        LanguageId = LanguageList[language]
        engine.setProperty('voice', voices[LanguageId].id)
    
    def playAudioCont(self, text):
        self._engine.say(text)
        self._engine.runAndWait()

