# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['niaaml',
 'niaaml.classifiers',
 'niaaml.data',
 'niaaml.fitness',
 'niaaml.preprocessing',
 'niaaml.preprocessing.encoding',
 'niaaml.preprocessing.feature_selection',
 'niaaml.preprocessing.feature_transform',
 'niaaml.preprocessing.imputation',
 'niaaml.tests']

package_data = \
{'': ['*'], 'niaaml.tests': ['tests_files/*']}

install_requires = \
['NiaPy>=2.0.0rc11,<3.0.0',
 'numpy>=1.19.1,<2.0.0',
 'pandas>=1.1.4,<2.0.0',
 'scikit-learn>=0.23.2,<0.24.0']

setup_kwargs = {
    'name': 'niaaml',
    'version': '1.1.1',
    'description': 'Python automated machine learning framework.',
    'long_description': "NiaAML\n======\n\n.. image:: https://travis-ci.com/lukapecnik/NiaAML.svg?branch=master\n    :target: https://travis-ci.com/lukapecnik/NiaAML\n\n.. image:: https://coveralls.io/repos/github/lukapecnik/NiaAML/badge.svg?branch=travisCI_integration\n    :target: https://coveralls.io/github/lukapecnik/NiaAML?branch=travisCI_integration\n\n.. image:: https://img.shields.io/pypi/v/niaaml.svg\n    :target: https://pypi.python.org/pypi/niaaml\n\n.. image:: https://img.shields.io/pypi/pyversions/niaaml.svg\n    :target: https://pypi.org/project/NiaPy/\n\n.. image:: https://img.shields.io/github/license/lukapecnik/niaaml.svg\n    :target: https://github.com/lukapecnik/niaaml/blob/master/LICENSE\n\nNiaAML is an automated machine learning Python framework based on\nnature-inspired algorithms for optimization. The name comes from the\nautomated machine learning method of the same name [1]. Its\ngoal is to efficiently compose the best possible classification pipeline\nfor the given task using components on the input. The components are\ndivided into three groups: feature seletion algorithms, feature\ntransformation algorithms and classifiers. The framework uses\nnature-inspired algorithms for optimization to choose the best set of\ncomponents for the classification pipeline on the output and optimize\ntheir parameters. We use `NiaPy framework <https://github.com/NiaOrg/NiaPy>`_ for the optimization process\nwhich is a popular Python collection of nature-inspired algorithms. The\nNiaAML framework is easy to use and customize or expand to suit your\nneeds.\n\nThe NiaAML framework allows you not only to run full pipeline optimization, but also separate implemented components such as classifiers, feature selection algorithms, etc. **It supports numerical and categorical features as well as missing values in datasets.**\n\n- **Documentation:** https://niaaml.readthedocs.io/en/latest/,\n- **Tested OS:** Windows, Ubuntu, Fedora, Linux Mint and CentOS. **However, that does not mean it does not work on others.**\n\nInstallation\n------------\n\npip\n~~~\n\nInstall NiaAML with pip3:\n\n.. code:: sh\n\n    pip3 install niaaml\n\nIn case you would like to try out the latest pre-release version of the framework, install it using:\n\n.. code:: sh\n\n    pip3 install niaaml --pre\n\nInstall From Source\n~~~~~~~~~~~~~~~~~~~\n\nIn case you want to install directly from the source code, use:\n\n.. code:: sh\n\n    git clone https://github.com/lukapecnik/NiaAML.git\n    cd NiaAML\n    python setup.py install\n\nGraphical User Interface\n------------------------\n\nYou can find a simple graphical user interface for NiaAML package `here <https://github.com/lukapecnik/NiaAML-GUI>`_.\n\nUsage\n-----\n\nSee the project's `repository <https://github.com/lukapecnik/NiaAML>`_ for usage examples.\n\nComponents\n----------\n\nIn the following sections you can see a list of currently implemented \ncomponents divided into groups: classifiers, feature selection \nalgorithms and feature transformation algorithms. At the end you can \nalso see a list of currently implemented fitness functions for the optimization process, \ncategorical features' encoders, and missing values' imputers.\n\nClassifiers\n~~~~~~~~~~~\n\n-  Adaptive Boosting (AdaBoost),\n-  Bagging (Bagging),\n-  Extremely Randomized Trees (ExtremelyRandomizedTrees),\n-  Linear SVC (LinearSVC),\n-  Multi Layer Perceptron (MultiLayerPerceptron),\n-  Random Forest Classifier (RandomForest),\n-  Decision Tree Classifier (DecisionTree),\n-  K-Neighbors Classifier (KNeighbors),\n-  Gaussian Process Classifier (GaussianProcess),\n-  Gaussian Naive Bayes (GaussianNB),\n-  Quadratic Discriminant Analysis (QuadraticDiscriminantAnalysis).\n\nFeature Selection Algorithms\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n-  Select K Best (SelectKBest),\n-  Select Percentile (SelectPercentile),\n-  Variance Threshold (VarianceThreshold).\n\nNature-Inspired\n^^^^^^^^^^^^^^^\n\n-  Bat Algorithm (BatAlgorithm),\n-  Differential Evolution (DifferentialEvolution),\n-  Self-Adaptive Differential Evolution (jDEFSTH),\n-  Grey Wolf Optimizer (GreyWolfOptimizer),\n-  Particle Swarm Optimization (ParticleSwarmOptimization).\n\nFeature Transformation Algorithms\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n-  Normalizer (Normalizer),\n-  Standard Scaler (StandardScaler),\n-  Maximum Absolute Scaler (MaxAbsScaler),\n-  Quantile Transformer (QuantileTransformer),\n-  Robust Scaler (RobustScaler).\n\nFitness Functions based on\n~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n-  Accuracy (Accuracy),\n-  Cohen's kappa (CohenKappa),\n-  F1-Score (F1),\n-  Precision (Precision).\n\nCategorical Feature Encoders\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n- One-Hot Encoder (OneHotEncoder).\n\nFeature Imputers\n~~~~~~~~~~~~~~~~\n\n- Simple Imputer (SimpleImputer).\n\nLicence\n-------\n\nThis package is distributed under the MIT License. This license can be\nfound online at http://www.opensource.org/licenses/MIT.\n\nDisclaimer\n----------\n\nThis framework is provided as-is, and there are no guarantees that it\nfits your purposes or that it is bug-free. Use it at your own risk!\n\nReferences\n----------\n\n[1] Iztok Fister Jr., Milan Zorman, Dušan Fister, Iztok Fister.\nContinuous optimizers for automatic design and evaluation of\nclassification pipelines. In: Frontier applications of nature inspired\ncomputation. Springer tracts in nature-inspired computing, pp.281-301,\n2020.\n",
    'author': 'Luka Pečnik',
    'author_email': 'lukapecnik96@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lukapecnik/NiaAML',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
