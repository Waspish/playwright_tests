import os
from datetime import datetime

import pytest
from playwright.sync_api import Page

@pytest.fixture(scope='function')
def page(page: Page, request):
    yield page
    if request.node.rep_call.failed:
        timestamp = datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
        screenshot_path = os.path.join('screenshots', timestamp)
        page.screenshot(path=f'test_failed_{screenshot_path}.png')