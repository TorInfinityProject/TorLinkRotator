import re
import random
import datetime
import aiohttp
from aiohttp import web
from aiohttp_socks import ProxyType, ProxyConnector

import config


recipient_regex = re.compile(r"^[\w\d\=\+\-\.\%\s\:\/\…\_\)\(]{1,256}$")

async def get_link(recipient):
    if isinstance(config.TOR_SOCKS5_PROXY, list) or isinstance(config.TOR_SOCKS5_PROXY, tuple):
        proxy_host, proxy_port = random.choice(config.TOR_SOCKS5_PROXY).split(':')
    else:
        proxy_host, proxy_port = config.TOR_SOCKS5_PROXY.split(':')

    try:
        async with aiohttp.ClientSession(
                    connector=ProxyConnector(
                        proxy_type=ProxyType.SOCKS5,
                        host=proxy_host,
                        port=int(proxy_port),
                        rdns=True
                    ),
                    timeout=aiohttp.ClientTimeout(total=None,sock_connect=30,sock_read=30),
                    headers={'X-RECIPIENT-ID': recipient} if recipient is not None else {}
                ) as session:
            async with session.get(f"{config.TOR_LINK_ROTATION_URL}/", timeout=30) as response:
                return True, await response.json()
    except:
        return False, None

async def web_handler(request):
    recipient = request.cookies.get('cf_clearance', None)
    if recipient is not None:
        if not recipient_regex.match(recipient):
            recipient = None
    
    status, resp = await get_link(recipient)
    if not status:
        return web.Response(text="error, can't connect to rotation gateway. Try refreshing the page")
    
    if resp.get('status', None) == 'OK':
        subdomain = '.'.join(request.host.split('.')[:-2])
        return web.Response(
            text=f"""<html><head><meta http-equiv="refresh" content="10;url={resp['scheme']}://{subdomain + '.' if len(subdomain) > 0 else ''}{resp['link']}{request.raw_path}" /></head><body><p>You will be redirected in 10-15 seconds</p><br><p>If you see a "Onion not found" error, please click on the "New Tor Circuit for this Site" button.</p>{'<br><p>The mirror will be deleted ' + str(int(datetime.timedelta(seconds=resp['lifetime']).total_seconds() // 3600)) + ' hours after the redirect</p>' if resp.get('lifetime') is not None else ''}</body></html>""",
            content_type='text/html'
        )
    else:
        return web.Response(text=resp.get('detail', ''))

async def index(request):
    if config.INDEX_HTML is None:
        return web.Response(status=404)
    
    subdomain = '.'.join(request.host.split('.')[:-2])
    alias_name = config.ALIAS_SUBDOMAIN_NAME.get(subdomain, None)
    return web.Response(
        text=config.INDEX_HTML.format(
            alias_subdomain_name=' ' + alias_name if alias_name is not None else '',
            subdomain=subdomain + '.' if len(subdomain) > 0 else '',
            query_params='?' + request.query_string if len(request.query_string) > 0 else ''
        ),
        content_type='text/html'
    )

app = web.Application()
app.add_routes([
    web.get(r'/_', index, allow_head=True),
    web.post(r'/_', index),
    web.get(r'/{path:.*}', web_handler, allow_head=False),
    web.post(r'/{path:.*}', web_handler)
])


if __name__ == '__main__':
    web.run_app(app)
