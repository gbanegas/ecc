import random
import math
from itertools import product
from itertools import chain
from thread_sum import ThreadSum

n = 512
N = 500
d = 1233932494 #31 bits
#d = 2654631857752342880925764945
#d = 265463185775234288092201526257649332892133932494809907679736989141210619872096735078276597605954826202148

#d = 13393249480990767973698914121061987209673507827659760595482620214891467806973397091277092174174393961305025200909026701058146674630543302845868229392185528

q = 2**252 + 27742317777372353535851937790883648493 #ed25519

#temp = int("8335dc163bb124b65129c96fde933d8d723a70aadc873d6d54a7bb0d", 16)
#q = 2^446 + 13818066809895115352007386748515426880336692474882178609894547503885 #Ed448-Goldilocks


window_size = 5
RANDOMIZED_BITS = 32
RANDOMIZE_V_0 = 1
r = []
v = []
alpha = []



def generate_v_values():
    for i in xrange(0, N):
        value = d + (alpha[i]*q)
        v.append(value)

def  generate_alpha_js():
    for i in xrange(1, N+1):
        al = r[i] - r[0]
        alpha.append(int(math.fabs(al)))

def  generate_r_js():
    for i in xrange(0, N+1):
        a = random.getrandbits(n)
        r.append(int(math.fabs(a)))


def bit_flip_fixed(bit_list, nr_of_changes):
    bit_list_t = bit_list[:]
    pos_list = []
    if len(bit_list) < nr_of_changes:
        raise Exception("Randomized bigger then d+(a*r)")
        print "Lenght: ", len(bit_list)
    print "FIXED: ", nr_of_changes
    #position = len(bit_list_t)-1
    for i in xrange(0, nr_of_changes):
        if bit_list_t[i] == 1:
            bit_list_t[i] = 0
        else:
            bit_list_t[i] = 1
        #position = position-1

    return bit_list


def bit_flip_random(bit_list, randomness):
    bit_list_t = bit_list[:]
    pos_list = []
    if len(bit_list) < randomness:
        raise Exception("Randomized bigger then d+(a*r)")
        print "Lenght: ", len(bit_list)
    for i in xrange(0, randomness):
        pos_bit_to_flip = random.randint(0, len(bit_list)-1)
        while(pos_bit_to_flip in pos_list):
            pos_bit_to_flip = random.randint(0, len(bit_list)-1)
        pos_list.append(pos_bit_to_flip)
        if bit_list_t[pos_bit_to_flip] == 1:
            bit_list_t[pos_bit_to_flip] = 0
        else:
            bit_list_t[pos_bit_to_flip] = 1

    return bit_list_t

def generate_v_values_with_bit_flip():
    value = d + (alpha[0]*q)
    bit_list = int_to_bin(value)
    bit_list_flipped = bit_flip_random(bit_list, RANDOMIZE_V_0)
    value_flipped = bin_to_int(bit_list_flipped)
    v.append(value_flipped)
    for i in xrange(1, N):
        value = d + (alpha[i]*q)
        bit_list = int_to_bin(value)
        #print len(bit_list)
        bit_list_flipped = bit_flip_random(bit_list, RANDOMIZED_BITS)
        value_flipped = bin_to_int(bit_list_flipped)
        v.append(value_flipped)

def int_to_bin(number):
    return [int(x) for x in bin(number)[2:]]

def bin_to_int(bit_list):
    output = 0
    for bit in bit_list:
        output = output * 2 + bit
    return output

def groupsof(n, xs):
    if len(xs) < n:
        return [xs]
    else:
        return chain([xs[0:n]], groupsof(n, xs[n:]))

def sum_all_ds(d_candidates, interval, mod_value):
    pairs = {}
    number_of_threads = 15
    ds = list(groupsof(len(d_candidates)/number_of_threads, d_candidates))
    threads = []
    for i in xrange(0, number_of_threads):
        threads.append(ThreadSum(i, ds[i], v, alpha, N, mod_value, interval))
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    for t in threads:
        key, d = t.return_result()
        try:
            if pairs[key] <> None:
                val = pairs[key]
                if val.count(1) > d.count(1):
                    pairs[key] = d
        except Exception as e:
            pairs[key] = d
    return min(pairs.keys()) , pairs


def test_d(to_test):
    """ Function to test the candidate to d. In our case, it is a comparasion
    with the original d. However, in a real case could be the ciphered text with the original
    and the candidate"""
    return (d==to_test)

def wide_widow_attack():
    generate_r_js()
    generate_alpha_js()
    generate_v_values_with_bit_flip()
    print "d = ",  int_to_bin(d), " len: ", len(int_to_bin(d))
    print "Starting...."
    w_prime = 0
    w = window_size
    d_prime = 0
    variations = []
    for i in product([0,1], repeat=window_size):
        variations.append(list(i))
    while(w < (n + window_size + window_size)):
        print "w: ", w
        print "w_prime: ", w_prime
        mod_value = 2**w
        d_prime = d_prime % mod_value
        d_prime_bin = int_to_bin(d_prime)
        to_iterate = []
        for variation in variations:
            to_iterate.append(variation+d_prime_bin)
        sum_d , d_candidate = sum_all_ds(to_iterate, w, mod_value)
        d_prime = bin_to_int(d_candidate[sum_d])
        print "sum: ", sum_d, " d_candidate = ", int_to_bin(d_prime)
        w_prime = w
        w = w + window_size

        if test_d(d_prime):
            break

    if (d == d_prime):
        print "FOUND KEY."
        return True
    else:
        print "SORRY"
        return False
    print "Finished."

nr_of_attempts = 10
correct = 0
for i in xrange(0,nr_of_attempts):
    if wide_widow_attack():
        correct = correct + 1

print "Correct: ", correct, " of ", nr_of_attempts
