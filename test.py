from Crypto.Util.number import getPrime
from lcg_attack import lcg_attack

class lcg():
    def __init__(self, bits, bigm):
        bit_b = bits
        self.a = getPrime(bits)
        self.x = getPrime(bits)
        if(bigm): bit_b += 5
        self.m = getPrime(bit_b)
        self.c = getPrime(bits)
    
    def next(self,):
        self.a = (self.a * self.x + self.c) % self.m
        return self.a
    
    def getAtr(self, ):
        return self.a, self.x, self.m, self.c
    
if __name__ == '__main__':
    case_number = 100
    inc = 0
    prob = 0
    prob_a = 0
    prob_m = 0
    prob_c = 0
    prob_x = 0
    len_lcg = [32, 64, 128, 256]
    for leng in len_lcg:
        for j in range(case_number):
            lcg1 = lcg(leng, True)
            a, x, m, c = lcg1.getAtr()
            datas = []
            for i in range(6):
                datas.append(lcg1.next())
            a_, x_, m_, c_ = lcg_attack.attack(datas)
            inc += 1
            if(a==a_): prob_a += 1
            if(m==m_): prob_m += 1
            if(x==x_): prob_x += 1
            if(c==c_): prob_c += 1
            if(a==a_ and m==m_ and x==x_ and c==c_): prob += 1
    print("Probability:",str(100*prob/inc)+"%")
    print("Probability value of a:",str(100*prob_a/inc)+"%")
    print("Probability value of m:",str(100*prob_m/inc)+"%")
    print("Probability value of x:",str(100*prob_x/inc)+"%")
    print("Probability value of c:",str(100*prob_c/inc)+"%")
    print("Testing process has been closed")