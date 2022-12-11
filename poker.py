#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from functools import reduce
from itertools import filterfalse, combinations


# -----------------
# Реализуйте функцию best_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. У каждой карты есть масть(suit) и
# ранг(rank)
# Масти: трефы(clubs, C), пики(spades, S), червы(hearts, H), бубны(diamonds, D)
# Ранги: 2, 3, 4, 5, 6, 7, 8, 9, 10 (ten, T), валет (jack, J), дама (queen, Q), король (king, K), туз (ace, A)
# Например: AS - туз пик (ace of spades), TH - дестяка черв (ten of hearts), 3C - тройка треф (three of clubs)

# Задание со *
# Реализуйте функцию best_wild_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. Кроме прочего в данном варианте "рука"
# может включать джокера. Джокеры могут заменить карту любой
# масти и ранга того же цвета, в колоде два джокерва.
# Черный джокер '?B' может быть использован в качестве треф
# или пик любого ранга, красный джокер '?R' - в качестве черв и бубен
# любого ранга.

# Одна функция уже реализована, сигнатуры и описания других даны.
# Вам наверняка пригодится itertools.
# Можно свободно определять свои функции и т.п.
# -----------------
card_order = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
card_rank_value = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                   'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}


def hand_rank(hand):
    """Возвращает значение определяющее ранг 'руки'"""
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return (8, max(ranks, key=lambda x: card_rank_value[x]))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)


def card_ranks(hand):
    """Возвращает список рангов (его числовой эквивалент),
    отсортированный от большего к меньшему"""
    sorted_cards = sorted(hand, key=lambda c: (card_order.index(c[0]), c[1]), reverse=True)
    print(sorted_cards)
    sorted_cards = list(map(lambda x: x[:1], sorted_cards))
    print(sorted_cards)
    return sorted_cards


def flush(hand):
    """Возвращает True, если все карты одной масти"""
    first_card_suit = hand[0][1]
    for card in hand:
        if first_card_suit != card[1]:
            return False
    return True


def straight(ranks):
    """Возвращает True, если отсортированные ранги формируют последовательность 5ти,
    где у 5ти карт ранги идут по порядку (стрит)"""
    card_order_reverse = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    str_card_order = "".join(card_order_reverse)
    ranks = list(map(lambda x: x[:1], ranks))
    str_ranks = "".join(ranks)
    # print("str_ranks=", str_ranks)
    for i in range(len(str_card_order) - 4):
        if str_card_order[i:i+5] in str_ranks:
            return True
    return False


def kind(n, ranks):
    """Возвращает первый ранг, который n раз встречается в данной руке.
    Возвращает None, если ничего не найдено"""
    for rank in ranks:
        calc_ranks = list(filter(lambda x: x == rank, ranks))
        if len(calc_ranks) == n:
            return rank
    return None


def two_pair(ranks):
    """Если есть две пары, то возвращает два соответствующих ранга,
    иначе возвращает None"""
    str_ranks = "".join(ranks)
    rank_list = []
    for rank in str_ranks:
        pair_list = []
        if rank not in rank_list:
            pair_list = list(filter(lambda x: x == rank, str_ranks))
        if len(pair_list) == 2:
            rank_list.append(rank)
        if len(rank_list) == 2:
            return rank_list
    return None


def best_hand(hand):
    """Из "руки" в 7 карт возвращает лучшую "руку" в 5 карт """
    rank = [0]
    current_hand = []
    all_possible_hands = combinations(hand, 5)
    for hand in all_possible_hands:
        current_hand_rank = hand_rank(hand)
        print("current_hand_rank=", current_hand_rank)
        if current_hand_rank[0] > rank[0]:
            rank = current_hand_rank
            current_hand = hand
        elif current_hand_rank[0] == 8 \
                and current_hand_rank[0] == rank[0] \
                and card_rank_value[current_hand_rank[1]] > card_rank_value[rank[1]]:
            rank = current_hand_rank
            current_hand = hand
        elif current_hand_rank[0] == 6 \
                and current_hand_rank[0] == rank[0] \
                and card_rank_value[current_hand_rank[2]] > card_rank_value[rank[2]]:
            rank = current_hand_rank
            current_hand = hand
    print("current_hand=", current_hand)
    print("rank=", rank)
    return current_hand


def best_wild_hand(hand):
    """best_hand но с джокерами"""
    return


def test_best_hand():
    print("test_best_hand...")
    assert (sorted(best_hand("6C 7C 8C 9C TC 5C JS".split()))
            == ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand("TD TC TH 7C 7D 8C 8S".split()))
            == ['8C', '8S', 'TC', 'TD', 'TH'])
    assert (sorted(best_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print('OK')


def test_best_wild_hand():
    print("test_best_wild_hand...")
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print('OK')


if __name__ == '__main__':
    # print(card_ranks("6C 7C 8C 9C TC 5C JS".split()))
    # print(card_ranks("6C 6S 6H 6D TC 5C JS".split()))
    # print(straight(card_ranks("6C 7C 8C 9C TC 5C JS".split())))
    # print(hand_rank("6C 7C 8C 9C TC 5C JS".split()))
    # print(straight(card_ranks("9D 9C TH KC JD QS 7H".split())))
    # print(kind(1, card_ranks("9D 9C TH KC JD QS 7H".split())))
    # print(two_pair(card_ranks("9D 9C KH KC 8D 8S 8H".split())))
    # print(flush("JD".split()))

    # print(best_hand("6C 7C 8C 9C TC QC JC".split()))
    test_best_hand()
    # test_best_wild_hand()
