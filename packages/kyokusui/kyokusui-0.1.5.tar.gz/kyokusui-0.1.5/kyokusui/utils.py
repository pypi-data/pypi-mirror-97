import re

def hiroyuki(text):
    text = re.sub(r'\>\>([0-9]+)', "<a href='#\\1'>&gt;&gt;\\1</a>", text)
    text = re.sub(r'\>\>([a-zA-Z0-9.-_]+)', "<a class='mention \\1'>&gt;&gt;\\1</a>", text)
    return text


