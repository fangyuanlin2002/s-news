from news import News, MingPaoNews, OrientalDailyNews,WenWeiPo,TaKungPao,HK01,InMediaHK,InitiumMedia,TheWitness,RTHK,HKET,HKEJ,TheStandard,HKFreePress,OrangeNews,HKGovernmentNews,ICable,HKCD,TheEpochTimes,HKCourtNews,NowTV

url = "https://www.bloomberg.com/news/articles/2025-07-01/ecb-s-guindos-says-euro-gain-beyond-1-20-would-be-complicated?srnd=phx-economics-v2"
article =News(url)

print("Title:", article.title)
print("Content:", article.content)  # show first 300 chars


