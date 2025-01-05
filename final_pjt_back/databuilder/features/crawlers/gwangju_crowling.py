import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver

BASE_URL = "https://www.shinhancard.com"
CREDIT_CARD_URL = 'https://www.samsungcard.com/home/card/cardinfo/PGHPPCCCardCardinfoCheckcard001'
print(1)

# 홈페이지에서 추출
def get_card_links():


    driver = webdriver.Chrome()
    driver.get(CREDIT_CARD_URL)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.prettify())

    card_links = []
    # a 태그 중 특정 클래스를 가진 항목 검색 (HTML 구조에 맞게 수정 필요)
    card_elements = soup.find_all('a', class_='card_name')  

    for card in card_elements:  # 각 링크 요소 반복
        href = card['href']  # a 태그의 href 속성 값 가져오기
        # print(href)
        full_link = BASE_URL + href  # 상대 경로를 절대 경로로 변환
        card_links.append(full_link)  # 리스트에 추가
    
    driver.quit()
    # print(card_links)
    return card_links
# print(get_card_links())


