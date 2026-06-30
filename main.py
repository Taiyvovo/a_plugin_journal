import datetime

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

# 简约文艺 + 复古拼贴风 手帐模板
# 米黄纸张底色 + 纸纹理 + washi tape 胶带 + 邮戳日期章 + 手写体标题
JOURNAL_TMPL = """
<link href="https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=Noto+Serif+SC:wght@400;600&display=swap" rel="stylesheet">
<style>
    html, body {
        margin: 0;
        padding: 0;
        width: fit-content;
        height: fit-content;
    }
    * { box-sizing: border-box; }
</style>
<div style="
    width: 720px;
    display: inline-block;
    box-sizing: border-box;
    background: #f7f1e3;
    background-image:
        repeating-linear-gradient(0deg, rgba(0,0,0,0.015) 0px, rgba(0,0,0,0.015) 1px, transparent 1px, transparent 3px),
        repeating-linear-gradient(90deg, rgba(0,0,0,0.01) 0px, rgba(0,0,0,0.01) 1px, transparent 1px, transparent 3px);
    border: 1px solid #d8cdb8;
    box-shadow: 0 0 0 8px #fffdf8 inset;
    padding: 64px 50px 56px 50px;
    position: relative;
    font-family: 'Noto Serif SC', serif;
">

    <!-- washi tape 左上 -->
    <div style="
        position:absolute; top:-18px; left:46px; width:140px; height:38px;
        background: repeating-linear-gradient(45deg, rgba(216,160,140,0.6) 0 10px, rgba(235,200,180,0.6) 10px 20px);
        transform: rotate(-7deg);
        box-shadow: 0 2px 4px rgba(0,0,0,0.12);
        opacity: 0.9;
    "></div>

    <!-- washi tape 右下 -->
    <div style="
        position:absolute; bottom:-16px; right:64px; width:120px; height:34px;
        background: repeating-linear-gradient(45deg, rgba(150,180,160,0.55) 0 10px, rgba(200,220,205,0.55) 10px 20px);
        transform: rotate(6deg);
        box-shadow: 0 2px 4px rgba(0,0,0,0.12);
        opacity: 0.9;
    "></div>

    <!-- 邮戳日期章 -->
    <div style="
        position:absolute; top:38px; right:46px; width:96px; height:96px;
        border: 2px dashed #b5453a; border-radius: 50%;
        display:flex; flex-direction:column; align-items:center; justify-content:center;
        transform: rotate(8deg); opacity:0.78; color:#b5453a;
        font-family:'Ma Shan Zheng', cursive;
    ">
        <div style="font-size:13px;">{{ weekday }}</div>
        <div style="font-size:15px; font-weight:bold; margin-top:2px;">{{ date }}</div>
    </div>

    <!-- 标题 -->
    <div style="font-family:'Ma Shan Zheng', cursive; font-size:42px; color:#3a3226; margin-bottom:8px; max-width:520px;">
        {{ title }}
    </div>
    <div style="width:90px; height:3px; background:#c9a98a; margin-bottom:36px; border-radius:2px;"></div>

    <!-- 正文 -->
    <div style="font-size:21px; line-height:2; color:#4a4234; letter-spacing:1px;">
        {% for p in paragraphs %}
        <p style="margin:0 0 18px 0; text-indent:2em;">{{ p }}</p>
        {% endfor %}
    </div>

    <!-- 落款 -->
    <div style="margin-top:24px; text-align:right; font-family:'Ma Shan Zheng', cursive; font-size:18px; color:#9c8a6a;">
        —— 静好 ✦
    </div>
</div>
"""

WEEKDAYS = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


@register(
    "astrbot_plugin_journal",
    "taiyvovo",
    "指令触发的手帐风格文字转图片插件",
    "1.0.0",
    "",
)
class JournalPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("手帐")
    async def journal(self, event: AstrMessageEvent, text: str):
        """生成手帐风格图片。用法: /手帐 今天发生的事情,可以多行..."""
        if not text or not text.strip():
            yield event.plain_result("写点什么吧~ 用法: /手帐 今天发生的事情...")
            return

        now = datetime.datetime.now()
        paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
        if not paragraphs:
            paragraphs = [text.strip()]

        data = {
            "title": now.strftime("%Y.%m.%d"),
            "date": now.strftime("%Y/%m/%d"),
            "weekday": WEEKDAYS[now.weekday()],
            "paragraphs": paragraphs,
        }

        try:
            # full_page=False + 不传 clip:配合模板里的 fit-content 重置,
            # 让截图紧贴卡片本身,避免页面默认视口造成的大片白边
            url = await self.html_render(
                JOURNAL_TMPL,
                data,
                options={"timeout": 30000, "full_page": True, "omit_background": False},
            )
        except Exception as e:
            logger.error(f"手帐图片渲染失败: {e}")
            yield event.plain_result("手帐渲染失败了,稍后再试试吧 😢")
            return

        yield event.image_result(url)

    async def terminate(self):
        """插件卸载/停用时调用"""
        pass
