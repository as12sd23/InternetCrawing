import requests
import datetime
from newspaper import Article
#from gensim.summarization import summarize
headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; fv:11.0) like Gecko"}

url = "https://news.naver.com/breakingnews/section/105/"
NewsClass = ["226"] #, "226", "227", "230", "732", "283", "229", "731"]
# 모바일, 인터넷/SNS, 통신/뉴미디어, IT일반, 보안/해킹, 컴퓨터, 게임/리뷰, 과학일반
ChracterReplace = {
    "&#x27;" : "'",
    "&quot;" : '"',
    "&lt;" : "<",
    "&gt;" : ">",
    "&amp;" : "&",
    "&#40;" : "(",
    "&#41;" : ")",
    "&#x2F;" : "/",
    "&#x3D;" : "=",
    "&#x60;" : "~"
    }

for Plus in NewsClass:
    site = requests.get(url + Plus, headers = headers)
    SiteData = site.text
    count = SiteData.count('"sa_text_lede">')

    for i in range(count):
        # 제목
        pos1 = SiteData.find('"sa_text_lede">') + len('"sa_text_lede">')
        SiteData = SiteData[pos1:]
        
        pos2 = SiteData.find("</div>")
        ExtractData = SiteData[:pos2]
        
        SiteData = SiteData[pos2 + 1:]

        #주소
        pos1 = SiteData.find('"sa_thumb_inner">')
        SiteData = SiteData[pos1:]
        pos1 = SiteData.find('<a href="') + len ('<a href="')
        SiteData = SiteData[pos1:]

        pos2 = SiteData.find('" class="')
        AddressData = SiteData[:pos2]

        SiteData = SiteData[pos2 + 1:]

        # 주소로 들어가기
        AddressInto = requests.get(AddressData, headers = headers)
        AddressText = AddressInto.text

        pos1 = AddressText.find("<em class=")
        AddressText = AddressText[pos1:]
        pos1 = AddressText.find('<a href="') + len ('<a href="')
        AddressText = AddressText[pos1:]

        pos2 = AddressText.find('" target=')
        AddressSiteData = AddressText[:pos2]

        
        
        # 제목 글자 치환
        for key, element in ChracterReplace.items():
            ExtractData = ExtractData.replace(key, element)
                
                    
        print(i + 1, ExtractData)
        print()
        
        #본문으로 긁어오기
        article = Article(AddressSiteData, language = 'ko')
        article.download()
        article.parse()
        
        print(article.title)
        print(article.summary(article.text))
        print()
        article = 0
