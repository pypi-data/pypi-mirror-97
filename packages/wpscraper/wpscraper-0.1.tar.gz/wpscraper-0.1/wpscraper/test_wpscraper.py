import unittest
import random
import math

from wpscraper import WPScraper
from datastores import CSVDataStore, SqliteDataStore

class WPScraperTestBase(unittest.TestCase):
    def _get_articles(self, n, max_count=None):
        if n == 1:
            print('scrape latest {} article...'.format(n))
        else:
            print('scrape latest {} articles...'.format(n))

        self.scraper.scrape(n)
        self.scraper.save()
        if max_count:
            self.assertEqual(self.scraper.count(), max(max_count,n))
        else:
            self.assertEqual(self.scraper.count(), n)


    def _scrape_times(self, n, given_count=None):
        for i in range(n):
            if not given_count:
                count = math.ceil(random.random()*1000)
            else:
                count = given_count
            
            if not self.max_count:
                self.max_count = count
            else:
                self.max_count = max(self.max_count, count)
                
            self._get_articles(count,self.max_count)
        return self.max_count

        

class WPScraperTestCSV(WPScraperTestBase):
    def setUp(self):
        self.csv = CSVDataStore('techcrunch-unittesting.csv')
        self.scraper = WPScraper('http://techcrunch.com/wp-json/wp/v2/posts?', self.csv)
        self.max_count = 0


    def test_scrape_1_times_1(self):
        count = self._scrape_times(1, 1)
        self.assertEqual(self.scraper.count(), count)

    def test_scrape_3_times_18_1_37(self):
        self._scrape_times(1, 18)
        self._scrape_times(1, 1)
        self._scrape_times(1, 37)
        self.assertEqual(self.scraper.count(), 37)

    # def test_scrape_3_times_1000(self):
    #     count = self._scrape_times(3, 1000)
    #     self.assertEqual(self.scraper.count(), count)

    # def test_scrape_100_times_random(self):
    #     count = self._scrape_times(100)
    #     self.assertEqual(self.scraper.count(), count)

#     def test_scrape_3_times_418_140_937(self):
#         self._scrape_times(1, 418)
#         self._scrape_times(1, 140)
#         self._scrape_times(1, 937)
#         self.assertEqual(self.scraper.count(), 937)



    def tearDown(self):
        self.csv.clean()

            
class WPScraperTestDB(WPScraperTestBase):
    def setUp(self):
        self.db = SqliteDataStore('techcrunch.db', 'techcrunch')
        self.scraper = WPScraper('http://techcrunch.com/wp-json/wp/v2/posts?', self.db)
        self.max_count = 0
        
    def test_scrape_1_times_1(self):
        count = self._scrape_times(1, 1)
        self.assertEqual(self.scraper.count(), count)

    def test_scrape_3_times_18_1_37(self):
        self._scrape_times(1, 18)
        self._scrape_times(1, 1)
        self._scrape_times(1, 37)
        self.assertEqual(self.scraper.count(), 37)

    # def test_scrape_3_times_random(self):
    #     count = self._scrape_times(3)
    #     self.assertEqual(self.scraper.count(), count)

    # def test_scrape_3_times_101(self):
    #     count = self._scrape_times(3, 101)
    #     self.assertEqual(self.scraper.count(), count)

    # def test_scrape_3_times_1000(self):
    #     count = self._scrape_times(3, 1000)
    #     self.assertEqual(self.scraper.count(), count)

    # def test_scrape_100_times_random(self):
    #     count = self._scrape_times(100)
    #     self.assertEqual(self.scraper.count(), count)

#     def test_scrape_1_times_909(self):
#         count = self._scrape_times(1, 909)
#         self.assertEqual(self.scraper.count(), count)

#     def test_scrape_2_times_903_909(self):
#         count = self._scrape_times(1, 903)
#         count = self._scrape_times(1, 909)
#         self.assertEqual(self.scraper.count(), 909)

#     def test_scrape_2_times_903_909(self):
#         count = self._scrape_times(1, 903)
#         count = self._scrape_times(1, 909)
#         self.assertEqual(self.scraper.count(), 909)


    def tearDown(self):
        self.db.clean()


