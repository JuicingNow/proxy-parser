import aiohttp
import asyncio
import json

PROXYCOMPASS_URL = "https://proxycompass.com/wp-admin/admin-ajax.php?action=proxylister_download&nonce=0c0ad340aa&format=json&filter={}"

def proxyshare_url(page):
    return "https://www.proxyshare.com/detection/proxyList?limit=500&page={}&sort_by=lastChecked&sort_type=desc".format(page)

GITHUBPROXY_URL = "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/json/proxies.json"

async def fetch_proxies():
    proxy_list = []
    proxycompass_count = 0
    proxyshare_count = 0
    githubproxy_count = 0

    async def fetch_proxycompass(session):
        nonlocal proxycompass_count
        async with session.get(PROXYCOMPASS_URL) as response:
            if response.status == 200:
                data = await response.json()
                for item in data:
                    ip = item.get('ip_address')
                    port = item.get('port')
                    if ip and port:
                        proxy = f"{ip}:{port}"
                        proxy_list.append(proxy)
                        proxycompass_count += 1

    async def fetch_proxyshare(session, page):
        nonlocal proxyshare_count
        url = proxyshare_url(page)
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if data and isinstance(data, dict) and 'data' in data and data['data']:
                    for item in data['data']:
                        ip = item.get('ip')
                        port = item.get('port')
                        if ip and port:
                            proxy = f"{ip}:{port}"
                            proxy_list.append(proxy)
                            proxyshare_count += 1
            else:
                print(f"Ошибка при получении данных со страницы {page}. Статус код: {response.status}")

    async def fetch_githubproxy(session):
        nonlocal githubproxy_count
        async with session.get(GITHUBPROXY_URL) as response:
            if response.status == 200:
                text = await response.text()
                try:
                    data = json.loads(text)
                    for protocol in ['http', 'https']:
                        if protocol in data:
                            proxy_list.extend(data[protocol])
                            githubproxy_count += len(data[protocol])
                except json.JSONDecodeError:
                    print("Ошибка при десериализации JSON данных с GitHub.")
            else:
                print(f"Ошибка при получении данных с GitHub. Статус код: {response.status}")

    async with aiohttp.ClientSession() as session:
        await fetch_proxycompass(session)
        tasks = [fetch_proxyshare(session, page) for page in range(1, 15)]
        await asyncio.gather(*tasks)
        await fetch_githubproxy(session)

    print(f"Всего прокси: {len(proxy_list)}")
    print(f"Добавлено из ProxyCompass: {proxycompass_count}")
    print(f"Добавлено из ProxyShare: {proxyshare_count}")
    print(f"Добавлено из GitHub: {githubproxy_count}")

    return proxy_list


proxies = asyncio.run(fetch_proxies())