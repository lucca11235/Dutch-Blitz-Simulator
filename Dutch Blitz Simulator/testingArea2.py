from player import Player
from game import Game
from tqdm import tqdm
import random
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

s_aveg_cards = []
s_act_t = []
s_final_scores = []
s_made_blitz = []

for i in tqdm(range(500)):
    g = Game()

    g.create_random_players(4, 5, 0)
    g.initialize_players()

    aveg_cards, act_t, final_score,made_blitz = g.simulate(return_stat=True)
    s_aveg_cards += aveg_cards
    s_act_t += act_t
    s_final_scores += final_score
    s_made_blitz += made_blitz


def unnorm_data(data):
    return_data = []

    mean = np.mean(data)
    sd = np.std(data)

    for num in data:
        z_score = (num - mean) / sd
        new_num = norm.cdf(z_score)
        return_data.append(new_num)
    return return_data


def min_max(data):
    min_d = np.min(data)
    max_d = np.max(data)
    return [(d - min_d) / (max_d - min_d) for d in data]

    return return_data


def plot_norm_data(data):
    min_p, max_p = min(data), max(data)
    num_bins = int(np.sqrt(len(data)))

    plt.hist(data, bins=np.linspace(min_p, max_p, num_bins))
    plt.show()


new_averages = unnorm_data(s_aveg_cards)
new_points = min_max(s_final_scores)
new_act_t = unnorm_data(s_act_t)

# filtered_data = [(a, p) for a, p in zip(new_averages, s_made_blitz) if p != 0]
# new_averages, new_points = zip(*filtered_data)

print(np.corrcoef(new_averages, new_points))

plt.scatter(new_averages, new_points,s = 5)
plt.show()
