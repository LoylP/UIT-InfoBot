import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
import time
import re
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse

class Crawler_Document:
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
            
    def is_document(self, url):
        if any(url.lower().endswith(ext) for ext in self.document_extensions):
            return True
        try: 
            head_response = requests.head(url, headers = self.header, allow_redirects=True)
        except:
            return False
        
        content_type = head_response.headers.get('content-type', '').lower()
        
        return any(doc_type in content_type for doc_type in[
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument',
            'application/vnd.ms-excel',
            'text/plain'
        ])
    
    def uri_validator(self, x):
        try:
            result = urlparse(x)
            return all([result.scheme, result.netloc])
        except AttributeError:
            return False
    
    def extract_document_urls(self, child_url):
        
        document_urls = set()
        response = requests.get(child_url, headers = self.header)
        soup = BeautifulSoup(response.content, 'html.parser').find(id = self.child_id)

        untested_links = []
        for link in soup.find_all('a', href = True):
            url = urllib.parse.urljoin(self.base_url, link['href'])
            untested_links.append(url)
            
        for iframe in soup.find_all('iframe', src = True):
            url = urllib.parse.urljoin(self.base_url, iframe['src'])
            untested_links.append(url)

        
        for embed in soup.find_all('embed', src = True):
            url = urllib.parse.urljoin(self.base_url, embed['src'])
            untested_links.append(url)

        for l in untested_links:
            if not self.uri_validator(l):
                continue
            if self.is_document(l):
                document_urls.add(l)
                
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string:
                urls = re.findall(r'(?:href=[\'"](.*?\.pdf)[\'"]|src=[\'"](.*?\.pdf)[\'"])', script.string)
                for url_groups in urls:
                    for url in url_groups:
                        if url:
                            full_url = urllib.parse.urljoin(self.base_url, url)
                            if self.is_document_url(full_url):
                                document_urls.add(full_url)
                                
        return document_urls

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
        visited = set()
        
        for link in container.find_all('a', href = True):
            new_link = urllib.parse.urljoin(('/').join(url.split('/')[0:3]), link["href"])
            if new_link in visited:
                continue
            
            visited.add(new_link)
            
            print("Link of Child Page: " + new_link)
            for j in self.extract_document_urls(new_link):
                if not (j in links):
                    links.add(j)
            
        for i in links:
            print("Document in Child Pages: ", i)
            
        return links
    
    def save_documents(self, links):
        for url in links:
            response = requests.get(url, headers = self.header)
            file_name = url.split('/')[-1]
            file_path = os.path.join(self.output_folder, file_name)
            
            print("Downloading: ", file_name)
            with open(file_path, "wb") as f:
                f.write(response.content)
            
    def start_crawl(self):
        max_pages = 7
        for i in range(max_pages + 1):
            print("Cur pages: ", i)
            sets = self.get_links_from_container(self.base_url + f"?page={i}")
            self.save_documents(sets)
            
    
crawler = Crawler_Document(
    output_folder = "output_folder", 
    base_url = "https://tuyensinh.uit.edu.vn/tuyen-sinh-uit",
    parent_class = "view-content",
    parent_id = "main-content",
    child_id = "content-body"
)

crawler.start_crawl()