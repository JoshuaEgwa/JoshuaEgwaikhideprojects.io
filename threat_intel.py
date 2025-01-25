import requests
import json
from prettytable import PrettyTable

VIRUSTOTAL_API_KEY = "0cc74a434fb5a3386f9faae0cae259e0aaa72f593f7831f419d1e2c00b1231a9"
ABUSEIPDB_API_KEY = "3984ccc1e1619bd3e25d8bee766deb83706805bf1dad47a0f5ed373202357c1a10ddb25ecec37261"

def get_virustotal_report(domain):
    url = f"https://www.virustotal.com/vtapi/v2/domain/report?apikey={VIRUSTOTAL_API_KEY}&domain={domain}"
    response = requests.get(url)
    return response.json()

def get_circl_passivedns_report(domain):
    url = f"https://www.circl.lu/pdns/query/{domain}"
    response = requests.get(url)
    print("CIRCL Response Status Code: ", response.status_code)
    print("CIRCL Response Content:", response.text)
    if response.status_code ==200:
        return response.json()
    else:
        return{}
    return response.json()

def get_abuseipdb_report(ip):
    url = f"https://api.abuseipdb.com/api/v2/check"
    headers = {
        'Accept': 'application/json',
        'key': ABUSEIPDB_API_KEY
    }
    params = {
        'ipAddress': ip,
        'maxAgeInDays': '90'
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def display_results (virus_data, circl_data, abuse_data, target):
    table = PrettyTable()
    table.field_names = ["Service", "Indicator", "Details"]

    vt_detected = virus_data.get('detected_urls', [])
    table.add_row(["VirusTotal", "Detected URLs", len(vt_detected)])

    circl_records = len(circl_data) if isinstance(circl_data, list) else 0
    table.add_row(["CIRCL Passive DNS", "DNS Records Found", circl_records])

    abuse_score = abuse_data.get('data', {}).get('abuseConfidenceScore', 0)
    table.add_row(["AbuseIPDB", "Abuse Score", abuse_score])

    print(f"Threat Intelligence Report for: {target}")
    print(table)

def main():
    target = input("Enter a domain or IP address: ").strip()

    if target:
        print("\nFetching VirusTotal Report...")
        virus_data = get_virustotal_report(target)

        print("\n Fetching CIRCL Passive DNS Report...")
        circl_data = get_circl_passivedns_report(target)

        print("\n Fetching AbuseIPDB Report...")
        abuse_data= get_abuseipdb_report(target)

        display_results(virus_data, circl_data, abuse_data, target)
    else:
        print("Invalid Input")

if __name__ == "__main__":
    main()