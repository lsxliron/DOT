import ipdb
import unittest
from mock import patch
import dot
class CLITests(unittest.TestCase):

    @patch('dot.logger')
    def test_parseDate_invalidDate(self, logger):
        #INVALID DATES
        with self.assertRaises(SystemExit) as dateError:
            dot.parseDate("X")
        self.assertEqual(dateError.exception.code,-1)

        with self.assertRaises(SystemExit) as dateError:
            dot.parseDate("xx-yy-zz")
        self.assertEqual(dateError.exception.code,-1)

    @patch('dot.logger')
    def test_parseDate_yearDoesNotExists(self, logger):
        #TEST YEAR < 1900
        with self.assertRaises(SystemExit) as dateError:
            dot.parseDate("1-1-1")
        self.assertEqual(dateError.exception.code,-1)

    @patch('dot.logger')
    def test_parseDate_invalidDateFormat(self, logger):
        #INVALID DATE FORMAT
        with self.assertRaises(SystemExit) as dateError:
            dot.parseDate("1/1:1")
        self.assertEqual(dateError.exception.code,-1)

    @patch('dot.logger')
    def test_parseDate_leap_year(self, logger):
        #TEST LEAP YEAR WHEN DOES NOT EXISTS
        with self.assertRaises(SystemExit) as dateError:
            dot.parseDate("02-29-2015")
        self.assertEqual(dateError.exception.code,-1)
        
        #TEST LEAP YEAR THAT EXISTS    
        tempDate = dot.parseDate("02-29-2016")
        self.assertEqual(tempDate.year, 2016)
        self.assertEqual(tempDate.month, 2)
        self.assertEqual(tempDate.day, 29)

    @patch('dot.logger')
    def test_parseDate_dateDoesNotExists(self, logger):
        #TEST DATE WHICH DOES NOT EXISTS
        with self.assertRaises(SystemExit) as dateError:
            dot.parseDate("31-12-2015")
        self.assertEqual(dateError.exception.code,-1)

    @patch('dot.logger')
    def test_parseDate_validDate(self, logger):
        tempDate = dot.parseDate("02-28-2015")
        self.assertEqual(tempDate.month,2)
        self.assertEqual(tempDate.day,28)
        self.assertEqual(tempDate.year,2015)

    @patch('dot.logger')
    def test_parseTime_invalidTime(self,logger):
        with self.assertRaises(SystemExit) as timeError:
            dot.parseTime("x")
        self.assertEqual(timeError.exception.code,-1)

        with self.assertRaises(SystemExit) as timeError:
            dot.parseTime("aa:bb:cc")
        self.assertEqual(timeError.exception.code,-1)

    @patch('dot.logger')
    def test_parseTime_timeDoesNotExists(self, logger):
        with self.assertRaises(SystemExit) as timeError:
            dot.parseTime("-11:22:33")
        self.assertEqual(timeError.exception.code, -1)

        with self.assertRaises(SystemExit) as timeError:
            dot.parseTime("99:99:99")
        self.assertEqual(timeError.exception.code, -1)

    @patch('dot.logger')
    def test_parseTime_invalidTimeFormat(self, logger):
        with self.assertRaises(SystemExit) as timeError:
            dot.parseTime("11-22-33")
        self.assertEqual(timeError.exception.code, -1)

    @patch('dot.logger')
    def test_parseTime_validTime(self, logger):
        tempTime = dot.parseTime("11:22:33")
        self.assertEqual(tempTime.hour, 11)
        self.assertEqual(tempTime.minute, 22)
        self.assertEqual(tempTime.second, 33)

    @patch('dot.logger')
    def test_negativeDateDelta(self, logger):
        with self.assertRaises(SystemExit) as deltaError:
            dot.getDates('01-02-2000', '01-01-2000')
        self.assertEqual(deltaError.exception.code, -1)

    @patch('dot.logger')
    def test_negativeTimeDelta(self, logger):
        with self.assertRaises(SystemExit) as deltaError:
            dot.getTimes('11:22:33', '11:22:32')
        self.assertEqual(deltaError.exception.code, -1)

    @patch('dot.logger')
    def test_validDateDelta(self, logger):
        delta = dot.getDates('01-01-2001', '01-02-2002')
        self.assertEqual(len(delta), 2)

    @patch('dot.logger')
    def test_validTimeDelta(self, logger):
        delta = dot.getTimes('11:22:33', '23:22:33')
        self.assertEqual(len(delta), 2)



if __name__ == '__main__':
    unittest.main()