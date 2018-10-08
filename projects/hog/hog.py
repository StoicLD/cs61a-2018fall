"""CS 61A Presents The Game of Hog."""

from dice import six_sided, four_sided, make_test_dice
from ucb import main, trace, interact
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
    "*** YOUR CODE HERE ***"
    #注意！要每次掷骰子保存上次的次数，继续从上次的地方开始
    sum=0;
    is_bog=False;   #if there is a 1s,then make this var true
    while(num_rolls):
        num_rolls-=1
        x=dice()
        if(x!=1):
            sum+=x
        else:
            sum=1
            is_bog=True
    if(is_bog):
        return 1
    else:
        return sum
    # END PROBLEM 1

def free_bacon(score):
    """Return the points scored from rolling 0 dice (Free Bacon).

    score:  The opponent's current score.
    """
    assert score < 100, 'The game should be over.'
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    # END PROBLEM 2
    #这道题是当选择不投筛子，也就是0的时候得到的分数（基于对手的分数!!!）
    ten_digit=score//10
    one_digit=score%10
    if (ten_digit*2-one_digit)<=1:
        return 1
    else:
        return (ten_digit*2-one_digit)
    

def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function that simulates a single dice roll outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    cur_score=0;
    #第一种情况，free_bacon发生
    if(num_rolls==0):
        cur_score=free_bacon(opponent_score)
    #正常情况
    else:
        cur_score=roll_dice(num_rolls,dice)
    #结算
    return cur_score
    # END PROBLEM 3


def is_swap(player_score, opponent_score):
    """
    Return whether the current player's score has the same absolute
    difference between its last two digits as the opponent's score.
    """
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    #这里实现是否交换分数,注意回合结束时可能会超过100!!!!，所以需要注意!!!
    play_tens=player_score//10-(player_score//100)*10
    opponent_tens=opponent_score//10-(opponent_score//100)*10
    player_score_diff=abs(play_tens-(player_score%10))
    opponent_score_diff=abs(opponent_tens-(opponent_score%10))
    if(player_score_diff==opponent_score_diff):
        return True
    else:
        return False
    # END PROBLEM 4


def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player


def silence(score0, score1):
    """Announce nothing (see Phase 2)."""
    return silence


def play(strategy0, strategy1, score0=0, score1=0, dice=six_sided,
         goal=GOAL_SCORE, say=silence):
    """Simulate a game and return the final scores of both players, with Player
    0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    score0:     Starting score for Player 0
    score1:     Starting score for Player 1
    dice:       A function of zero arguments that simulates a dice roll.
    goal:       The game ends and someone wins when this score is reached.
    say:        The commentary function to call at the end of the first turn.
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    #注意几个坑！！！pig out的时候是基于对手分数的！ 然后strategy函数返回的是投骰子的个数！！！
    is_win=False        #判断是否有人已经胜利
    cur_score0=score0   #当前回合的累积分数
    cur_score1=score1
    cur_say=say
    while(is_win==False):
        if(player==0):
            #本回合要投掷的骰子个数
            num_roll_this_turn=strategy0(cur_score0,cur_score1)             
            cur_score0+= take_turn(num_roll_this_turn,cur_score1,dice)
            if(is_swap(cur_score0,cur_score1)):
                #交换分数
                change_score=cur_score0
                cur_score0=cur_score1
                cur_score1=change_score
            #Q6添加的代码
            cur_say=cur_say(cur_score0,cur_score1)
            #交换玩家       
            player=other(player)                                           
        else:
            #本回合要投掷的骰子个数
            num_roll_this_turn=strategy1(cur_score1,cur_score0)     
            cur_score1+= take_turn(num_roll_this_turn,cur_score0,dice)
            if(is_swap(cur_score0,cur_score1)):
                #交换分数
                change_score=cur_score0
                cur_score0=cur_score1
                cur_score1=change_score
            player=other(player)          
            #Q6添加的代码
            cur_say=cur_say(cur_score0,cur_score1)
        if(cur_score0>=goal or cur_score1>=goal):
            is_win=True
    score0=cur_score0
    score1=cur_score1
    # END PROBLEM 5
    # (note that the indentation for the problem 6 prompt (***YOUR CODE HERE***) might be misleading)
    # BEGIN PROBLEM 6
    "*** YOUR CODE HERE ***"
    # END PROBLEM 6
    return score0, score1


#######################
# Phase 2: Commentary #
#######################


def say_scores(score0, score1):
    """A commentary function that announces the score for each player."""
    print("Player 0 now has", score0, "and Player 1 now has", score1)
    return say_scores

def announce_lead_changes(previous_leader=None):
    """Return a commentary function that announces lead changes.

    >>> f0 = announce_lead_changes()
    >>> f1 = f0(5, 0)
    Player 0 takes the lead by 5
    >>> f2 = f1(5, 12)
    Player 1 takes the lead by 7
    >>> f3 = f2(8, 12)
    >>> f4 = f3(8, 13)
    >>> f5 = f4(15, 13)
    Player 0 takes the lead by 2
    """
    def say(score0, score1):
        if score0 > score1:
            leader = 0
        elif score1 > score0:
            leader = 1
        else:
            leader = None
        if leader != None and leader != previous_leader:
            print('Player', leader, 'takes the lead by', abs(score0 - score1))
        return announce_lead_changes(leader)
    return say

def both(f, g):
    """Return a commentary function that says what f says, then what g says.

    >>> h0 = both(say_scores, announce_lead_changes())
    >>> h1 = h0(10, 0)
    Player 0 now has 10 and Player 1 now has 0
    Player 0 takes the lead by 10
    >>> h2 = h1(10, 6)
    Player 0 now has 10 and Player 1 now has 6
    >>> h3 = h2(6, 18) # Player 0 gets 8 points, then Swine Swap applies
    Player 0 now has 6 and Player 1 now has 18
    Player 1 takes the lead by 12
    """
    def say(score0, score1):
        return both(f(score0, score1), g(score0, score1))
    return say


def announce_highest(who, previous_high=0, previous_score=0):
    """Return a commentary function that announces when WHO's score
    increases by more than ever before in the game.

    >>> f0 = announce_highest(1) # Only announce Player 1 score gains
    >>> f1 = f0(12, 0)
    >>> f2 = f1(12, 11)
    11 point(s)! That's the biggest gain yet for Player 1
    >>> f3 = f2(20, 11)
    >>> f4 = f3(13, 20) # Player 1 gets 2 points, then Swine Swap applies
    >>> f5 = f4(20, 35) # Player 0 gets 22 points, then Swine Swap applies
    15 point(s)! That's the biggest gain yet for Player 1
    >>> f6 = f5(20, 47) # Player 1 gets 12 points; not enough for a new high
    >>> f7 = f6(21, 47)
    >>> f8 = f7(21, 77)
    30 point(s)! That's the biggest gain yet for Player 1
    >>> f9 = f8(77, 22) # Swap!
    >>> f10 = f9(33, 77) # Swap!
    55 point(s)! That's the biggest gain yet for Player 1
    """
    assert who == 0 or who == 1, 'The who argument should indicate a player.'
    # BEGIN PROBLEM 7
    "*** YOUR CODE HERE ***"
    #上面的测试例子中传入的参数是两个选手的目前得分
    #两个玩家之前的分数
    def say(player0_score,player1_score):
        #当前得分
        cur_score=previous_score
        cur_high=previous_high
        if(who==0):
            cur_player=player0_score-cur_score
        else:
            cur_player=player1_score-cur_score
        if(cur_player>cur_high):
            if(who==0):            
                print(cur_player,"point(s)! That's the biggest gain yet for Player 0")
                cur_high=cur_player
            else:
                print(cur_player,"point(s)! That's the biggest gain yet for Player 1")
                cur_high=cur_player
        cur_score+=cur_player
        #我最终的解决方案是返回带参数的函数，这样相当于把下次调用时想要的参数先穿进去了
        #return func(返回一个函数)，只会执行这个函数的定义和参数定义，函数体是不执行的
        #这样就实现了接力棒，而不是覆盖参数，使得下次调用前几次定义的函数是参数依旧是
        #之前定义的参数
        return announce_highest(who,cur_high,cur_score)
    return say
    
    #END PROBLEM 7
#######################
# Phase 3: Strategies #
#######################

#这里把 roll改成了always_roll
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


def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.0
    """
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    #这个函数决定在num_samples次call fn这个函数的评价返回值
    def average_inern(*args):
        sum=0
        cur_numbers=num_samples
        while(cur_numbers):
            sum+=fn(*args)
            cur_numbers-=1
        #太zz了啊啊啊啊啊，这里应该改为num_samples
        return sum/num_samples
    return average_inern
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
    "*** YOUR CODE HERE ***"
    #这题其实就是暴力调用，没有技巧，结果只能在1到10之间取值，因此直接调用
    #逐一比较num_samples次调用后取得的总分数，取最大值
    max_score_rolls=1
    max_score=0
    for i in range(1,11):
        cur_score_fc=make_averaged(roll_dice,num_samples)
        cur_score=cur_score_fc(i,dice)        
        if(cur_score>max_score):
            max_score=cur_score
            max_score_rolls=i
    return max_score_rolls
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
    #这里的函数后面两个括号的call法，当函数里面还有函数的时候,后面的参数是给内嵌函数传参数的
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    #本函数用来测试胜率
    if False:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)

    if True:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))
    if True:
        print('always_roll(4) win rate:', average_win_rate(always_roll(4)))
    if True:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if True:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if False:  # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"


def bacon_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice if that gives at least MARGIN points, and
    rolls NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 10
    #使用0投策略的得分!!注意啦0投是得分而不是交换分数，是根据对方的分数得分！！！
    if(free_bacon(opponent_score)>=margin):
        return 0
    return num_rolls  # Replace this statement
    # END PROBLEM 10


def swap_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least MARGIN points and does not trigger a
    non-beneficial swap. Otherwise, it rolls NUM_ROLLS.
    """
    # BEGIN PROBLEM 11
    future_score=score+free_bacon(opponent_score)
    if(is_swap(future_score,opponent_score)):
        if(future_score>opponent_score):
            return num_rolls
        else:
            return 0
    elif((future_score-score)>=margin):
        return 0
    return num_rolls  # Replace this statement
    # END PROBLEM 11


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN PROBLEM 12
    
    return 4  # Replace this statement
    # END PROBLEM 12


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