import algorithm

print(algorithm.find_cds(
    {
        0: {3},
        1: {2, 3},
        2: {1},
        3: {1, 0},
    }
))

#
# 0 ----- 3 <-
#         |
#         |
# 2 ----- 1 <-
# answer is {1, 3}
#
