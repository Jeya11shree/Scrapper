import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

class CoinMarketCap:
    BASE_URL = "https://coinmarketcap.com/currencies/"

    def __init__(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def get_coin_data(self, coin):
        url = self.BASE_URL + coin.lower() + "/"
        self.driver.get(url)
        time.sleep(5)  # Allow time for the page to load

        try:
            price = self.driver.find_element(By.CSS_SELECTOR, '.priceValue').text
            price_change = self.driver.find_element(By.CSS_SELECTOR, '.sc-15yy2pl-0.kAXKAX span').text
            market_cap = self.driver.find_element(By.CSS_SELECTOR, '.statsValue').text
            market_cap_rank = self.driver.find_elements(By.CSS_SELECTOR, '.sc-16r8icm-0.kXPxnI div')[0].text
            volume = self.driver.find_elements(By.CSS_SELECTOR, '.statsValue')[1].text
            volume_change = self.driver.find_element(By.CSS_SELECTOR, '.sc-15yy2pl-0.kAXKAX span').text

            circulating_supply = self.driver.find_element(By.CSS_SELECTOR, '.maxSupplyValue').text
            total_supply = self.driver.find_elements(By.CSS_SELECTOR, '.maxSupplyValue')[1].text
            diluted_market_cap = self.driver.find_element(By.CSS_SELECTOR, '.sc-1ow4cwt-1.ieFnWP span').text

            contracts = []
            for contract in self.driver.find_elements(By.CSS_SELECTOR, '.contract-address'):
                contracts.append({
                    'name': contract.find_element(By.CSS_SELECTOR, 'div').text,
                    'address': contract.find_element(By.CSS_SELECTOR, 'a').text
                })

            official_links = []
            for link in self.driver.find_elements(By.CSS_SELECTOR, '.link-button'):
                official_links.append({
                    'name': link.get_attribute('innerHTML').strip(),
                    'link': link.get_attribute('href')
                })

            socials = []
            for social in self.driver.find_elements(By.CSS_SELECTOR, '.iconLink'):
                socials.append({
                    'name': social.find_element(By.CSS_SELECTOR, 'a').get_attribute('title'),
                    'url': social.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                })

            return {
                "price": price,
                "price_change": price_change,
                "market_cap": market_cap,
                "market_cap_rank": market_cap_rank,
                "volume": volume,
                "volume_change": volume_change,
                "circulating_supply": circulating_supply,
                "total_supply": total_supply,
                "diluted_market_cap": diluted_market_cap,
                "contracts": contracts,
                "official_links": official_links,
                "socials": socials
            }
        except Exception as e:
            return {"error": str(e)}
        finally:
            self.driver.quit()
