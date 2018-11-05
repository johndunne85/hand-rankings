import itertools, random

# make a deck of cards
deck = list(itertools.product([6,7,8,9,10,'J','Q','K','A'],['H','C','D','S']))

# shuffle the cards
random.shuffle(deck)
a = str(deck[1][0])
b = str(deck[1][1])
c = str(deck[2][0])
d = str(deck[2][1])
x = a+b
y = c+d

t1 = str(deck[5][0])
t2 = str(deck[5][1])
t3 = str(deck[6][0])
t4 = str(deck[6][1])
t5 = str(deck[7][0])
t6 = str(deck[7][1])
t7 = str(deck[8][0])
t8 = str(deck[8][1])
t9 = str(deck[9][0])
t10 = str(deck[9][1])

ta = t1 + t2
tb = t3 + t4
tc = t5 + t6
td = t7 + t8
te = t9 + t10


hand = [x,y]
opponent = [deck[3][0], deck[3][1],deck[4][0], deck[4][1]]
table = [ta, tb, tc, td, te]
turn = [deck[10][0],deck[10][1]]
river = [deck[11][0], deck[11][1]]


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
        'Three of a kind',
        'Straight',
        'Flush',
        'Full house',
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


cards = hand + table
best_hand = get_best_hand(cards)

print('Hand:', end=' ')
for n in hand:
    print(n, end=' ')

print('')
print('Cards on table:',end=' ')
for n in table:
    print(n, end=' ')

print('')

print('Best hand of five:', end=' ')
for n in best_hand:
    print(n, end=' ')

print('')

print(evaluate_hand(best_hand))


#print('My cards {} {}'.format(hand[0],hand[1]))
#print('Opponents cards {}{}, {}{}'.format(opponent[0],opponent[1],opponent[2],opponent[3]))
#print('flop cards {}, {}, {}'.format(table[0],table[1],table[2]))
#print('Turn card {}{}'.format(turn[0],turn[1]))
#print('River card {}{}'.format(river[0],river[1]))
