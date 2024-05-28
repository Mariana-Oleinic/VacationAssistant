import pytest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from convertor_scraper import scrape_currency_conversion


@pytest.fixture
def mock_playwright():
    with patch('convertor_scraper.sync_playwright') as mock_sync_playwright:
        yield mock_sync_playwright

def test_scrape_currency_conversion_success(mock_playwright):
    mock_browser = MagicMock()
    mock_page = MagicMock()
    mock_playwright.return_value.__enter__.return_value.chromium.launch.return_value = mock_browser
    mock_browser.new_page.return_value = mock_page
    mock_page.eval_on_selector.return_value = '100'

    result = scrape_currency_conversion('50', 'USD', 'EUR')

    mock_page.goto.assert_called_once_with('https://www.curs.md/en')
    mock_page.fill.assert_called_once_with('input[placeholder="Input sum"]', '50')
    mock_page.click.assert_any_call('.btn.src-currency:has-text("USD")', force=True)
    mock_page.click.assert_any_call('.btn.tgt-currency:has-text("EUR")', force=True)
    mock_page.eval_on_selector.assert_called_once_with('.tgt-sum', 'el => el.value')
    assert result == '100 EUR'

def test_scrape_currency_conversion_failure(mock_playwright):
    mock_playwright.return_value.__enter__.side_effect = Exception('Playwright error')

    result = scrape_currency_conversion('50', 'USD', 'EUR')

    assert result is None
