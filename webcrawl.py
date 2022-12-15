import selenium
import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pygsheets
from oauth2client.service_account import ServiceAccountCredentials
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

path = r'\chromedriver.exe'
driver = webdriver.Chrome(executable_path = path)
driver.get(r'https://www.amazon.com/')
sleep(5)
driver.find_element(By.XPATH,'//*[@id="nav-search-dropdown-card"]/div').click()
driver.find_element(By.XPATH,r'//*[@id="searchDropdownBox"]/option[8]').click()
driver.find_element(By.XPATH,r'//*[@id="nav-search-submit-button"]').click()
sleep(5)
a = driver.find_elements(By.CLASS_NAME,r'a-cardui-body')
a[1].click()
product_name_list = []
avg_star_list = []
rating_count_list = []
price_list = []
reviewer_name_list = []
stances_list = []
review_list = []
reviewer_star_list = []
p = 2

while p <= 20:
    print('page',p-1)
    cur_link = driver.current_url
    for product in range(2,26):
        print('page ',p-1,' sản phẩm',product - 1)
        try:
            driver.find_element(By.XPATH,f'//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[{product}]').click()
        except:
            continue
        sleep(2)
        try:
            name = driver.find_element(By.XPATH,r'//*[@id="productTitle"]').text
            print(name)
            rating_star = driver.find_element(By.XPATH,r'//*[@id="acrPopover"]').get_attribute('title')
            print(rating_star)
            rating_count = driver.find_element(By.XPATH,r'//*[@id="averageCustomerReviews"]/span[3]').text
            print(rating_count)
            price = '$0.00'
            try:
                price = '$' + driver.find_element(By.XPATH,r'//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span/span[2]/span[2]').text
            except:
                price = '$'+driver.find_element(By.XPATH,r'//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[2]/span[2]/span[2]').text
            finally:
                pass
            print(price)
            driver.find_element(By.XPATH,r'//*[@id="acrCustomerReviewText"]').click()
            driver.find_element(By.XPATH,r'//*[@data-hook="see-all-reviews-link-foot"]').click()
            sleep(4)
            # most recent review
            driver.find_element(By.CLASS_NAME,r'a-dropdown-prompt').click()
            driver.find_element(By.XPATH,r'//*[@id="sort-order-dropdown_1"]').click()
            
            k = 1
            while k <= 10:
                height = driver.execute_script("return document.body.scrollHeight")
                for scrol in range(100,height,100):
                    driver.execute_script(f"window.scrollTo(0,{scrol})")
                    sleep(0.1)
                reviews = driver.find_elements(By.XPATH,r'//*[@data-hook="review"]')
                for rev in range(len(reviews)):
                    try:
                        reviewer = driver.find_element(By.XPATH,f'//*[@id="customer_review-{reviews[rev].get_attribute("id")}"]/div[1]/a/div[2]/span').text
                        stance = driver.find_element(By.XPATH,f'//*[@id="customer_review-{reviews[rev].get_attribute("id")}"]/div[2]/a[2]/span').text
                        review = driver.find_element(By.XPATH,f'//*[@id="customer_review-{reviews[rev].get_attribute("id")}"]/div[4]/span/span').text
                        reviewer_star = driver.find_element(By.XPATH,f'//*[@id="customer_review-{reviews[rev].get_attribute("id")}"]/div[2]/a[1]').get_attribute('title')
                        
                        product_name_list.append(name)
                        avg_star_list.append(float(rating_star[:3]))
                        rating_count_list.append(rating_count)
                        price_list.append(float(price[1:]))
                        reviewer_name_list.append(reviewer)
                        stances_list.append(stance)
                        review_list.append(review)
                        reviewer_star_list.append(float(reviewer_star[:3]))
                    except:
                        pass
                print('page ',p-1,' sản phẩm',product - 1,' trang: ',k)
                driver.find_element(By.XPATH,r'//*[@id="cm_cr-pagination_bar"]/ul/li[2]/a').click()
                k += 1
                sleep(2)
            driver.get(cur_link)
            sleep(3)
        except:
            driver.get(cur_link)
    driver.find_element(By.XPATH,f'//*[@aria-label="Go to next page, page {p}"]').click()
    sleep(4)
    p += 1


result_df = pd.DataFrame(zip(product_name_list,avg_star_list,rating_count_list,price_list,reviewer_name_list,stances_list,review_list,reviewer_star_list))
result_df.columns = [['product name','average star','rating count','price','reviewer','summary','review','score']]
result_df.to_csv('review_data.csv',index = False)