# -*- coding: utf-8 -*-


a = [[0.0, 0.0], [1.0, 0.0]]
b = [0.5, 0.5]
c = [0.0, 1.0]


strings = r'\\begin{array}{c|%s}' % ('c' * len(a[0])) + '\n'
for i in range(len(c)):
    strings += ' & '.join([str(c[i])] + [str(j) for j in a[i]]) + r'\\\\' + '\n'
strings += r'\\hline & ' + ' & '.join([str(j) for j in b])
print(strings)


