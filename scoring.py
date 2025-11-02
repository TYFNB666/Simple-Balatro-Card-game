from typing import List, Dict, Tuple, Optional
from cards import Card, Suit, CardType

def ranks_map(cards: List[Card]) -> Dict[str, List[Card]]:
    m = {}
    for c in cards:
        m.setdefault(c.rank, []).append(c)
    return m

def suits_map(cards: List[Card]) -> Dict[Suit, List[Card]]:
    m = {}
    for c in cards:
        m.setdefault(c.suit, []).append(c)
    return m

def rank_value(rank: str) -> int:
    # map rank to numeric value
    if rank == 'A':
        return 14
    if rank == 'K':
        return 13
    if rank == 'Q':
        return 12
    if rank == 'J':
        return 11
    return int(rank)

def top_n(cards: List[Card], n: int) -> List[Card]:
    # pick highest n by points
    return sorted(cards, key=lambda c: c.points, reverse=True)[:n]

# ---------- type checks ----------

def is_pair(rank_counts: Dict[str, int]) -> bool:
    return 2 in rank_counts.values()

def is_two_pair(rank_counts: Dict[str, int]) -> bool:
    # allow >=2 pairs in bigger hands
    count_pair = 0
    for i in rank_counts.values():
        if i == 2:
            count_pair += 1
    return count_pair == 2

def is_three(rank_counts: Dict[str, int]) -> bool:
    return 3 in rank_counts.values()

def is_four(rank_counts: Dict[str, int]) -> bool:
    return 4 in rank_counts.values()

def is_full_house(rank_counts: Dict[str, int]) -> bool:
    counts = sorted(rank_counts.values())
    return counts == [2, 3]

def is_flush(suits: List[Suit]) -> bool:
    return len(suits) >= 5 and len(set(suits)) == 1

def is_straight(values: List[int]) -> bool:
    if len(values) < 5:
        return False
    uniq = sorted(set(values))
    if len(uniq) < 5:
        return False
    # normal
    for i in range(len(uniq) - 4):
        if uniq[i+4] - uniq[i] == 4 and len(set(uniq[i:i+5])) == 5:
            return True
    # wheel (A as 1)
    if 14 in uniq:
        alt = sorted({1 if v == 14 else v for v in uniq})
        for i in range(len(alt) - 4):
            if alt[i+4] - alt[i] == 4 and len(set(alt[i:i+5])) == 5:
                return True
    return False

def is_straight_flush(values: List[int], suits: List[Suit]) -> bool:
    return is_straight(values) and is_flush(suits)

# ---------- pick scoring cards for each type ----------

def pick_four(cards: List[Card]) -> List[Card]:
    rm = ranks_map(cards)
    cands = [r for r, lst in rm.items() if len(lst) >= 4]
    if not cands:
        return []
    r = max(cands, key=rank_value)
    return top_n(rm[r], 4)

def pick_three(cards: List[Card]) -> List[Card]:
    rm = ranks_map(cards)
    cands = [r for r, lst in rm.items() if len(lst) >= 3]
    if not cands:
        return []
    r = max(cands, key=rank_value)
    return top_n(rm[r], 3)

def pick_pairs(cards: List[Card], k: int) -> List[Card]:
    # pick k distinct pairs (highest first)
    rm = ranks_map(cards)
    pair_ranks = sorted([r for r, lst in rm.items() if len(lst) >= 2],key=rank_value, reverse=True)
    if len(pair_ranks) < k:
        return []
    used: List[Card] = []
    for i in range(k):
        used.extend(top_n(rm[pair_ranks[i]], 2))
    return used  # length == 2*k

def pick_full_house(cards: List[Card]) -> List[Card]:
    rm = ranks_map(cards)
    triples = sorted([r for r, lst in rm.items() if len(lst) >= 3],key=rank_value, reverse=True)
    if not triples:
        return []
    t = triples[0]  # best triple
    pair_ranks = sorted([r for r, lst in rm.items() if r != t and len(lst) >= 2],key=rank_value, reverse=True)
    if pair_ranks:
        return top_n(rm[t], 3) + top_n(rm[pair_ranks[0]], 2)
    return []

def best_straight_values(values: List[int]) -> Optional[List[int]]:
    # return the 5 values of the highest straight; else None
    uniq = sorted(set(values))
    # find straight in cards
    for i in range(len(uniq) - 4, -1, -1):
        window = uniq[i:i + 5]
        if window[-1] - window[0] == 4:
            return window
    # 'A' as 1
    if 14 in uniq:
        alt = sorted({1 if v == 14 else v for v in uniq})
        for i in range(len(alt) - 4, -1, -1):
            if alt[i+4] - alt[i] == 4 and len(set(alt[i:i+5])) == 5:
                return alt[i:i+5]
    return None

def pick_straight(cards: List[Card]) -> List[Card]:
    seq = best_straight_values([c.points for c in cards])
    if not seq:
        return []
    chosen = []
    used_vals = set()
    for need in seq:
        if need == 1:
            want = 14
        else:
            want = need
        for c in sorted(cards, key=lambda x: x.points, reverse=True):
            if c.points == want and want not in used_vals:
                chosen.append(c)
                used_vals.add(want)
                break
    if len(chosen) == 5:
        return chosen
    else:
        return []

def pick_flush(cards: List[Card]) -> List[Card]:
    sm = suits_map(cards)
    best_suit = None
    best_sum = -1
    for s, lst in sm.items():
        if len(lst) >= 5:
            five = top_n(lst, 5)
            ssum = sum(c.points for c in five)
            if ssum > best_sum:
                best_sum = ssum
                best_suit = s
    return top_n(sm[best_suit], 5) if best_suit is not None else []

def pick_straight_flush(cards: List[Card]) -> List[Card]:
    sm = suits_map(cards)
    best = []
    best_top = -1
    for s, lst in sm.items():
        if len(lst) < 5:
            continue
        seq = best_straight_values([c.points for c in lst])
        if not seq:
            continue
        got = []
        used_vals = set()
        for need in seq:
            want = 14 if need == 1 else need
            for c in sorted(lst, key=lambda x: x.points, reverse=True):
                if c.points == want and want not in used_vals:
                    got.append(c)
                    used_vals.add(want)
                    break
        if len(got) == 5:
            top_val = max(v if v != 1 else 5 for v in seq)
            if top_val > best_top:
                best_top = top_val
                best = got
    return best

# ---------- evaluate ----------

def evaluate_hand(cards: List[Card]) -> Tuple[str, int, int, List[Card]]:
    if not cards:
        return ("Empty", 0, 0, [])

    suits = [c.suit for c in cards]
    ranks = [c.rank for c in cards]
    rank_counts = {}
    for r in ranks:
        rank_counts[r] = rank_counts.get(r, 0) + 1
    values = sorted(c.points for c in cards)

    if is_straight_flush(values, suits):
        picked = pick_straight_flush(cards)
        if picked:
            name, base, mult = CardType.STRAIGHT_FLUSH
            return (name, base, mult, picked)

    if is_four(rank_counts):
        picked = pick_four(cards)
        if picked:
            name, base, mult = CardType.FOUR
            return (name, base, mult, picked)

    if is_full_house(rank_counts):
        picked = pick_full_house(cards)
        if picked:
            name, base, mult = CardType.FULL_HOUSE
            return (name, base, mult, picked)

    if is_flush(suits):
        picked = pick_flush(cards)
        if picked:
            name, base, mult = CardType.FLUSH
            return (name, base, mult, picked)

    if is_straight(values):
        picked = pick_straight(cards)
        if picked:
            name, base, mult = CardType.STRAIGHT
            return (name, base, mult, picked)

    if is_three(rank_counts):
        picked = pick_three(cards)
        if picked:
            name, base, mult = CardType.THREE
            return (name, base, mult, picked)

    if is_two_pair(rank_counts):
        picked = pick_pairs(cards, 2)
        if picked:
            name, base, mult = CardType.TWO_PAIR
            return (name, base, mult, picked)

    if is_pair(rank_counts):
        picked = pick_pairs(cards, 1)
        if picked:
            name, base, mult = CardType.PAIR
            return (name, base, mult, picked)

    # high card: only the highest one
    top1 = top_n(cards, 1)
    name, base, mult = CardType.HIGH_CARD
    return (name, base, mult, top1)
