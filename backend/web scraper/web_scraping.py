from news import News, MingPaoNews, OrientalDailyNews,WenWeiPo,TaKungPao,HK01,InMediaHK,InitiumMedia,TheWitness,RTHK,HKET,HKEJ,TheStandard

url = "https://www.thestandard.com.hk/hong-kong-news/article/305786/Vietnamese-womans-disappearance-now-a-murder-investigation-says-HK-police"
article =TheStandard(url)

print("Title:", article.title)
print("Content:", article.content)  # show first 300 chars


