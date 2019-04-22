from datasketch import MinHash, MinHashLSH

a = "7690,7691,7692,7693,7694,7695,7698,7701,7703,7704,7707,7709,7710,7712,7713,7716,7718,7720,7721,7723,7724,7726,7728,7729,7731,7732,7734,7735,7736,7740,7745,7747,7748,7749,7751,7752,7753,7754,7755,7756,7757,7758,7759,7761,7762,7765,7766,7767,7769,7770,7771,7776,7779,7780,7789,7792"
b = "7690,7691,7692,7693,7694,7695,7698,7701,7703,7704,7707,7709,7710,7712,7713,7716,7718,7720,7721,7723,7724,7726,7728,7729,7731,7732,7734,7735,7736,7740,7745,7747,7748,7749,7751,7752,7753,7754,7755,7756,7757,7758,7759,7761,7762,7765,7766,7767,7769,7770,7771,7776,7779,7780,7789,7792,7817"

c = "374,378,381,384,386,387,388,390,392,393,394,396,397,402,403,404"
dd = "374,378,381,384,385,386,387,388,390,392,393,394,396,397,402,403,404"

e = "7994,7995,7996,7999,8000,8001,8002,8004"
f = "7010,7011,7012,7013,7014,7015,7016,7017,7019,7020,7021,7025,7026,7028,7030,7035,7038,7039,7042"


m1 = MinHash(num_perm=128)
m2 = MinHash(num_perm=128)
m3 = MinHash(num_perm=128)
m4 = MinHash(num_perm=128)
m5 = MinHash(num_perm=128)
m6 = MinHash(num_perm=128)
for d in set(a.split(',')):
    m1.update(d.encode('utf8'))
for d in set(b.split(',')):
    m2.update(d.encode('utf8'))
for d in set(c.split(',')):
    m3.update(d.encode('utf8'))
for d in set(dd.split(',')):
    m4.update(d.encode('utf8'))
for d in set(e.split(',')):
    m5.update(d.encode('utf8'))
for d in set(f.split(',')):
    m6.update(d.encode('utf8'))


lsh = MinHashLSH(threshold=0.5, num_perm=128)
lsh.insert("m1", m1)
lsh.insert("m2", m2)
lsh.insert("m3", m3)
lsh.insert("m4", m4)
# lsh.insert("m5", m5)
lsh.insert("m6", m6)

result = lsh.query(m5)
print("Approximate neighbours with Jaccard similarity > 0.5", result)