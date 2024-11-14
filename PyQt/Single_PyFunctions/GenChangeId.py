import random
import string

def generate_change_id(length=41):
    # 生成一个指定长度的随机字符串
    characters = string.ascii_letters + string.digits
    change_id = ''.join(random.choices(characters, k=length))
    return change_id

# 示例用法
if __name__ == "__main__":
    print("生成的 Change-ID:", generate_change_id())