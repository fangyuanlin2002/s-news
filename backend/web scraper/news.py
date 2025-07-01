import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import undetected_chromedriver 


class News(ABC):
    def __init__(self, url):
        self.url = url
        self.title = None
        self.subtitle = None
        self.content = None
        self._fetch_and_parse()

    def _fetch_and_parse(self):
        try:
            headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://google.com/',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
}
            response = requests.get(self.url, headers=headers)
            response.encoding = 'utf-8'
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            self._parse_article(soup)
        except Exception as e:
            print(f"Error fetching article: {e}")

    def _parse_article(self, soup):
        # Extract title
        title_tag = soup.find("meta", property="og:title")
        self.title = title_tag["content"].strip() if title_tag else "No title found"

        # Extract content
        content_div = soup.find("article")
        if not content_div:
            content_div = soup.find("article", class_="news-text")

        if content_div:
            paragraphs = content_div.find_all("p")
            self.content = "\n".join(p.get_text(strip=True) for p in paragraphs)
        else:
            self.content = "No content found"

class MingPaoNews(News):
    """Uses the default parser; override only if needed."""
    pass

class SingTaoDaily(News):
    pass

class SCMP(News):
    pass

class HKFreePress(News):
    # Extract title
    def _parse_article(self, soup):
        # Extract title
        title_tag = soup.find("meta", property="og:title")
        self.title = title_tag["content"].strip() if title_tag else "No title found"
        # Extract content
        content_div = soup.find("div",class_="entry-content")
        print("content_div:",content_div)
        if content_div:
            paragraphs = content_div.find_all("p",recursive=False)
            self.content = "\n".join(p.get_text(strip=True) for p in paragraphs)
        else:
            self.content = "No content found"

class WenWeiPo(News):
    def _parse_article(self, soup):
    # Extract title
        title_tag = soup.find("meta", property="og:title")
        self.title = title_tag["content"].strip() if title_tag else "No title found"

        # Extract content
        content_div = soup.find("div",class_="post-content")

        if content_div:
            paragraphs = content_div.find_all("p")
            self.content = "\n".join(p.get_text(strip=True) for p in paragraphs)
        else:
            self.content = "No content found"

class OrientalDailyNews(News):
    """Overrides parsing logic for a different HTML structure."""
    def _parse_article(self, soup):
        # Extract title
        title_tag = soup.find("meta", property="og:title")
        self.title = title_tag["content"].strip() if title_tag else "No title found"

        # Extract content
        content_div = soup.find("main")

        if content_div:
            paragraphs = content_div.find_all("div",class_="content")
            self.content = "\n".join(p.get_text(strip=True) for p in paragraphs)
        else:
            self.content = "No content found"

class TaKungPao(News):
    """Overrides parsing logic for a different HTML structure."""
    def _parse_article(self, soup):
        # Extract title
        title_tag = soup.find("h1", class_="tkp_con_title")
        self.title = title_tag.get_text(strip=True) if title_tag else "No title"

        # Extract content
        content_div = soup.find("div",class_="tkp_content")

        if content_div:
            paragraphs = content_div.find_all("p")
            self.content = "\n".join(p.get_text(strip=True) for p in paragraphs)
        else:
            self.content = "No content found"

class HK01(News):
    pass

class InitiumMedia(News):
    pass

class YahooNews(News):
    pass

class HKCD(News):
    def _parse_article(self, soup):
        # Extract title
        self.title = soup.find("h2").get_text()

        # Extract content
        content_div = soup.find("div",class_="newsDetail")

        if content_div:
            paragraphs = content_div.find_all("p")
            self.content = "\n".join(p.get_text(strip=True) for p in paragraphs)
        else:
            self.content = "No content found"

class TheEpochTimes(News):
    def _parse_article(self, soup):
        # Extract title
        self.title = soup.find("h2").get_text()

        # Extract content
        content_div = soup.find("div",class_="post_content")

        if content_div:
            paragraphs = content_div.find_all("p")
            self.content = "\n".join(p.get_text(strip=True) for p in paragraphs)
        else:
            self.content = "No content found"

class NowTV(News):
    def _parse_article(self, soup):
        # Extract title
        self.title = soup.find("h1").get_text()

        # Extract content
        content_div = soup.find("div",class_="newsLeading")
        print("content_div:",content_div)
        if content_div:
            paragraphs = content_div.find_all("p")
            self.content = "\n".join(p.get_text(strip=True) for p in paragraphs)
        else:
            self.content = "No content found"

class HKCourtNews(News):
    def _parse_article(self, soup):
        # Extract title
        self.title = soup.find("h1").get_text()

        # Extract content
        content_div = soup.find("div",class_="elementor-element elementor-element-cd4b5e9 elementor-widget elementor-widget-theme-post-content")
        print("content_div:",content_div)
        if content_div:
            paragraphs = content_div.find_all("p")
            self.content = "\n".join(p.get_text(strip=True) for p in paragraphs)
        else:
            self.content = "No content found"

class ICable(News):
    def _parse_article(self, soup):
        # Extract title
        title_tag = soup.find("meta", property="og:title")
        self.title = title_tag["content"].strip() if title_tag else "No title found"

        # Extract content
        content_div = soup.find("article")

        if content_div:
            paragraphs = content_div.find_all("p",recursive=False)
            self.content = "\n".join(p.get_text(strip=True) for p in paragraphs)
        else:
            self.content = "No content found"

class HKGovernmentNews(News):
    def _parse_article(self, soup):
        # Extract title
        title_tag = soup.find("h1", class_="tkp_con_title")
        self.title = title_tag.get_text(strip=True) if title_tag else "No title"

        # Extract content
        content_div = soup.find("div",class_="newsdetail-content")
        if content_div:
            paragraphs = content_div.find_all("p")
            self.content = "\n".join(p.get_text(strip=True) for p in paragraphs)
        else:
            self.content = "No content found"


# It uses Vue to fetch data with JavaScript
class OrangeNews(News):
    def _fetch_and_parse(self):
        self._parse_article()

    def _parse_article(self):
        # 使用非 headless 模式（可視化）
        options = Options()
        options.add_argument("--headless")
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
        print("🔗 嘗試連線至：", self.url)

        try:
            driver.get(self.url)
            time.sleep(10)  # 等待 JS 載入

            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            self.title = soup.find("h1").getText()
            self.content = soup.find("article").find_all("p")

            print("📰 Title:", self.title if self.title else "無標題")
            print("self.content:",self.content)

            if self.content:
                self.content = "\n".join(p.get_text(strip=True) for p in  self.content)
                print("📄 Content Preview:\n",  self.content, "...")
            else:
                print("⚠️ 找不到文章內容")
        except Exception as e:
            print("❌ 錯誤：", e)

        driver.quit()

class TheStandard(News):
    def _parse_article(self, soup):
        # Extract title
        title_tag = soup.find("meta", property="og:title")
        self.title = title_tag["content"].strip() if title_tag else "No title found"

        # Extract content
        paragraphs = soup.find_all("p")
        print("paragraphs:",paragraphs)
        if paragraphs:
            self.content = "\n".join(p.get_text(strip=True) for p in paragraphs)
        else:
            self.content = "No content found"

class HKEJ(News):
    def _parse_article(self, soup):
        # Extract title
        title_tag = soup.find("meta", property="og:title")
        self.title = title_tag["content"].strip() if title_tag else "No title found"

        # Extract content
        content_div = soup.find("div",id="article-content")
        if not content_div:
            content_div = soup.find("article", class_="news-text")
        if content_div:
            paragraphs = content_div.find_all("p")
            self.content = "\n".join(p.get_text(strip=True) for p in paragraphs)
        else:
            self.content = "No content found"

class HKET(News):
    def _parse_article(self, soup):
        # Extract title
        title_tag = soup.find("meta", property="og:title")
        self.title = title_tag["content"].strip() if title_tag else "No title found"

        # Extract content
        content_div = soup.find("div",class_="article-detail-content-container")
        if not content_div:
            content_div = soup.find("article", class_="news-text")

        if content_div:
            paragraphs = content_div.find_all("p")
            self.content = "\n".join(p.get_text(strip=True) for p in paragraphs)
        else:
            self.content = "No content found"

class RTHK(News):
    def _parse_article(self, soup):
        # Extract title
        title_tag = soup.find("meta", property="og:title")
        self.title = title_tag["content"].strip() if title_tag else "No title found"

        # Extract content
        content_div = soup.find("div",class_="itemFullText")

        if content_div:
            # Replace <br> with newline so text is readable
            for br in content_div.find_all("br"):
                br.replace_with("\n")
            self.content = content_div.get_text(strip=True, separator="\n")
        else:
            self.content = "No content found"

class TheWitness(News):
    def _fetch_and_parse(self):
        self._parse_article()

    def _parse_article(self):
        # 使用非 headless 模式（可視化）
        options = Options()
        options.add_argument("--headless")
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
        print("🔗 嘗試連線至：", self.url)

        try:
            driver.get(self.url)
            time.sleep(10)  # 等待 JS 載入

            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            self.title = soup.find("meta", property="og:title")
            self.subtitle = soup.find("meta", property="og:description")
            self.content = soup.find_all("p")

            print("📰 Title:", self.title["content"] if self.title else "無標題")
            print("📝 Subtitle:", self.subtitle["content"] if self.subtitle else "無副標題")
            print("self.content:",self.content)

            if self.content:
                self.content = "\n".join(p.get_text(strip=True) for p in  self.content)
                print("📄 Content Preview:\n",  self.content, "...")
            else:
                print("⚠️ 找不到文章內容")
        except Exception as e:
            print("❌ 錯誤：", e)

        driver.quit()

# They use anti-bot mechanism to prevent web scraping
class InMediaHK(News):
    def _fetch_and_parse(self):
        self._parse_article()

    def _parse_article(self):
        # 使用非 headless 模式（可視化）
        options = undetected_chromedriver.ChromeOptions()
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
        print("🔗 嘗試連線至：", self.url)

        try:
            driver.get(self.url)
            time.sleep(10)  # 等待 JS 載入

            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            self.title = soup.find("meta", property="og:title")
            self.subtitle = soup.find("meta", property="og:description")
            self.article = soup.find("article")

            print("📰 Title:", self.title["content"] if self.title else "無標題")
            print("📝 Subtitle:", self.subtitle["content"] if self.subtitle else "無副標題")

            if self.article:
                paragraphs = self.article.find_all("p")
                text = "\n".join(p.get_text(strip=True) for p in paragraphs)
                print("📄 Content Preview:\n", text, "...")
            else:
                print("⚠️ 找不到文章內容")
        except Exception as e:
            print("❌ 錯誤：", e)

        driver.quit()
# If we use Selenium


# class News:
    # def __init__(self, url):
    #     self.url = url
    #     self.title = None
    #     self.subtitle = None
    #     self.content = None

    #     self._parse_article()
