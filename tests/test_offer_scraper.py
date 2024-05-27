import pytest
from unittest.mock import patch, AsyncMock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from offer_scraper import scrape_offers


@pytest.mark.asyncio
@patch('offer_scraper.aiohttp.ClientSession.get')
async def test_scrape_offers_valid_agency(mock_get):
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.text.return_value = '<html><div class="select_tur_item_bar">Test Offer</div><div class="select_tur_item_info_incluse_transport">2024-05-01</div><div class="select_tur_item_price_item">1000</div></html>'
    mock_get.return_value.__aenter__.return_value = mock_response

    agency_name, offers_titles, offers_dates, offers_prices = await scrape_offers('Admiral TUR')
    
    assert agency_name == 'Admiral TUR'
    assert offers_titles == ['Test Offer']
    assert offers_dates == ['2024-05-01']
    assert offers_prices == ['1000']


@pytest.mark.asyncio
async def test_scrape_offers_invalid_agency_error():
    with pytest.raises(ValueError):
        await scrape_offers('Test Agency')

if __name__ == "__main__":
    pytest.main()
