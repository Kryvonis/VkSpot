from time import sleep
from lxml import html
import requests as req
from urllib.request import urlretrieve
import vk, os, time, math

# Ваш логін, пароль
with open('access_tok.txt') as f:
    access_tkn = f.read()

session = vk.Session(access_token=access_tkn)

vkapi = vk.API(session=session)

result = vkapi.audio.search(q='Vagrant - Feint')

print(result)
