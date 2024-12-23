from crawl_document import Crawler_Document
from crawl_html import Crawler_Html

crawler_document = Crawler_Document(
    output_folder = "output_folder", 
    base_url = "https://tuyensinh.uit.edu.vn/tuyen-sinh-uit",
    parent_class = "view-content",
    parent_id = "main-content",
    child_id = "content-body"
)

crawler_html = Crawler_Html(
    output_folder = "output_folder", 
    base_url = "https://tuyensinh.uit.edu.vn/tuyen-sinh-uit",
    parent_class = "view-content",
    parent_id = "main-content",
    child_id = "content-body"
)

crawler_document.start_crawl()
crawler_html.start_crawl()