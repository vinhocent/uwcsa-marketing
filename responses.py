import os

from typing import Optional

urlReplaceDict = {
    "https://x.com/": "https://fixupx.com/",
    "https://twitter.com/": "https://fixup.com/",
    "instagram.com/": "ddinstagram.com/",
    "https://tiktok.com/": "https://vxtiktok.com/",
    "https://pixiv.net/": "https://phixiv.net/"
}


def handle_response(message, author):
    for originalUrl in urlReplaceDict:
        if originalUrl in message:
            reply = message.replace(originalUrl, urlReplaceDict[originalUrl])  
            return author.mention+ ": " + reply , True

    return None, False
