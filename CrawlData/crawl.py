import requests
from bs4 import BeautifulSoup

# URL của trang cần crawl
url = "https://www.uit.edu.vn/gioi-thieu-cac-cau-lac-bo-doi-nhom-cua-uit"

# Gửi yêu cầu HTTP
response = requests.get(url)

# Kiểm tra trạng thái phản hồi
if response.status_code != 200:
    print(f"Không thể truy cập URL: {url}")
else:
    # Phân tích HTML của trang
    soup = BeautifulSoup(response.text, "html.parser")

    # Tìm tất cả các thẻ <p> chứa nội dung bài viết
    paragraphs = soup.find_all("span")

    # Tạo danh sách chứa văn bản đã trích xuất
    text_content = ""
    for p in paragraphs:
        text_content += p.get_text(separator=' ', strip=True) + "\n"

    # Lưu nội dung vào file .txt
    with open("../Document/thanhtich.txt", "w", encoding="utf-8") as file:
        file.write(text_content)

