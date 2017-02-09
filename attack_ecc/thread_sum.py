import threading

q = 2**255 - 19

def int_to_bin(number):
    return [int(x) for x in bin(number)[2:]]

def bin_to_int(bit_list):
    output = 0
    for bit in bit_list:
        output = output * 2 + bit
    return output

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

class ThreadSum(threading.Thread):

    def __init__(self, threadID, d_list, v_list, alpha_list, N, mod_value, interval):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.d_list = d_list
        self.v = v_list
        self.alpha = alpha_list
        self.N = N
        self.mod_value = mod_value
        self.key = 0
        self.d = []
        self.interval = interval


    def run(self):
        pairs = {}
        for d in self.d_list:
            sum_hw_d = 0
            for j in xrange(0,self.N-1):
                d_prime = bin_to_int(d)+(self.alpha[j]*q) % self.mod_value
                v_j = bin_to_int(self.v[j]) % self.mod_value
                pre_sum = xor_operation(int_to_bin(v_j), int_to_bin(d_prime))[-self.interval:].count(1)
                sum_hw_d = sum_hw_d + pre_sum
            pairs[sum_hw_d] = d
        self.key = min(pairs.keys())
        self.d = pairs[self.key]

    def return_result(self):
        return self.key, self.d