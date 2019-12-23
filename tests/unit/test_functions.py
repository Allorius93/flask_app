from project.helper import count_rating
 

def test_rating_counter_1():
    old_num = 2
    old_avg = 3.5
    new_rating = 5
    new_num, new_avg = count_rating(old_num, old_avg, new_rating)
    assert new_num == 3
    assert new_avg == 4

def test_rating_counter_2():
    old_num = 0
    old_avg = 0
    new_rating = 5
    new_num, new_avg = count_rating(old_num, old_avg, new_rating)
    assert new_num == 1
    assert new_avg == 5