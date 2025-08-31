from pydantic.dataclasses import dataclass


@dataclass
class Song:
    name: str
    singer: str
    clip_path: str
    context_path: str


songs = [
    Song(
        name="木兰行",
        singer="忘川风华录",
        clip_path="vid1/mulanx.mp3",
        context_path="vid1/mulanx.mp3",
    ),
    Song(
        name="双生蝶",
        singer="阿yueyue",
        clip_path="vid1/ssdie.mp3",
        context_path="vid1/ssdie.mp3",
    ),
    Song(
        name="古龙群侠传",
        singer="河图",
        clip_path="vid1/gulong.mp3",
        context_path="vid1/gulong.mp3",
    ),
    Song(
        name="依山观澜",
        singer="河图",
        clip_path="vid1/yishanguanl.mp3",
        context_path="vid1/yishanguanl.mp3",
    ),
    Song(
        name="敢归云间宿",
        singer="三无",
        clip_path="vid1/ggyunjiansu.mp3",
        context_path="vid1/ggyunjiansu.mp3",
    ),
    Song(
        name="业火苍云歌",
        singer="aaa",
        clip_path="vid1/yehuocyg.mp3",
        context_path="vid1/yehuocyg.mp3",
    ),
    Song(
        name="腐草为萤",
        singer="银临",
        clip_path="vid1/fucaowy.mp3",
        context_path="vid1/fucaowy.mp3",
    ),
    Song(
        name="祖籁",
        singer="黄诗扶",
        clip_path="vid1/zulai.mp3",
        context_path="vid1/zulai.mp3",
    ),
    Song(
        name="易水诀",
        singer="忘川风华录",
        clip_path="vid1/yishuijue.mp3",
        context_path="vid1/yishuijue.mp3",
    ),
    Song(
        name="夜奔",
        singer="黄诗扶",
        clip_path="vid1/yeben.mp3",
        context_path="vid1/yeben.mp3",
    ),
    Song(
        name="心上秋",
        singer="忘川风华录",
        clip_path="vid1/xinshangq.mp3",
        context_path="vid1/xinshangq.mp3",
    ),
    Song(
        name="倾尽天下",
        singer="河图",
        clip_path="vid1/qingjin.mp3",
        context_path="vid1/qingjin.mp3",
    ),
]
