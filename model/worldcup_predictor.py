"""
This approach is based on a simulation model for football soccer championships,
proposed by Ruud H. Koning et. al. in 2002. For details, please refer to the
paper: http://www-bcf.usc.edu/~ridder/Wpapers/eor_5353_proofs.pdf

NOTE: The dataset 'International football results from 1872 to 2018' was sourced
from Kaggle. For details, please refer to
https://www.kaggle.com/martj42/international-football-results-from-1872-to-2017
"""


import numpy as np
import pandas as pd
from collections import defaultdict
from datetime import datetime
from itertools import chain, combinations
from scipy.stats import skellam

GROUPS = {'A': ['Egypt', 'Russia', 'Saudi Arabia', 'Uruguay'],
          'B': ['Iran', 'Morocco','Portugal', 'Spain'],
          'C': ['Australia', 'Denmark', 'France', 'Peru'],
          'D': ['Argentina', 'Croatia', 'Iceland', 'Nigeria'],
          'E': ['Brazil', 'Costa Rica', 'Serbia', 'Switzerland'],
          'F': ['Germany', 'Korea Republic', 'Mexico', 'Sweden'],
          'G': ['Belgium', 'England', 'Panama', 'Tunisia'],
          'H': ['Colombia', 'Japan', 'Poland', 'Senegal']}

def fetch_matches(filename, threshold, date_format='%Y-%m-%d'):
    """
    Fetch data about past international football results.

    Reads the results of international football matches, keeping only
    non-friendly matches that took place after threshold (inclusive).

    - **parameters**, **types**, **return** and **return types**::

    :param filename: The name of the csv file.
    :type filename: string

    :param threshold: Earliest date of interest (inclusive).
    :type threshold: string
    
    :param date_format: Format in which threshold and the dataset are specified.
    :type date_format: string

    :return: A table with recent non-friendly matches.
    :rtype: dataframe
    """
    past = pd.read_csv(filename)
    threshold = datetime.strptime(threshold, date_format)
    past['date'] = past['date'].apply(lambda x: 
                                        datetime.strptime(x, date_format))
    recent = past['date'] >= threshold
    friendly = past['tournament'] == 'Friendly'
    return past[recent & ~friendly]


def get_defense_capabilities(matches):
    """
    Measures the defense capabilities of all countries.

    Calculates the average number of goals all countries concede to rivals: the
    lower this number is, the better the defense of a country.

    - **parameters**, **types**, **return** and **return types**::

    :param matches: A table with recent non-friendly matches.
    :type matches: dataframe

    :return: A dictionary containing the average number of goals conceded by
    each country.
    :rtype: dict(float)
    """
    avg_goals_against = defaultdict(float)
    home_countries = {ctry for ctry in matches['home_team'].unique()}
    away_countries = {ctry for ctry in matches['away_team'].unique()}
    countries = home_countries.union(away_countries)

    for country in countries:
        # goals against as home team
        as_home = matches[matches['home_team'] == country]['away_score']
        # goals against as away team
        as_away = matches[matches['away_team'] == country]['home_score']
        goals_against = as_home.sum() + as_away.sum()
        number_matches = len(as_home) + len(as_away)
        avg_goals_against[country] = goals_against / number_matches
    return avg_goals_against


def _triangulate(source_data, source_status, target, defense):
    """
    Extrapolates how many goals source would score against target based on past
    performance, adjusting for defense strength.
    """
    inflated_sum = 0
    source = {word == source_status: word for word in ['home', 'away']}
    for i in range(source_data.shape[0]):
        source_score = source_data[source[True]+'_score'].iloc[i]
        pivot = source_data[source[not True]+'_team'].iloc[i]
        weight = defense[target] / defense[pivot]
        inflated_sum += weight * source_score
    return inflated_sum


def _estimate_goal_intensity(source, target, matches, defense):
    """
    Estimates the expected number of goals scored in a match. This parameter
    depends on the teams involved and is not symmetric. The estimator considers
    all goals scored by source in recent matches, weighed by the relative
    defense capability of target with respect to each source's opponent.
    """
    as_home = matches[matches['home_team'] == source]
    as_away = matches[matches['away_team'] == source]
    home_sum = _triangulate(as_home, 'home', target, defense)
    away_sum = _triangulate(as_away, 'away', target, defense)
    matches_played = as_home.shape[0] + as_away.shape[0]
    return (home_sum + away_sum) / matches_played  


def _realize_matches(pair, matches, defense, numsim=1):
    """
    Returns a plausible match score, based on the goal intensity of each team.
    It is assumed that the number of goals scored by a team follows a Poisson
    distribution.
    """
    country1, country2 = pair
    lambda1 = _estimate_goal_intensity(country1, country2, matches, defense)
    lambda2 = _estimate_goal_intensity(country2, country1, matches, defense)
    scores1 = np.random.poisson(lambda1, numsim)
    scores2 = np.random.poisson(lambda2, numsim)
    return list(zip(scores1, scores2))

"""
NOTE: The outcome of a match can be summarized via X - Y, where both random
variables follow a Poisson distribution (and thus the difference is Skellam
distributed: https://en.wikipedia.org/wiki/Skellam_distribution). If X - Y > 0,
then the first team wins the match; else if X - Y < 0, then the second team
wins the match; else there is a tie.
"""

def predict_group_match(country1, country2, matches, defense):
    """
    Probability of winning, tying or losing a match.

    Computes the probability that country1 wins, ties or loses a match in the
    round-robin phase, when facing country2. Assumptions: goal intensities are
    homogeneous throughout the game.

    - **parameters**, **types**, **return** and **return types**::

    :param country1: The name of the first country involved in a match.
    :type country1: string

    :param country2: The name of the second country involved in a match.
    :type country2: string
    
    :param matches: A table containing the results of international football
    matches.
    :type matches: dataframe
    
    :param defense: A dictionary containing the average number of goals conceded
    to rivals.
    :type defense: dict(float)

    :return: A dictionary with the probabilities of a 'win', 'draw' or 'lose'
    with respect to country1.
    :rtype: dict(float)
    """
    lambda1 = _estimate_goal_intensity(country1, country2, matches, defense)
    lambda2 = _estimate_goal_intensity(country2, country1, matches, defense)
    outcomes = defaultdict(float)
    outcomes['win'] = 1 - skellam.cdf(0, lambda1, lambda2)
    outcomes['draw'] = skellam.pmf(0, lambda1, lambda2)
    outcomes['lose'] = 1 - outcomes['win'] - outcomes['draw']
    return outcomes


def win_knockout_match(winner, loser, matches, defense):
    """
    Probability of winning a knockout match.

    Computes the probability of winning a match in the knockout phase, where
    ties are not allowed. Assumptions: if overtime is needed, two 15-minute
    halves must be played to completion; if a penalty shootout is required, both
    teams have the same chance of winning; goal intensities are homogeneous
    throughout the game.

    - **parameters**, **types**, **return** and **return types**::

    :param winner: The name of the country expected to win a knockout match.
    :type winner: string

    :param loser: The name of the country expected to lose a knockout match.
    :type loser: string
    
    :param matches: A table containing the results of international football
    matches.
    :type matches: dataframe
    
    :param defense: A dictionary containing the average number of goals conceded
    to rivals.
    :type defense: dict(float)

    :return: A number representing the probability of winning a knockout match.
    :rtype: float
    """
    lambda1 = _estimate_goal_intensity(winner, loser, matches, defense)
    lambda2 = _estimate_goal_intensity(loser, winner, matches, defense)

    regular = 1 - skellam.cdf(0, lambda1, lambda2)
    overtime = 1 - skellam.cdf(0, lambda1 / 3, lambda2 / 3)
    overtime *= skellam.pmf(0, lambda1, lambda2)
    kicks = skellam.pmf(0, lambda1 / 3, lambda2 / 3)
    kicks *= skellam.pmf(0, lambda1, lambda2)
    return regular + overtime + 1 / 2 * kicks


def _win_stage(prev_stage, best16, matches, defense):
    """
    Computes the probability of all countries winning any stage of the knockout
    phase, using the law of total probability: 
    P[Country i wins stage A] = sum_j{ P[Country i beats Country j]
                                *P[Country i proceeds to stage A]
                                *P[Country j proceeds to stage A] }
    """
    prev_matches = len(prev_stage.keys())
    new_matches = int(prev_matches / 2)
    proceed = {i: defaultdict(float) for i in range(new_matches)}
    for pivot_group in range(prev_matches):
        rival_group = pivot_group + np.power(-1, pivot_group)
        new_group = int(pivot_group / 2)
        for pivot in prev_stage[pivot_group].keys():
            pivot_arrive = prev_stage[pivot_group][pivot]
            for rival in prev_stage[rival_group].keys():
                rival_arrive = prev_stage[rival_group][rival]
                pivot_win = win_knockout_match(best16[pivot], best16[rival],
                                                matches, defense)
                proceed[new_group][pivot] += pivot_win*pivot_arrive*rival_arrive
    return proceed


def _simulate_round_robin(matches, defense):
    """
    Runs a simulation of all 48 matches in the groups phase (six matches for
    each of the eight groups) and returns the resulting winners and runners-up.
    """
    best16 = {}
    # Wins | Draws | Loses | Points | Goals Difference | Goals Scored
    colnames = ['W', 'D', 'L', 'Pts', 'GD', 'GS']
    for key in GROUPS.keys():
        table = pd.DataFrame(index=GROUPS[key], columns=colnames, data=0)
        for pair in combinations(GROUPS[key], 2):
            scores = _realize_matches(pair, matches, defense)[0]
            if scores[0] > scores[1]:
                table.loc[pair[0]] += [1,0,0,3,scores[0]-scores[1],scores[0]]
                table.loc[pair[1]] += [0,0,1,0,scores[1]-scores[0],scores[1]]
            elif scores[0] < scores[1]:
                table.loc[pair[0]] += [0,0,1,0,scores[0]-scores[1],scores[0]]
                table.loc[pair[1]] += [1,0,0,3,scores[1]-scores[0],scores[1]]
            else:
                table.loc[pair[0]] += [0,1,0,1,scores[0]-scores[1],scores[0]]
                table.loc[pair[1]] += [0,1,0,1,scores[1]-scores[0],scores[1]]
        # FIXME: Not all tie-breaking rules are implemented.
        table.sort_values(['Pts', 'GD', 'GS'], ascending=False, inplace=True)
        best16[key+'1'] = table.index[0]
        best16[key+'2'] = table.index[1]
    return best16


def _merge_simulation(simulation, aggregator, best16, total, groups=False):
    """
    Approximates the unconditional probability of reaching any given stage of
    the knockout phase by averaging plausible scenarios, one at a time.
    """
    for group in simulation.keys():
        for key in simulation[group].keys():
        	if groups:
        		aggregator[best16[key]][key[-1]] += 1 / total
        	else:
        		aggregator[best16[key]] += simulation[group][key] / total
    return aggregator


def predict_worldcup(matches, defense, best16={}, numsim=100):
    """
    Probabilities of winning the worldcup.

    Computes the probability each participating country has of winning the
    worldcup, using the law of total probability on the knockout tree. If the
    winners and runners-up are unknown, several simulations are run, which are
    then aggregated to obtain the unconditional probabilities.

    - **parameters**, **types**, **return** and **return types**::
    
    :param matches: A table containing the results of international football
    matches.
    :type matches: dataframe
    
    :param defense: A dictionary containing the average number of goals conceded
    to rivals.
    :type defense: dict(float)

    :param best16: A dictionary containing the names of the countries -and their
    corresponding positions- that passed to the knockout phase.
    :type best16: dict(string)

    :param numsim: The number of simulations to run in case the winners and the
    runners-up are unknown.
    :type numsim: int

    :return: A tuple containing dictionaries with the probabilities of reaching
    any given stage of the knockout phase (round of 16, quarters, semis, final)
    and ultimately winning the worldcup.
    :rtype: tuple
    """
    if best16.keys():
        numsim = 1
    order = ['A1', 'B2', 'C1', 'D2', 'E1', 'F2', 'G1', 'H2']
    order += ['B1', 'A2', 'D1', 'C2', 'F1', 'E2', 'H1', 'G2']
    countries = list(chain(*GROUPS.values()))
    gets_round16 = {i: {order[i]:1} for i in range(len(order))}

    round16 = {country: {'1': 0, '2': 0} for country in countries}
    quarters = {country: 0 for country in countries}
    semis = {country: 0 for country in countries}
    final = {country: 0 for country in countries}
    champion = {country: 0 for country in countries}

    for i in range(numsim):
        if not best16.keys():
            best16 = _simulate_round_robin(matches, defense)
        gets_quarters = _win_stage(gets_round16, best16, matches, defense)
        gets_semis = _win_stage(gets_quarters, best16, matches, defense)
        gets_final = _win_stage(gets_semis, best16, matches, defense)
        gets_cup = _win_stage(gets_final, best16, matches, defense)

        round16 = _merge_simulation(gets_round16, round16, best16, numsim, True)
        quarters = _merge_simulation(gets_quarters, quarters, best16, numsim)
        semis = _merge_simulation(gets_semis, semis, best16, numsim)
        final = _merge_simulation(gets_final, final, best16, numsim)
        champion = _merge_simulation(gets_cup, champion, best16, numsim)
        best16 = {}
    return round16, quarters, semis, final, champion
