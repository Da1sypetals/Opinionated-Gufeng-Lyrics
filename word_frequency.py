import os
from collections import Counter

def count_2char_combinations(directory, k=50):
    """
    统计指定目录下所有txt文件中任意相邻的两个字符组合的词频，并返回前k个高频组合及其频率。
    :param directory: 目录路径
    :param k: 返回的高频组合数量
    :return: 前k个高频组合及其频率
    """
    combination_counter = Counter()
    
    # 遍历目录下的所有txt文件
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    for i in range(len(line) - 1):
                        combination = line[i:i+2]
                        combination_counter[combination] += 1
    
    # 返回前k个高频组合
    return combination_counter.most_common(k)

if __name__ == "__main__":
    directory = "filtered_songs"
    k = 50
    
    if not os.path.exists(directory):
        print(f"目录 {directory} 不存在！")
    else:
        top_combinations = count_2char_combinations(directory, k)
        print(f"Top {k} 相邻两字符组合及其频率：")
        for combination, count in top_combinations:
            print(f"{combination}: {count}")