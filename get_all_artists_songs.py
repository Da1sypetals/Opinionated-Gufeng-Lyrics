#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
读取artists_output.json并批量获取所有艺术家的歌曲
"""

import os
import json
import argparse
from pyncm.apis.artist import GetArtistTracks, GetArtistDetails
from pyncm.apis.track import GetTrackLyricsNew
 
credit_keywords = [
    "作词",
    "作曲",
    "编曲",
    "制作",
    "策划",
    "编剧",
    "混音",
    "统筹",
    "题字",
]


def save_songs(singer_id: str, max_tracks=100):
    """
    获取歌手的曲目并保存到本地
    Args:
        singer_id (str): 歌手ID
        max_tracks (int, optional): 最多获取的曲目数量. Defaults to 100.
    """
    # 获取歌手名称
    artist_details = GetArtistDetails(singer_id)

    if artist_details.get("data") and artist_details["data"].get("artist"):
        singer_name = artist_details["data"]["artist"]["name"]
    else:
        print(f"未找到歌手 ID {singer_id} 的详情，将使用歌手ID作为目录名")
        singer_name = singer_id

    # 创建歌曲目录
    songs_dir = os.path.join("lyrics", singer_name)
    os.makedirs(songs_dir, exist_ok=True)

    # 获取歌手的曲目
    tracks_response = GetArtistTracks(singer_id, limit=max_tracks, order="hot")
    if not tracks_response.get("songs"):
        print(f"未找到歌手 {singer_name} 的曲目")
        return

    # 遍历曲目并保存
    for track in tracks_response["songs"]:
        track_name = track["name"]
        track_id = track["id"]
        print(f"正在处理歌曲: {track_name} (ID: {track_id})")

        # 保存曲目信息到文件
        # 对文件名进行安全处理
        safe_track_name = track_name.replace("/", "-").replace("(", "[").replace(")", "]")
        song_file = os.path.join(songs_dir, f"{safe_track_name}.txt")

        # 确保目录存在
        os.makedirs(songs_dir, exist_ok=True)

        try:
            # 获取歌词
            lyrics_data = GetTrackLyricsNew(track_id)

            # 保存歌词内容
            with open(song_file, "w", encoding="utf-8") as f:
                if lyrics_data.get("lrc") and lyrics_data["lrc"].get("lyric"):
                    # 如果解析失败，回退到原始处理方式
                    lyrics = lyrics_data["lrc"]["lyric"]
                    cleaned_lyrics = "\n".join(
                        line.split("]", 1)[1]
                        for line in lyrics.splitlines()
                        if not line.startswith('{"t":')
                        and not any(keyword in line for keyword in credit_keywords)
                    )
                    f.write(cleaned_lyrics.strip())
                else:
                    f.write(f"歌曲ID: {track_id}\n歌曲名: {track_name}\n\n未找到歌词")
            print(f"歌词已保存到: {song_file}")
        except Exception as e:
            print(f"无法获取或保存歌词 {track_name}: {str(e)}")


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='批量获取艺术家的歌曲')
    parser.add_argument('--overwrite', action='store_true', help='强制删除lyrics目录下的所有内容')
    args = parser.parse_args()

    # 如果指定了--overwrite，删除lyrics目录及其内容
    if args.overwrite and os.path.exists("lyrics"):
        import shutil
        shutil.rmtree("lyrics")

    # 读取artists_output.json
    try:
        with open("artists_output.json", "r", encoding="utf-8") as f:
            artists_data = json.load(f)
    except FileNotFoundError:
        print("错误: 未找到artists_output.json文件")
        return

    # 处理每个艺术家
    for artist in artists_data:
        print(f"\n开始处理艺术家: {artist['name']} (ID: {artist['id']})")
        save_songs(artist["id"])


if __name__ == "__main__":
    main()
