from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

class News:
    def __init__(self, url):
        self.url = url
        self.title = None
        self.subtitle = None
        self.content = None

        self._parse_article()

    def _parse_article(self):
        if "mingpao.com" in self.url:
            self._parse_mingpao()
        else:
            print("Unsupported news source.")

    def _parse_mingpao(self):
        # 使用非 headless 模式（可視化）
        options = Options()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1280,800")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

        driver = webdriver.Chrome(options=options)

        # 加上防偵測腳本
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
                });
            """
        })
        driver.execute_script("""
            let modals = document.querySelectorAll('.popup, .modal, .ad, .overlay, .vjs-modal');
            modals.forEach(el => el.remove());
        """)

        # 建議測試短網址，避免過長導致連線問題
        url = "https://news.mingpao.com/ins/%E6%B8%AF%E8%81%9E/article/20250701/s00001/1751277698096"
        print("🔗 嘗試連線至：", url)

        try:
            driver.get(url)
            time.sleep(5)  # 等待 JS 載入

            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            self.title = soup.find("meta", property="og:title")
            self.subtitle = soup.find("meta", property="og:description")
            self.article = soup.find("article")

            print("📰 Title:", self.title["content"] if self.title else "無標題")
            print("📝 Subtitle:", subtitle["content"] if self.subtitle else "無副標題")

            if self.article:
                paragraphs = self.article.find_all("p")
                text = "\n".join(p.get_text(strip=True) for p in paragraphs)
                print("📄 Content Preview:\n", text, "...")
            else:
                print("⚠️ 找不到文章內容")
        except Exception as e:
            print("❌ 錯誤：", e)

        driver.quit()