from news import News

url = "https://news.mingpao.com/ins/%e6%b8%af%e8%81%9e/article/20250701/s00001/1751277698096/%e6%8e%88%e5%8b%b3%e5%8f%8a%e5%98%89%e7%8d%8e%e5%90%8d%e5%96%ae%e5%87%ba%e7%88%90-3%e4%ba%ba%e7%8d%b2%e9%a0%92%e5%a4%a7%e7%b4%ab%e8%8d%8a%e5%8b%b3%e7%ab%a0-%e5%8c%85%e6%8b%ac%e3%80%8a%e7%b6%93%e6%bf%9f%e6%97%a5%e5%a0%b1%e3%80%8b%e5%89%b5%e8%be%a6%e4%ba%ba%e9%a6%ae%e7%b4%b9%e6%b3%a2-%e9%aa%a8%e5%a4%96%e7%a7%91%e5%b0%88%e5%ae%b6%e6%a2%81%e6%99%ba%e4%bb%81-%e6%9e%97%e5%ae%9a%e5%9c%8b-%e8%95%ad%e6%be%a4%e9%a0%a4%e7%8d%b2%e9%a0%92%e9%87%91%e7%b4%ab%e8%8d%8a%e6%98%9f%e7%ab%a0"
article = News(url)

print("Title:", article.title)
print("Subtitle:", article.subtitle)
print("Content:", article.content)  # show first 300 chars


