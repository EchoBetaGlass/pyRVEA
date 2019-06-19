from pyrvea.Problem.baseProblem import baseProblem
from pyrvea.Population.Population import Population
from pyrvea.EAs.PPGA import PPGA
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
        name,
        X_train=None,
        y_train=None,
        num_input_nodes=4,
        num_hidden_nodes=5,
        num_of_objectives=2,
        w_low=-5.0,
        w_high=5.0,
        prob_omit=0.2,
        params=None,
    ):
        super().__init__()

        self.name = name
        self.X_train = X_train
        self.y_train = y_train
        self.num_input_nodes = num_input_nodes
        self.num_hidden_nodes = num_hidden_nodes
        self.num_of_objectives = num_of_objectives
        self.w_low = w_low
        self.w_high = w_high
        self.prob_omit = prob_omit
        self.params = params

    def fit(self, training_data, target_values):
        """Fit data in EvoNN model.

        Parameters
        ----------
        training_data : ndarray, shape = (numbers of samples, number of variables)
            Training data
        target_values : ndarray
            Target values
        """

        self.X_train = training_data
        self.y_train = target_values
        self.num_of_samples = target_values.shape[0]
        self.num_of_variables = training_data.shape[1]
        self.num_input_nodes = self.num_of_variables
        self.num_hidden_nodes = self.params["num_hidden_nodes"]

    def train(self, model):

        pop = Population(self, assign_type="EvoNN", pop_size=self.params["pop_size"], plotting=False)
        pop.evolve(
            PPGA,
            {
                "logging": self.params["logging"],
                "iterations": 10,
                "generations_per_iteration": 10
            }
        )

        non_dom_front = pop.non_dominated()
        model.w1 = self.select(pop, non_dom_front, self.params["criterion"])
        activated_layer = self.activation(model.w1)
        model.w2, _, model.y_pred = self.minimize_error(activated_layer)

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
        _, _, predicted_values = self.minimize_error(activated_layer)
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
        w1 = decision_variables
        # Calculate the dot product
        wi = np.dot(self.X_train, w1[1:, :]) + w1[0]

        if self.params["activation_func"] == "sigmoid":
            activated_layer = lambda x: 1 / (1 + np.exp(-x))

        if self.params["activation_func"] == "relu":
            activated_layer = lambda x: np.maximum(x, 0)

        if self.params["activation_func"] == "tanh":
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

        if self.params["opt_func"] == "llsq":
            w2 = np.linalg.lstsq(activated_layer, self.y_train, rcond=None)
            rss = w2[1]
            predicted_values = np.dot(activated_layer, w2[0])
            return w2[0], rss, predicted_values

    def loss_function(self, predicted_values):

        if self.params["loss_func"] == "mse":
            return ((self.y_train - predicted_values) ** 2).mean()
        if self.params["loss_func"]:
            return np.sqrt(((self.y_train - predicted_values) ** 2).mean())

    def calculate_complexity(self, w_matrix):

        k = np.count_nonzero(w_matrix[1:, :])

        return k

    def information_criterion(self, decision_variables):

        z = self.activation(decision_variables)
        w_matrix2, rss, prediction = self.minimize_error(z)
        # rss = ((self.y_train - prediction) ** 2).sum()
        k = self.calculate_complexity(decision_variables) + np.count_nonzero(w_matrix2)
        aic = 2 * k + self.num_of_samples * np.log(rss / self.num_of_samples)
        aicc = aic + (2 * k * (k + 1) / (self.num_of_samples - k - 1))

        return aicc

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
        model = None
        if criterion == "min_error":
            # Return the model with the lowest error

            lowest_error = np.argmin(pop.objectives[:, 0])
            model = pop.individuals[lowest_error]

        elif criterion == "akaike_corrected":

            # Calculate Akaike information criterion for the non-dominated front
            # and return the model with the lowest value

            info_c_rank = []

            for i in non_dom_front:

                info_c = self.information_criterion(pop.individuals[i])
                info_c_rank.append((info_c, i))

            info_c_rank.sort()

            model = pop.individuals[info_c_rank[0][1]]

        return model

    def create_logfile(self):

        # Save params to log file
        log_file = open(
            self.name
            + "_var"
            + str(self.num_of_variables)
            + "_nodes"
            + str(self.num_hidden_nodes)
            + ".log",
            "a",
        )
        print(
            "samples: "
            + str(self.num_of_samples)
            + "\n"
            + "variables: "
            + str(self.num_of_variables)
            + "\n"
            + "nodes: "
            + str(self.num_hidden_nodes)
            + "\n"
            + "activation: "
            + self.params["activation_func"]
            + "\n"
            + "opt func: "
            + self.params["opt_func"]
            + "\n"
            + "loss func: "
            + self.params["loss_func"],
            file=log_file,
        )
        return log_file

    def create_plot(self, model):

        trace0 = go.Scatter(x=model.y_pred, y=self.y_train, mode="markers")
        trace1 = go.Scatter(x=self.y_train, y=self.y_train)
        data = [trace0, trace1]
        plotly.offline.plot(
            data,
            filename=self.name
            + "_var"
            + str(self.num_of_variables)
            + "_nodes"
            + str(self.num_hidden_nodes)
            + ".html",
            auto_open=True,
        )


class EvoNNModel(EvoNN):
    def __init__(self, name, w1=None, w2=None, y_pred=None, svr=None):
        super().__init__(name)
        self.name = name
        self.w1 = w1
        self.w2 = w2
        self.y_pred = y_pred
        self.svr = svr
        self.log = None
        self.set_params()

    def fit(self, training_data, target_values):
        """Fit data in EvoNN model.

        Parameters
        ----------
        training_data : ndarray, shape = (numbers of samples, number of variables)
            Training data
        target_values : ndarray
            Target values
        """
        f1 = EvoNN(name=self.name, params=self.params)
        f1.fit(training_data, target_values)
        f1.train(self)
        if f1.params["logging"]:
            self.log = f1.create_logfile()
        if f1.params["plotting"]:
            f1.create_plot(self)
        self.num_of_samples = f1.num_of_samples
        self.single_variable_response(ploton=True, log=self.log)

    def predict(self, decision_variables):

        wi = np.dot(decision_variables, self.w1[1:, :]) + self.w1[0]

        if self.params["activation_func"] == "sigmoid":
            activated_layer = lambda x: 1 / (1 + np.exp(-x))

        if self.params["activation_func"] == "relu":
            activated_layer = lambda x: np.maximum(x, 0)

        if self.params["activation_func"] == "tanh":
            activated_layer = lambda x: np.tanh(x)

        out = np.dot(activated_layer(wi), self.w2)

        return out

    def set_params(
        self,
        name=None,
        num_hidden_nodes=15,
        pop_size=500,
        activation_func="sigmoid",
        opt_func="llsq",
        loss_func="rmse",
        criterion="akaike_corrected",
        logging=False,
        plotting=False,
    ):
        params = {
            "name": name,
            "num_hidden_nodes": num_hidden_nodes,
            "pop_size": pop_size,
            "activation_func": activation_func,
            "opt_func": opt_func,
            "loss_func": loss_func,
            "criterion": criterion,
            "logging": logging,
            "plotting": plotting,
        }

        self.params = params

    def single_variable_response(self, ploton=False, log=None):

        trend = np.loadtxt("trend")
        trend = trend[0: self.num_of_samples]
        avg = np.ones((1, self.w1[1:].shape[0])) * (0 + 1) / 2
        svr = np.empty((0, 2))

        for i in range(self.w1[1:].shape[0]):
            variables = np.ones((len(trend), 1)) * avg
            variables[:, i] = trend

            out = self.predict(variables)

            if min(out) == max(out):
                out = 0.5 * np.ones(out.size)
            else:
                out = (out - min(out)) / (max(out) - min(out))

            if ploton:
                trace0 = go.Scatter(
                    x=np.arange(len(variables[:, 1])), y=variables[:, i], name="input"
                )
                trace1 = go.Scatter(
                    x=np.arange(len(variables[:, 1])), y=out, name="output"
                )
                data = [trace0, trace1]
                plotly.offline.plot(
                    data, filename="x" + str(i + 1) + "_response.html", auto_open=True
                )

            p = np.diff(out)
            q = np.diff(trend)
            r = np.multiply(p, q)
            r_max = max(r)
            r_min = min(r)
            if r_max <= 0 and r_min <= 0:
                response = -1
                s = "inverse"
            elif r_max >= 0 and r_min >= 0:
                response = 1
                s = "direct"
            elif r_max == 0 and r_min == 0:
                response = 0
                s = "nil"
            elif r_min < 0 < r_max:
                response = 2
                s = "mixed"

            print("x" + str(i + 1) + " response: " + str(response) + " " + s, file=log)
            svr = np.vstack((svr, ["x" + str(i + 1), s]))
            self.svr = svr
