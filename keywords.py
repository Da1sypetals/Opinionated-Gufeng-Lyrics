import subprocess

keywords = [
    "时光",
    "生死",
    "杨柳",
    "四季",
    "少年",
    "红尘",
    "相思",
    "春秋",
    "眉目",
    "桃花",
    "天地",
    "岁月",
    "多少",
    "春风",
    "故人",
    "万里",
    "故事",
    "青山",
    "相逢",
    "明月",
    "心上",
    "江湖",
    "风流",
    "梦里",
]

for keyword in keywords:
    subprocess.run(["python", "query.py", keyword])
