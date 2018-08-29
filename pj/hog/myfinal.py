if six_sided:
        is_six_sided = True
    else:
        is_six_sided = False


    score_with_bacon = free_bacon(opponent_score)

    if score < opponent_score:
        if is_swap(total_score_with_bacon, opponent_score):
            return 0
        elif is_swap(score + 1, opponent_score):
            return 10
        elif is_perfect_piggy(free_bacon(opponent_score)) and is_six_sided:
            is_six_sided = False
            return 0
        elif free_bacon(opponent_score) >= 8:
            return 0
        else:
            if is_six_sided:
                return 4
            else:
                return 0
    else:
        if total_score_with_bacon >= 100 and not is_swap(total_score_with_bacon, opponent_score):
            return 0
        elif is_swap(score + 1, opponent_score):
            return 0
        elif free_bacon(opponent_score) >= 8:
            return 0
        elif is_perfect_piggy(free_bacon(opponent_score)) and is_six_sided:
            is_six_sided = False
            return 0
        else:
            if is_six_sided:
                return 4
            else:
                return 0