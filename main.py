from time import sleep

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

import model.restaurant
import model.review_crawling
import service.restaurant_service
import service.review_crawling_service
from datetime import datetime

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('lang=ko_KR')
chromedriver_path = "chromedriver"
# driver = webdriver.Chrome(os.path.join(os.getcwd(), chromedriver_path), options=options)
# driver = webdriver.Chrome(executable_path='/Users/andes/PycharmProjects/pythonProject/chromedriver2')
driver = webdriver.Chrome(ChromeDriverManager().install())

restaurant_service = service.restaurant_service.Restaurant_service()
review_crawling_service = service.review_crawling_service.Review_crawling_service()


def read(file):
    df = pd.read_csv(file, encoding="cp949")
    return df


def main():
    global driver, load_wb, review_num

    driver.implicitly_wait(4)  # 렌더링 될 때까지 4초 대기
    driver.get('https://map.kakao.com/')
    df = read('./data/shops_edit.csv')
    pd.set_option('display.max_columns', None)
    df = df.loc[df['영업상태코드'] == 1]
    global store
    store = df['사업장명']
    store = store.values
    store_list = store.tolist()
    global address
    address = df['도로명주소_검색용']
    address = address.values
    address = address.tolist()

    for i in range(len(store_list) - 1):
        print('for문 인덱스버전 확인 ' + store_list[i] + address[i])
        search(store_list[i], address[i])
        continue
    driver.quit()
    print("finish")
    print("세은 git clone test~~~~~~~~!!!!!")


def search(place_csv, addr_csv):
    global driver
    restaurant = model.restaurant.Restaurant()
    search_area = driver.find_element(By.XPATH, "//*[@id=\"search.keyword.query\"]")
    search_area.send_keys('마포 ' + place_csv)  # 검색어 입력
    restaurant.original_name = place_csv
    driver.find_element(By.XPATH, '//*[@id="search.keyword.submit"]').send_keys(Keys.ENTER)  # Enter로 검색
    sleep(2)
    # 1번 페이지 place list 읽기
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    try:
        place_lists = soup.select('.placelist > .PlaceItem > .head_item > .tit_name > .link_name ')[0].text
        place_address = soup.select('.info_item > .addr > p')[0].text
        restaurant.address = place_address
        if (place_lists in place_csv) & (addr_csv in place_address):
            print('place가 더 긴 경우')
            crawling(place_lists, restaurant)
        elif (place_csv in place_lists) & (addr_csv in place_address):
            print('place_lists가 더 긴 경우')
            crawling(place_lists, restaurant)
        else:
            print('불일치')
    except (NoSuchElementException, ElementNotInteractableException, IndexError, StaleElementReferenceException) as e:
        print("---검색 결과 없음!---")
        print(e)
    sleep(2)
    search_area.clear()


def crawling(place_lists, restaurant):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    while_flag = False  # 수정(false->False)
    for i, place in enumerate(place_lists):
        place_name = soup.select('.placelist > .PlaceItem > .head_item > .tit_name > .link_name ')[
            0].text  # place name #수정IndexError: list index out of range오류나길래 [0]을 지워볼까? 했는데 지우면 text로 변환하는 문제가 생김;
        restaurant.name = place_name
        place_star = soup.select('.placelist > .PlaceItem > .rating > .score > .num ')[0].text
        restaurant.star = place_star
        # place_address = soup.select('.info_item > .addr > p')[0].text  # place address(도로명주소.지번은 class='lot_number')
        detail_page_xpath = driver.find_element(By.XPATH, '//*[@id="info.search.place.list"]/li[' + str(
            i + 1) + ']/div[5]/div[4]/a[1]')  # 세은해결
        detail_page_xpath.send_keys(Keys.ENTER)
        driver.switch_to.window(driver.window_handles[-1])  # 상세정보 탭으로 변환 / 탭을 객체 리스트로 반환. 즉 맨 마지막 탭으로 이동하는 함수
        sleep(2)
        print('####', place_name, ' ', place_star)

        '''
        try:
            place_update = driver.find_element(By.XPATH, '//*[@id="mArticle"]/div[1]/div[2]/span/span[1]').text
            print('update: ', place_update)
        except(NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException):
            print("no place_update information")

        try:
            place_call = driver.find_element(By.CLASS_NAME, 'txt_contact').text
            print('대표번호: ', place_call)

        except(NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException):
            print("no place_call information")

        try:
            detail_operation = driver.find_element(By.CLASS_NAME, 'btn_more')
            detail_operation.send_keys(Keys.ENTER)
            operation_time = driver.find_element(By.CLASS_NAME, 'inner_floor').text
            print(operation_time)
        except(NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException):
            print("no detailed operation_time information")
        '''

        idx = 1
        extract_review(restaurant)  # 리뷰 추출
        # time.sleep(3)

        idx = 2
        while True:
            try:
                driver.find_element(By.XPATH, "//a[@data-page='" + str(idx) + "']").send_keys(Keys.ENTER)
                sleep(3)
                extract_review(restaurant)
                if (idx % 5 == 0):
                    driver.find_element(By.LINK_TEXT, '다음').send_keys(Keys.ENTER)  # 5페이지가 넘는 경우 다음 버튼 누르기
                    idx += 1
                else:
                    idx += 1
                    sleep(1)
            except (NoSuchElementException, ElementNotInteractableException):
                # print(idx)
                print("no review in crawling")
                break

        driver.close()
        driver.switch_to.window(driver.window_handles[0])  # 검색 탭으로 전환
        # Todo break why?
        break


def extract_review(restaurant):
    global driver
    ret = True
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    try:
        place_update = driver.find_element(By.XPATH, '//*[@id="mArticle"]/div[1]/div[2]/span/span[1]').text
        restaurant.infodttm = place_update
        print('update: ', place_update)
    except(NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException):
        print("no place_update information")

    try:
        place_call = driver.find_element(By.CLASS_NAME, 'txt_contact').text
        restaurant.number = place_call
        print('대표번호: ', place_call)

    except(NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException):
        print("no place_call information")

    try:
        detail_operation = driver.find_element(By.CLASS_NAME, 'btn_more')
        detail_operation.send_keys(Keys.ENTER)
        operation_time = driver.find_element(By.CLASS_NAME, 'inner_floor').text
        restaurant.operation = operation_time.replace("\n", " ").replace("닫기", "")
        print(operation_time)
    except(NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException):
        print("no detailed operation_time information")
    '''
    try:
        date_now = datetime.now()
        date_now = date_now.date()
        date_now = str(date_now)
        restaurant.regdttm = date_now
        print('등록일 : ', date_now)
    except(NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException):
        print("no regdate")
    '''
    # save restaurant

    try:
        id = restaurant_service.get_id(restaurant)
        if not id:
            id = restaurant_service.save(restaurant)
        restaurant.id = id
    except Exception as e:
        print(e, '1')
        return ret
    #TODO id=0으로 불러오는 가게들 별도로 기록
    if id == 0:
        print("fail restaurant : ", restaurant)
        return ret

    # 첫 페이지 리뷰 목록 찾기
    review_lists = soup.select('.list_evaluation > li')  # class명 없어서 그냥 li 쓴건가?
    # 리뷰가 있는 경우
    # result_review = []
    if len(review_lists) != 0:
        for i, review in enumerate(review_lists):
            comment = review.select('.comment_info > .txt_comment > span')  # 리뷰
            # rating = review.select('.grade_star size_s > em')  # 별점
            writername = review.select('.comment_info > .append_item > .link_user ')[0].text  # 작성자
            writedt = review.select('.comment_info > .append_item > .time_write ')[0].text  # 작성일자
            print('@@@@@@@@@@@@@@',writername, writedt)
            if len(comment) != 0 and len(comment[0].text) > 0:
                review_crawling = model.review_crawling.Review_crawling(
                    content=comment[0].text,
                    writer=writername,
                    writedttm=writedt,
                    restaurant=restaurant
                )
                '''
                review_crawling = model.review_crawling.Review_crawling(
                    writer=writername[0].text,
                    restaurant=restaurant
                )
                review_crawling = model.review_crawling.Review_crawling(
                    writedttm = writedt[0].text,
                    restaurant=restaurant
                )
                '''
                print("review_crawling : ", review_crawling)
                try:
                    review_crawling_service.save(review_crawling=review_crawling)
                except Exception as e:
                    print(e, '2')
                    continue
    else:
        print('no review in extract')
        ret = False
    return ret


'''
def search(place, addr):
    global driver
    search_area = driver.find_element(By.XPATH, "//*[@id=\"search.keyword.query\"]")
    search_area.send_keys('마포 ' + place)  # 검색어 입력
    driver.find_element(By.XPATH, '//*[@id="search.keyword.submit"]').send_keys(Keys.ENTER)  # Enter로 검색
    sleep(7)
    # 1번 페이지 place list 읽기
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    try:
        place_lists = soup.select('.placelist > .PlaceItem > .head_item > .tit_name > .link_name ')[0].text
        place_address = soup.select('.info_item > .addr > p')[0].text
        if (place_lists in place) & (addr in place_address):
            print('place가 더 긴 경우')
            crawling(place, place_lists, addr)
        elif (place in place_lists) & (addr in place_address):
            print('place_lists가 더 긴 경우')
            crawling(place, place_lists, addr)
        else:
            print('불일치')
    except (NoSuchElementException, ElementNotInteractableException, IndexError, StaleElementReferenceException):
        print("---검색 결과 없음!---")
    search_area.clear()



def crawling(place, place_lists,addr):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    while_flag = False  # 수정(false->False)
    for i, place in enumerate(place_lists):
        # 광고에 따라서 index 조정해야함
        # if i >= 3:
        #   i += 1
        place_name = soup.select( '.placelist > .PlaceItem > .head_item > .tit_name > .link_name ')[0].text
        place_address = soup.select('.info_item > .addr > p')[0].text  # place address(도로명주소.지번은 class='lot_number')
        place_star = soup.select('.placelist > .PlaceItem > .rating > .score > .num ')[0].text
        place_call = soup.select('.placelist > .PlaceItem > .info_item > .contact > .phone')[0].text

        detail_page_xpath = driver.find_element(By.XPATH, '//*[@id="info.search.place.list"]/li[' + str(i + 1) + ']/div[5]/div[4]/a[1]')  # 세은해결
        detail_page_xpath.send_keys(Keys.ENTER)
        driver.switch_to.window(driver.window_handles[-1])  # 상세정보 탭으로 변환 / 탭을 객체 리스트로 반환. 즉 맨 마지막 탭으로 이동하는 함수
        sleep(5)
        print('####', place_name, ' ', place_star)

        try:
            place_update = driver.find_element(By.XPATH, '//*[@id="mArticle"]/div[1]/div[2]/span/span[1]').text
            print('update: ', place_update)
            place_call = driver.find_element(By.XPATH, '//*[@id="mArticle"]/div[1]/div[2]/div[3]/div/div[1]/span').text
            print('대표번호: ', place_call)

            detail_operation = driver.find_element(By.XPATH, '//*[@id="mArticle"]/div[1]/div[2]/div[2]/div/div[1]/ul/li/a')
            detail_operation.send_keys(Keys.ENTER)
            
            operation_time = driver.find_element(By.XPATH, '//*[@id="mArticle"]/div[1]/div[2]/div[2]/div/div[2]/div').text
            # print('휴무일: ', place_closehour)
            print(operation_time)
        except (NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException):
            print("no detailed information")


        idx = 1
        extract_review(place_name)  # 리뷰 추출
        time.sleep(5)

        idx = 2
        while True:
            try:
                driver.find_element(By.XPATH, "//a[@data-page='" + str(idx) + "']").send_keys(Keys.ENTER)
                sleep(3)
                extract_review(place_name)
                if (idx % 5 == 0) :
                    driver.find_element(By.LINK_TEXT, '다음').send_keys(Keys.ENTER)  # 5페이지가 넘는 경우 다음 버튼 누르기
                    idx += 1
                else :
                    idx += 1
                    sleep(3)
            except (NoSuchElementException, ElementNotInteractableException):
                #print(idx)
                print("no review in crawling")
                break

        driver.close()
        driver.switch_to.window(driver.window_handles[0])  # 검색 탭으로 전환
        break


def extract_review(place_name):
    global driver
    ret = True
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # 첫 페이지 리뷰 목록 찾기
    review_lists = soup.select('.list_evaluation > li')  # class명 없어서 그냥 li 쓴건가?
    # 리뷰가 있는 경우
    #result_review =[]

    if len(review_lists) != 0:
        for i, review in enumerate(review_lists):
            comment = review.select('.comment_info > .txt_comment > span')  # 리뷰
            #rating = review.select('.star_info > .grade_star size_s > num_rate')  # 별점
            #val = ''
            if len(comment) != 0:
                comment = comment[0].text
                print(comment)

    else:
        print('no review in extract')
        ret = False
    return ret
'''
if __name__ == "__main__":
    main()
