import os
import subprocess
from playwright.sync_api import sync_playwright, Error
from elfakPages import pagesList

# set up the browser
playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=True)
page = browser.new_page()
page.set_default_timeout(15000)

# cs log in
try:
    page.goto("https://cs.elfak.ni.ac.rs/nastava/login/index.php")
    page.wait_for_selector('xpath=//*[@id="region-main"]/div/div/div/div/div[2]/a')
    page.click('xpath=//*[@id="region-main"]/div/div/div/div/div[2]/a')
    page.wait_for_selector('xpath=//*[@id="i0116"]')
    page.fill('xpath=//*[@id="i0116"]', os.environ['email'])
    page.click('xpath=//*[@id="idSIButton9"]')
    page.wait_for_selector('xpath=//*[@id="i0118"]')
    page.fill('xpath=//*[@id="i0118"]', os.environ['password'])
    page.click('xpath=//*[@id="idSIButton9"]')
    page.wait_for_selector('xpath=//*[@id="idBtn_Back"]')
    page.click('xpath=//*[@id="idBtn_Back"]')
    page.wait_for_selector('xpath=//*[@id="region-main-box"]')
except Error as e:
    print(f"CS LOG IN: {e}")
    browser.close()
    playwright.stop()
    exit(1)

# scrapping 
for pageName, info in pagesList.items():
    try:
        response = page.goto(info['url'])
        if not response or not response.ok:
            print(f"Skipping {pageName}")
            continue
        page.wait_for_selector(info['xpath'])
        page_content = page.inner_text(info['xpath']).strip()
        with open (f"{pageName}.md", "r+", encoding="utf-8") as f:
            file_content = f.read().strip()
            if file_content != page_content:
                f.seek(0)
                f.truncate(0)
                f.write(page_content)
                print(f"{pageName}.md is updated !!!")
                page.screenshot(path=f"{pageName}.png") 
                subprocess.run([
                    "python", "discordBot.py", 
                    str(info['id']), 
                    info['url'], 
                    f"{pageName}.png"
                ])
    except Error as e:
        print(f"{pageName} : {e}")
        continue

browser.close()
playwright.stop()
