from pyrvea.Problem.baseProblem import baseProblem
import numpy as np
import plotly
import plotly.graph_objs as go


class EvoNN(baseProblem):
    """Creates an Artificial Neural Network (ANN) for the EvoNN algorithm.

    Attributes
    ----------
    name : str
        Name of the sample
    num_input_nodes : int
        The number of nodes in the input layer
    num_hidden_nodes : int
        The number of nodes in the hidden layer
    num_of_objectives : int
        The number of objectives
    w_low : float
        The lower bound for randomly generated weights
    w_high : float
        The upper bound for randomly generated weights
    prob_omit : float
        The probability of setting some weights to zero initially
    activation_func : str
        The function to use for activating the hidden layer
    opt_func : str
        The function to use for optimizing the upper part of the network
    loss_func : str
        The loss function to use
    """

    def __init__(
        self,
        name=None,
        num_input_nodes=4,
        num_hidden_nodes=5,
        num_of_objectives=2,
        w_low=-5.0,
        w_high=5.0,
        prob_omit=0.2,
        activation_func="sigmoid",
        opt_func="llsq",
        loss_func="rmse"
    ):
        super().__init__()

        self.name = name
        self.num_input_nodes = num_input_nodes
        self.num_hidden_nodes = num_hidden_nodes
        self.num_of_objectives = num_of_objectives
        self.w_low = w_low
        self.w_high = w_high
        self.prob_omit = prob_omit
        self.activation_func = activation_func
        self.opt_func = opt_func
        self.loss_func = loss_func

    def fit(self, training_data, target_values):
        """Fit data in EvoNN model.

        Parameters
        ----------
        training_data : ndarray, shape = (numbers of samples, number of variables)
            Training data
        target_values : ndarray
            Target values
        """

        self.training_data_input = training_data
        self.training_data_output = target_values
        self.num_of_samples = target_values.shape[0]
        self.num_of_variables = training_data.shape[1]
        if len(self.training_data_input) > 0:
            self.num_input_nodes = np.shape(training_data)[1]

    def objectives(self, decision_variables) -> list:

        """ Use this method to calculate objective functions.

        Parameters
        ----------
        decision_variables : ndarray
            Variables from the neural network

        Returns
        -------
        obj_func : list
            The objective function

        """

        activated_layer = self.activation(decision_variables)
        w_matrix2, rss, predicted_values = self.minimize_error(activated_layer)
        training_error = self.loss_function(predicted_values)
        complexity = self.calculate_complexity(decision_variables)

        obj_func = [training_error, complexity]

        return obj_func

    def activation(self, decision_variables):
        """ Calculates the dot product and applies the activation function.

        Parameters
        ----------
        decision_variables : ndarray
            Variables from the neural network
        name : str
            The activation function to use

        Returns
        -------
        The penultimate layer Z before the output

        """
        # Calculate the dot product
        wi = (
            np.dot(self.training_data_input, decision_variables[1:, :])
            + decision_variables[0]
        )

        if self.activation_func == "sigmoid":
            activated_layer = lambda x: 1 / (1 + np.exp(-x))

        if self.activation_func == "relu":
            activated_layer = lambda x: np.maximum(x, 0)

        if self.activation_func == "tanh":
            activated_layer = lambda x: np.tanh(x)

        return activated_layer(wi)

    def minimize_error(self, activated_layer):
        """ Minimize the training error.

        Parameters
        ----------
        activated_layer : ndarray
            Output of the activation function
        name : str
            Name of the optimizing algorithm to use

        Returns
        -------
        w_matrix[0] : ndarray
            The weight matrix of the upper part of the network
        rss : float
            Sums of residuals
        predicted_values : ndarray
            The prediction of the model
        """

        if self.opt_func == "llsq":
            w_matrix2 = np.linalg.lstsq(activated_layer, self.training_data_output, rcond=None)
            rss = w_matrix2[1]
            predicted_values = np.dot(activated_layer, w_matrix2[0])

        return w_matrix2[0], rss, predicted_values

    def loss_function(self, predicted_values):

        if self.loss_func == "mse":
            return ((self.training_data_output - predicted_values) ** 2).mean()
        if self.loss_func == "rmse":
            return np.sqrt(((self.training_data_output - predicted_values) ** 2).mean())

    def calculate_complexity(self, w_matrix):

        k = np.count_nonzero(w_matrix[1:, :])

        return k

    def information_criterion(self, decision_variables):

        z = self.activation(decision_variables)
        w_matrix2, rss, prediction = self.minimize_error(z)
        # rss = ((self.training_data_output - prediction) ** 2).sum()
        k = self.calculate_complexity(decision_variables) + np.count_nonzero(w_matrix2)
        aic = 2 * k + self.num_of_samples * np.log(rss / self.num_of_samples)
        aicc = aic + (2 * k * (k + 1) / (self.num_of_samples - k - 1))

        return aicc

    def predict(self, decision_variables):

        activated_layer = self.activation(decision_variables)
        _, _, predicted_values = self.minimize_error(activated_layer)

        return predicted_values

    def select(self, pop, non_dom_front, criterion="min_error"):
        """ Select target model from the population.

        Parameters
        ----------
        pop : obj
            The population object
        non_dom_front : list
            Indices of the models on the non-dominated front
        criterion : str
            The criterion to use for selecting the model.
            Possible values: 'min_error', 'akaike_corrected', 'manual'

        Returns
        -------
        The selected model
        """
        if criterion == "min_error":
            # Return the model with the lowest error

            lowest_error = np.argmin(pop.objectives[:, 0])
            return pop.individuals[lowest_error]

        elif criterion == "akaike_corrected":

            # Calculate Akaike information criterion for the non-dominated front
            # and return the model with the lowest value

            info_c_rank = []

            for i in non_dom_front:

                info_c = self.information_criterion(pop.individuals[i])
                info_c_rank.append((info_c, i))

            info_c_rank.sort()

            return pop.individuals[info_c_rank[0][1]]

    def single_variance_response(self, model):

        print("number of variables: " + str(self.num_of_variables))
        # pref_val = float(
        #     input("Please input a value worse than the ideal: ")
        # )
        activated_layer = self.activation(model)
        _, _, predicted_values = self.minimize_error(activated_layer)

        trace0 = go.Scatter(x=predicted_values, y=self.training_data_output, mode="markers")
        trace1 = go.Scatter(x=self.training_data_output, y=self.training_data_output)
        data = [trace0, trace1]
        plotly.offline.plot(
            data,
            filename="svr.html",
            auto_open=True,
        )

        model[1, :] = model[1] + 1

        activated_layer = self.activation(model)
        _, _, predicted_values = self.minimize_error(activated_layer)

        trace0 = go.Scatter(x=predicted_values, y=self.training_data_output, mode="markers")
        trace1 = go.Scatter(x=self.training_data_output, y=self.training_data_output)
        data = [trace0, trace1]
        plotly.offline.plot(
            data,
            filename="svr1.html",
            auto_open=True,
        )
