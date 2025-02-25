import os

from typing import Optional

urlReplaceDict = {
    "https://x.com/": "https://fixupx.com/",
    "https://twitter.com/": "https://fixup.com/",
    "instagram.com/": "ddinstagram.com/",
    "tiktok.com/": "vxtiktok.com/",
}


def handle_response(message, author):
    # Replace base URLs based on the dictionary
    for originalUrl in urlReplaceDict:
        if originalUrl in message:
            message = message.replace(originalUrl, urlReplaceDict[originalUrl])
            if "instagram.com/share/" in message:
                message = message.replace("/share/", "/reels/")

            if "instagram.com/reel/" in message:
                message = message.replace("/reel/", "/reels/")
            return author.mention + ": " + message, True

    return None, False