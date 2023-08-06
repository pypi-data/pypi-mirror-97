# PyMathRender

Pretty rendering method for mathematic functions

## Install

From Pypi:

`py -m pip install PyMathRender`

From GitHub:

`py -m pip install git+https://github.com/donno2048/Maths`

## Use

```py
from PyMathRender import main
main("sum([math.cos(3 ** n * x / 1000) / (3 ** n) for n in range(10)])", Text = r"$\sum_{n=0}^\infty\frac{\cos\left(3^nx\right)}{3^n}$ Is continuous but not differentiable in any point", LineColor = "blue", TextColor = "blue", start = 0, end = 10, step = .001, required = ["math"])
```

Or:

```py
from PyMathRender import main
from math import cos, e, sqrt
def fun(x): return sum([cos(3 ** n * x / 1000) / (e ** (sqrt(3 ** n) - 1)) for n in range(10)])
main(fun, Text = r"$\sum_{n=0}^\infty\frac{\cos\left(3^nx\right)}{e^{-1+\sqrt{3^n}}}$ Is smooth but not analytic in any point", LineColor = "red", TextColor = "red", start = 0, end = 10, step = .001)
```

The first argument is the function (`x` is the variable if you use the string method) - It is the only required argument,

`Text` is the additional text,

`LineColor` is the color of the line plotted, either `blue`, `green`, `red`, `cyan`, `magenta`, `yellow`, `black` or `white`,

`TextColor` is the color of the additional text, same colors as LineColor,

`start`, `end` and `step` are the starting and ending points and the size of the steps between them,

`required` is a list of required packages for the function - needed only using the string method.
