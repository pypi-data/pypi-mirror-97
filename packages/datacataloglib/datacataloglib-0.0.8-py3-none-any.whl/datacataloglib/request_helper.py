from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import requests, os


retry_strategy = Retry(
    total=5,
    backoff_factor=15,
    status_forcelist=[429, 500, 502, 503, 504],
    method_whitelist=["HEAD", "GET", "OPTIONS"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)


# def get_dvc_scout_auth():
#   return { "auth": HTTPBasicAuth(os.getenv('PROJECT_INFO_USER'), os.getenv('PROJECT_INFO_PASSWORD')) }
  
  
def request_post_if_has_value(url, json=None, extra={}):
  if json:
    for each_row in json:
      response = http.post(url, json=each_row, **extra)
      if response.status_code == 200:
        return response.json() 
      else: 
          False
        