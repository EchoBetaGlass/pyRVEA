import numpy as np
#from scipy.linalg import lstsq
import timeit
from pyrvea.Problem.baseProblem import baseProblem

class EvoNNProblem():
    """Creates an Artificial Neural Network (ANN) for the EvoNN algorithm."""

    def __init__(
        self,
        training_data_input=None,
        training_data_output=None,
        name=None,
        num_input_nodes=4,
        num_hidden_nodes=6,
        num_output_nodes=1,
        num_of_objectives=2,
        num_of_constraints=0,
        w_low=-5.0,
        w_high=5.0,
    ):

        """

        Parameters
        ----------
        training_data_input : numpy array
            Training data input matrix
        training_data_output : numpy array
            Training data expected output
        name : str
            Name of the sample
        num_input_nodes : int
            The number of nodes in the input layer
        num_hidden_nodes : int
            The number of nodes in the hidden layer
        num_output_nodes : int
            The number of nodes in the output layer
        w_low : float
            The lower bound for randomly generated weights
        w_high : float
            The upper bound for randomly generated weights
        """

        self.training_data_input = training_data_input
        self.training_data_output = training_data_output
        self.name = name
        self.num_input_nodes = num_input_nodes
        self.num_hidden_nodes = num_hidden_nodes
        self.num_output_nodes = num_output_nodes
        self.num_of_objectives = num_of_objectives
        self.num_of_variables = num_input_nodes
        self.num_of_constraints = num_of_constraints
        self.w_low = w_low
        self.w_high = w_high
        self.lower_limits = w_low
        self.upper_limits = w_high
        self.bias = 1
        self.num_of_samples = np.shape(training_data_output)[0]

        if len(self.training_data_input) > 0:
            self.num_input_nodes = np.shape(training_data_input)[1]

    def objectives(self, decision_variables) -> list:

        """ Use this method to calculate objective functions.

        Parameters
        ----------
        decision_variables : tuple
            Variables from the neural network

        Returns
        -------
        obj_func : array
            The objective function

        """

        #w_matrix, bias = self.init_weight_matrix()
        weighted_input = self.dot_product(decision_variables)
        activated_function = self.activation(weighted_input, "sigmoid")
        w_matrix2, predicted_values = self.optimize_error(activated_function, "llsq")
        training_error = self.loss_function(predicted_values, "rmse")

        complexity = self.calculate_complexity(decision_variables, w_matrix2)
        minimized_complexity = self.minimize_complexity(predicted_values, complexity)
        obj_func = []
        obj_func.extend([training_error, minimized_complexity])

        return obj_func

    def init_weight_matrix(self):

        # Initialize the weight matrix with random weights within boundaries
        # Rows = hidden nodes
        # Columns = input nodes
        # Last column is for bias

        w_matrix = np.random.uniform(
            self.w_low, self.w_high, size=(self.num_hidden_nodes, self.num_input_nodes)
        )

        #bias = np.full((self.num_hidden_nodes, 1), 1)
        bias = 1
        return w_matrix, bias

    def dot_product(self, w_matrix):
        """ Calculate the dot product of input and weight + bias.

        Parameters
        ----------
        w_matrix
        bias

        Returns
        -------

        """

        wi = np.dot(self.training_data_input, w_matrix) + self.bias
        #biased_matrix = np.hstack((w_matrix, bias))
        #wi = (
        #    np.dot(self.training_data_input, biased_matrix[..., :-1].transpose())
        #    + biased_matrix[:, -1]
        #)

        return wi

    def activation(self, wi, name):
        """ Activation function

        Returns
        -------
        The penultimate layer Z before the output

        """

        if name == "sigmoid":
            activated_function = lambda x : 1 / (1 + np.exp(-x))

        return activated_function(wi)

    def optimize_error(self, activated_function, name):
        """ Optimize the training error

        Parameters
        ----------
        activated_function
            Output of the activation function

        Returns
        -------
        """
        if name == "llsq":
            w_matrix2 = np.linalg.lstsq(activated_function, self.training_data_output)
            predicted_values = np.dot(activated_function, w_matrix2[0])

        return w_matrix2[0], predicted_values

    def loss_function(self, predicted_values, name):

        if name == "rmse":
            return np.sqrt(((self.training_data_output - predicted_values) ** 2).mean())

    def calculate_complexity(self, w_matrix, w_matrix2):

        k = np.count_nonzero(w_matrix) + np.count_nonzero(w_matrix2)

        return k

    def minimize_complexity(self, predicted_values, k):

        rss = ((self.training_data_output - predicted_values) ** 2).sum()
        aic = 2 * k + self.num_of_samples * np.log(rss/self.num_of_samples)
        aicc = aic + (2*k*(k+1)/(self.num_of_samples-k-1))

        return aicc
