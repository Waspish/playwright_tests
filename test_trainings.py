from time import sleep

from playwright.sync_api import Page, expect
import re

def apply_stealth(page):
    page.add_init_script("""
    delete Object.getPrototypeOf(navigator).webdriver;
    window.navigator.chrome = { runtime: {} };
    Object.defineProperty(navigator, 'languages', {
        get: () => ['en-US', 'en']
    });
    """)
    page.set_extra_http_headers({
        'Accept-Language': 'en-US,en;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })

def test_chrome(page: Page):
    apply_stealth(page)
    page.goto('https://www.google.com/')
    search_field = page.get_by_role('combobox')
    search_field.fill('cat')
    page.keyboard.press('Enter')
    expect(page).to_have_title(re.compile('^cat'))

def test_by_text(page: Page):
    page.goto("https://www.qa-practice.com/")
    page.get_by_text('Single UI Elements').click()

def test_by_label(page: Page):
    page.goto("https://www.qa-practice.com/elements/input/simple")
    field = page.get_by_label("Text string")
    field.press_sequentially('iuashdfauishd',delay=200)
    sleep(1)
    field.clear()
    sleep(3)

def test_by_placeholder(page: Page):
    page.goto("https://www.qa-practice.com/elements/input/simple")
    field = page.get_by_placeholder('Submit me')
    sleep(1)
    field.fill('Hello world')
    sleep(1)
    field.clear()
    sleep(1)

def test_by_alt_text(page: Page):
    sleep(3)
    # page.screenshot(path="hello.png", full_page=True)
    page.goto('https://epam.com')
    page.get_by_alt_text('The Complex Path of GenAI Adoption').click()
    sleep(3)

def test_by_title(page: Page):
    sleep(3)
    page.goto('https://www.google.com/')
    page.get_by_title('Шукаць').fill('cat')
    sleep(3)

def test_by_test_id(page:Page):
    page.goto("https://www.airbnb.com/experiences")
    pop_up = page.get_by_text("Explore experiences")
    pop_up.press("Escape")
    item = page.get_by_test_id('tab-bar-entry-video').first
    item.click()

def test_by_role(page: Page):
    page.goto("https://www.qa-practice.com")
    whats_new_link = page.get_by_role('link', name = "What's new")
    whats_new_link.click()
    heading = page.get_by_role('heading', name="What's new")
    print(heading.text_content())

def test_by_css_selector(page: Page):
    page.goto("https://www.qa-practice.com/elements/button/simple")
    button = page.locator('#submit-id-submit')
    button.click()
    sleep(1)

def test_by_xpath(page: Page):
    page.goto("https://www.qa-practice.com/elements/button/disabled")
    selector = page.locator("//select[@id='id_select_state']")
    selector.select_option("enabled")
    sleep(2)

