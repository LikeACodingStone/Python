import os
mp3ListRCK = []
mp3ListMidi = []

for root, dirs, files in os.walk("F:\MidiMp3Music", topdown=False):
    for mp3 in files:
        listName = []
        listFilter = []
        if "_" in mp3:
            listName = mp3.split("_")
        else:
            listName = mp3.split(" ")
        try:
            listFilter.append(listName[-1].split(".")[0])
            listFilter.append(listName[-2])
            listFilter.append(listName[-3])
        
        except IndexError:
            pass
        #print(listFilter)
        mp3ListRCK.append(listFilter)
         
        
for root, dirs, files in os.walk("F:\MidiMp3Music", topdown=False):
    for mp3 in files:
        listName = []
        listFilterMidi = []
        if "_" in mp3:
            listName = mp3.split("_")
        else:
            listName = mp3.split(" ")
        try:
            listFilterMidi.append(listName[-1].split(".")[0])
            listFilterMidi.append(listName[-2])
            listFilterMidi.append(listName[-3])
  
        except IndexError:
            pass
        mp3ListMidi.append(listFilterMidi)
           
        count = 0
        for already in mp3ListRCK:
            if not already or not listFilterMidi:
                pass
            try:
                if already[0] == listFilterMidi[0] and  already[1] == listFilterMidi[1] \
                    and already[2] == listFilterMidi[2]:             
                    count = count + 1
            except IndexError:
                pass
        if count > 1:
            print(mp3)
            absPath = root + os.sep + mp3
            #os.remove(absPath)
      

        



