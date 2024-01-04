from pyrogram import Client, filters
from pyrogram.types import Message
from bs4 import BeautifulSoup
import re
import requests
from asyncio import sleep as asleep
from cloudscraper import create_scraper
from re import findall, compile
from requests import Session
from curl_cffi.requests import Session as cSession
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from re import match, findall


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
        elif re.search(r'droplink\.co', url):
            burl = await transcript(url, "https://droplink.co/", "https://yoshare.net/",8)
        elif re.search(r'shrinkme\.org', url):
            burl = await transcript(url, "https://en.shrinke.me/", "https://themezon.net/", 15)
        elif bool(match(r"https?:\/\/.+\.tnshort\.\S+", url)):
            burl = await transcript(url, "https://go.tnshort.net/", "https://market.finclub.in/", 8)
        elif bool(match(r"https?:\/\/(xpshort|push.bdnewsx|techymozo)\.\S+", url)):
            burl = await transcript(url, "https://techymozo.com/", "https://portgyaan.in/", 8)
        elif bool(match(r"https?:\/\/go.lolshort\.\S+", url)):
            burl = await transcript(url, "https://get.lolshort.tech/", "https://tech.animezia.com/", 8)
        elif bool(match(r"https?:\/\/onepageurl\.\S+", url)):
            burl = await transcript(url, "https://go.onepageurl.in/", "https://gorating.in/", 3.1)
        elif bool(match(r"https?:\/\/earn.moneykamalo\.\S+", url)):
            burl = await transcript(url, "https://go.moneykamalo.com/", "https://bloging.techkeshri.com/", 4)
        elif bool(match(r"https?:\/\/dropurl\.\S+", url)):
            burl = await transcript(url, "https://dropurl.co/", "https://yoshare.net/", 3.1)
        elif bool(match(r"https?:\/\/tinyfy\.\S+", url)):
            burl = await transcript(url, "https://tinyfy.in", "https://www.yotrickslog.tech/", 0)
        elif bool(match(r"https?:\/\/adrinourls\.\S+", url)):
            burl = await transcript(url, "https://adrinourls.in", "https://bhojpuritop.in/", 8)
        elif bool(match(r"https?:\/\/krownurls\.\S+", url)):
            burl = await transcript(url, "https://go.hostadviser.net/", "blog.hostadviser.net/", 8)
        elif bool(match(r"https?:\/\/(du-url|duurl)\.\S+", url)):
            burl = await transcript(url, "https://du-url.in", "https://profitshort.com/", 0)
        elif bool(match(r"https?:\/\/indianshortner\.\S+", url)):
            burl = await transcript(url, "https://indianshortner.com/", "https://moddingzone.in/", 5)
        elif bool(match(r"https?:\/\/m.easysky\.\S+", url)):
            burl = await transcript(url, "https://techy.veganab.co/", "https://veganab.co/", 8)
            burl = await transcript(url, "https://vip.urlbnao.com", "https://ffworld.xyz/", 2)
        elif bool(match(r"https?:\/\/.+\.tnurl\.\S+", url)):
            burl = await transcript(url, "https://go.tnshort.net/", "https://market.finclub.in/", 0.8)
        elif bool(match(r"https?:\/\/url4earn\.\S+", url)):
            burl = await transcript(url, "https://url4earn.com", "https://studyis.xyz/", 6)
        elif bool(match(r"https?:\/\/shortingly\.\S+", url)):
            burl = await transcript(url, "https://go.blogytube.com/", "https://blogytube.com/", 5)
        elif bool(match(r"https?:\/\/short2url\.\S+", url)):
            burl = await transcript(url, "https://techyuth.xyz/blog", "https://blog.coin2pay.xyz/", 10)
        elif bool(match(r"https?:\/\/urlsopen\.\S+", url)):
            burl = await transcript(url, "https://s.humanssurvival.com/", "https://1topjob.xyz/", 5)
        elif bool(match(r"https?:\/\/mdisk\.\S+", url)):
            burl = await transcript(url, "https://mdisk.pro", "https://m.meclipstudy.in/", 8)
        elif bool(match(r"https?:\/\/(pkin|go.paisakamalo)\.\S+", url)):
            burl = await transcript(url, "https://go.paisakamalo.in", "https://healthtips.techkeshri.com/", 5)
        elif bool(match(r"https?:\/\/urlpays\.\S+", url)):
            burl = await transcript(url, "https://tech.smallinfo.in/Gadget/", "https://finance.filmypoints.in/", 6)
        elif bool(match(r"https?:\/\/skurls\.\S+", url)):
            burl = await transcript(url, "https://skurls.in", "https://dailynew.online/", 5)
        elif bool(match(r"https?:\/\/url1s\.\S+", url)):
            burl = await transcript(url, "https://url1s.com", "https://anhdep24.com/", 9)
        elif bool(match(r"https?:\/\/tuurls\.\S+", url)):
            burl = await transcript(url, "https://tuurls.one", "https://www.blogger.com/", 8)
        elif bool(match(r"https?:\/\/.+\.tuurls\.\S+", url)):
            burl = await transcript(url, "https://go.tuurls.online", "https://tutelugu.co/", 8)
        elif bool(match(r"https?:\/\/(.+\.)?vipurl\.\S+", url)):
            burl = await transcript(url, "https://count.vipurl.in/", "https://kiss6kartu.in/", 5)
        elif bool(match(r"https?:\/\/indyshare\.\S+", url)):
            burl = await transcript(url, "https://indyshare.net", "https://insurancewolrd.in/", 3.1)
        elif bool(match(r"https?:\/\/urlyearn\.\S+", url)):
            burl = await transcript(url, "https://urlyearn.com", "https://gktech.uk/", 5)
        elif bool(match(r"https?:\/\/earn4url\.\S+", url)):
            burl = await transcript(url, "https://m.open2get.in/", "https://ezeviral.com/", 8)
        elif bool(match(r"https?:\/\/urlsly\.\S+", url)):
            burl = await transcript(url, "https://go.urlsly.co/", "https://en.themezon.net/", 5)
        elif bool(match(r"https?:\/\/.+\.mdiskshortner\.\S+", url)):
            burl = await transcript(url, "https://loans.yosite.net/", "https://yosite.net/", 10)
        elif bool(match(r"https?://(?:\w+\.)?rockurls\.\S+", url)):
            burl = await transcript(url, "https://insurance.techymedies.com/", "https://blog.disheye.com/", 5)
        elif bool(match(r"https?:\/\/mplayurl\.\S+", url)):
            burl = await transcript(url, "https://tera-box.cloud/", "https://mvplayurl.in.net/", 5)
        elif bool(match(r"https?:\/\/shrinke\.\S+", url)):
            burl = await transcript(url, "https://en.shrinke.me/", "https://themezon.net/", 15)
        elif bool(match(r"https?:\/\/urlspay\.\S+", url)):
            burl = await transcript(url, "https://finance.smallinfo.in/", "https://tech.filmypoints.in/", 5)
        elif bool(match(r"https?:\/\/.+\.tnvalue\.\S+", url)):
            burl = await transcript(url, "https://page.finclub.in/", "https://finclub.in/", 8)
        elif bool(match(r"https?:\/\/sxsurl\.\S+", url)):
            burl = await transcript(url, "https://geturl.sxsurl.com/", "https://cinemapettai.in/", 5)
        elif bool(match(r"https?:\/\/zipurler\.\S+", url)):
            burl = await transcript(url, "https://zipurler.net/web/", "https://ontechhindi.com/", 5)
        elif bool(match(r"https?:\/\/moneycase\.\S+", url)):
            burl = await transcript(url, "https://last.moneycase.url/", "https://www.infokeeda.xyz/", 3.1)
        elif bool(match(r"https?:\/\/urlurlshort\.\S+", url)):
            burl = await transcript(url, "https://web.urlurlshort.in", "https://suntechu.in/", 5)
        elif bool(match(r"https?:\/\/.+\.dtgurls\.\S+", url)):
            burl = await transcript(url, "https://happyfiles.dtgurls.in/", "https://tech.filohappy.in/", 5)
        elif bool(match(r"https?:\/\/v2urls\.\S+", url)):
            burl = await transcript(url, "https://vzu.us/", "https://newsbawa.com/", 5)
        elif bool(match(r"https?:\/\/kpsurl\.\S+", url)):
            burl = await transcript(url, "https://kpsurl.in/", "https://infotamizhan.xyz/", 3.1)
        elif bool(match(r"https?:\/\/v2.kpsurl\.\S+", url)):
            burl = await transcript(url, "https://v2.kpsurl.in/", "https://infotamizhan.xyz/", 5)
        elif bool(match(r"https?:\/\/tamizhmasters\.\S+", url)):
            burl = await transcript(url, "https://tamizhmasters.com/", "https://pokgames.com/", 5)
        elif bool(match(r"https?:\/\/tgurl\.\S+", url)):
            burl = await transcript(url, "https://tgurl.in/", "https://www.proappapk.com/", 5)
        elif bool(match(r"https?:\/\/pandaznetwork\.\S+", url)):
            burl = await transcript(url, "https://pandaznetwork.com/", "https://panda.freemodsapp.xyz/", 5)
        elif bool(match(r"https?:\/\/url4earn\.\S+", url)):
            burl = await transcript(url, "https://go.url4earn.in/", "https://techminde.com/", 8)
        elif bool(match(r"https?:\/\/ez4short\.\S+", url)):
            burl = await transcript(url, "https://ez4short.com/", "https://ez4mods.com/", 5)
        elif bool(match(r"https?:\/\/daurl\.\S+", url)):
            burl = await transcript(url, "https://get.tamilhit.tech/MR-X/tamil/", "https://www.tamilhit.tech/", 8)
        elif bool(match(r"https?:\/\/.+\.omnifly\.\S+", url)):
            burl = await transcript(url, "https://f.omnifly.in.net/", "https://ignitesmm.com/", 5)
        elif bool(match(r"https?:\/\/sheraurls\.\S+", url)):
            burl = await transcript(url, "https://sheraurls.com/", "https://blogyindia.com/", 0.8)
        elif bool(match(r"https?:\/\/bindaasurls\.\S+", url)):
            burl = await transcript(url, "https://thebindaas.com/blog/", "https://blog.appsinsta.com/", 5)
        elif bool(match(r"https?:\/\/vipurls\.\S+", url)):
            burl = await transcript(url, "https://m.vip-url.net/", "https://m.leadcricket.com/", 5)
        elif bool(match(r"https?:\/\/.+\.short2url\.\S+", url)):
            burl = await transcript(url, "https://techyuth.xyz/blog/", "https://blog.mphealth.online/", 10)
        elif bool(match(r"https?:\/\/shrinkforearn\.\S+", url)):
            burl = await transcript(url, "https://shrinkforearn.in/", "https://wp.uploadfiles.in/", 8)
        elif bool(match(r"https?:\/\/bringlifes\.\S+", url)):
            burl = await transcript(url, "https://bringlifes.com/", "https://loanoffering.in/", 5)
        elif bool(match(r"https?:\/\/.+\.urlfly\.\S+", url)):
            burl = await transcript(url, "https://insurance.yosite.net/", "https://yosite.net/", 10)
        elif bool(match(r"https?:\/\/.+\.anurls\.\S+", url)):
            burl = await transcript(url, "https://anurls.in/", "https://dsblogs.fun/", 5)
        elif bool(match(r"https?:\/\/.+\.earn2me\.\S+", url)):
            burl = await transcript(url, "https://blog.filepresident.com/", "https://easyworldbusiness.com/", 5)
        elif bool(match(r"https?:\/\/.+\.vpurls\.\S+", url)):
            burl = await transcript(url, "https://get.vpurls.in/", "https://infotamizhan.xyz/", 5)
        elif bool(match(r"https?:\/\/.+\.narzourls\.\S+", url)):
            burl = await transcript(url, "https://go.narzourls.click/", "https://hydtech.in/", 5)
        elif bool(match(r"https?:\/\/adsfly\.\S+", url)):
            burl = await transcript(url, "https://go.adsfly.in/", "https://loans.quick91.com/", 5)
        elif bool(match(r"https?:\/\/earn2short\.\S+", url)):
            burl = await transcript(url, "https://go.earn2short.in/", "https://tech.insuranceinfos.in/", 0.8)
        elif bool(match(r"https?:\/\/instantearn\.\S+", url)):
            burl = await transcript(url, "https://get.instantearn.in/", "https://love.petrainer.in/", 5)
        elif bool(match(r"https?:\/\/urljust\.\S+", url)):
            burl = await transcript(url, "https://urljust.com/", "https://forexrw7.com/", 3.1)
        elif bool(match(r"https?:\/\/pdiskshortener\.\S+", url)):
            burl = await transcript(url, "https://pdiskshortener.com/", "", 10)
        else:
            await status.edit("<b>This Site Functions Not Found!</b>")

        await status.edit_text(f"""
<b>˜”°•✩•°”˜ 𝙱𝚢𝚙𝚊𝚜𝚜 𝚂𝚝𝚊𝚝𝚞𝚜 ˜”°•✩•°”˜</b>
                        
𝐋𝐢𝐧𝐤:<a> {url}</a>
𝐁𝐲𝐩𝐚𝐬𝐬 𝐋𝐢𝐧𝐤:<a> {burl}</a>
⎚ 𝐑𝐞𝐪𝐮𝐞𝐬𝐭 𝐁𝐲: @{cmd.from_user.username}
""")


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

async def transcript(url: str, DOMAIN: str, ref: str, sltime) -> str:
    code = url.rstrip("/").split("/")[-1]
    cget = create_scraper(allow_brotli=False).request
    resp = cget("GET", f"{DOMAIN}/{code}", headers={"referer": ref})
    soup = BeautifulSoup(resp.content, "html.parser")
    data = {inp.get('name'): inp.get('value')
            for inp in soup.find_all("input")}
    await asleep(sltime)
    resp = cget("POST", f"{DOMAIN}/links/go", data=data,
                headers={"x-requested-with": "XMLHttpRequest"})
    try:
        return resp.json()['url']
    except:
        return "Link Extraction Failed"


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
        print(e)
        await cmd.reply_text("<b>Link Extraction Failed! Please Provide Valid Link</b>")
