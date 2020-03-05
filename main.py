# coding: utf-8

import random
import math

# ----------------------< Game rules constants >-----------------------------------------------------------------------

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

# ----------------------< Game functions >-----------------------------------------------------------------------------

def roll_dices(dices_number):
    values_occurences = [0] * NB_DICE_SIDE

    rolled_dices = 0
    while rolled_dices < dices_number:
        rolled_dice_value = random.randint(1, NB_DICE_SIDE)      
        values_occurences[rolled_dice_value - 1] += 1
        
        rolled_dices += 1
    return values_occurences

def count_bonus(values_occurences):
    bonus_score = 0

    index = 0
    while index < NB_DICE_SIDE:
        bonus_multiplier = BONUS_VALUE_FOR_NORMAL_BONUS
        if index == 0:
            bonus_multiplier = BONUS_VALUE_FOR_ACE_BONUS

        bonus_number = values_occurences[index] // TRIGGER_OCCURRENCE_FOR_BONUS
        
        if bonus_number > 0:
            bonus_score += bonus_multiplier * bonus_number * (index + 1)
            values_occurences[index] %= TRIGGER_OCCURRENCE_FOR_BONUS
        
        index += 1 
    return bonus_score, values_occurences

def count_normal_score(values_occurences):
    score = 0
    dice_index = 0
    while dice_index < len(LIST_SCORING_DICE_VALUE):
        values_occurences_index = LIST_SCORING_DICE_VALUE[dice_index] - 1

        score += values_occurences[values_occurences_index] * LIST_SCORING_MULTIPLIER[dice_index]
        values_occurences[values_occurences_index] = 0
        
        dice_index += 1
    return score, values_occurences

def analyze_roll_score(values_occurences):
    bonus_score, remaining_occurences = count_bonus(values_occurences)
    normal_score, remaining_occurences = count_normal_score(remaining_occurences)

    total_score = bonus_score + normal_score

    return total_score, remaining_occurences

def player_turn():
    turn_score = 0
    play_flag = 1
    dices_number = DEFAULT_DICES_NB
    
    while play_flag == 1:
        values_occurences = roll_dices(dices_number)
        print(values_occurences)
        roll_score, remaining_dices_list = analyze_roll_score(values_occurences)
        dices_number = sum(remaining_dices_list)
        print('Score: %d\nnon scoring dices number = %d \n' % (roll_score, dices_number))

        if roll_score == 0:
            turn_score = 0
            play_flag = 0
            print('Lost turn')
            continue
        else:
            if dices_number == 0:
                dices_number = DEFAULT_DICES_NB
            play_flag = random.randint(0, 1)
            if play_flag == 1:
                print('play again')
            else:
                print('stopping here')
            turn_score += roll_score
    
    print('\nturn score: %d points' % turn_score)
    return turn_score

def play_until_fail(nb_dices):
    turn_score = 0

    dices_number = nb_dices
    
    while True:
        values_occurences = roll_dices(dices_number)
        # print(values_occurences)

        roll_score, remaining_dices_list = analyze_roll_score(values_occurences)
        dices_number = sum(remaining_dices_list)

        if roll_score == 0:
            # print('Lost turn with a potential gain of %d points' % turn_score)
            return  turn_score
        else:
            if dices_number == 0:
                dices_number = nb_dices
            turn_score += roll_score
    
    # print('\nturn score: %d points' % turn_score)
    return turn_score

def analyze_roll_distribution(nb_rolls, nb_dices, step):
    scores = []
    remaining_dices_stats = [0] * (nb_dices + 1)

    # Creating samples
    rolled_dices = 0
    while rolled_dices < nb_rolls:
        values_occurences = roll_dices(nb_dices)
        score, remaining_dices = analyze_roll_score(values_occurences)
        remaining_dices_number = sum(remaining_dices)

        remaining_dices_stats[remaining_dices_number] += 1
        scores.append(score)

        rolled_dices += 1
    
    # Remaining dices stats
    index = 0
    while index < nb_dices + 1:
        remaining_dices_stats[index] = (100 * remaining_dices_stats[index]) / nb_rolls
        index += 1

    max_score = max(scores)
    score_stats = [0] * (math.ceil(max_score/step) + 1)

    # Counting occurences
    index = 0
    while index < nb_rolls:
        score_index = math.ceil(scores[index]/step)
        score_stats[score_index] += 1
        index += 1
    
    # Turning occurences to percentage
    index = 0
    while index < len(score_stats):
        score_stats[index] = (100 * score_stats[index]) / nb_rolls
        index += 1

    return remaining_dices_stats, score_stats

def analyze_turn_distribution(nb_turns, nb_dices, step):
    scores = []

    # Creating samples
    played_turns = 0
    while played_turns < nb_turns:
        score = play_until_fail(nb_dices)
        scores.append(score)

        played_turns += 1
    
    # Counting occurences
    max_score = max(scores)
    score_occurences = [0] * ((max_score // step) + 1)
    print((max_score // step) + 1)
    index = 0
    while index < nb_turns:
        # print(math.ceil(scores[index] / step))
        score_index = math.ceil(scores[index] / step)
        score_occurences[score_index] += 1
        index += 1
    
    score_stats = score_occurences
    index = 0
    while index < len(score_stats):
        score_stats[index] = (100 * score_stats[index]) / nb_turns
        index += 1

    return max_score, score_stats
    
# ----------------------< Tests part >---------------------------------------------------------------------------------

# print(play_until_fail(5))
print(analyze_turn_distribution(100000, 5, 100))

# remaining_dices_stats, score_stats = analyze_roll_distribution(1000000, DEFAULT_DICES_NB, 50)
# print(remaining_dices_stats)
# print(score_stats)