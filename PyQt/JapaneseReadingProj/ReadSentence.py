def read_sentences(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    sentences_dict = {}
    key = None

    for line in lines:
        line = line.strip()
        if '|' in line:
            key = line.split('|')[0].strip()
        elif line and key:
            sentences_dict[key] = line
            key = None

    return sentences_dict

# 示例文件路径
file_path1 = "c:/worksrc/VSCODE_PROJ/PythonCode/JapaneseReadingProj/backFiles/sentence1.txt"
file_path2 = "c:/worksrc/VSCODE_PROJ/PythonCode/JapaneseReadingProj/backFiles/sentence2.txt"

# 读取文件内容并创建字典
sentences_dict1 = read_sentences(file_path1)
sentences_dict2 = read_sentences(file_path2)

# 合并两个字典
combined_dict = {**sentences_dict1, **sentences_dict2}


