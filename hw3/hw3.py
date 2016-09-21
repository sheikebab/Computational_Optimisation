import scipy
import matplotlib.pyplot as plt
import pandas

class Parabola:

    # '''Defines  a  function  that  looks  like:
    #
    # f(x) = Summ over i (alpha_i(x_i-c_i)^2) '''

    def __init__(self, alpha, center = 0):
        self.alpha = alpha
        self.center = center
