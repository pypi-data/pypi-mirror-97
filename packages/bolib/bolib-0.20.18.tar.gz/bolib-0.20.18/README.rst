
BOlib
=====

A python library for Bayesian Optimization.

Setup BOlib
-----------

- Create and activate virtualenv (for python2) or
  venv (for python3)

.. code-block:: bash

  # for python3
  python3 -m venv .env
  # or for python2
  python2 -m virtualenv .env

  source .env/bin/activate

- Upgrade pip

.. code-block:: bash

  python -m pip install --upgrade pip

- Install BOlib package

.. code-block:: bash

  python -m pip install bolib

- Matplotlib requires to install a backend to work interactively
  (See https://matplotlib.org/faq/virtualenv_faq.html).
  The easiest solution is to install the Tk framework,
  which can be found as python-tk (or python3-tk) on
  certain Linux distributions.


Use BOlib
---------

- Import BOlib to use it in your python script.

.. code-block:: python

  import bolib

- Some well-known objetive functions have been included.

.. code-block:: python

  of = bolib.ofs.Branin()

  of.evaluate([1.0, 1.0])  # 27.702905548512433

- To use Bayesian Optimization we need a probabilistic model. In this example we will use Gaussian Processes.

.. code-block:: python

  import gplib

  model = gplib.GP(
      mean_function=gplib.mea.Fixed(),
      covariance_function=gplib.ker.SquaredExponential(ls=([1.] * of.d))
  )

  metric = gplib.me.LML()

  fitting_method = gplib.fit.MultiStart(
      obj_fun=metric.fold_measure,
      max_fun_call=300,
      nested_fit_method=gplib.fit.LocalSearch(
          obj_fun=metric.fold_measure,
          max_fun_call=75,
          method='Powell'
      )
  )

  validation = gplib.dm.Full()

- Bayesian Optimization also needs an acquisition function.

.. code-block:: python

  af = bolib.afs.ExpectedImprovement()

- Finally, we can initialize our optimization model and start the optimization process.

.. code-block:: python

  bo = bolib.methods.BayesianOptimization(
      model, fitting_method, validation, af
  )

  bo.set_seed(seed=1)

  x0 = bo.random_sample(of.get_bounds(), batch_size=10)

  bo.minimize(
      of.evaluate, x0,
      bounds=of.get_bounds(),
      tol=1e-5,
      maxiter=of.get_max_eval(),
      disp=True
  )

- BOlib is also Scipy compatible.

.. code-block:: python

  import scipy.optimize as spo

  bo.set_seed(seed=1)

  x0 = bo.random_sample(of.get_bounds(), batch_size=5)

  result = spo.minimize(
      of.evaluate,
      x0,
      bounds=of.get_bounds(),
      method=bo.minimize,
      tol=1e-5,
      options={
          'maxiter': of.get_max_eval(),
          'disp': True
      }
  )

- There are more examples in examples/ directory. Check them out!

Develop BOlib
-------------

-  Download the repository using git

.. code-block:: bash

  git clone https://gitlab.com/ibaidev/bolib.git
  cd bolib
  git config user.email 'MAIL'
  git config user.name 'NAME'
  git config credential.helper 'cache --timeout=300'
  git config push.default simple

-  Update API documentation

.. code-block:: bash

  source ./.env/bin/activate
  pip install Sphinx
  cd docs/
  sphinx-apidoc -f -o ./ ../bolib
