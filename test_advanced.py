import re
from time import sleep

from playwright.sync_api import Page, expect, BrowserContext, Dialog


def test_visible(page: Page):
    page.goto("https://www.qa-practice.com/elements/input/simple")
    req_locator = page.locator('#req_text')
    expect(req_locator).not_to_be_visible()
    expect(req_locator).to_be_hidden()
    page.locator('#req_header').click()
    expect(req_locator).to_be_visible()

def test_enabled_and_select(page:Page):
    page.goto("https://www.qa-practice.com/elements/button/disabled")
    select_state = page.locator("#id_select_state")
    select_state.select_option("Enabled")
    submit_btn = page.locator("#submit-id-submit")
    expect(submit_btn).to_be_enabled()
    expect(submit_btn).to_have_text("Submit")
    expect(submit_btn).to_contain_text("ubm")
    submit_btn.click()
    sleep(2)

def test_input_value(page: Page):
    text = "qwerty"
    page.goto("https://www.qa-practice.com/elements/input/simple")
    text_input = page.locator("#id_text_string")
    text_input.fill(text)
    expect(text_input, f"value is not {text}").to_have_value(text)

def test_sort_and_waits(page:Page):
    page.goto("https://magento.softwaretestingboard.com/men/tops-men/jackets-men.html")
    sorter = page.locator("#sorter").first
    first_man = page.locator(".product-item-link").first
    print(first_man.inner_text())
    sorter.select_option("Price")
    expect(page).to_have_url(re.compile('price'))
    print(first_man.inner_text())

def test_focused(page: Page):
    page.goto("https://www.google.com")
    input_field = page.locator('[name="q"]')
    expect(input_field).to_be_focused()

def test_tabs(page: Page, context: BrowserContext):
    page.goto("https://www.qa-practice.com/elements/new_tab/link")
    with context.expect_page() as new_page_event:
        page.get_by_role("link",name="New page will be opened on a new tab").click()
    new_page = new_page_event.value
    result_text = new_page.locator("#result-text")
    expect(result_text).to_have_text("I am a new page in a new tab")
    new_page.close()
    new_tab_button = page.get_by_role("link",name="New tab button")
    new_tab_button.click()

def test_hover(page: Page):
    page.goto("https://magento.softwaretestingboard.com/")
    man_locator = page.locator("#ui-id-5")
    top_locator = page.locator("#ui-id-17")
    jackets_locator = page.locator("#ui-id-19")
    man_locator.hover()
    top_locator.hover()
    jackets_locator.click()

def test_d_n_d(page: Page):
    page.goto("https://www.qa-practice.com/elements/dragndrop/boxes")
    rect_draggable = page.locator("#rect-draggable")
    rect_droppable = page.locator("#rect-droppable")
    rect_draggable.drag_to(rect_droppable)

def test_alert(page: Page):
    def cancel_alert(alert: Dialog):
        print(alert.message)
        print(alert.type)
        alert.dismiss()

    def fill_and_accept(alert: Dialog):
        alert.accept('some text')
    page.on('dialog', fill_and_accept)
    # page.on('dialog', lambda alert: alert.accept('another text'))
    page.goto('https://www.qa-practice.com/elements/alert/prompt')
    # page.on('dialog', lambda alert: alert.accept('another text'))
    page.get_by_role('link', name='Click').click()
    sleep(5)

