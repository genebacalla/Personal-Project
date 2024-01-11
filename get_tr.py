from bs4 import BeautifulSoup
import asyncio
import csv
import os
from pyppeteer import launch





def get_csv(hero):
    csv_file = ["MOST USED ITEMS", "BEST VERSUS", "WORST VERSUS"]
    try:
        os.mkdir("csv/"+f"{hero}")
    except FileExistsError:
        print(f"csv/{hero}"+" folder already exists.")
   
    for i,file in enumerate(csv_file):

        csv_file_path = "csv/"+f"{hero}/"+f"{file}.csv"
        print(csv_file_path)

        with open(csv_file_path,'w',newline='') as f:
            writer = csv.writer(f)
            if (i==0):
                writer.writerows([["Item","Matches","Wins","Win Rate"]])
            else:
                writer.writerows([["Hero","Advantage","Win Rate","Matches"]])
            f.close()




async def get_html(hero):
    
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


def build_csv(hero):

    
    td_elements = ""
    with open (f"html/{hero}.html","r",encoding="utf-8") as f:
        contents = f.read()
        soup = BeautifulSoup(contents,"html.parser")

    for tag in soup.find_all('td'):
        td_elements += tag.text +"\n"

    
    #print(td_elements)
    
    td_elements = td_elements.splitlines()

    file_list,item_list = ["MOST USED ITEMS", "BEST VERSUS", "WORST VERSUS"],[None]*4
    flag_start = False
    idx_row,idx_item,idx_file,item_idx = 0,0,0,0

    for row in td_elements:

        if row == "":
            flag_start = True
            continue

        if flag_start:
            item_list[idx_row] = row
            idx_row += 1

            if (idx_row == 4):

                # Not all rows are stored into one csv file. In fact, they are stored into multiple csv files. 
                # Therefore, we need to create a method to save a specific number of rows into a file. This is
                # done by specifying a range which corresponds to the targeted file name. 

                if (idx_item < 12):
                    idx_file = 0
                elif (idx_item >= 12 and idx_item < 22):
                    idx_file = 1
                elif (idx_item >= 22 and idx_item < 32):
                    idx_file = 2
                else:
                    break

                with open("csv/"+f"{hero}/"+f"{file_list[idx_file]}.csv",'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows([item_list])
            
                idx_item += 1
                idx_row = 0
            
            
        
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
loop = asyncio.new_event_loop()
loop.run_until_complete(get_html("brewmaster"))


get_csv("brewmaster")
build_csv("brewmaster")
        
#get_csv("Brewmaster")