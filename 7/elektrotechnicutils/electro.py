def count_voltage(i,r):
    return  i*r
def count_current(u,r):
    return u/r
def count_resistance(u,i):
    return u/i
def count_coulomb(q1,q2,r):
    k = 8.9875e9 #coulombs constant
    return k * abs(q1 * q2) / r**2