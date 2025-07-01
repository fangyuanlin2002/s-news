from news import News, MingPaoNews, OrientalDailyNews,WenWeiPo,TaKungPao,HK01,InMediaHK,InitiumMedia,TheWitness,RTHK,HKET,HKEJ,TheStandard,HKFreePress,OrangeNews,HKGovernmentNews,ICable,HKCD,TheEpochTimes,HKCourtNews,NowTV,ChineseBBC,VOC,DeutscheWelle,ChineseNewYorkTimes,PeopleDaily,XinhuaNewsAgency,GlobalTimes, CCTV

url = "https://www.globaltimes.cn/page/202507/1337381.shtml"
article =CCTV(url)

print("Title:", article.title)
print("Content:", article.content)  # show first 300 chars


