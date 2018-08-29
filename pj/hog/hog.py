"""CS 61A Presents The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################

def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    score = 0
    pig_out = False

    # Roll dice with "num_rolls" times 
    for i in range(num_rolls):
        dice_roll = dice()

        # if roll a "1", then set pig_out to be true, meaning that the player scores 1 point
        if dice_roll == 1:
            pig_out = True
        else:
            score = score + dice_roll

    if pig_out:
        return 1
    else:
        return score
    # END PROBLEM 1


def free_bacon(opponent_score):
    """Return the points scored from rolling 0 dice (Free Bacon)."""
    # BEGIN PROBLEM 2

    # temp: used to store the bacon points, but still need to check if it's a prime
    temp = 1 + max(opponent_score // 10, opponent_score % 10)
    # check if it's a prime
    if is_prime(temp):
        return next_prime(temp)
    else:
        return temp
    # END PROBLEM 2


# Write your prime functions here!
def is_prime(num):
    # 1 is not a prime
    if num == 1:
        return False

    # try from 2 up to n - 1 to see if there's a divisor 
    i = 2
    while i < num:
        if num % i == 0:
            return False
        else:
            i += 1

    return True

def next_prime(num):
    next_num = num + 1

    #loop until we find the next prime and return it
    while not(is_prime(next_num)):
        next_num += 1

    return next_num


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player. Also
    implements the Hogtimus Prime rule.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function that simulates a single dice roll outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 2

    # if player chooses not to roll a dice, then calculate the bacon points.
    if num_rolls == 0:
        return free_bacon(opponent_score)
    else:
        # otherwise check the score from roll_dice
        score = roll_dice(num_rolls, dice)

        # take care for Hogtimus Prime
        if is_prime(score):
            return next_prime(score)
        else:
            return score
    # END PROBLEM 2


def select_dice(dice_swapped):
    """Return a six-sided dice unless four-sided dice have been swapped in due
    to Perfect Piggy. DICE_SWAPPED is True if and only if four-sided dice are in
    play.
    """
    # BEGIN PROBLEM 3
    if dice_swapped:
        return four_sided
    else:
        return six_sided
    # END PROBLEM 3


# Write additional helper functions here!


def is_perfect_piggy(turn_score):
    """Returns whether the Perfect Piggy dice-swapping rule should occur."""
    # BEGIN PROBLEM 4

    # is not included in the Perfect Piggy
    if turn_score == 1:
        return False

    # test if the score is cube or square or not
    test_cube = round(turn_score ** (1. / 3))
    test_square = round(turn_score ** (1. / 2))

    # return the results
    if test_square ** 2 == turn_score or test_cube ** 3 == turn_score:
        return True
    else:
        return False
    # END PROBLEM 4


def is_swap(score0, score1):
    """Returns whether one of the scores is double the other."""
    # BEGIN PROBLEM 5

    if score0 == 0 or score1 == 0:
        return False

    # see if the max score of these two scores is double the other
    # for the rule of Swine Swap 
    if max(score0, score1) / min(score0, score1) == 2:
        return True
    else:
        return False
    # END PROBLEM 5


def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player


def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with Player
    0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0:     The starting score for Player 0
    score1:     The starting score for Player 1
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    dice_swapped = False # Whether 4-sided dice have been swapped for 6-sided
    # BEGIN PROBLEM 6
    dice = select_dice(dice_swapped)

    # This_turn_score: used to check if other rule are triggered or not
    this_turn_score0 = score0
    this_turn_score1 = score1

    # Loop until someone scores over the goal
    while score0 < goal and score1 < goal:
        # Player_0 takes the first turn 
        if player == 0:

            # Decides how many dice this player want to roll depending on this player's strategy
            total_dice_0 = strategy0(score0, score1) 
            # Call take_turn to determine the points scored for the turn
            this_turn_score0 = take_turn(total_dice_0, score1, dice)

            # Check the perfect piggy
            if is_perfect_piggy(this_turn_score0):
                dice_swapped = not dice_swapped
                dice = select_dice(dice_swapped)

            # Update the score for player_0
            score0 += this_turn_score0
    
            # Check if Swine Swap happens 
            if is_swap(score0, score1):
                score0, score1 = score1, score0

            # Check if the game ends or not
            if score0 >= goal or score1 >= goal:
                return score0, score1
            else:
                # If not, change to player1
                player = other(player)
        else:

            # Symmetric code to the Player_0
            total_dice1 = strategy1(score1, score0)
            this_turn_score1 = take_turn(total_dice1, score0, dice)

            if is_perfect_piggy(this_turn_score1):
                dice_swapped = not dice_swapped
                dice = select_dice(dice_swapped)

            score1 += this_turn_score1

            if is_swap(score0, score1):
                score0, score1 = score1, score0

            if score0 >= goal or score1 >= goal:
                return score0, score1
            else:
                player = other(player)

    # END PROBLEM 6
    return score0, score1


#######################
# Phase 2: Strategies #
#######################

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def check_strategy_roll(score, opponent_score, num_rolls):
    """Raises an error with a helpful message if NUM_ROLLS is an invalid
    strategy output. All strategy outputs must be integers from -1 to 10.

    >>> check_strategy_roll(10, 20, num_rolls=100)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(10, 20) returned 100 (invalid number of rolls)

    >>> check_strategy_roll(20, 10, num_rolls=0.1)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(20, 10) returned 0.1 (not an integer)

    >>> check_strategy_roll(0, 0, num_rolls=None)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(0, 0) returned None (not an integer)
    """
    msg = 'strategy({}, {}) returned {}'.format(
        score, opponent_score, num_rolls)
    assert type(num_rolls) == int, msg + ' (not an integer)'
    assert 0 <= num_rolls <= 10, msg + ' (invalid number of rolls)'


def check_strategy(strategy, goal=GOAL_SCORE):
    """Checks the strategy with all valid inputs and verifies that the strategy
    returns a valid input. Use `check_strategy_roll` to raise an error with a
    helpful message if the strategy returns an invalid output.

    >>> def fail_15_20(score, opponent_score):
    ...     if score != 15 or opponent_score != 20:
    ...         return 5
    ...
    >>> check_strategy(fail_15_20)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(15, 20) returned None (not an integer)
    >>> def fail_102_115(score, opponent_score):
    ...     if score == 102 and opponent_score == 115:
    ...         return 100
    ...     return 5
    ...
    >>> check_strategy(fail_102_115)
    >>> fail_102_115 == check_strategy(fail_102_115, 120)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(102, 115) returned 100 (invalid number of rolls)
    """
    # BEGIN PROBLEM 7

    # Run every possible input with (input_i, input_j)
    for input_i in range(goal):
        for input_j in range(goal):
            rolls = strategy(input_i, input_j)
            if check_strategy_roll(input_i, input_j, rolls) != None:
                check_strategy_roll(input_i, input_j, rolls)
    
    # END PROBLEM 7


# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.0
    """
    # BEGIN PROBLEM 8
    # average_dice takes the same number args as fn
    def average_dice(*args):
        total_roll = 0

        # repeat for num_samples times
        for i in range(num_samples):
            total_roll += fn(*args)

        # calculate the mean
        return total_roll / num_samples

    return average_dice
    # END PROBLEM 8


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9

    # initialized the higest score, perfect dice number and the dice for testing
    higest_score = 0
    perfect_dice_num = 1
    test_dice = make_averaged(roll_dice, num_samples)

    # try number of dice from (1 to 10), record the highest average turn score with the test_dice
    for i in range(1, 11):
        # update the information for higest score, dice number
        if test_dice(i, dice) > higest_score:
            higest_score = test_dice(i, dice)
            perfect_dice_num = i

    return perfect_dice_num
    # END PROBLEM 9


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(4)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if True:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if True:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if True:  # Change to True to test swap_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"


# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice if that gives at least MARGIN points, and
    rolls NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 10
    # if free bacon scores over than our margin, then the player choose to roll 0 die
    if free_bacon(opponent_score) >= margin:
        return 0
    else:
        return num_rolls
    # END PROBLEM 10
check_strategy(bacon_strategy)


def swap_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least MARGIN points. Otherwise, it rolls
    NUM_ROLLS.
    """
    # BEGIN PROBLEM 11
    total_score = score + free_bacon(opponent_score)

    # check if free_bacon can force a swap
    # if can then return 0
    if score < opponent_score and is_swap(total_score, opponent_score):
        return 0
    elif free_bacon(opponent_score) >= margin:
        return 0
    else:
        return num_rolls
    # END PROBLEM 11
check_strategy(swap_strategy)



def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    1. Try to force a beneficial swap.
        a. if free_bacon can force a swap -> use 0 dice.
        b. if score 1 point this turn can force a swap on the "current turn" -> use 10 dice, it has around 80% to score 1 point this turn.
        c. if score 1 point this turn can force a swap on the "oppenent's turn" -> use 10 dice
    2. Try to avoid a harmful swap.
        a. if free_bacon will trigger a harmful swap on the "current turn" -> use 5 dice(because the range of score for free_bacon is {0, 9}, so we choose to roll 5 dice to dodge this range.
        b. if free_bacon will trigger a harmful swap on the "oppenent's turn" -> use 5 dice
        c. if score 1 point this turn can trigger a harmful swap on "oppenent's turn" -> roll 0 dice for bacon_score. Because the only situation that bacon_score = 1 is when oppenent's score = 0.
        d. if score 1 points this trun can trigger a harmful swap on "oppenent's turn" -> roll 0 dice too.
    2. Force my oppoment to use four_sided if free_bacon can do that.
        a. if free_bacon can force this -> use 0 dice.
    3. Margin for free_bacon is 8
    3. If is leading more than 80 -> play safe, use 2 dice.
    4. If opponent is leading more than 80 -> play more risky, use 8 dice.
    5. Otherwise roll 4 dice

    """
    # BEGIN PROBLEM 12

    score_with_bacon = free_bacon(opponent_score)

    if score < opponent_score:
        if score + score_with_bacon >= 100 and not is_swap(score + score_with_bacon, opponent_score):
            return 0
        elif is_swap(score + score_with_bacon, opponent_score):
            return 0
        elif is_swap(score + score_with_bacon, opponent_score + take_turn(4, score + score_with_bacon)):
            return 0
        elif is_swap(score + 1, opponent_score):
            return 10
        elif is_swap(score + 1, opponent_score + take_turn(4, score + 1)):
            return 10
        elif free_bacon(opponent_score) >= 8:
            return 0
        elif is_perfect_piggy(free_bacon(opponent_score)):
            return 0
        elif opponent_score - score > 80:
            return 8
        else:
            return 4
    else:
        if score + score_with_bacon >= 100 and not is_swap(score + score_with_bacon, opponent_score):
            return 0
        elif is_swap(score + score_with_bacon, opponent_score):
            return 5
        elif is_swap(score + score_with_bacon, opponent_score + take_turn(4, score + score_with_bacon)):
            return 5
        elif is_swap(score + 1, opponent_score):
            return 0
        elif is_swap(score + 1, opponent_score + take_turn(4, score + 1)):
            return 0
        elif free_bacon(opponent_score) >= 8:
            return 0
        elif is_perfect_piggy(free_bacon(opponent_score)):
            return 0
        elif score - opponent_score > 80:
            return 2
        else:
            return 4

    # END PROBLEM 12
check_strategy(final_strategy)


##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.

@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()