import datetime

def get_current_date():
    dt = datetime.datetime.now()
    strg =dt.strftime('%Y-%m-%d %H:%M:%S')
    return strg

async def trans_page_str(page):
    page_de1 = page.decode('utf-8','ignore')
    return page_de1