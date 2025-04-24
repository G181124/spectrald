import requests
import json
import os
import re
from sigunit.utils import color_text
from bs4 import BeautifulSoup

def run_username_check(username, verbose=False):
    sites_path = os.path.join(os.path.dirname(__file__), "sites.json")
    with open(sites_path, "r") as f:
        sites = json.load(f)

    output_lines = [f"Hasil pencarian untuk username: {username}\n"]
    found_count = 0

    for site, url in sites.items():
        check_url = url.replace("{username}", username)
        try:
            r = requests.get(check_url, timeout=10)
            if r.status_code == 200:
                line = f"[+] {site:<13} → ✅ {check_url}"
                print(color_text(line, 'green'))
                output_lines.append(line)
                found_count += 1
                if verbose:
                    details = get_profile_info(site, username, check_url)
                    output_lines.extend(details)
        except:
            pass

    print(f"\n[✓] Pencarian selesai — {found_count} hasil ditemukan.")
    print(f"📁 Hasil disimpan di: hasil/{username}.txt")

    output_lines.append(f"\n[✓] Pencarian selesai — {found_count} hasil ditemukan.")
    output_lines.append(f"📁 Hasil disimpan di: hasil/{username}.txt")

    output_lines.append("\n[+] Dork OSINT:")
    print("\n[+] Dork OSINT:")
    dorks = [
        f'"{username}" site:pastebin.com | site:throwbin.io | site:hastebin.com | site:ghostbin.com',
        f'"{username}" inurl:admin | inurl:login | inurl:signin | inurl:dashboard',
        f'"{username}" intitle:index.of | inurl:/config | inurl:/backup',
        f'"{username}" filetype:pdf | filetype:docx | filetype:xls | filetype:txt',
        f'"{username}" site:github.com | site:replit.com | site:glitch.com | site:bitbucket.org',
        f'"{username}" site:linkedin.com/in | site:about.me | site:medium.com',
        f'"{username}" site:facebook.com | site:twitter.com | site:instagram.com | site:t.me',
        f'"{username}" site:jsfiddle.net | site:codepen.io',
        f'"{username}" site:telegra.ph | site:blogspot.com',
        f'"{username}" site:archive.org',
        f'intext:"{username}" AND ("password" | "passwd" | "login")',
        f'intext:"{username}" AND ("sql" | "database" | "root")',
        f'"ssh-rsa" "{username}" site:github.com'
    ]
    for dork in dorks:
        url = f"https://www.google.com/search?q={requests.utils.quote(dork)}"
        line = f"    {url}"
        print(line)
        output_lines.append(line)

    return output_lines  # Pastikan mengembalikan list hasil

def extract_links(text):
    return re.findall(r"https?://\S+", text)

def print_reverse_image_links(img_url):
    links = [
        f"    ↳ Reverse Image:",
        f"       Yandex : https://yandex.com/images/search?rpt=imageview&url={img_url}",
        f"       Google : https://www.google.com/searchbyimage?image_url={img_url}",
        f"       Bing   : https://www.bing.com/images/search?q=imgurl:{img_url}&view=detailv2"
    ]
    for line in links:
        print(line)
    return links

def get_profile_info(site, username, url):
    lines = []
    try:
        if site in ["GitHub", "Medium", "TikTok"]:
            r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(r.text, "html.parser")

            if site == "GitHub":
                name = soup.find("span", class_="p-name")
                bio = soup.find("div", class_="p-note")
                avatar = soup.find("img", class_="avatar avatar-user width-full border color-bg-default")
                if name:
                    line = f"    ↳ Nama  : {name.text.strip()}"
                    print(line)
                    lines.append(line)
                if bio:
                    bio_text = bio.text.strip()
                    line = f"    ↳ Bio   : {bio_text}"
                    print(line)
                    lines.append(line)
                    for link in extract_links(bio_text):
                        l = f"    ↳ Link  : {link}"
                        print(l)
                        lines.append(l)
                if avatar:
                    img_url = avatar['src']
                    line = f"    ↳ Foto  : {img_url}"
                    print(line)
                    lines.append(line)
                    lines.extend(print_reverse_image_links(img_url))

            elif site == "Medium":
                title = soup.find("title")
                desc = soup.find("meta", attrs={"name": "description"})
                if title:
                    line = f"    ↳ Judul : {title.text.strip()}"
                    print(line)
                    lines.append(line)
                if desc and desc.get("content"):
                    line = f"    ↳ Bio   : {desc['content'].strip()}"
                    print(line)
                    lines.append(line)

            elif site == "TikTok":
                bio_tag = soup.find("meta", attrs={"name": "description"})
                if bio_tag and bio_tag.get("content"):
                    bio_text = bio_tag["content"].strip()
                    line = f"    ↳ Bio   : {bio_text}"
                    print(line)
                    lines.append(line)
                    for link in extract_links(bio_text):
                        l = f"    ↳ Link  : {link}"
                        print(l)
                        lines.append(l)

    except:
        pass

    return lines

def main():
    print_banner()
    parser = argparse.ArgumentParser(description="SpectraLD RLD - Investigative Username OSINT Tool")
    parser.add_argument("--username", help="Username(s) yang ingin dicari", required=True, nargs='+')
    parser.add_argument("--verbose", action="store_true", help="Tampilkan metadata jika tersedia")
    parser.add_argument("--fast", action="store_true", help="Aktifkan multithread untuk kecepatan maksimal")
    args = parser.parse_args()

    all_output_lines = []  # Menyimpan semua hasil dalam satu file

    for username in args.username:
        print(f"\n--- Mencari untuk username: {username} ---")
        username_output_lines = run_username_check(username, verbose=args.verbose)
        all_output_lines.extend(username_output_lines)

    # Menyimpan semua hasil di satu file
    save_path = os.path.join("hasil", "all_results.txt")
    os.makedirs("hasil", exist_ok=True)
    with open(save_path, "w", encoding="utf-8") as f:
        f.write("\n".join(all_output_lines))

    print(f"\n[✓] Semua hasil disimpan di: hasil/all_results.txt")

if __name__ == "__main__":
    main()
