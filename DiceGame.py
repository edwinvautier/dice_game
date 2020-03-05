# coding: utf-8

import random
import math

# ----------------------< Game rules constants  >-----------------------------------------------------------------------

# Number of dices by default in the set
DEFAULT_DICES_NB = 5
# Target total score to win by default
DEFAULT_TARGET_SCORE = 2000
# Number of side of the dices used in the game
NB_DICE_SIDE = 6

# List of dice value scoring
LIST_SCORING_DICE_VALUE = [1, 5]
# List of associated score for scoring dice values
LIST_SCORING_MULTIPLIER = [100, 50]

# Trigger for multiple bonus
TRIGGER_OCCURRENCE_FOR_BONUS = 3
# Special bonus multiplier for multiple ace bonus
BONUS_VALUE_FOR_ACE_BONUS = 1000
# Standard multiplier for multiple dices value bonus
BONUS_VALUE_FOR_NORMAL_BONUS = 100


def roll_dices(nb_dice_to_roll):
    dices_value_occurrence_list = [0] * NB_DICE_SIDE

    dice_index = 0
    while dice_index < nb_dice_to_roll:
        dice_value = random.randint(1, NB_DICE_SIDE)
        dices_value_occurrence_list[dice_value - 1] += 1
        dice_index += 1

    return dices_value_occurrence_list


def analyse_roll_bonus_score(dices_value_occurrence_list):
    roll_score_from_bonus = 0

    dice_side_index = 0
    while dice_side_index < NB_DICE_SIDE:
        nb_of_bonus = dices_value_occurrence_list[dice_side_index] // TRIGGER_OCCURRENCE_FOR_BONUS
        if nb_of_bonus > 0:
            if dice_side_index == 0:
                bonus_multiplier = BONUS_VALUE_FOR_ACE_BONUS
            else:
                bonus_multiplier = BONUS_VALUE_FOR_NORMAL_BONUS

            roll_score_from_bonus += nb_of_bonus * bonus_multiplier * (dice_side_index + 1)

            dices_value_occurrence_list[dice_side_index] %= TRIGGER_OCCURRENCE_FOR_BONUS

        dice_side_index += 1

    return roll_score_from_bonus, dices_value_occurrence_list


def analyse_non_bonus_score(dices_value_occurrence_list):
    roll_score_from_non_bonus = 0

    scoring_value_index = 0
    while scoring_value_index < len(LIST_SCORING_DICE_VALUE):
        scoring_value = LIST_SCORING_DICE_VALUE[scoring_value_index]
        scoring_multiplier = LIST_SCORING_MULTIPLIER[scoring_value_index]

        scoring_value_occurrence = dices_value_occurrence_list[scoring_value - 1]

        if scoring_value_occurrence > 0:
            roll_score_from_non_bonus += scoring_multiplier * scoring_value_occurrence
            dices_value_occurrence_list[scoring_value - 1] = 0

        scoring_value_index += 1

    return roll_score_from_non_bonus, dices_value_occurrence_list


def analyse_roll_score(dices_value_occurrence_list):
    score_from_bonus, remaining_value_occurrence_list = analyse_roll_bonus_score(dices_value_occurrence_list)
    score_from_non_bonus, remaining_value_occurrence_list = analyse_non_bonus_score(remaining_value_occurrence_list)

    return score_from_bonus + score_from_non_bonus, remaining_value_occurrence_list


def play_until_fail(nb_dice):
    total_score = 0
    remaining_dice_to_roll = nb_dice

    while True:
        roll_score, remainning_dice_occurence = analyse_roll_score(roll_dices(remaining_dice_to_roll))

        if roll_score == 0:
            return total_score
        else:
            total_score += roll_score

        remaining_dice_to_roll = sum(remainning_dice_occurence)
        if remaining_dice_to_roll == 0:
            remaining_dice_to_roll = nb_dice


def roll_score_distribution(nb_roll, nb_dices, interval):
    score_list = []

    scoring_dice_occurrence = [0] * (nb_dices + 1)

    roll_index = 0
    while roll_index < nb_roll:
        roll_score, remaining_value_occurrence_list = analyse_roll_score(roll_dices(nb_dices))

        score_list.append(roll_score)
        scoring_dice_occurrence[nb_dices - sum(remaining_value_occurrence_list)] += 1

        roll_index += 1

    max_roll_score = max(score_list)

    score_occurrence_list = [0] * ((max_roll_score // interval) + 1)

    roll_index = 0
    while roll_index < nb_roll:
        score_occurrence_index = math.ceil(score_list[roll_index] / interval)
        score_occurrence_list[score_occurrence_index] += 1
        roll_index += 1

    score_occurrence_index = 0
    while score_occurrence_index < len(score_occurrence_list):
        score_occurrence_list[score_occurrence_index] /= nb_roll
        score_occurrence_index += 1

    remaining_dice_occurrence_index = 0
    while remaining_dice_occurrence_index <= nb_dices:
        scoring_dice_occurrence[remaining_dice_occurrence_index] /= nb_roll
        remaining_dice_occurrence_index += 1

    return max_roll_score, score_occurrence_list, scoring_dice_occurrence


def turn_score_distribution(nb_turn, nb_dice, interval):
    score_list = []

    roll_index = 0
    while roll_index < nb_turn:
        score_list.append(play_until_fail(nb_dice))
        roll_index += 1

    max_roll_score = max(score_list)

    score_occurrence_list = [0] * ((max_roll_score // interval) + 2)

    roll_index = 0
    while roll_index < nb_turn:
        score_occurrence_index = math.ceil(score_list[roll_index] / interval)
        score_occurrence_list[score_occurrence_index] += 1
        roll_index += 1

    occurrence_index = 0
    while occurrence_index < len(score_occurrence_list):
        score_occurrence_list[occurrence_index] /= nb_turn
        occurrence_index += 1

    return max_roll_score, score_occurrence_list


# max_roll_score, score_distribution, remaining_dice_occurrence_distribution = roll_score_distribution(1000, 5, 50)

# print(score_distribution)
# print(remaining_dice_occurrence_distribution)
# print(max_roll_score)

print(turn_score_distribution(1000000, 5, 1000))
