import os
import subprocess
from video_250831 import songs

FINAL_OUTPUT = "out.mp4"
FONT_PATH = "/home/da1sypetals/dev/pyncm/SourceHanSerifSC-Medium.otf"


def run_cmd(cmd):
    subprocess.run(cmd, check=True)


# 获取音频时长
def probe_duration(path: str) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            path,
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(result.stdout.strip())


def check_files():
    missing = []
    for s in songs:
        if not os.path.exists(s.clip_path):
            missing.append(s.clip_path)
        if not os.path.exists(s.context_path):
            missing.append(s.context_path)
    if missing:
        raise FileNotFoundError(f"缺少文件: {missing}")


def make_song_video(song, index):
    base_name = f"song_{index}"
    out_file = f"{base_name}.mp4"

    # 计算 part1 所需视频时长
    clip_dur = probe_duration(song.clip_path)
    part1_dur = 8.0 + 3.0 * clip_dur  # 8秒静音 + 3次 clip 播放

    # ========== part1 (第 i 首歌) ==========
    part1 = f"{base_name}_part1.mp4"
    cmd1 = [
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        f"color=c=black:s=1280x720:d={part1_dur}",
        "-vf",
        f"drawtext=fontfile={FONT_PATH}:"
        f"text='第{index}首歌':fontcolor=white:fontsize=60:x=(w-text_w)/2:y=(h-text_h)/2",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        part1,
    ]
    run_cmd(cmd1)

    audio1 = f"{base_name}_part1_audio.wav"
    silence2 = "anullsrc=r=44100:cl=stereo:d=2"
    filter_complex = "[0:a][1:a][0:a][1:a][0:a][1:a][0:a]concat=n=7:v=0:a=1[outa]"
    cmd1a = [
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        silence2,
        "-i",
        song.clip_path,
        "-filter_complex",
        filter_complex,
        "-map",
        "[outa]",
        audio1,
    ]
    run_cmd(cmd1a)

    part1_final = f"{base_name}_part1_final.mp4"
    cmd1b = [
        "ffmpeg",
        "-y",
        "-i",
        part1,
        "-i",
        audio1,
        "-shortest",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        part1_final,
    ]
    run_cmd(cmd1b)

    # ========== part2 (倒计时 3,2,1) ==========
    part2 = f"{base_name}_part2.mp4"
    drawtext = (
        f"drawtext=fontfile={FONT_PATH}:"
        "text='%{eif\\:floor(4-t)\\:d}':fontsize=120:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2"
    )
    cmd2 = [
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        "color=c=black:s=1280x720:d=3",
        "-f",
        "lavfi",
        "-i",
        "anullsrc=r=44100:cl=stereo:d=3",  # 3秒静音音轨
        "-vf",
        drawtext,
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-shortest",
        part2,
    ]
    run_cmd(cmd2)

    # ========== part3 (歌名 + 歌手) ==========
    part3 = f"{base_name}_part3.mp4"
    text = f"{song.name}\n{song.singer}"
    cmd3 = [
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        "color=c=black:s=1280x720:d=20",
        "-vf",
        f"drawtext=fontfile={FONT_PATH}:"
        f"text='{text}':fontsize=60:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        part3,
    ]
    run_cmd(cmd3)

    audio3 = f"{base_name}_part3_audio.wav"
    cmd3a = [
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        "anullsrc=r=44100:cl=stereo:d=0.3",
        "-i",
        song.context_path,
        "-f",
        "lavfi",
        "-i",
        "anullsrc=r=44100:cl=stereo:d=3",
        "-filter_complex",
        "[0:a][1:a][2:a]concat=n=3:v=0:a=1[outa]",
        "-map",
        "[outa]",
        audio3,
    ]
    run_cmd(cmd3a)

    part3_final = f"{base_name}_part3_final.mp4"
    cmd3b = [
        "ffmpeg",
        "-y",
        "-i",
        part3,
        "-i",
        audio3,
        "-shortest",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        part3_final,
    ]
    run_cmd(cmd3b)

    # ========== 合并三个part ==========
    txtlist = f"{base_name}_list.txt"
    with open(txtlist, "w", encoding="utf-8") as f:
        f.write(f"file '{part1_final}'\n")
        f.write(f"file '{part2}'\n")
        f.write(f"file '{part3_final}'\n")

    cmd_final = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        txtlist,
        "-c",
        "copy",
        out_file,
    ]
    run_cmd(cmd_final)

    # 清理中间文件
    for f in [part1, audio1, part1_final, part2, part3, audio3, part3_final, txtlist]:
        if os.path.exists(f):
            os.remove(f)

    return out_file


if __name__ == "__main__":
    check_files()

    song_videos = []
    for idx, song in enumerate(songs, 1):
        song_videos.append(make_song_video(song, idx))

    # 拼接所有歌曲
    biglist = "all_songs.txt"
    with open(biglist, "w", encoding="utf-8") as f:
        for v in song_videos:
            f.write(f"file '{os.path.abspath(v)}'\n")

    run_cmd(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", biglist, "-c", "copy", FINAL_OUTPUT])

    # 删除每首歌的视频和列表文件
    for f in song_videos + [biglist]:
        if os.path.exists(f):
            os.remove(f)

    print(f"最终视频已生成: {FINAL_OUTPUT}")
