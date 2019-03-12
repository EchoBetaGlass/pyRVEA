from pyRVEA.Problem.baseProblem import baseProblem


class KrigingProblem(baseProblem):
    """Create and update kriging models."""

    def __init__(self, dataset, otherarguments):
        """Create a kriging model on the dataset.

        Args:
            dataset:
            otherarguments:
        """
        super.__init__()
        pass

    def objectives(self, decision_variables):
        """Return objective values based on decision variables.

        Args:
            decision_variables:
        """
        pass

    def update(self, population: Population):
        """Update the kriging model based on population.

        Change the return of method objectives.

        Args:
            population (Population):
        """
        pass
