#from bs4 import BeautifulSoup
import asyncio
from pyppeteer import launch


async def get_heroCSV(hero):
    
    browser = await launch(headless=True)
    page = await browser.newPage()

    await page.goto(f"https://www.dotabuff.com/heroes/{hero}")
    
    await page.waitFor(5000)

    html_content = await page.content()
    await browser.close()

    file = "html/"+f"{hero}.html"
    with open(file, "w", encoding="utf-8") as file:
        file.write(html_content)
        file.close()



asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
loop = asyncio.new_event_loop()
loop.run_until_complete(get_heroCSV("brewmaster"))


