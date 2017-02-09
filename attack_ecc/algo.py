import random
from itertools import product

n = 250
N = 1200
q = 2**255 - 19
window_size = 10
v = []
alpha = []

def generate_v_values():
    for i in xrange(0, N):
        a = random.getrandbits(n)
        v.append(int_to_bin(a))

def  generate_alpha_j():
    for i in xrange(0, N):
        a = random.getrandbits(n)
        alpha.append(a)


def int_to_bin(number):
    return [int(x) for x in bin(number)[2:]]

def bin_to_int(bit_list):
    output = 0
    for bit in bit_list:
        output = output * 2 + bit
    return output

def generate_d_candidates(difference):
    all_combinations = []
    general_zeros = [0]*(n-difference)
    for i in product([0,1], repeat=difference):
        all_combinations.append(list(i)+general_zeros)
    return all_combinations

def xor_operation(v, d):
    #l = [int(x) for x in bin(v)[2:]]
    size_d = len(d)
    complementary = [0]*(size_d-len(v))
    v_list = complementary + v
    result = []
    for j in xrange(0, size_d):
        result.append((v_list[j]+d[j]) % 2)
    #print result
    return result

#TODO create argmin{S(d)}
def sum_all_ds(d_candidates, interval, mod_value):
    pairs = {}
    for d in d_candidates:
        sum_hw_d = 0
        for j in xrange(1,N):
            d_prime = bin_to_int(d)+(alpha[j]*q) % mod_value
            v_j = bin_to_int(v[j]) % mod_value
            pre_sum = xor_operation(int_to_bin(v_j), int_to_bin(d_prime))[-interval:].count(1)
            sum_hw_d = sum_hw_d + pre_sum
        pairs[sum_hw_d] = d
    print pairs.keys()

    return min(pairs.keys()) , pairs



def wide_widow_attack():
    generate_v_values()
    generate_alpha_j()
    print "Starting...."
    w_l = 0
    w = window_size
    d_l = 0


    while(w < n):
        print "Interaction"
        print "w_l ", w_l, " w ", w
        mod_value = 2**w
        d_candidates = generate_d_candidates(w-w_l)
        sum_d , d_candidate = sum_all_ds(d_candidates,w-w_l, mod_value)

        w_l = w
        w = w + window_size

        #print d_candidate

    print "Finished."



wide_widow_attack()
