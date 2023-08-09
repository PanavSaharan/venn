from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_product_price(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_price_amazon = get_product_price_amazon(product_name)
        product_price_flipkart = get_product_price_flipkart(product_name)
        product_price_croma = get_product_price_croma(product_name)

        context = {
            'product_name': product_name,
            'product_price_amazon': product_price_amazon,
            'product_price_flipkart': product_price_flipkart,
            'product_price_croma': product_price_croma
        }

        return render(request, 'product_price.html', context)

    return render(request, 'get_product_price.html')


def get_product_price_amazon(product_name):
    """Get the product price from Amazon"""
    url_amazon = f"https://www.amazon.in/s?k={product_name.replace(' ', '+')}"
    browser = get_webdriver()
    browser.get(url_amazon)

    # List of possible XPaths for the product link
    xpath_list = [
        '//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[3]/div/div/div/div/div/div[2]/div/div/div[1]/h2/a',
        '//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[3]/div/div/div/div/div/div/div/div[2]/div/div/div[1]/h2/a',
        '//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[3]/div/div/div/div/div[2]/div[2]/h2/a',
        '//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[3]/div/div/div/div/div/div/div[2]/div[1]/h2/a'
    ]

# My name is Aarit Hooda and I am very intrested in coding and impressing people by my ability of solving question and my ability to solve any problem y coding and rn I am working on a very big project called venn and this is working out very well.
    # Loop through each XPath and try to find the product link
    for xpath in xpath_list:
        try:
            product_link = browser.find_element(By.XPATH, xpath)
            browser.get(product_link.get_attribute('href'))
            product_name_element = browser.find_element(By.XPATH, '//*[@id="productTitle"]')
            product_price = browser.find_element(By.XPATH, '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[2]/span[2]')

            return {
                'product_name': product_name_element.text,
                'price': product_price.text,
                'website': 'Amazon'
            }
        except:
            pass

    return {'error': 'Unable to find the product on Amazon'}


def get_product_price_flipkart(product_name):
    """Get the product price from Flipkart"""
    url_flipkart = f"https://www.flipkart.com/search?q={product_name.replace(' ', '%20')}"
    browser = get_webdriver()
    browser.get(url_flipkart)

    # List of possible XPaths for the product link
    xpath_list = [
        '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div/div/a',
        '//*[@id="container"]/div/div[3]/div/div[2]/div[2]/div/div[3]/div/div/a[1]',
        '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div/a'
    ]

    # Loop through each XPath and try to find the product link
    for xpath in xpath_list:
        try:
            product_link = browser.find_element(By.XPATH, xpath)
            browser.get(product_link.get_attribute('href'))
            product_name_element = browser.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[1]/h1/span')
            product_price = browser.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[4]/div[1]/div/div[1]')

            return {
                'product_name': product_name_element.text,
                'price': product_price.text,
                'website': 'Flipkart'
            }
        except:
            pass

    return {'error': 'Unable to find the product on Flipkart'}


def get_product_price_croma(product_name):
    """Get the product price from Croma"""
    url_croma = f"https://www.croma.com/searchB?q={product_name.replace(' ', '%20')}%3Arelevance&text={product_name.replace(' ', '%20')}"
    browser = get_webdriver()
    browser.get(url_croma)

    # Set the maximum time to wait for a page to load
    max_wait_time = 1  # in seconds

    # Create a loop that refreshes the page until it loads
    while True:
        try:
            # Wait for an element on the page to load
            element = WebDriverWait(browser, max_wait_time).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[3]/div[1]/div[2]/div/div/div[3]/ul/li[1]/div/div[2]/div[1]/h3/a')))
            break
        except:
            browser.refresh()

    product_link = browser.find_element(By.XPATH, '/html/body/main/div[3]/div[1]/div[2]/div/div/div[3]/ul/li[1]/div/div[2]/div[1]/h3/a')
    browser.get(product_link.get_attribute('href'))
    product_name_element = browser.find_element(By.XPATH, '//*[@id="pdpdatael"]/div[2]/div[1]/div/div/div/div[3]/div/ul/li[1]/h1')
    product_price = browser.find_element(By.XPATH, '//*[@id="pdp-product-price"]')

    return {
        'product_name': product_name_element.text,
        'price': product_price.text,
        'website': 'Croma'
    }


def get_webdriver():
    """Create a webdriver object for Chrome"""
    wait_imp = 10
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--start-maximized')
    browser = webdriver.Chrome(executable_path='C:/Users/Panav Saharan/Downloads/chromedriver.exe', options=chrome_options)
    return browser
