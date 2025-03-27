from http.cookiejar import domain_match

from lxml import etree
import requests
from urllib.parse import urlparse

sitemap_url = "https://theemployhires.com/sitemap.xml"
parsed_domain = urlparse(sitemap_url).netloc
response = requests.get(sitemap_url)
if response.status_code == 200:
    tree = etree.fromstring(response.content)
    urls = tree.xpath("//*[contains(text(),'https')]/text()")
    def check_url_status(url):
        try:
            res = requests.get(url.strip(), timeout=5)
            if parsed_domain in urlparse(url).netloc:
                print(f"{url} - Status: {res.status_code} - Domain Verified")
            else:
                domain_name()
                print(f"{url} - Status: {res.status_code} - Domain Mismatch")
        except requests.exceptions.RequestException as e:
            print(f"{url} - Error: {e}")
    if urls:
        for url in urls:
            check_url_status(url)
    else:
        print("No URLs found in the sitemap.")
else:
    print(f"Failed to fetch sitemap. Status code: {response.status_code}")

