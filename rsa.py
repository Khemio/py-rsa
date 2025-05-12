import random

def euclid(a, b):
    if b == 0:
        return a
    r = a % b
    return euclid(b, r)

def ext_euclid(a,b):
    x0,x1,y0,y1,s = 1,0,0,1,1
    while b!=0:
        r = a % b
        q = a // b
        a = b
        b = r
        x = x1
        y = y1
        x1 = q*x1 + x0
        y1 = q*y1+ y0
        x0,y0= x,y
        s = -s
    x=s*x0
    y=-s*y0
    d,x,y = a,x,y
    return(d,x,y)

def mod_exp(base, exp, mod):
    base = base % mod
    if exp == 0:
        return 1
    elif exp == 1:
        return base
    elif exp % 2 == 0:
        return mod_exp(base*base%mod,exp/2, mod)
    else:
        return base*mod_exp(base,exp-1,mod)%mod


def is_prime_mr(n):
    num_of_tests = 5  # number of rounds
    if n < 2:
        return False
    # If the number is 2 (only one even prime number)
    if n == 2:
        return True
    # n definitely an odd number
    if n % 2 == 0:
        return False

    # division with two without remainder
    s = 0
    d = n - 1
    while True:
        quotient, remainder = divmod(d, 2)
        if remainder == 1:
            break

        s += 1
        d = quotient

    # assert ((2 ** s) * d == n - 1)

    # primetest( a^d, a^((2^i)*d) )
    def try_composite(a):
        if mod_exp(a, d, n) == 1:
            return False
        for i in range(s):
            if mod_exp(a, (2 ** i) * d, n) == n - 1:
                return False
        return True  # n is a composite number

    for _ in range(num_of_tests):
        a = random.randrange(2, n)
        if try_composite(a):
            return False
    # n is a possible prime
    return True

def chinese_rem(c, m1_q, m2_p, d, m_n):
    c1 = mod_exp(c, (d % (m2_p - 1)), m2_p)
    c2 = mod_exp(c, (d % (m1_q - 1)), m1_q)
    g, y2, y1 = ext_euclid(m2_p, m1_q)
    return ((c1 * y1 * m1_q) + (c2 * y2 * m2_p)) % m_n



def main():

    p = random.randint(1000, 100000)
    while not is_prime_mr(p):
        p = random.randint(1000, 100000)
    q = random.randint(1000, 100000)
    while not is_prime_mr(q) or q == p:
        q = random.randint(1000, 100000)
    n = p * q
    phi = (p-1)*(q-1)
    e = random.randint(2, phi - 1)
    while not (euclid(e, phi) == 1):
        e = random.randint(2, phi - 1)
    _, x, _ = ext_euclid(e,phi)
    d = (x % phi + phi) % phi

    m = 71331513
    # c = mod_exp(m,e,n)
    c = chinese_rem(m,q,p,e,n)
    # dec = mod_exp(c,d,n)
    dec = chinese_rem(c, q, p, d, n)

    print(m)
    print(c)
    print(dec)

    # sig = chinese_rem(m,q,p,d,n)
    # m1 = chinese_rem(sig,q,p,e,n)
    sig = mod_exp(m, d, n)
    m1 = mod_exp(sig,e,n)
    print(m == m1)

if __name__ == "__main__":
    main()