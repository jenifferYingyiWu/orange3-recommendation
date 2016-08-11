import Orange
from orangecontrib.recommendation.tests.coverage import TestRankingModels
from orangecontrib.recommendation import CLiMFLearner

import unittest

__dataset__ = 'binary_data.tab'
__dataset2__ = 'binary_data_dis.tab'


class TestCLiMF(unittest.TestCase, TestRankingModels):

    def test_input_data_continuous(self):
        learner = CLiMFLearner(num_factors=2, num_iter=1, verbose=2)
        super().test_input_data_continuous(learner, filename=__dataset__)

    def test_input_data_discrete(self):
        learner = CLiMFLearner(num_factors=2, num_iter=1)
        super().test_input_data_discrete(learner, filename=__dataset2__)

    @unittest.skip("Skipping test")
    def test_CV(self):
        learner = CLiMFLearner(num_factors=2, num_iter=1)
        super().test_CV(learner, filename=__dataset__)

    def test_warnings(self):
        learner = CLiMFLearner(num_factors=2, num_iter=1, learning_rate=0.0)
        super().test_warnings(learner, filename=__dataset__)

    def test_objective(self):
        from orangecontrib.recommendation.ranking.climf import compute_loss

        # Load data
        data = Orange.data.Table(__dataset__)

        steps = [1, 10, 30]
        objectives = []
        learner = CLiMFLearner(num_factors=2, random_state=42)

        for step in steps:
            learner.num_iter = step
            recommender = learner(data)

            # Set parameters
            low_rank_matrices = (recommender.U, recommender.V)
            params = learner.lmbda

            objective = compute_loss(data, low_rank_matrices, params)
            objectives.append(objective)

        # Assert objective values decrease
        test = list(
            map(lambda t: t[0] <= t[1], zip(objectives, objectives[1:])))
        self.assertTrue(all(test))

    def test_outputs(self):
        # Load data
        data = Orange.data.Table(__dataset__)

        # Train recommender
        learner = CLiMFLearner(num_factors=2, num_iter=1)
        # Train recommender
        recommender = learner(data)

        # Check tables P, Q, Y and W
        U = recommender.getUTable()
        V = recommender.getVTable()

        diff = len(set([U.X.shape[1], V.X.shape[1]]))
        self.assertEqual(diff, 1)


if __name__ == "__main__":
    # Test all
    unittest.main()

    # # Test single test
    # suite = unittest.TestSuite()
    # suite.addTest(TestCLiMF("test_objective"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
