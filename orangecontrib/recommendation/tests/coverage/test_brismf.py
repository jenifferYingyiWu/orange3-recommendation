from orangecontrib.recommendation.tests.coverage import TestRatingModels
from orangecontrib.recommendation import BRISMFLearner

import unittest


class TestBRISMF(TestRatingModels):

    def test_predict_items(self):
        learner = BRISMFLearner(num_factors=2, num_iter=1, verbose=True)
        super().test_predict_items(learner, filename='ratings.tab')
    #
    # def test_input_data_discrete(self):
    #     learner = BRISMFLearner(num_factors=2, num_iter=1)
    #     super().test_input_data_discrete(learner, filename='ratings_dis.tab')
    #
    # def test_input_data_continuous(self):
    #     learner = BRISMFLearner(num_factors=2, num_iter=1, min_rating=0,
    #                             max_rating=5)
    #     super().test_input_data_continuous(learner, filename='ratings.tab')
    #
    # def test_pairs(self):
    #     learner = BRISMFLearner(num_factors=2, num_iter=1)
    #     super().test_pairs(learner, filename='ratings.tab')
    #
    # def test_CV(self):
    #     learner = BRISMFLearner(num_factors=2, num_iter=1)
    #     super().test_CV(learner, filename='ratings.tab')
    #
    # def test_warnings(self):
    #     learner = BRISMFLearner(num_factors=2, num_iter=1, learning_rate=0.0)
    #     super().test_warnings(learner, filename='ratings.tab')
    #
    # def test_objective(self):
    #     learner = BRISMFLearner(num_factors=2, learning_rate=0.007)
    #     super().test_objective(learner, filename='ratings.tab')


if __name__ == "__main__":
    # Test all
    unittest.main()

    # # Test single test
    # suite = unittest.TestSuite()
    # suite.addTest(TestBRISMF("test_predict_items"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)

