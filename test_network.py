from time import sleep

import pytest
from idna import ulabel
from playwright.sync_api import Page, Request, Dialog, Response, expect, Route
import re
import json

@pytest.mark.extended
def test_listen_data(page:Page):
    def handle_request(request: Request):
        print(f"REQUEST: {request.post_data}, {request.url}")

    page.on('request', handle_request)
    page.on('response', lambda response: print(f"RESPONSE: {response.status}, {response.url}"))

    page.goto("https://www.qa-practice.com")
    page.get_by_role('link',name="Text input").click()
    input_field = page.locator('#id_text_string')
    input_field.fill('qwerty')
    input_field.press('Enter')

@pytest.mark.extended
def test_catch_response(page: Page):
    page.goto("https://www.airbnb.ru/")
    pop_up = page.get_by_role("dialog")
    pop_up.locator('button:not([aria-label])').click()
    # pop_up.get_by_role('button').nth(1).click()
    with page.expect_response(re.compile('autoSuggestionsRequest')) as response_event:
        page.locator('#search-block-tab-EXPERIENCES').click()

    response:Response = response_event.value
    print(response.url)
    print(response.json()['data'])
    print(response.status)
    pop_up = page.get_by_role("dialog")
    pop_up.locator('button:not([aria-label])').click()
    assert response.json()['data'] is not None

@pytest.mark.extended
def test_pogoda(page: Page):
    def handle_route(route: Route):
        response = route.fetch()
        body = response.json()
        body['temperature'] = '+45'
        body['icon'] = 'A2'
        body=json.dumps(body)
        route.fulfill(response=response,body=body)
    def handle_route2(route: Route):
        url = route.request.url
        url = url.replace('pogoda/api/', '')
        route.continue_(url=url)
    page.route('**/pogoda/**', handle_route)
    page.goto("https://www.onliner.by/")
    page.get_by_text("+45").nth(1).wait_for()
    page.locator('[name="query"]').click()

@pytest.mark.extended
def test_change_req(page:Page):

    def change_req(route: Route):
        url = route.request.url
        print(url)
        url = url.replace('filter5=15p01', '')
        route.continue_(url=url)
    page.route(re.compile('product/finder/'), change_req)
    page.goto('https://www.samsung.com/au/smartphones/galaxy-z/')
    page.locator('[data-di-id="di-id-c9e22f1b-594586ed"]').click()
    page.locator('[for="checkbox-series15p01"]').click()
    sleep(5)

