# 二次元音乐库 · Anime Music Library

一个独立的二次元音乐收藏仓库，支持动漫 OP/ED、游戏 OST、Vocaloid、同人音乐、纯音乐分类。

## 在线使用
启用 GitHub Pages（Settings → Pages → Deploy from a branch → main / root）后即可通过 `https://tyqittle.github.io/anime-music-library/` 访问。

## 目录
- `index.html` — 音乐浏览与播放器（搜索、分类、队列、进度、音量、单曲循环）
- `data/tracks.json` — 已收录且具有合法播放链接的音乐数据
- `music/` — 可按作品和类别上传获准分发的 MP3/OGG/FLAC 文件
- `covers/` — 封面素材（确保有使用权）

## 添加歌曲
在 `data/tracks.json` 的 `tracks` 数组中添加：
```json
{"id":"unique-id","title":"歌曲名","artist":"歌手","series":"作品","category":"动画 OP/ED","src":"music/作品名/歌曲.mp3","cover":"","license":"来源或许可说明"}
```
`category` 建议使用：动画 OP/ED、游戏 OST、Vocaloid、同人音乐、纯音乐、其他。

也可以使用首页的“本地试听”功能，选取电脑上的音频文件直接在浏览器播放，不会上传到 GitHub。

> 为避免版权问题，仓库不会自动收录未经授权的商业歌曲。外链失效或无法跨域播放时，请换成合法托管的音频文件。

## 已核实的完整歌曲
- **FREELY TOMORROW** — Mitchie M feat. 初音未来；3分59秒；[CC BY 3.0，来源 Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Freely_Tomorrow.ogg)。

此前加入的 VOCALOID / Synthesizer V 演示短音频已从曲库删除。新收录必须是完整作品且具有允许公开分发的授权；单独列出处不等于取得版权许可。
