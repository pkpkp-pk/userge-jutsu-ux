# paimon Plugin for Labstack Uploads (https://up.labstack.com)
# Author: Sumanjay (https://github.com/cyberboysumanjay) (@cyberboysumanjay)
# All rights reserved.

from aiofiles import os
from telegraph import upload_file

from userge import Config, Message, pool, userge


@userge.on_cmd(
    "yrs",
    about={
        "header": "Yandex Reverse Search",
        "description": "Reverse Search any Image/sticker",
        "usage": "{tr}yrs [Reply to image | sticker]",
        "note": "Gif & Animated Stickers won't work!",
    },
    check_downpath=True,
)
async def labstack(message: Message):
    replied = message.reply_to_message
    if replied and (replied.sticker or replied.photo or replied.video or replied.gif):
        await message.edit("`processing ...`")
        dl_loc = await message.client.download_media(
            message=message.reply_to_message,
            file_name=Config.DOWN_PATH,
        )
    else:
        return await message.err("Media not found!")

    try:
        response = await pool.run_in_thread(upload_file)(dl_loc)
    except Exception as t_e:
        await message.err(str(t_e))
    else:
        media_link = f"https://telegra.ph{response[0]}"
        yandex_link = f"https://yandex.com/images/search?rpt=imageview&url={media_link}"
        await message.edit(f"**[Yandex Search Results]({yandex_link})**")
    finally:
        await os.remove(dl_loc)
