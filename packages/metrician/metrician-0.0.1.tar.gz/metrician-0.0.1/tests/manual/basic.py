import unittest

class BasicTest(unittest.TestCase):

    def test_writer(self):
        from tests.manual.utils import make_classifier,make_data
        from src.configs.defaults import SimpleClf
        from src.writers.writer import MetricWriter
        from torch import nn
        loss = nn.L1Loss() # it doesn't really matter all that much for right now, though later I'll test them all
        clf = make_classifier()
        mw = MetricWriter( SimpleClf )
        self.assertTrue( mw.cfg is not None,mw.cfg )
        for _ in range(20):
            x,y = make_data()
            y_hat = clf(x)
            mw( y_hat, y, loss )
        mw.close()
        return True


if __name__ == "__main__":
    unittest.main()
