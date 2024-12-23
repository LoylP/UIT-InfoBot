import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
import time
import re
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse

class Crawler_Html:
    def __init__(self, output_folder, base_url, parent_id = None, child_id = None, parent_class = None, child_class = None):
        self.output_folder = output_folder
        self.base_url = base_url
        self.parent_id = parent_id
        self.child_id = child_id
        self.parent_class = parent_class
        self.child_class = child_class
        
        self.header = {
            'Host': 'tuyensinh.uit.edu.vn',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://tuyensinh.uit.edu.vn/tuyen-sinh-uit',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8'
        }
        
        self.delay = 1
        self.document_extensions = ('.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx')

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
    def get_max_pages(self):
        
        response = requests.get(self.base_url, headers=self.header)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        container = soup.find(id = self.parent_id)
        
        max_page = 0
        for link in container.find_all('a', href = True):
            if link.has_attr('title'):
                if link['title'] == 'Đến trang cuối cùng':
                    max_page = int(link['href'].split('=')[1])
                    break
        
        return max_page
    
    def get_links_from_container(self, url):
        response = requests.get(url, headers = self.header)
        soup = BeautifulSoup(response.content, 'html.parser')

        container = soup.find(class_ = self.parent_class)

        links = set()
        
        for link in container.find_all('a', href = True):
            new_link = urllib.parse.urljoin(('/').join(url.split('/')[0:3]), link["href"])
            if new_link in links:
                continue
            
            # print("Find a new_link: ", new_link)
            
            links.add(new_link)
        
        return links
    
    def save_file(self, url, content_list):
        
        if content_list == 1: return
        
        file_name = urllib.parse.quote(url.split("/")[-1], safe = "")
        
        folder_path = os.path.join("./", self.output_folder, "txt")
        os.makedirs(folder_path, exist_ok=True) 
        
        file_path = f"{folder_path}/{file_name}.txt"

        try: 
            with open(file_path, "w", encoding="utf-8") as file:
                for content in content_list:
                    file.write(content + "\n")
                    
                print(f"Downloading: {file_name}.txt")
        except:
            print(f"Error while downloading: {file_name}.txt")
                

                
    def crawl_one_page(self, url, one_page_id):
        response = requests.get(url, headers=self.header)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        container_p = soup.find(id = one_page_id)

        if container_p:
            elements = container_p.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            content_list = []
            for element in elements:
                content_list.append(element.get_text(strip=True))
            
            # for content in content_list:
            #     print(content)
            
        self.save_file(url, content_list)

    
    def start_crawl(self):
        max_pages = 7
        for i in range(max_pages + 1):
            # print("Cur pages: ", i)
            links = self.get_links_from_container(self.base_url + f"?page={i}")
            for link in links:
                # print("Current Link: ", link)
                self.crawl_one_page(link, self.child_id)


crawler = Crawler_Html(
    output_folder = "output_folder", 
    base_url = "https://tuyensinh.uit.edu.vn/tuyen-sinh-uit",
    parent_class = "view-content",
    parent_id = "main-content",
    child_id = "content-body"
)

crawler.start_crawl()