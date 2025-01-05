import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "https://www.shinhancard.com"
CREDIT_CARD_URL = 'https://www.shinhancard.com/pconts/html/card/check/MOBFM282R09.html'
print(1)

# 홈페이지에서 카드상세 URL 추출
def get_card_links():

    driver = webdriver.Chrome()
    driver.get(CREDIT_CARD_URL)
    # 페이지 열리는 속도가 느려서 데이터가 넘어오기전에 함수가 종료되는 문제 해결방안
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'card_name')))
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.prettify())

    card_links = []
    # a 태그 중 특정 클래스를 가진 항목 검색 (HTML 구조에 맞게 수정 필요)
    card_elements = soup.find_all('a', class_='card_name')  

    for card in card_elements: 
        href = card['href']  
        print(href)
        # 상대 경로를 절대 경로로 변환
        full_link = BASE_URL + href  
        card_links.append(full_link)  
    
    driver.quit()
    # print(card_links)
    return card_links




# def card_benefit(card_url):
    
#     driver = webdriver.Chrome()
#     driver.get(card_url)
    
#     html = driver.page_source
#     soup = BeautifulSoup(html,'html.parser')
    
#     benefit_section = soup.find('div', class_='sect benefit')
#     benefit_item = benefit_section.find_all('div', class_='item')
    
#     card_benefits = []
#     for item in benefit_item:
#         title = item.find('strong', class_='title').text.strip()
#         benefits = [li.text.strip() for li in item.find_all('li')]
#         card_benefits.append(title)
#         card_benefits.append(benefits)
    
#     print(card_benefits)
# card_links = get_card_links()
# for link in card_links:
#     card_bene = card_benefit(link)
#     print(card_benefit)


# 상세페이지에서 카드 상세 데이터 추출
def get_card_details(card_url):
    driver = webdriver.Chrome()
    driver.get(card_url)  # 카드 상세 페이지 로드
    WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[@class='card_name']"))
)

    html = driver.page_source  # HTML 코드 추출
    soup = BeautifulSoup(html, 'html.parser')

    # 카드 종류 지정(신용카드는 카드이름이 없음)
    # 여기만 변경하기!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    card_company = '신한'
    card_type = '체크카드'
    card_benefits_category = '공공'

    # 카드 이름 추출 (예시로 '카드명'이 있는 곳을 찾는 코드)
    card_name=None
    card_find = soup.find('div', id='info')
    # card_name = card_find.find('div', class_='card_name').find('h1').get_text(strip=True)
    card_find = soup.find('div', id='cardCompareAfter')  # id가 정확한지 확인
    if card_find:
        card_name_div = card_find.find('div', class_='card_name')  # class도 정확한지 확인
        if card_name_div:
            h1_tag = card_name_div.find('h1')  # h1 태그 확인
            if h1_tag:
                card_name = h1_tag.get_text(strip=True)  # 카드 이름 추출


    
    # 각 카드 헤택 정보 추출
    benefit_section = soup.find('div', class_='sect benefit')
    # 혜택정보가 없을시 넘어가기
    if not benefit_section:
        print('혜택정보없음, 넘어감')
        driver.quit()
        return None
    
    benefit_item = benefit_section.find_all('div', class_='item')

    # 이미지 url 추출
    img_url = soup.find('span', class_='front').find('img')['src']
    card_img = BASE_URL + img_url
    # print (card_img)
    
    card_benefits = []
    for item in benefit_item: 
            title = item.find('strong', class_='title')
            # benefits = [li.text.strip() for li in item.find_all('li')]
            
            if title:
                title = title.text.strip()
            else:
                continue
            
            benefits = item.find_all('li')
            if benefits:
                benefits = [li.text.strip() for li in benefits]
            else:
                continue
        
            card_benefits.append({
                'title': title,
                'benefits': benefits})
            # print(card_benefits)

    card_details = {
        'card_company' : card_company,
        'card_type' : card_type,
        'card_name' : card_name,
        'card_url' : card_url,
        'card_img' : card_img,
        'card_benefits_category' : card_benefits_category,
        'card_benefits' : card_benefits
    }

    # print(card_details)
    driver.quit()
    return card_details

card_links = get_card_links()

all_card_details = []

try:
    for link in card_links: 
        card_info = get_card_details(link)
        if card_info:
            all_card_details.append(card_info)
    
    # json 파일 더미데이터 만들기
    with open('card_details.json', 'w', encoding='utf-8') as json_file:
        json.dump(all_card_details, json_file, ensure_ascii=False, indent=4)
        print("카드 정보가 card_details.json 파일에 저장되었습니다.")

except Exception as e:
    print(f"오류 발생: {e}")
    # 오류가 발생하면 그때까지의 데이터를 저장
    with open('card_details.json', 'w', encoding='utf-8') as json_file:
        json.dump(all_card_details, json_file, ensure_ascii=False, indent=4)
        print("오류 발생 시, 이전 데이터만 저장되었습니다.")


