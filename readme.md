## 前言

学习Python快一年半时间，做过需对基于django的管理平台后端的开发，比如存储管理平台、监控类管理平台。
最近爬虫基本没有接触，先做一个小小爬虫，爬虫网易云音乐，制作成api接口方便调用。

## 项目计划

- 阶段一：制作API接口
- 阶段二：使用vue做前段页面，制作一个vue的音乐平台
- 阶段三：学习并编写手机app，调用平台API接口

## 音乐API接口

### 搜索歌曲API

- **简要描述：**搜索歌曲API接口
- **请求**`GET/api/music/search_music?keyword=因为爱上你&page=10`
- **请求阐述示例：**无
- **请求参数示例：**无

- **请求参数说明：**无

- **返回数据示例：**

```json
{
    "status": 0,
    "msg": "搜索成功",
    "data": [
        {
            "al_name": "美丽心境",
         	"author": "孙思怡",
         	"id": 291875,
         	"img": "http://p2.music.126.net/MiRh-nMg3AADgllxeXGDVw==/918092209225224.jpg",
         	"song_name": "因为爱上你"
        }
    ]
}
```

- **返回参数示例：**

|    键     | 类型 |       说明       |
| :-------: | :--: | :--------------: |
|  status   | int  | 0：成功、1：失败 |
|    msg    | str  |     描述信息     |
|  al_name  | str  |       专辑       |
|  author   | str  |       作者       |
|    id     | int  |      歌曲id      |
|    img    | str  |     歌曲图片     |
| song_name | str  |     歌曲名称     |