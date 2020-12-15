import requests
from bs4 import BeautifulSoup
import re
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}


def create_soup(url):
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup


def scrape_weather():
    print("[오늘의 날씨]")
    url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EC%84%9C%EC%9A%B8+%EB%82%A0%EC%94%A8&oquery=%EC%98%A4%EB%8A%98%EC%9D%98%EB%82%A0%EC%94%A8&tqi=U9l9Xwprvxssss7QyZ4ssssssh0-353764"
    soup = create_soup(url)

    # 흐림, 어제보다 OO도 높아요
    cast = soup.find("p", attrs={"class": "cast_txt"}).get_text()

    # 현재온도(최저, 최고)
    curr_temp = soup.find(
        "p", attrs={"class": "info_temperature"}).get_text().replace("도씨", "")
    min_temp = soup.find("span", attrs={"class": "min"}).get_text()  # 최저 온도
    max_temp = soup.find("span", attrs={"class": "max"}).get_text()  # 최고 온도

    # 오전 강수 확률, 오후 강수 확률
    morning_rain_rate = soup.find(
        "span", attrs={"class": "point_time morning"}).get_text().strip()
    afternoon_rain_rate = soup.find(
        "span", attrs={"class": "point_time afternoon"}).get_text().strip()

    # 미세먼지
    # 초미세먼지
    dust = soup.find("dl", attrs={"class": "indicator"})
    pm10 = dust.find_all("dd")[0].get_text()  # 미세먼지
    pm25 = dust.find_all("dd")[1].get_text()  # 초미세먼지

    # 출력
    print(cast)
    print("현재 {} (최저 {} / 최고 {})".format(curr_temp, min_temp, max_temp))
    print("오전 {} / 오후 {}".format(morning_rain_rate, afternoon_rain_rate))
    print()
    print("미세먼지 {}".format(pm10))
    print("초미세먼지 {}".format(pm25))
    print()


def scrape_headline_news():
    print("[헤드라인 뉴스]")
    url = "https://news.naver.com"
    soup = create_soup(url)

    # news_list = soup.find(
    # "ul", attrs={"class": "hdline_article_list"}).find_all("li", limit = 3) # 최대 3개만 가져와라
    news_list = soup.find(
        "ul", attrs={"class": "hdline_article_list"}).find_all("li")
    for index, news in enumerate(news_list):
        title = news.find("a").get_text().strip()
        link = url + news.find("a")["href"]
        print("{}. {}".format(index+1, title))
        print("  (링크 : {})".format(link))
    print()


def scrape_it_news():
    print("[IT 뉴스]")
    url = "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=105&sid2=230"
    soup = create_soup(url)
    news_list = soup.find(
        "ul", attrs={"class": "type06_headline"}).find_all("li")
    for index, news in enumerate(news_list):
        a_idx = 0
        img = news.find("img")

        if img:
            a_idx = 1  # img 태그가 있으면 1번째 a 태그의 정보를 사용

        title = news.find_all("a")[a_idx].get_text().strip()
        link = news.find_all("a")[a_idx]["href"]
        print("{}. {}".format(index+1, title))
        print("  (링크 : {})".format(link))
    print()


def scrape_english():
    print("[오늘의 영어 회화]")
    url = "https://www.hackers.co.kr/?c=s_eng/eng_contents/I_others_english&keywd=haceng_submain_lnb_eng_I_others_english&logger_kw=haceng_submain_lnb_eng_I_others_english"
    soup = create_soup(url)
    sentences = soup.find_all("div", attrs={"id": re.compile("^conv_kor_t")})
    print("(영어 지문)")
    for sentence in sentences[len(sentences)//2:]:  # 8문장 있다고 가정할 때, 4~7까지 잘라서
        print(sentence.get_text().strip())

    print()
    print("(한글 지문)")
    for sentence in sentences[:len(sentences)//2]:  # 8문장 있다고 가정할 때, 0~3까지 잘라서
        print(sentence.get_text().strip())


def today():
    tm = time.localtime()
    today = time.strftime("%Y-%m-%d %I:%M:%S %p", tm)
    return today


if __name__ == "__main__":
    scrape_weather()  # 오늘의 날씨 정보 가져오기
    scrape_headline_news()  # 헤드라인 뉴스 정보 가져오기
    scrape_it_news()  # IT뉴스 정보 가져오기
    scrape_english()  # 오늘의 영어 회화 가져오기
