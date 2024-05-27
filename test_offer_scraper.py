import asyncio
import unittest
from unittest.mock import patch, MagicMock
from offer_scraper import scrape_offers

class TestScrapeOffers(unittest.TestCase):
    @patch('offer_scraper.aiohttp.ClientSession.get')
    async def test_scrape_offers_valid_agency(self, mock_get):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.text.return_value = '<html><body><div class="select_tur_item_bar">Test Offer</div></body></html>'
        mock_get.return_value.__aenter__.return_value = mock_response

        result = await scrape_offers('Admiral TUR')

        self.assertEqual(result[0], 'Admiral TUR')
        self.assertEqual(result[1], ['Test Offer'])

    @patch('offer_scraper.aiohttp.ClientSession.get')
    async def test_scrape_offers_invalid_agency(self):
        with self.assertRaises(ValueError):
            await scrape_offers('Invalid Agency')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(unittest.main())
    loop.close()
