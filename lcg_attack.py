from math import gcd, lcm
from itertools import combinations

# I'm created attack on LCG with minimum known output length is 6 that give probability of 87% on params recovery 
# needed:
# 1. Minimum output leng is 6
# 2. m must be the biggest value than m, x, c
# 3. if needed number 2 not filled, the accurate will drop but also can solve with some probability
# 4. Increase the output length will increase probability also
# created by: @wondPing in 2023
class lcg_attack:
    def eliminationB(self, x,y):
        x1,x2,x3 = x
        y1,y2,y3 = y
        # the rules is coefisien b is 1
        assert x2 == 1 and y2 == 1
        ret_a = x1-y1
        ret_out = x3-y3
        return (ret_a, ret_out)

    def eliminationA(self, x,y):
        x1,x2 = x
        y1,y2 = y
        # find the correspodensi Mod * k
        common_modulus = lcm(x1,y1)
        x2 = (common_modulus//x1) * x2
        y2 = (common_modulus//y1) * y2
        ret_out = x2-y2
        return ret_out

    def convert(self, datas):
        ret = []
        for i in range(len(datas)-1):
            ret.append((datas[i], 1, datas[i+1]))
        return ret

    def gcdOnList(self, datas):
        ret = datas[0]
        for i in datas[1:]:
            ret = gcd(ret, i)
        return ret
    
    def getXFromList(self, datas, m):
        for coefA0, coefA1 in datas:
            if(gcd(coefA0, m)==1):
                return (pow(coefA0, -1, m) * coefA1) % m
        return 1
    
    def getCFromList(self, datas, m, x):
        coefA0, coef, coefA1 = datas
        return (coefA1-coefA0*x)%m
    
    def getA(self, datas, m, x, c):
        coefA0, coef, coefA1 = datas
        if(gcd(x, m)!=1): return 1
        return ((coefA0-c)*pow(x, -1, m))%m


    @staticmethod
    def attack(output):
        attack_lcg = lcg_attack()
        data = attack_lcg.convert(output)
        leng = len(data)
        # I think i will make array of elimination
        el_b = [attack_lcg.eliminationB(data[i],data[j]) for i,j in combinations([_ for _ in range(leng)], 2)]
        el_a = [attack_lcg.eliminationA(el_b[i],el_b[j]) for i,j in combinations([_ for _ in range(leng)], 2)]
        # getting modulus
        m = attack_lcg.gcdOnList(el_a)
        x = attack_lcg.getXFromList(el_b, m)
        c = attack_lcg.getCFromList(data[0], m, x)
        a = attack_lcg.getA(data[0], m, x, c)
        return a, x, m, c




