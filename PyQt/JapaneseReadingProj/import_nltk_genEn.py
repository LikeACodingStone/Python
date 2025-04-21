import nltk
from nltk.corpus import brown
from nltk import bigrams, trigrams
from collections import defaultdict
import random

# 下载所需的 NLTK 数据集
nltk.download('brown')

# 构建三元组模型
model = defaultdict(lambda: defaultdict(lambda: 0))
for sentence in brown.sents():
    for w1, w2, w3 in trigrams(sentence, pad_right=True, pad_left=True):
        model[(w1, w2)][w3] += 1

# 将计数转换为概率
for w1_w2 in model:
    total_count = float(sum(model[w1_w2].values()))
    for w3 in model[w1_w2]:
        model[w1_w2][w3] /= total_count

# 生成句子
def generate_sentence(seed, length=15):
    sentence = list(seed)
    for _ in range(length):
        w1, w2 = sentence[-2], sentence[-1]
        next_word = max(model[(w1, w2)], key=model[(w1, w2)].get)
        sentence.append(next_word)
        if next_word is None:
            break
    return ' '.join([word for word in sentence if word])

seed = ("the", "quick")
print(generate_sentence(seed))