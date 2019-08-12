import unittest

import bike24 as crawler


class TestGetUrlForCrawler(unittest.TestCase):
    #get_url_for_crowl(category: str, item_name: str) -> str:

    def test_1(self):
        category = 'mtb_disc_brake_pads'
        item_name = 'Shimano XTR Disc Brake Pads'
        result = r'https://www.bike24.com/search/catalog-120?searchTerm=Shimano%20XTR%20Disc%20Brake%20Pads'
        self.assertEqual(crawler.get_url_for_crowl(category, item_name), result)

    def test_3(self):
        category = 'mtb_26_wheels'
        item_name = 'Mavic Crossride FTS-X'
        result = r'https://www.bike24.com/search/catalog-17?searchTerm=Mavic%20Crossride%20FTS-X'
        self.assertEqual(crawler.get_url_for_crowl(category, item_name), result)

    def test_2(self):
        category = 'mtb_11_speed'
        item_name = 'Shimano Deore XT RD-M8000-GS'
        result = r'https://www.bike24.com/search/catalog-111?searchTerm=Shimano%20Deore%20XT%20RD-M8000-GS%2011-speed'
        self.assertEqual(crawler.get_url_for_crowl(category, item_name), result)


if __name__ == '__main__':
    unittest.main()
