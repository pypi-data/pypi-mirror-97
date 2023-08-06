import requests

cookies = {
    '_ga': 'GA1.2.1281528400.1612170044',
    '__cfduid': 'd2763dfa3b999ebfeba4a7a48a89e298b1614781754',
    'kf_session': '9SyErQjE3YkpWeK1eLnSDVvsRF3r3GFh',
    'public_token': 'U7N47NluNhROqMjPCUYoiNxzUk3ffdML',
    'user_id': 'XB3665',
    'enctoken': '0WD1v0ztdy28FQvza1kCCUuxWEQJqssgehEg9k0+7OPONzmpSKLGAPj30r7yVIroXPoTsUOv8No3221KaE7DNeC5QC3TUQ==',
}

headers = {
    'authority': 'kite.zerodha.com',
    'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
    'accept': 'application/json, text/plain, */*',
    'authorization': 'enctoken 0WD1v0ztdy28FQvza1kCCUuxWEQJqssgehEg9k0+7OPONzmpSKLGAPj30r7yVIroXPoTsUOv8No3221KaE7DNeC5QC3TUQ==',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://kite.zerodha.com/chart/web/tvc/NSE/AARTIDRUGS/1147137',
    'accept-language': 'en-US,en;q=0.9,kn;q=0.8',
}

response = requests.get('https://kite.zerodha.com/oms/instruments/historical/1147137/minute?user_id=XB3665&oi=1&from=2021-03-04&to=2021-03-05', headers=headers, cookies=cookies)
print(response.content)