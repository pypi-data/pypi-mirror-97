

# Runge–Kutta methods

Runge–Kutta methods are numerical methods for solving first-order ordinary differential equations ofthe form
$$
y^{\prime}(x)=f(t, y(x))
$$


A Butcher table has the form
$$
\begin{array}{c|cccc}
c_{1} & a_{1,1} & a_{1,2} & \ldots & a_{1, s} \\
c_{2} & a_{2,1} & a_{2,2} & \ldots & a_{2, s} \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
c_{s} & a_{s, 1} & a_{s, 2} & \cdots & a_{s, s} \\
\hline & b_{1} & b_{2} & \ldots & b_{s}
\end{array}
$$
and is a simple mnemonic device for specifying a Runge–Kutta method (One often also wants to demand that $c_{i}=\sum_{j=1}^{s} a_{i, j}$).
$$
y_{n+1}=y_{n}+h\sum_{i=1}^{s} b_{i} k_{i}
$$
where, for $1 \leq i \leq s$,
$$
k_{i}=h f\left(x_{n}+c_{i} h, y_{n}+\sum_{j=1}^{s} a_{i, j} k_{j}\right)
$$
Observe that the *explicit* methods are precisely those for which the only non-zero entries in the $𝑎_{𝑖,𝑗}$-part of the table lie strictly below the diagonal. Entries at or above the diagonal will cause the right hand side of equation (1) to involve $𝑦_{𝑛+1}$, and so give an *implicit* method (verify this for yourself).

The four Runge–Kutta methods we have covered have Butcher tables as follows. Verify for yourself thatthe tables give formulas in agreement with Kreyszig!

- Euler’s method (explicit)

$$
\begin{array}{l|l}
0 & 0 \\
\hline & 1
\end{array}
$$

- mproved Euler’s method (Heun’s method) (explicit):

$$
\begin{array}{c|cc}
0 & 0 & 0 \\
1 & 1 & 0 \\
\hline & 1 / 2 & 1 / 2
\end{array}
$$

- K4 (explicit):

$$
\begin{array}{c|cccc}
0 & 0 & 0 & 0 & 0 \\
1 / 2 & 1 / 2 & 0 & 0 & 0 \\
1 / 2 & 0 & 1 / 2 & 0 & 0 \\
1 & 0 & 0 & 1 & 0 \\
\hline & 1 / 6 & 1 / 3 & 1 / 3 & 1 / 6
\end{array}
$$

- ackwards Euler’s method (implicit):

$$
\begin{array}{l|l}
1 & 1 \\
\hline & 1
\end{array}
$$





