def count_rating(num_rating, old_avg, new_rating):
    old_total = old_avg*num_rating
    new_num = num_rating + 1
    new_avg = (old_total + new_rating)/(new_num)
    return new_num, new_avg