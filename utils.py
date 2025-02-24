import logging

import openai

import config

openai.api_key = config.OPENAI_TOKEN


async def generate_text(prompt) -> dict:
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
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


async def edit_image(orig, mask, prompt, n=1, size="512x512") -> list[str]:
    try:
        response = openai.Image.create_edit(
            image=open(
                f"/Users/zhansen/vscode/incubator/neurobot/images/{orig}.png",
                "rb"
            ),
            mask=open(
                f"/Users/zhansen/vscode/incubator/neurobot/images/{mask}.png",
                "rb"
            ),
            prompt=prompt,
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
