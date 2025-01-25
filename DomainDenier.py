import time
import os


hosts_path = r"c:\Windows\System32\drivers\etc\hosts"

redirect_ip = "127.0.0.1"
blocked_sites =["twitter.com", "www.twitter.com", "x.com", "www.x.com", "reddit.com", "www.reddit.com", "redgifs.com", "old.reddit.com", "v.redgifs.com" "www.redgifs.com"]


def block_sites():
    with open(hosts_path, 'r+') as file:
        content = file.read()
        for site in blocked_sites:
            if site not in content:
                file.write(f"{redirect_ip} {site}\n")

def unblocked_sites():
    with open(hosts_path, 'r') as file:
        lines = file.readlines()
    with open(hosts_path, 'w') as file:
        for line in lines:
            if not any(site in line for site in blocked_sites):
                file.write(line)


if __name__ =="__main__":
    while True:
        block_sites()
        os.system("ipconfig /flushdns")
        time.sleep(60*60)