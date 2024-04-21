import requests
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import messagebox
import  random


def get_data():
    PROXI_OPTIONS = [
        "185.68.245.224:50101:folinas:bonbon9999",
        "166.88.55.226:50101:folinas:bonbon9999",
        "181.215.184.36:50101:folinas:bonbon9999",
        "64.113.0.205:50101:folinas:bonbon9999"
    ]

    proxy = random.choice(PROXI_OPTIONS)
    print(proxy)
    urls = url_entry.get("1.0", tk.END).split("\n")
    if not urls:
        messagebox.showerror("Error", "Please enter at least one valid URL")
        return

    all_data = []




    for url in urls:
        if not url:
            continue

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

# Create GUI window
root = tk.Tk()
root.title("Ebay Data Scraper")

# Create URL input field
url_label = tk.Label(root, text="Enter URLs (one per line):")
url_label.pack()
url_entry = tk.Text(root, height=10, width=50)
url_entry.pack()

# Create button to submit request
submit_button = tk.Button(root, text="Get Data", command=get_data)
submit_button.pack()

# Run the application
root.mainloop()
