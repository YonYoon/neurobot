import logging

import openai
from PIL import Image

import config

openai.api_key = config.OPENAI_TOKEN


async def generate_text(prompt) -> dict:
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
        )
        return (
            response["choices"][0]["message"]["content"],
            response["usage"]["total_tokens"],
        )
    except Exception as e:
        logging.error(e)


async def generate_image(prompt, n=1, size="1024x1024") -> list[str]:
    try:
        response = await openai.Image.acreate(prompt=prompt, n=n, size=size)
        urls = []
        for i in response["data"]:
            urls.append(i["url"])
    except Exception as e:
        logging.error(e)
        return []
    else:
        return urls


async def edit_image(orig, mask, edit_prompt, n=1, size="512x512") -> list[str]:
    path_to_orig = f"/Users/zhansen/Pictures/{orig}.png"
    path_to_mask = f"/Users/zhansen/Pictures/{mask}.png"
    orig = Image.open(path_to_orig)
    mask = Image.open(path_to_mask)

    if mask.mode != "RGBA":
        mask = mask.convert("RGBA")

    orig.save("/Users/zhansen/Pictures/orig.png", "PNG")
    mask.save("/Users/zhansen/Pictures/mask.png", "PNG")

    try:
        response = openai.Image.create_edit(
            image=open("/Users/zhansen/Pictures/orig.png", "rb"),
            mask=open("/Users/zhansen/Pictures/mask.png", "rb"),
            prompt=edit_prompt,
            n=n,
            size=size,
        )
        urls = []
        for i in response["data"]:
            urls.append(i["url"])
    except Exception as e:
        logging.error(e)
        return []
    else:
        return urls
