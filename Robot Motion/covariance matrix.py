import numpy as np

# X = [-0.8,-0.5,-0.7,-0.4,-0.3,-0.1,0.2,0.4,0.1,0.4]
# Y = [-0.4,-0.3,-1,0,0.2,-0.1,0,-0.4,0,0]

X = [0.9,0.1,0.1,-0.2,-0.1,0.4,0.3,0.9,1.2,1.2]
Y = [0,0.1,0.5,-0.1,0.7,0.6,1,0.6,0.5,1.1]
def covariance(X, Y):
    N = len(X)
    sum_x = 0
    sum_y = 0
    mean_x = 0
    mean_y = 0
    cross_diff = 0
    diff_squqre_x = 0
    diff_squqre_y = 0

    for i in range(len(X)):
        sum_x += X[i]
        sum_y += Y[i]

    mean_x = 1 / N * sum_x
    mean_y = 1 / N * sum_y

    for i in range(len(X)):
        diff_squqre_x += ((X[i] - mean_x) ** 2)
        diff_squqre_y += ((Y[i] - mean_y) ** 2)

    for i in range(len(X)):
        cross_diff += ((X[i] - mean_x) * (Y[i] - mean_y))

    top_left = 1 / N * diff_squqre_x
    cross = 1 / N * cross_diff
    bottom_right = 1 / N * diff_squqre_y

    P = np.array([[top_left, cross],
                  [cross, bottom_right]]) 


    return P

print(covariance(X,Y))
print(np.std(X) ** 2)
print(np.std(Y) ** 2)