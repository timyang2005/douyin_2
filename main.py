from astrbot.api.all import *
import requests
import re

@register("douyin_video", "Your Name", "解析抖音视频链接并发送视频及信息", "1.0.0")
class DouyinVideoPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @event_message_type(EventMessageType.ALL)
    async def on_message(self, event: AstrMessageEvent):
        message_str = event.message_str
        # 检测消息中是否包含抖音视频链接
        if "<url id=\"cv9ra4vftae0fdkm7cjg\" type=\"url\" status=\"parsed\" title=\"抖音-记录美好生活\" wc=\"442\">https://v.douyin.com/</url>" in message_str:
            # 提取抖音视频链接
            douyin_url = re.search(r"https://v\.douyin\.com/\S+", message_str).group()
            # 调用 API 解析抖音视频
            api_url = f"<url id=\"cv9ra4vftae0fdkm7ck0\" type=\"url\" status=\"parsed\" title=\"\" wc=\"89\">https://api.makuo.cc/api/get.video.douyin</url>?url={douyin_url}"
            headers = {
                'Authorization': 'raedFk37Z0iixed5132hoA'
            }
            response = requests.get(api_url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data["code"] == 200:
                    video_url = data["data"]["video_url"]
                    title = data["data"]["title"]
                    author = data["data"]["author"]
                    cover = data["data"]["cover"]
                    # 发送视频文件
                    if event.get_platform_name() == "aiocqhttp":
                        from astrbot.api.message_components import Video
                        yield event.chain_result([Video.fromURL(video_url)])
                    else:
                        yield event.plain_result(f"视频链接：{video_url}")
                    # 发送视频标题、作者名称和封面图片
                    from astrbot.api.message_components import Image, Plain
                    cover_image = Image.fromURL(cover)
                    message_chain = [
                        Plain(f"视频标题：{title}"),
                        Plain(f"\n作者名称：{author}"),
                        Plain("\n视频封面："),
                        cover_image
                    ]
                    yield event.chain_result(message_chain)
                else:
                    yield event.plain_result("解析抖音视频失败")
            else:
                yield event.plain_result("解析抖音视频失败")
