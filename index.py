# import modules
import itertools, random
import collections



# a = str(deck[1][0])
# b = str(deck[1][1])
# c = str(deck[2][0])
# d = str(deck[2][1])
# x = a+b
# y = c+d
#
# t1 = str(deck[5][0])
# t2 = str(deck[5][1])
# t3 = str(deck[6][0])
# t4 = str(deck[6][1])
# t5 = str(deck[7][0])
# t6 = str(deck[7][1])
# t7 = str(deck[8][0])
# t8 = str(deck[8][1])
# t9 = str(deck[9][0])
# t10 = str(deck[9][1])
#
# ta = t1 + t2
# tb = t3 + t4
# tc = t5 + t6
# td = t7 + t8
# te = t9 + t10
#
# op1 = str(deck[10][0])
# op2 = str(deck[10][1])
# op3 = str(deck[11][0])
# op4 = str(deck[11][1])
#
# opp1 = op1 + op2
# opp2 = op3 + op4




def numeric_ranks(cards):
    """
    Changes the input list of card strings to a list of
    strings with numbers substituting for face cards.
    ex.
    numeric_ranks(['AS','3S','4S','5S','JC'])
    returns ['14S','3S','4S','5S','11C']
    """
    suits = get_suits(cards)
    face_numbers = {'A': 14, 'J': 11, 'Q': 12, 'K': 13}
    for index, card in enumerate(cards):
        rank = card[0:-1]
        try:
            int(rank)
        except:
            # Rank is a letter, not a number
            cards[index] = str(face_numbers[rank])+suits[index]
    return cards


def get_ranks(cards):
    """
    Returns a list of ints containing the rank of each card in cards.
    ex.
    get_ranks(['2S','3C','5C','4D','6D'])
    returns [2,3,5,4,6]
    """
    cards = numeric_ranks(cards) # Convert rank letters to numbers (e.g. J to 11)
    return [int(card[0:-1]) for card in cards]


def get_suits(cards):
    """
    Returns a list of strings containing the suit of each card in cards.
    ex.
    get_ranks(['2S','3C','5C','4D','6D'])
    returns ['S','C','C','D','D']
    """
    return [card[-1] for card in cards]


def evaluate_hand(hand):
    """
    Returns a string containing the name of the hand in poker.
    Input hand must be a list of 5 strings.
    ex.
    evaluate_hand(['2S','3C','5C','4D','6D'])
    returns 'Straight'
    """
    hand = numeric_ranks(hand)
    ranks = get_ranks(hand)
    suits = get_suits(hand)
    if len(set(hand)) < len(hand) or max(ranks) > 14 or min(ranks) < 1:
        # There is a duplicate
        return 'Invalid hand'
    if isconsecutive(ranks):
        # The hand is a type of straight
        if all_equal(suits):
            # Hand is a flush
            if max(ranks) == 14:
                # Highest card is an ace
                return 'Royal flush'
            return 'Straight flush'
        return 'Straight'
    if all_equal(suits):
        return 'Flush'
    total = sum([ranks.count(x) for x in ranks])
    hand_names = {
        17: 'Four of a kind',
        13: 'Full house',
        11: 'Three of a kind',
        9: 'Two pair',
        7: 'One pair',
        5: 'High card'
        }
    return hand_names[total]


def all_equal(lst):
    """
    Returns True if all elements of lst are the same, False otherwise
    ex.
    all_equal(['S,'S','S']) returns True
    """
    return len(set(lst)) == 1


def isconsecutive(lst):
    """
    Returns True if all numbers in lst can be ordered consecutively, and False otherwise
    """
    return len(set(lst)) == len(lst) and max(lst) - min(lst) == len(lst) - 1


def sort_cards(cards):
    """
    Sorts cards by their rank.
    If rank is a string (e.g., 'A' for Ace), then the rank is changed to a number.
    Cards of the same rank are not sorted by suit.
    ex.
    sort_cards(['AS','3S','4S','5S','JC'])
    returns
    ['3S','4S','5S','11C','14S']
    """
    cards = numeric_ranks(cards)
    rank_list = get_ranks(cards)
    # Keep track of the sorting permutation
    new_order = sorted((e,i) for i,e in enumerate(rank_list))
    unsorted_cards = list(cards)
    for index, (a, b) in enumerate(new_order):
        cards[index] = unsorted_cards[b]
    return cards


def get_best_hand(cards):
    """
    Returns the best hand of five cards, from a larger list of cards.
    If ranks are alphabetical (e.g., A for ace), it will convert the rank to a number.
    ex.
    get_best_hand(['7C', '7S', '2H', '3C', 'AC', 'AD', '5S'])
    returns
    ['5S', '7C', '7S', '14C', '14D']
    """
    # All combinations of 5 cards from the larger list
    all_hand_combos = itertools.combinations(cards, 5)
    hand_name_list = [
        'Invalid hand',
        'High card',
        'One pair',
        'Two pair',
        'Straight',
        'Three of a kind',
        'Full house',
        'Flush',
        'Four of a kind',
        'Straight flush',
        'Royal flush'
        ]
    num_hand_names = len(hand_name_list)
    max_value = 0
    best_hands = {x: [] for x in range(num_hand_names)}
    for combo in all_hand_combos:
        hand = list(combo)
        hand_name = evaluate_hand(hand) # Get the type of hand (e.g., one pair)
        hand_value = hand_name_list.index(hand_name)
        if hand_value >= max_value:
            # Stronger or equal hand has been found
            max_value = hand_value
            best_hands[hand_value].append(hand) # Store hand in dictionary
    max_hand_idx = max(k for k, v in best_hands.items() if len(best_hands[k])>0)
    rank_sum, max_sum = 0, 0
    # The strongest hand type out of the combinations has been found
    for hand in best_hands[max_hand_idx]:
        # Iterate through hands of this strongest type
        ranks = get_ranks(hand)
        rank_sum = sum(ranks)
        if rank_sum > max_sum:
            max_sum = rank_sum
            best_hand = hand # Choose hand with highest ranking cards
    return best_hand

def highest_card_in_draw(hand, my_cards, opp_cards):
    if hand == 'One pair':
        hand = numeric_ranks(my_cards)
        my_ranks = get_ranks(hand)
        mylist = [item for item, count in collections.Counter(my_ranks).items() if count > 1]
        my_value = mylist

        handop = numeric_ranks(opp_cards)
        opp_ranks = get_ranks(handop)
        opplist = [item for item, count in collections.Counter(opp_ranks).items() if count > 1]
        opp_value = opplist

        return my_value, opp_value

    if hand == 'Two pair' or hand == 'Three of a kind':

        hand = numeric_ranks(my_cards)
        my_ranks = get_ranks(hand)
        mylist = [item for item, count in collections.Counter(my_ranks).items() if count > 1]
        my_value = max(mylist)

        handop = numeric_ranks(opp_cards)
        opp_ranks = get_ranks(handop)
        opplist = [item for item, count in collections.Counter(opp_ranks).items() if count > 1]
        opp_value = max(opplist)

        if my_value == opp_value:
            return sum(mylist), sum(opplist)


        return my_value, opp_value

    if  hand == 'Full house':

        hand = numeric_ranks(my_cards)
        my_ranks = get_ranks(hand)
        mylist = [item for item, count in collections.Counter(my_ranks).items() if count > 1]
        my_value = sum(mylist)

        handop = numeric_ranks(opp_cards)
        opp_ranks = get_ranks(handop)
        opplist = [item for item, count in collections.Counter(opp_ranks).items() if count > 1]
        opp_value = sum(opplist)

        return my_value, opp_value

    if hand == 'Straight':
        hand = numeric_ranks(my_cards)
        my_ranks = get_ranks(hand)
        my_value = sum(my_ranks)

        handop = numeric_ranks(opp_cards)
        opp_ranks = get_ranks(handop)
        opp_value = sum(opp_ranks)

        return my_value, opp_value



    else:
        return -1, -1

def main():
    # make a deck of cards
    deck = list(itertools.product([6,7,8,9,10,'J','Q','K','A'],['H','C','D','S']))
    deck2 = ['6H','7H','8H','9H','10H','JH','QH','KH','AH','6C','7C','8C','9C','10C','JC','QC','KC','AC','6D','7D','8D','9D','10D','JD','QD','KD','AD','6S','7S','8S','9S','10S','JS','QS','KS','AS']

    winning_hands = {'Invalid hand': 0, 'High card': 1,'One pair': 2, 'Two pair': 3, 'Straight': 4,'Three of a kind': 5,'Full house':6,'Flush': 7,'Four of a kind': 8,'Straight flush': 9,'Royal flush': 10}
    outfile = open('results_of_games.txt', 'wt')

    matrix = [[' ','A','K','Q','J','T',9,8,7,6],['A',0,0,0,0,0,0,0,0,0],\
    ['K',0,0,0,0,0,0,0,0,0],\
    ['Q',0,0,0,0,0,0,0,0,0],['J',0,0,0,0,0,0,0,0,0],\
    ['T',0,0,0,0,0,0,0,0,0],['9',0,0,0,0,0,0,0,0,0],\
    ['8',0,0,0,0,0,0,0,0,0],['7',0,0,0,0,0,0,0,0,0],\
    ['6',0,0,0,0,0,0,0,0,0]]

    dict = {'A':1,'K':2,'Q':3,'J':4,'1':5,'9':6,'8':7,'7':8,'6':9}

    # for m in matrix:
    #     for i in m:
    #         print(i,end='  ')
    #     print()



    for n in range(6000):
        # shuffle the cards
        random.shuffle(deck2)

        hand = [deck2[0],deck2[1]]
        opponents_cards2 = [deck2[2], deck2[3]]
        cards_at_flop = [deck2[4], deck2[5], deck2[6]]
        table = [deck2[4], deck2[5], deck2[6], deck2[7], deck2[8]]
        turn = [deck2[9],deck[10]]
        river = [deck2[11], deck2[12]]


        my_cards = hand + table
        opponents_cards5 = opponents_cards2 + table
        my_best_hand = get_best_hand(my_cards)
        opponents_best_hand = get_best_hand(opponents_cards5)
        did_i_win = ''


        # print('My Hand:', end=' ')
        # for n in hand:
        #     print(n, end=' ')
        # print('')
        #
        # print('Opponents Hand:', end=' ')
        # for n in opponents_cards2:
        #     print(n, end=' ')
        #
        # print('')
        # print('Cards on table:',end=' ')
        # for n in table:
        #     print(n, end=' ')
        #
        # print('')
        #
        # print('my best hand of five:', end=' ')
        # for n in my_best_hand:
        #     print(n, end=' ')
        #
        # print('')
        #
        # print('opponents best hand of five:', end=' ')
        # for n in opponents_best_hand:
        #     print(n, end=' ')
        #
        # print('')
        #
        # print('My hand : ' + evaluate_hand(my_best_hand))
        # print('Opponents hand : '+evaluate_hand(opponents_best_hand))

        my_hand = evaluate_hand(my_best_hand)
        oppent_hand = evaluate_hand(opponents_best_hand)

        my_highest_card = max(hand)
        opp_highest_card = max(opponents_cards2)

        if winning_hands[my_hand] > winning_hands[oppent_hand]:
            did_i_win = 'win'
        elif my_hand == oppent_hand:
            if my_hand == 'High card':
                if max(hand) > max(opponents_cards2):
                    did_i_win = 'win'
                elif max(hand) == max(opponents_cards2):
                    did_i_win = 'draw'
                else:
                    did_i_win = 'loss'

            else:
                my_value, opp_val = highest_card_in_draw(my_hand, my_best_hand,opponents_best_hand)
                if my_value > opp_val:
                    did_i_win = 'win'
                elif my_value == opp_val:
                    did_i_win = 'draw'
                else:
                    did_i_win = 'loss'


        else:
            did_i_win = 'loss'


        flop_cards = ','.join(cards_at_flop)
        jhand = ','.join(hand)
        print(jhand+' '+did_i_win,file=outfile)

        are_suited = False

        if did_i_win == 'win':

            if jhand[3] == ',':
                if jhand[2] == jhand[5]:
                    num_a = jhand[0]
                    num_b = jhand[4]
                    if num_a > num_b:
                        matrix[dict[num_a]][dict[num_b]] += 1
                    else:
                        matrix[dict[num_b]][dict[num_a]] += 1
                else:

                    num_a = jhand[0]
                    num_b = jhand[4]
                    if num_a > num_b:
                        matrix[dict[num_a]][dict[num_b]] += 1
                    else:
                        matrix[dict[num_b]][dict[num_a]] += 1

            else:
                if jhand[1] == jhand[4]:
                    num_a = jhand[0]
                    num_b = jhand[3]
                    if num_a > num_b:
                        matrix[dict[num_a]][dict[num_b]] += 1
                    else:
                        matrix[dict[num_b]][dict[num_a]] += 1
                else:
                    num_a = jhand[0]
                    num_b = jhand[3]
                    if num_a < num_b:
                        matrix[dict[num_a]][dict[num_b]] += 1
                    else:
                        matrix[dict[num_b]][dict[num_a]] += 1


        if did_i_win == 'loss':
            if jhand[3] == ',':
                if jhand[2] == jhand[5]:
                    num_a = jhand[0]
                    num_b = jhand[4]
                    if num_a > num_b:
                        matrix[dict[num_a]][dict[num_b]] -= 1
                    else:
                        matrix[dict[num_b]][dict[num_a]] -= 1
                else:

                    num_a = jhand[0]
                    num_b = jhand[4]
                    if num_a > num_b:
                        matrix[dict[num_a]][dict[num_b]] -= 1
                    else:
                        matrix[dict[num_b]][dict[num_a]] -= 1

            else:
                if jhand[1] == jhand[4]:
                    num_a = jhand[0]
                    num_b = jhand[3]
                    if num_a > num_b:
                        matrix[dict[num_a]][dict[num_b]] -= 1
                    else:
                        matrix[dict[num_b]][dict[num_a]] -= 1
                else:
                    num_a = jhand[0]
                    num_b = jhand[3]
                    if num_a < num_b:
                        matrix[dict[num_a]][dict[num_b]] -= 1
                    else:
                        matrix[dict[num_b]][dict[num_a]] -= 1

    for idx, m in enumerate(matrix):
        for i in m:
            if isinstance(i,int) and idx > 0:
                if i > 0:
                    print(i,end='\t')
                else:
                    print(0,end='\t')
            else:
                print(i,end='\t')

        print()




    outfile.close()
if __name__=='__main__':main()


#print('My cards {} {}'.format(hand[0],hand[1]))
#print('Opponents cards {}{}, {}{}'.format(opponent[0],opponent[1],opponent[2],opponent[3]))
#print('flop cards {}, {}, {}'.format(table[0],table[1],table[2]))
#print('Turn card {}{}'.format(turn[0],turn[1]))
#print('River card {}{}'.format(river[0],river[1]))
