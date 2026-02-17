import re
import requests
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# --- [تنظیمات تلگرام] ---
API_ID = 20062451
API_HASH = '71823b474e1dc2c7e6d87e32f335e5d2'
# سشن استرینگی که گرفتی رو اینجا گذاشتم
SESSION_STRING = '1BJWap1sBuy2Yp7X5qUFkzNTpv6zKEDdB7x94GP2ifRObv1Unxqoj27I-zTPGBK4aHB9wZ2k8UGAd3iWwuhUZN9hMde6ae4lwW7R9FWRuJ2iGH2QO7Ot1nt7__J5Am56O78AZLBms_mpZb2RWl-mBeWjgg538EnkSF2sEm7saa-f8jE0N8Owu3NkHX87F6HHizd4jXdaCzAwW_wu99tXFIB2TLoQeu1AcRTHXTuW9lRPzBMe4vZMGi9kW8Qa-RhgeSpX44XDQi3wl89JoJ9vpsf4ROoDhhWsMuCN2ZkFmz_Zkfen3eoaYF7lyUR9_tWQqnh05clxsfs78XDBfizdqeMcu3Qc-YBk='

# کانال‌های مانیتورینگ
CHANNELS = ['thrillkod', 'Thrillcom', 'alerts4nayz', 'OldManThrill', 'ghorolom', -1002023352769]

# --- [تنظیمات Thrill] ---
THRILL_URL = 'https://api.thrill.com/reward/v2/players/self/cash-drops'
TOKEN = """eyJhbGciOiJSUzI1NiIsImtpZCI6Imp3ay1saXZlLTAzNmExZjQ0LTk3YzUtNGRkMi05MjQyLTQ0NWU0NzJkYTZlNyIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsicHJvamVjdC1saXZlLWU2NzZhMmEwLTY2NmMtNDVhMi05ZGE4LTcwY2IzZTU4M2FmOSJdLCJlbWFpbCI6InphaGJ0Y3JhQGdtYWlsLmNvbSIsImV4cCI6MTc3MTIxMTE3NSwiaHR0cHM6Ly9zdHl0Y2guY29tL3Nlc3Npb24iOnsiaWQiOiJzZXNzaW9uLWxpdmUtNTgzMjlkYzUtZjEwMi00M2Y0LTgwODEtNzA3YjE4NDE2M2M1Iiwic3RhcnRlZF9hdCI6IjIwMjYtMDItMTZUMDI6NDc6NDdaIiwibGFzdF9hY2Nlc3NlZF9hdCI6IjIwMjYtMDItMTZUMDM6MDE6MTVaIiwiZXhwaXJlc19hdCI6IjIwMjYtMDMtMThUMDI6NDc6NDdaIiwiYXR0cmlidXRlcyI6eyJ1c2VyX2FnZW50IjoiIiwiaXBfYWRkcmVzcyI6IiJ9LCJhdXRoZW50aWNhdGlvbl9mYWN0b3JzIjpbeyJ0eXBlIjoib2F1dGgiLCJkZWxpdmVyeV9tZXRob2QiOiJvYXV0aF9nb29nbGUiLCJsYXN0X2F1dGhlbnRpY2F0ZWRfYXQiOiIyMDI2LTAyLTE2VDAyOjQ3OjQ3WiIsImdvb2dsZV9vYXV0aF9mYWN0b3IiOnsiaWQiOiJvYXV0aC11c2VyLWxpdmUtZDM0ZjZmYWMtODY4Mi00YTcyLTkwMzUtODEyOTAwOWEyMzJlIiwicHJvdmlkZXJfc3ViamVjdCI6IjEwNzg5ODczMjIwNTA4NjE2NDAyNCJ9fV0sInJvbGVzIjpbInN0eXRjaF91c2VyIl19LCJpYXQiOjE3NzEyMTA4NzUsImlzcyI6InN0eXRjaC5jb20vcHJvamVjdC1saXZlLWU2NzZhMmEwLTY2NmMtNDVhMi05ZGE4LTcwY2IzZTU4M2FmOSIsIm5iZiI6MTc3MTIxMDg3NSwicHVibGljSWQiOiI0ZTA2OTYzYy1jNmFkLTQ2NWQtODJjMy02N2Q3YjAxODNkY2IiLCJyb2xlIjoiUExBWUVSIiwic3ViIjoidXNlci1saXZlLTI3MjQ0MmU4LTdjN2QtNGY3OC1hZTkzLWY3MjQwMDZiNjM4OSJ9.dKXHmC4Vw3ClEfqsfJbxpwQEnrzYppERiQPiQyYKvrDg1OqFxzVeMYF-x_GICimg_gYjbRaqp36U4G_jt7H1j0ZF9jWYyrAMPsFA927m6ukXs3Wxu3DGTg5WH1CrmGh2htdEvE1OAO_ZnhGJDmuPJHuzmEQ9IUTvQqFHgTHpv8L_OdrjugqErOS8-FO2-hgknJOugl-iN-iQKHIh_Gl1r90MDvU7OZKK07tVSNyEuwXAOfp9VxDWO5kJTGYz18QJbrYtWSLzZXRYlPgYnkqRSaa_GIggrq46HrXNGDJqM3vFCIl6QUXCspx65WVlEMh7hKnfmCTBQLuoUd9XThmzOQ"""

COOKIES = {
    '__cf_bm': 'eOdlCrm.noVUp3xCAhmE2ZFS0gw.65FsJduEelkowtk-1771210013-1.0.1.1-uV7ZWXkmWx79qL.pohgRHttKNFPIM1OSmSPBMoW0ZrWk0kZR5uVHvqfA93opoO9e1xBLcbLMQe8NrIu_uaYG4gBbmLuh3pSWRON4vnfgWe8',
    'cf_clearance': 'Cu5mqzYiEPUd9Gdb.0nNj14UgcNoikyqbDzPeMaIQtg-1771210030-1.2.1.1-vsb9VvJZ9bpyugHvjfTQUlNrVPwTKpiIiNcKIpRc5rLW1AEQwbZFNbCmz2hJlouIqfa8HFn9DsDJ3wPiooi4unIYVUNAUtd2FeFZ8KM4mG6A5gFnZJaANHFTrAvmd_mV81NM_kgwpkGIvEklCoJo4E2.RHU5ok4xlwAgziST8drmPLNQmFnjnKZVREOkb4O6bMTYYiGiYwTWQoeCaBdYMR_iTAOD6UwNL5XfIkDcgRE',
    'token': TOKEN.strip(),
    'intercom-session-zkeu56p5': 'Rzh2MjJyTDNHY0NsdHVod1luL0NZcmx1bjJlSUtKSFQxK3ViZE9WS1RScnd2MncrK2ZyWVJYb3VjbHVsNkZVYjZHRUJCTEx4Um9zQXZFZVRJeXVrVXhleE1kbTgyaVZxWlp5aXZVWGp5QlFIUEhXYS91b1NFUUorYVljcWdRczIrQVVoRlJZdU4zSGdsRjBCTkRHelpETWlHaEJnSy81Z3dtZ3dEU1FWaGRQektyWGJjR2dsUE14MDRuTHV2VVQ0LS1WTnFQODgvOVhDTnBTYm42dEx5YVN3PT0=--24d9e335725c7d14fdbc5275144fa45a3231487e',
}

HEADERS = {
    'authority': 'api.thrill.com',
    'content-type': 'application/json',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
    'origin': 'https://thrill.com',
    'referer': 'https://thrill.com/',
}

BANNED = {'DAILY', 'VIP', 'THRILL', 'DROP', 'DOGE', 'CASH', 'CODE', 'JOIN', 'LINK'}

def claim_code(code):
    payload = {"code": code, "currency": "DOGE"}
    try:
        res = requests.post(THRILL_URL, headers=HEADERS, cookies=COOKIES, json=payload, timeout=10)
        print(f"📡 Code: [{code}] | Status: {res.status_code} | Res: {res.text[:100]}")
    except Exception as e:
        print(f"❌ Claim Error: {e}")

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(chats=CHANNELS))
async def handler(event):
    text = event.raw_text
    print(f"📩 New msg from: {event.chat_id}")
    clean_text = re.sub(r'http\S+', '', text)
    potential_codes = re.findall(r'\b([A-Z0-9]{4,15})\b', clean_text)

    for code in potential_codes:
        if code not in BANNED and not code.isdigit():
            print(f"💎 Found: {code}")
            # اجرای غیرهمزمان درخواست برای سرعت بیشتر
            asyncio.get_event_loop().run_in_executor(None, claim_code, code)

print("🚀 Bot is LIVE on Koyeb/Cloud...")
client.start()
client.run_until_disconnected()