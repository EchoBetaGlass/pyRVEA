from pyrvea.Problem.evonn_test_functions import EvoNNTestProblem
from pyrvea.Problem.evonn_problem import EvoNNModel
from pyrvea.Problem.evodn2_problem import EvoDN2Model
from pyrvea.Problem.testProblem import testProblem
from pyrvea.Problem.dataproblem import DataProblem
from pyrvea.Population.Population import Population
from pyrvea.EAs.PPGA import PPGA
from pyrvea.EAs.RVEA import RVEA
from pyrvea.EAs.slowRVEA import slowRVEA
import numpy as np
import pandas as pd


# import matplotlib
# matplotlib.use("WebAgg")
# import matplotlib.pyplot as plt

# test_prob = EvoNNTestProblem("Sphere", num_of_variables=3)
# training_data_input, training_data_output = test_prob.create_training_data(
#     samples=250, method="random", seed=31
# )
#
# model_evodn2 = EvoDN2Model(name="EvoDN2_" + test_prob.name)
# model_evodn2.set_params(
#         pop_size=500,
#         subnet_struct=(4, 6),
#         num_nodes=6,
#         prob_omit=0.2,
#         activation_func="sigmoid",
#         opt_func="llsq",
#         loss_func="rmse",
#         criterion="min_error",
#         logging=True,
#         plotting=True)

# model_evodn2.fit(training_data_input, training_data_output)
# y = model_evodn2.predict(training_data_input)
# model_evodn2.plot(y, training_data_output)

# model_evonn = EvoNNModel(name="EvoNN_" + test_prob.name)
# model_evonn.set_params(
#         num_nodes=20,
#         pop_size=500,
#         prob_omit=0.2,
#         activation_func="sigmoid",
#         opt_func="llsq",
#         loss_func="rmse",
#         criterion="akaike_corrected",
#         logging=True,
#         plotting=True)
#
# model_evonn.fit(training_data_input, training_data_output)
# y = model_evonn.predict(training_data_input)
# model_evonn.plot(y, training_data_output)
#
#
# test_prob = EvoNNTestProblem("Matyas")
# training_data_input, training_data_output = test_prob.create_training_data(
#     samples=250, method="random", seed=31
# )
#
# model_evodn2 = EvoDN2Model(name="EvoDN2_" + test_prob.name)
# model_evodn2.set_params(
#         pop_size=500,
#         subnet_struct=(6, 10),
#         num_nodes=10,
#         prob_omit=0.2,
#         activation_func="sigmoid",
#         opt_func="llsq",
#         loss_func="rmse",
#         criterion="min_error",
#         logging=True,
#         plotting=True)
#
# model_evodn2.fit(training_data_input, training_data_output)
# y = model_evodn2.predict(training_data_input)
# model_evodn2.plot(y, training_data_output)
#
# model_evonn = EvoNNModel(name="EvoNN_" + test_prob.name)
# model_evonn.set_params(
#         num_nodes=20,
#         pop_size=500,
#         prob_omit=0.2,
#         activation_func="sigmoid",
#         opt_func="llsq",
#         loss_func="rmse",
#         criterion="akaike_corrected",
#         logging=True,
#         plotting=True)
#
# model_evonn.fit(training_data_input, training_data_output)
# y = model_evonn.predict(training_data_input)
# model_evonn.plot(y, training_data_output)
#
# test_prob = EvoNNTestProblem("Himmelblau")
# training_data_input, training_data_output = test_prob.create_training_data(
#     samples=250, method="random", seed=31
# )
#
# model_evodn2 = EvoDN2Model(name="EvoDN2_" + test_prob.name)
# model_evodn2.set_params(
#         pop_size=500,
#         subnet_struct=(6, 10),
#         num_nodes=10,
#         prob_omit=0.2,
#         activation_func="sigmoid",
#         opt_func="llsq",
#         loss_func="rmse",
#         criterion="min_error",
#         logging=True,
#         plotting=True)
#
# model_evodn2.fit(training_data_input, training_data_output)
# y = model_evodn2.predict(training_data_input)
# model_evodn2.plot(y, training_data_output)
#
# model_evonn = EvoNNModel(name="EvoNN_" + test_prob.name)
# model_evonn.set_params(
#         num_nodes=20,
#         pop_size=500,
#         prob_omit=0.2,
#         activation_func="sigmoid",
#         opt_func="llsq",
#         loss_func="rmse",
#         criterion="akaike_corrected",
#         logging=True,
#         plotting=True)
#
# model_evonn.fit(training_data_input, training_data_output)
# y = model_evonn.predict(training_data_input)
# model_evonn.plot(y, training_data_output)
#
#
# test_prob = EvoNNTestProblem("Rastigrin", num_of_variables=2)
# training_data_input, training_data_output = test_prob.create_training_data(
#     samples=250, method="random", seed=31
# )
#
# model_evodn2 = EvoDN2Model(name="EvoDN2_" + test_prob.name)
# model_evodn2.set_params(
#         pop_size=500,
#         subnet_struct=(6, 10),
#         num_nodes=10,
#         prob_omit=0.2,
#         activation_func="sigmoid",
#         opt_func="llsq",
#         loss_func="rmse",
#         criterion="min_error",
#         logging=True,
#         plotting=True)
#
# model_evodn2.fit(training_data_input, training_data_output)
# y = model_evodn2.predict(training_data_input)
# model_evodn2.plot(y, training_data_output)
#
# model_evonn = EvoNNModel(name="EvoNN_" + test_prob.name)
# model_evonn.set_params(
#         num_nodes=20,
#         pop_size=500,
#         prob_omit=0.2,
#         activation_func="sigmoid",
#         opt_func="llsq",
#         loss_func="rmse",
#         criterion="akaike_corrected",
#         logging=True,
#         plotting=True)
#
# model_evonn.fit(training_data_input, training_data_output)
# y = model_evonn.predict(training_data_input)
# model_evonn.plot(y, training_data_output)
#
#
# test_prob = EvoNNTestProblem("Three-hump camel")
# training_data_input, training_data_output = test_prob.create_training_data(
#     samples=250, method="random", seed=31
# )
#
# model_evodn2 = EvoDN2Model(name="EvoDN2_" + test_prob.name)
# model_evodn2.set_params(
#         pop_size=500,
#         subnet_struct=(6, 10),
#         num_nodes=10,
#         prob_omit=0.2,
#         activation_func="sigmoid",
#         opt_func="llsq",
#         loss_func="rmse",
#         criterion="min_error",
#         logging=True,
#         plotting=True)
#
# model_evodn2.fit(training_data_input, training_data_output)
# y = model_evodn2.predict(training_data_input)
# model_evodn2.plot(y, training_data_output)
#
# model_evonn = EvoNNModel(name="EvoNN_" + test_prob.name)
# model_evonn.set_params(
#         num_nodes=20,
#         pop_size=500,
#         prob_omit=0.2,
#         activation_func="sigmoid",
#         opt_func="llsq",
#         loss_func="rmse",
#         criterion="akaike_corrected",
#         logging=True,
#         plotting=True)
#
# model_evonn.fit(training_data_input, training_data_output)
# y = model_evonn.predict(training_data_input)
# model_evonn.plot(y, training_data_output)
#
#
# test_prob = EvoNNTestProblem("Goldstein-Price")
# training_data_input, training_data_output = test_prob.create_training_data(
#     samples=250, method="random", seed=31
# )
# model_evodn2 = EvoDN2Model(name="EvoDN2_" + test_prob.name)
# model_evodn2.set_params(
#         pop_size=500,
#         subnet_struct=(6, 10),
#         num_nodes=10,
#         prob_omit=0.2,
#         activation_func="sigmoid",
#         opt_func="llsq",
#         loss_func="rmse",
#         criterion="min_error",
#         logging=True,
#         plotting=True)
#
# model_evodn2.fit(training_data_input, training_data_output)
# y = model_evodn2.predict(training_data_input)
# model_evodn2.plot(y, training_data_output)
#
# model_evonn = EvoNNModel(name="EvoNN_" + test_prob.name)
# model_evonn.set_params(
#         num_nodes=20,
#         pop_size=500,
#         prob_omit=0.2,
#         activation_func="sigmoid",
#         opt_func="llsq",
#         loss_func="rmse",
#         criterion="akaike_corrected",
#         logging=True,
#         plotting=True)
#
# model_evonn.fit(training_data_input, training_data_output)
# y = model_evonn.predict(training_data_input)
# model_evonn.plot(y, training_data_output)
#
#
# test_prob = EvoNNTestProblem("LeviN13")
# training_data_input, training_data_output = test_prob.create_training_data(
#     samples=250, method="random", seed=31
# )
# model_evodn2 = EvoDN2Model(name="EvoDN2_" + test_prob.name)
# model_evodn2.set_params(
#         pop_size=500,
#         subnet_struct=(6, 10),
#         num_nodes=10,
#         prob_omit=0.2,
#         activation_func="sigmoid",
#         opt_func="llsq",
#         loss_func="rmse",
#         criterion="min_error",
#         logging=True,
#         plotting=True)
#
# model_evodn2.fit(training_data_input, training_data_output)
# y = model_evodn2.predict(training_data_input)
# model_evodn2.plot(y, training_data_output)
#
# model_evonn = EvoNNModel(name="EvoNN_" + test_prob.name)
# model_evonn.set_params(
#         num_nodes=20,
#         pop_size=500,
#         prob_omit=0.2,
#         activation_func="sigmoid",
#         opt_func="llsq",
#         loss_func="rmse",
#         criterion="akaike_corrected",
#         logging=True,
#         plotting=True)
#
# model_evonn.fit(training_data_input, training_data_output)
# y = model_evonn.predict(training_data_input)
# model_evonn.plot(y, training_data_output)
#
#
# test_prob = EvoNNTestProblem("SchafferN2")
# training_data_input, training_data_output = test_prob.create_training_data(
#     samples=250, method="random", seed=31
# )
# model_evodn2 = EvoDN2Model(name="EvoDN2_" + test_prob.name)
# model_evodn2.set_params(
#         pop_size=500,
#         subnet_struct=(6, 10),
#         num_nodes=10,
#         prob_omit=0.2,
#         activation_func="sigmoid",
#         opt_func="llsq",
#         loss_func="rmse",
#         criterion="min_error",
#         logging=True,
#         plotting=True)
#
# model_evodn2.fit(training_data_input, training_data_output)
# y = model_evodn2.predict(training_data_input)
# model_evodn2.plot(y, training_data_output)
#
# model_evonn = EvoNNModel(name="EvoNN_" + test_prob.name)
# model_evonn.set_params(
#         num_nodes=20,
#         pop_size=500,
#         prob_omit=0.2,
#         activation_func="sigmoid",
#         opt_func="llsq",
#         loss_func="rmse",
#         criterion="akaike_corrected",
#         logging=True,
#         plotting=True)
#
# model_evonn.fit(training_data_input, training_data_output)
# y = model_evonn.predict(training_data_input)
# model_evonn.plot(y, training_data_output)
#
# # # ZDT 1 & 2
test_prob = testProblem("ZDT2", 30, 2, 0, 1, 0)
# np.random.seed(31)
training_data_input = np.random.rand(250, 30)
training_data_output = np.asarray(
    [test_prob.objectives(x) for x in training_data_input]
)
data = np.hstack((training_data_input, training_data_output))
f1_training_data_output = training_data_output[:, 0]
f2_training_data_output = training_data_output[:, 1]

dataset = pd.DataFrame.from_records(data)
x = []
for n in range(training_data_input.shape[1]):
    x.append("x" + str(n + 1))
y = ["f1", "f2"]
dataset.columns = x + y
problem = DataProblem(data=dataset, x=x, y=y)
problem.train_test_split()

problem.train(model_type="EvoNN", iterations=1, generations_per_iteration=1)

# pop = problem.optimize(RVEA)
pop = problem.optimize(
    algorithm=PPGA,
    opt=True,
    prob_prey_move=0.5,
    kill_interval=4,
    iterations=1,
    generations_per_iteration=1,
)

problem.plot_pareto(pop)

# f1_all = pop.objectives[:, 0]
# f2_all = pop.objectives[:, 1]
# f1_pareto = pareto[:, 0]
# f2_pareto = pareto[:, 1]
#
# plt.scatter(f1_all, f2_all)
# plt.plot(f1_pareto, f2_pareto, color='r')
# plt.xlabel('f1')
# plt.ylabel('f2')
# plt.show()


# model_evodn_f1 = EvoDN2Model(name="EvoDN2_" + test_prob.name + "_f1")
# model_evodn_f1.set_params(
#         pop_size=500,
#         subnet_struct=(6, 10),
#         num_nodes=10,
#         activation_func="sigmoid",
#         opt_func="llsq",
#         loss_func="rmse",
#         criterion="min_error",
#         logging=True,
#         plotting=True)
#
# model_evodn_f2 = EvoDN2Model(name="EvoDN2_" + test_prob.name + "_f2")
# model_evodn_f2.set_params(
#         pop_size=500,
#         subnet_struct=(6, 10),
#         num_nodes=10,
#         activation_func="sigmoid",
#         opt_func="llsq",
#         loss_func="rmse",
#         criterion="min_error",
#         logging=True,
#         plotting=True)
# model_evodn_f1.fit(training_data_input, f1_training_data_output)
# y = model_evodn_f1.predict(training_data_input)
# model_evodn_f1.plot(y, f1_training_data_output)
#
# model_evodn_f2.fit(training_data_input, f2_training_data_output)
# y = model_evodn_f2.predict(training_data_input)
# model_evodn_f2.plot(y, f2_training_data_output)
#
# model_evonn_f1 = EvoNNModel(name="EvoNN_" + test_prob.name + "_f1")
# model_evonn_f1.set_params(
#         num_nodes=20,
#         pop_size=500,
#         prob_omit=0.2,
#         activation_func="sigmoid",
#         opt_func="llsq",
#         loss_func="rmse",
#         criterion="akaike_corrected",
#         logging=True,
#         plotting=True)
#
# model_evonn_f2 = EvoNNModel(name="EvoNN_" + test_prob.name + "_f2")
# model_evonn_f2.set_params(
#         num_nodes=20,
#         pop_size=500,
#         prob_omit=0.2,
#         activation_func="sigmoid",
#         opt_func="llsq",
#         loss_func="rmse",
#         criterion="akaike_corrected",
#         logging=True,
#         plotting=True)
#
# model_evonn_f1.fit(training_data_input, f1_training_data_output)
# y = model_evonn_f1.predict(training_data_input)
# model_evonn_f1.plot(y, f1_training_data_output)
#
# model_evonn_f2.fit(training_data_input, f2_training_data_output)
# y = model_evonn_f2.predict(training_data_input)
# model_evonn_f2.plot(y, f2_training_data_output)
#
# test_prob = testProblem('ZDT2', 30, 2, 0, 1, 0)
# np.random.seed(31)
# training_data_input = np.random.rand(250, 30)
# training_data_output = np.asarray([test_prob.objectives(x) for x in training_data_input])
#
# f1_training_data_output = training_data_output[:, 0]
# f2_training_data_output = training_data_output[:, 1]
#
# model_evodn_f1 = EvoDN2Model(name="EvoDN2_" + test_prob.name + "_f1")
# model_evodn_f1.set_params(
#         pop_size=500,
#         subnet_struct=(6, 10),
#         num_nodes=10,
#         prob_omit=0.2,
#         activation_func="sigmoid",
#         opt_func="llsq",
#         loss_func="rmse",
#         criterion="min_error",
#         logging=True,
#         plotting=True)
#
# model_evodn_f2 = EvoDN2Model(name="EvoDN2_" + test_prob.name + "_f2")
# model_evodn_f2.set_params(
#         pop_size=500,
#         subnet_struct=(6, 10),
#         num_nodes=10,
#         activation_func="sigmoid",
#         opt_func="llsq",
#         loss_func="rmse",
#         criterion="min_error",
#         logging=True,
#         plotting=True)
# model_evodn_f1.fit(training_data_input, f1_training_data_output)
# y = model_evodn_f1.predict(training_data_input)
# model_evodn_f1.plot(y, f1_training_data_output)
#
# model_evodn_f2.fit(training_data_input, f2_training_data_output)
# y = model_evodn_f2.predict(training_data_input)
# model_evodn_f2.plot(y, f2_training_data_output)
#
#
# model_evonn_f1 = EvoNNModel(name="EvoNN_" + test_prob.name + "_f1")
# model_evonn_f1.set_params(
#         num_nodes=20,
#         pop_size=500,
#         prob_omit=0.2,
#         activation_func="sigmoid",
#         opt_func="llsq",
#         loss_func="rmse",
#         criterion="akaike_corrected",
#         logging=True,
#         plotting=True)
#
# model_evonn_f2 = EvoNNModel(name="EvoNN_" + test_prob.name + "_f2")
# model_evonn_f2.set_params(
#         num_nodes=20,
#         pop_size=500,
#         prob_omit=0.2,
#         activation_func="sigmoid",
#         opt_func="llsq",
#         loss_func="rmse",
#         criterion="akaike_corrected",
#         logging=True,
#         plotting=True)
#
# model_evonn_f1.fit(training_data_input, f1_training_data_output)
# y = model_evonn_f1.predict(training_data_input)
# model_evonn_f1.plot(y, f1_training_data_output)
#
# model_evonn_f2.fit(training_data_input, f2_training_data_output)
# y = model_evonn_f2.predict(training_data_input)
# model_evonn_f2.plot(y, f2_training_data_output)
