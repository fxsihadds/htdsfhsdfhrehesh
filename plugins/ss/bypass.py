from pyrogram import Client, filters
from pyrogram.types import Message
import requests
from bs4 import BeautifulSoup
import re
from re import findall, compile
from requests import Session
from curl_cffi.requests import Session as cSession
from urllib.parse import urlparse

@Client.on_message(filters.command("bypass", ["/", "."]))
async def bypass(bot: Client, cmd: Message):
    global status
    try:
        status = await cmd.reply_text("<b>⎚ `Bypassing...`</b>")
        _, url = cmd.text.split()
    except ValueError:
        await status.edit("<b>⎚ Use <code>/bypass</code> Url To Bypass Your Link!</b>")
    else:
        if re.search(r'savelinks\.me', url):
            await savelinks(bot, cmd, url)
        elif re.search(r'ouo\.io', url):
            await ouo(bot, cmd, url)
        else:
            await status.edit("<b>This Site Functions Not Found!</b>")

# bypass Recptchav3

async def recaptchaV3(ANCHOR_URL='https://www.google.com/recaptcha/api2/anchor?ar=1&k=6Lcr1ncUAAAAAH3cghg6cOTPGARa8adOf-y9zv2x&co=aHR0cHM6Ly9vdW8ucHJlc3M6NDQz&hl=en&v=pCoGBhjs9s8EhFOHJFe8cqis&size=invisible&cb=ahgyd1gkfkhe'):
    rs = Session()
    rs.headers.update({'content-type': 'application/x-www-form-urlencoded'})
    matches = findall('([api2|enterprise]+)\/anchor\?(.*)', ANCHOR_URL)[0]
    url_base = 'https://www.google.com/recaptcha/' + matches[0] + '/'
    params = matches[1]
    res = rs.get(url_base + 'anchor', params=params)
    token = findall(r'"recaptcha-token" value="(.*?)"', res.text)[0]
    params = dict(pair.split('=') for pair in params.split('&'))
    res = rs.post(url_base + 'reload', params=f'k={params["k"]}',
                  data=f"v={params['v']}&reason=q&c={token}&k={params['k']}&co={params['co']}")
    return findall(r'"rresp","(.*?)"', res.text)[0]


# All bypass Fuctions

async def ouo(bot, cmd, url: str):
    tempurl = url.replace("ouo.io", "ouo.press")
    p = urlparse(tempurl)
    id = tempurl.split('/')[-1]
    client = cSession(headers={'authority': 'ouo.press', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                      'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8', 'cache-control': 'max-age=0', 'referer': 'http://www.google.com/ig/adde?moduleurl=', 'upgrade-insecure-requests': '1'})
    res = client.get(tempurl, impersonate="chrome110")
    next_url = f"{p.scheme}://{p.hostname}/go/{id}"
    for _ in range(2):
        if res.headers.get('Location'):
            break
        bs4 = BeautifulSoup(res.content, 'lxml')
        inputs = bs4.form.findAll("input", {"name": compile(r"token$")})
        data = {inp.get('name'): inp.get('value') for inp in inputs}
        data['x-token'] = await recaptchaV3()
        res = client.post(next_url, data=data, headers={
                          'content-type': 'application/x-www-form-urlencoded'}, allow_redirects=False, impersonate="chrome110")
        next_url = f"{p.scheme}://{p.hostname}/xreallcygo/{id}"
        link = res.headers.get('Location')
        await status.edit(f"""
<b>˜”°•✩•°”˜ 𝙱𝚢𝚙𝚊𝚜𝚜 𝚂𝚞𝚌𝚌𝚎𝚜𝚜𝚏𝚞𝚕𝚕 ˜”°•✩•°”˜</b>
                          
𝐋𝐢𝐧𝐤:<code> {url}</code>
𝐁𝐲𝐩𝐚𝐬𝐬 𝐋𝐢𝐧𝐤:<code> {link}</code>
⎚ 𝐑𝐞𝐪𝐮𝐞𝐬𝐭 𝐁𝐲: @{cmd.from_user.username}
""")


async def savelinks(bot, cmd, url: str):
    r = requests.get(url=url)
    soup = BeautifulSoup(r.content, "html.parser")
    try:
        inputs = soup.form.findAll("input")
        data = {inp.get('name'): inp.get('value') for inp in inputs}
        res = requests.post(url=url, data=data, headers={
                            'content-type': 'application/x-www-form-urlencoded'})
        res_contents = BeautifulSoup(res.content, "lxml")
        link = res_contents.find("div", "view-well")
        links = link.find_all("a", href=True)
        m_lnk = " \n".join([link["href"] for link in links])
        await status.edit(f"""
<b>˜”°•✩•°”˜ 𝙱𝚢𝚙𝚊𝚜𝚜 𝚂𝚞𝚌𝚌𝚎𝚜𝚜𝚏𝚞𝚕𝚕 ˜”°•✩•°”˜</b>

▂ ▃ ▅ ▆ ▇ █ 𝐋𝐢𝐧𝐤  █ ▇ ▆ ▅ ▃ ▂               
<code>{url}</code>
▂ ▃ ▅ ▆ ▇ █ ❝𝐁𝐲𝐩𝐚𝐬𝐬 𝐋𝐢𝐧𝐤  █ ▇ ▆ ▅ ▃ ▂
<code>{m_lnk}</code>
⎚ 𝐑𝐞𝐪𝐮𝐞𝐬𝐭 𝐁𝐲: @{cmd.from_user.username}
""")
    except Exception as e:
        await cmd.reply_text("<b>Link Extraction Failed! Please Provide Valid Link</b>")



