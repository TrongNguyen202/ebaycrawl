import requests
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import messagebox
import  random


headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://www.ebay.com',
    'pragma': 'no-cache',
    'referer': 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p4432023.m570.l1313&_nkw=tour+shirt&_sacat=0&_ipg=60',
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
}



responsed = requests.get('https://www.ebay.com/sch/i.html?_from=R40&_trksid=p4432023.m570.l1313&_nkw=tour+shirt&_sacat=0&_ipg=60', headers=headers)
soup = BeautifulSoup(responsed.text, 'html.parser')


ul = soup.find_all('ul', class_="srp-results srp-grid clearfix")
products = ul[0]

li_elements = ul[0].find_all('li')
href_list = []
for li in li_elements:

    a_tags = li.find_all('a', href=True)

    for a in a_tags:

        href = a['href']
        href_list.append(href)
item_input = []
for item in href_list:
    if item[21:24] =="itm":
        item_input.append(item)


PROXI_OPTIONS = [
        "185.68.245.224:50101:folinas:bonbon9999",
        "166.88.55.226:50101:folinas:bonbon9999",
        "181.215.184.36:50101:folinas:bonbon9999",
        "64.113.0.205:50101:folinas:bonbon9999"
    ]

proxy = random.choice(PROXI_OPTIONS)
urls = item_input
if not urls:
    messagebox.showerror("Error", "Please enter at least one valid URL")


all_data = []




for url in urls:
    if not url:
        continue
    print(url)

    try:
        response = requests.get(url, proxies={"http": f"http://{proxy}"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        divs = soup.find_all('div', class_='ux-image-carousel-item image-treatment active image')
        if divs:
            second_div = divs[1]
            img_second_tag = second_div.find('img')
            if img_second_tag:
                src_value = img_second_tag['src']
            else:
                src_value = "No image found"
        else:
            src_value = "No image found"

        title = soup.find_all('span', class_='ux-textspans ux-textspans--BOLD')
        if title:
            title_text = title[0].text
        else:
            title_text = "No title found"

        not_main_image = soup.find_all('div', class_='ux-image-carousel-item image-treatment image')
        not_main_img = []
        if not_main_image:
            for div_image in not_main_image[::-1]:
                img = div_image.find('img')
                not_main_img.append(img)

            alter_images = []
            for i in range(len(not_main_img) // 2, len(not_main_img)):
                if 'data-zoom-src' in not_main_img[i].attrs:
                    img_src = not_main_img[i]['data-zoom-src']
                    alter_images.append(img_src)

            data = {
                'title': title_text,
                'main_image': src_value,
                **{f"alter_image_{i+1}": img for i, img in enumerate(alter_images)}
                }
        else:
            data = {
                'title': title_text,
                'main_image': src_value
            }

        all_data.append(data)

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch data for URL {url}: {str(e)}")
        continue

if all_data:
    df = pd.DataFrame(all_data)
    df.to_excel("C:/hehe/ebay_data.xlsx", index=False)
    messagebox.showinfo("Success", "Data saved successfully to ebay_data.xlsx")
else:
    messagebox.showwarning("Warning", "No data fetched from the provided URLs")

