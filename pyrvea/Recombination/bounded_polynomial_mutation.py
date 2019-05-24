import numpy as np


def mutation(population, offspring, prob_mut=0.3, dis_mut=20):

    min_val = np.ones_like(offspring) * population.lower_limits
    max_val = np.ones_like(offspring) * population.upper_limits
    k = np.random.random(offspring.shape)
    miu = np.random.random(offspring.shape)
    temp = np.logical_and((k <= prob_mut), (miu < 0.5))
    offspring_scaled = (offspring - min_val) / (max_val - min_val)
    offspring[temp] = offspring[temp] + (
        (max_val[temp] - min_val[temp])
        * (
            (
                2 * miu[temp]
                + (1 - 2 * miu[temp]) * (1 - offspring_scaled[temp]) ** (dis_mut + 1)
            )
            ** (1 / (dis_mut + 1))
            - 1
        )
    )
    temp = np.logical_and((k <= prob_mut), (miu >= 0.5))
    offspring[temp] = offspring[temp] + (
        (max_val[temp] - min_val[temp])
        * (
            1
            - (
                2 * (1 - miu[temp])
                + 2 * (miu[temp] - 0.5) * offspring_scaled[temp] ** (dis_mut + 1)
            )
            ** (1 / (dis_mut + 1))
        )
    )
    offspring[offspring > max_val] = max_val[offspring > max_val]
    offspring[offspring < min_val] = min_val[offspring < min_val]

    return offspring
