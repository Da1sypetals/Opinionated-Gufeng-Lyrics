编写一个脚本，导入这个文件，然后生成这样的视频：
首先检查所有的path 包括clip path和context path都存在。
然后：对每一首歌：
画面一：“第i首歌” 音频：空2s - 播放clip path的音频-空2s-播放clip path的音频-空2s-播放clip path的音频-空2s  
画面2：倒计时三秒，画面对应为3, 2, 1 没有音频  
画面3：第一行：歌名 第二行：歌手名 音频：空0.3s - 播放 context path的音频一次 