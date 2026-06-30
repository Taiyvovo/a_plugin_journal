# 手帐生成器 astrbot_plugin_journal

指令触发的手帐风格文转图插件。简约文艺 + 复古拼贴风:米黄纸张纹理、washi tape 胶带、圆形邮戳日期章、手写体标题。

## 安装

1. 把整个 `astrbot_plugin_journal` 文件夹放进 `AstrBot/data/plugins/` 目录
2. 在 WebUI 插件管理里重载插件(或重启 AstrBot)

## 使用

```
/手帐 今天发生的事情...
```

支持多行(换行会自动分段),例如在 QQ 里用 Shift+Enter 换行写多段日记,会按段落分别渲染。

## 效果预览要点

- 顶部左侧贴一条暖色 washi tape,底部右侧贴一条冷色 washi tape
- 右上角是带虚线边框的圆形邮戳,显示星期 + 日期,微微倾斜
- 标题用手写字体(Ma Shan Zheng),正文用衬线字体(Noto Serif SC),行距拉大、首行缩进,模拟真实手账书写感
- 字体走 Google Fonts CDN,渲染时需要服务器能访问外网;如果你的 AstrBot 部署在无法访问 Google Fonts 的环境,字体会优雅降级为系统默认字体,不影响出图

## 可定制方向

- 想要更多风格(贴纸风 / 复古风),可以复制 `main.py` 里的 `JOURNAL_TMPL` 改样式,或者用官方在线工具调试:
  https://t2i-playground.astrbot.app/
- 想自动追加天气、心情标签,可以在 `journal()` 函数里往 `data` 字典加字段,再在模板里用 `{{ 字段名 }}` 引用
- 想存历史手帐而不是只发图,可以参考 AstrBot 存储指南把每次内容写进 `data` 目录下的本地文件或数据库
