# fxy
Just a convenience imports for scientific functions and packages for calculation.

`pip install fxy` to get the import shortcuts.
`pip install fxy[all]` to install all libraries for which the shortcuts exist.

<<<<<<< HEAD
## About
This package may be useful for computing basic things, doing things to emulate Python's capabilities in computational and symbolic mathematics and statistics, so this package will introduce just convenient imports so that one doesn't have to [configure Jupyter notebook profile](https://mindey.com/blog/how_to_set_up_ipython_for_statistics_on_linux), to have those imports every time, and works well as an on-the-go calculator.

This package does not assume versions of the imported packages, it just performs the basic imports, assuming that those namespaces within those packages will exist for a long time to come, so it is _dependencies-agnostic_.
=======
## Usage

- `from fxy.n import *`, if you need just `mpmath`.
- `from fxy.np import *`, if you need just `mpmath` and `matplotlib`.
- `from fxy.ns import *`, if you need just `mpmath` and `sympy`.
- `from fxy.nsp import *`, if you need just `mpmath`, `sympy`, and `matplotlib`.
- `from fxy.nsa import *`, if you need just `mpmath`, `sympy`, `numpy`, `pandas`, `scipy`, `statsmodels`.
- `from fxy.nsap import *`, if you need just `mpmath`, `sympy`, `numpy`, `pandas`, `scipy`, `statsmodels`, and `matplotlib`.
- `from fxy.nsal import *`, if you need just `mpmath`, `sympy`, `numpy`, `pandas`, `scipy`, `statsmodels` and `sklearn`.
- `from fxy.nsalp import *`, if you need just `mpmath`, `sympy`, `numpy`, `pandas`, `scipy`, `statsmodels`, `sklearn`, and `matplotlib`.

## Examples
>>>>>>> 792b56ec8e4d85425003f6a9e754bde6803b7e26

```
# Numeric (mpmath.*)
>>> from fxy.n import * (394 functions)
>>> pi
<pi: 3.14159~>
```

<<<<<<< HEAD
# Symbolic (sympy.*)
>>> from fxy.s import * (915 functions, and "isympy" imports)
>>> f = x**4 - 4*x**3 + 4*x**2 - 2*x + 3
>>> f.subs([(x, 2), (y, 4), (z, 0)])
-1
>>> plot(f)

# Actuarial (np: numpy, pd: pandas, sm: statsmodels.api, st: scipy.stats, scipy, smf: statsmodels.formula.api, statsmodels)
>>> from fxy.a import *
>>> df = pandas.DataFrame({'x': numpy.arange(10), 'y': np.random.random(10)})
=======
```
>>> from fxy.ns import *
>>> expr = x**4 - 4*x**3 + 4*x**2 - 2*x + 3
>>> expr.subs([(x, 2), (y, 4), (z, 0)])
-1
```

```
>>> from fxy.nsa import *
>>> df = pandas.DataFrame({'x': np.arange(10), 'y': np.random.random(10)})
>>>>>>> 792b56ec8e4d85425003f6a9e754bde6803b7e26
>>> df.sum()
x    45.000000
y     4.196558
dtype: float64
```

<<<<<<< HEAD
# Learning (sklearn.* as sklearn)
>>> from fxy.l import *
=======
```
>>> from fxy.nsal import *
>>>>>>> 792b56ec8e4d85425003f6a9e754bde6803b7e26
>>> X = [[0], [1], [2], [3]]
>>> y = [0, 0, 1, 1]
>>> neigh = skl.neighbors.KNeighborsClassifier(n_neighbors=3)
>>> neigh.fit(X, y)
>>> print(neigh.predict([[1.1]]))
[0]
>>> print(neigh.predict_proba([[0.9]]))
[[0.66666667 0.33333333]]
<<<<<<< HEAD

# Plotting (plt, matplotlib)
>>> from fxy.p import *
>>> plt.plot([1, 2, 3, 4])
>>> plt.ylabel('some numbers')
>>> plt.show()
<image>
=======
```

## About
I'm lazy every time importing things I need for computing basic things, doing things to emulate Python's capabilities in computational and symbolic mathematics and statistics, so this package will introduce just convenient imports so that I don't have to set up my Jupyter lab every time, and works well as an on-the-go calculator.

This package does not assume versions of the imported packages, it just performs the basic imports, assuming that those namespaces within those packages will exist for a long time to come, so it is _dependencies-agnostic_.

I often use Python for powerful **math**, importing:

```
from mpmath import *
import matplotlib.pyplot as plt
```

I often use Python to do **calculus**, emulateing **[Maple](https://www.maplesoft.com)** and **[Mathematica](https://www.wolfram.com/mathematica/)**'s functionality:

```
import sympy
from sympy import symbols
x, y = symbols('x y')
```

I often use Python to do **statistics**, emulating **[base-R language](https://www.r-project.org)**, importing:

```
import numpy as np; import numpy
import pandas as pd; import pandas
import scipy.stats as st; import scipy
import statsmodels.api as sm; import statsmodels
import statsmodels.formula.api as smf
```
and [configuring Jupyter notebook profile](https://mindey.com/blog/how_to_set_up_ipython_for_statistics_on_linux), to have those imports...

I often use Python to emulate **[MATLAB](https://www.mathworks.com/products/matlab.html)**'s functionality:

```
import scipy
import scipy.optimize
import scipy.integrate
import scipy.interpolate
>>>>>>> 792b56ec8e4d85425003f6a9e754bde6803b7e26
```

I often collect convenient computations and functions in various fields, like what **[WolframAlpha](https://www.wolframalpha.com)** [does](https://wiki.mindey.com/shared/screens/Screenshot_2021-02-28_06-16-43.png) cataloguing implementations of advanced computations to be reused.

<<<<<<< HEAD

## Usage

`from fxy.n import *`, if you need `mpmath` and plotting.
`from fxy.s import *`, if you need `sympy`, and `matplotlib`.
`from fxy.a import *`, if you need `numpy`, `pandas`, `scipy`, `statsmodels` and `matplotlib`.
`from fxy.p import *`, if you need `matplotlib`.
`from fxy.l import *`, if you need `sklearn.* as sklearn`.
=======
## Explanation

### Basic Math
`from fxy.n[umeric] import *` `<=>` `from mpmath import *; import mpmath`

### Basic Math & Calculus
`from fxy.ns[ymbolic] import *` `<=>` `from fxy.n import *` & `import sympy; exec(sympy.interactive.session.preexec_source)`

(Note: sympy is imported same as if it were run by [isympy](https://linux.die.net/man/1/isympy) command.)

### Basic Math & Statistics
`from fxy.nsa[ctuarial] import *` `<=>` `from fxy.ns import *` &
```
import numpy
import numpy as np
import pandas
import pandas as pd
import scipy
import scipy.stats as st
import statsmodels
import statsmodels.api as sm
import statsmodels.formula.api as smf
```

### Basic Math & Statistics and Machine Learning
`from fxy.nsal[earning] import *` `<=>` `from fxy.nsa import *` & `import sklearn`


### Basic Math & Statistics, and Plotting
`from fxy.__p[lotting] import *` `<=>` `from fxy.__ import *` &
```
import matplotlib.pyplot as plt; import matplotlib
```
>>>>>>> 792b56ec8e4d85425003f6a9e754bde6803b7e26
