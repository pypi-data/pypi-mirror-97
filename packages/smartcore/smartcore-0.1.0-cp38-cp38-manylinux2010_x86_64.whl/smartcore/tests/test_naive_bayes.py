import numpy as np
from smartcore.naive_bayes import BernoulliNB, CategoricalNB, GaussianNB, MultinomialNB
from sklearn.datasets import load_iris
from sklearn.utils._testing import assert_array_equal
from sklearn.utils._testing import assert_array_almost_equal
from sklearn.naive_bayes import BernoulliNB as SklearnBernoulliNB
from sklearn.naive_bayes import GaussianNB as SklearnGaussianNB


# Data is just 6 separable points in the plane
X = np.array([[-2, -1], [-1, -1], [-1, -2], [1, 1], [1, 2], [2, 1]])
y = np.array([1, 1, 1, 2, 2, 2])

# A bit more random tests
rng = np.random.RandomState(0)
X1 = rng.normal(size=(10, 3))
y1 = (rng.normal(size=(10)) > 0).astype(int)

# Data is 6 random integer points in a 100 dimensional space classified to
# three classes.
X2 = rng.randint(5, size=(6, 100))
y2 = np.array([1, 1, 2, 2, 3, 3])


def test_gnb():
    # Gaussian Naive Bayes classification.
    # This checks that GaussianNB implements fit and predict and returns
    # correct values for a simple toy dataset.

    clf = GaussianNB()
    clf.fit(X, y)
    y_pred = clf.predict(X)
    assert_array_equal(y_pred, y)


def test_gnb_prior():
    # Test whether class priors are properly set.
    clf = GaussianNB()
    clf.fit(X, y)
    assert_array_almost_equal(np.array([3, 3]) / 6.0, clf.class_prior_, 8)
    clf = GaussianNB()
    clf.fit(X1, y1)
    # Check that the class priors sum to 1
    assert_array_almost_equal(clf.class_prior_.sum(), 1)


def test_gnb_priors():
    """Test whether the class prior override is properly used"""
    clf = GaussianNB(priors=np.array([0.3, 0.7]))
    clf.fit(X, y)
    assert_array_almost_equal(clf.class_prior_, np.array([0.3, 0.7]))


def test_gnb_priors_sum_isclose():
    # test whether the class prior sum is properly tested"""
    X = np.array(
        [
            [-1, -1],
            [-2, -1],
            [-3, -2],
            [-4, -5],
            [-5, -4],
            [1, 1],
            [2, 1],
            [3, 2],
            [4, 4],
            [5, 5],
        ]
    )
    priors = np.array([0.08, 0.14, 0.03, 0.16, 0.11, 0.16, 0.07, 0.14, 0.11, 0.0])
    Y = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    clf = GaussianNB(priors=priors)
    # smoke test for issue #9633
    clf.fit(X, Y)


def test_gnb_naive_bayes_scale_invariance():
    # Scaling the data should not change the prediction results
    iris = load_iris()
    X, y = iris.data, iris.target
    labels = []
    for f in [1e-10, 1, 1e10]:
        clf = GaussianNB()
        clf.fit(f * X, y)
        labels += [clf.predict(f * X)]
    assert_array_equal(labels[0], labels[1])
    assert_array_equal(labels[1], labels[2])


def test_gnb_scikit_parity():
    """
    Test that checks parity with scikit GaussianNB class
    """
    clf = GaussianNB()
    clf.fit(X, y)

    clf_sk = SklearnGaussianNB()
    clf_sk.fit(X, y)

    attribute_names = ["classes_", "class_count_", "class_prior_", "sigma_", "theta_"]

    for attribute_name in attribute_names:
        attribute = getattr(clf, attribute_name)
        attribute_sk = getattr(clf_sk, attribute_name)
        assert_array_almost_equal(attribute, attribute_sk)


def test_mnnb():
    # Test Multinomial Naive Bayes classification.
    # This checks that MultinomialNB implements fit and predict and returns
    # correct values for a simple toy dataset.

    X = X2

    # Check the ability to predict the learning set.
    clf = MultinomialNB()
    clf.fit(X, y2)
    y_pred = clf.predict(X)
    assert_array_equal(y_pred, y2)


def test_bnb():
    # Tests that BernoulliNB when alpha=1.0 gives the same values as
    # those given for the toy example in Manning, Raghavan, and
    # Schuetze's "Introduction to Information Retrieval" book:
    # https://nlp.stanford.edu/IR-book/html/htmledition/the-bernoulli-model-1.html

    # Training data points are:
    # Chinese Beijing Chinese (class: China)
    # Chinese Chinese Shanghai (class: China)
    # Chinese Macao (class: China)
    # Tokyo Japan Chinese (class: Japan)

    # Features are Beijing, Chinese, Japan, Macao, Shanghai, and Tokyo
    X = np.array(
        [[1, 1, 0, 0, 0, 0], [0, 1, 0, 0, 1, 0], [0, 1, 0, 1, 0, 0], [0, 1, 1, 0, 0, 1]]
    )

    # Classes are China (0), Japan (1)
    Y = np.array([0, 0, 0, 1])

    # Fit BernoulliBN w/ alpha = 1.0
    clf = BernoulliNB(alpha=1.0)
    clf.fit(X, Y)

    # Check the feature probabilities are correct
    feature_prob = np.array(
        [
            [0.4, 0.8, 0.2, 0.4, 0.4, 0.2],
            [1 / 3.0, 2 / 3.0, 2 / 3.0, 1 / 3.0, 1 / 3.0, 2 / 3.0],
        ]
    )
    assert_array_almost_equal(np.exp(clf.feature_log_prob_), feature_prob)

    # Testing data point is:
    # Chinese Chinese Chinese Tokyo Japan
    X_test = np.array([[0, 1, 1, 0, 0, 1]])
    y_expected = np.array([1.0])

    Y_pred = clf.predict(X_test)
    assert_array_equal(Y_pred, y_expected)


def test_bnb_feature_log_prob():
    # Test for issue #4268.
    # Tests that the feature log prob value computed by BernoulliNB when
    # alpha=1.0 is equal to the expression given in Manning, Raghavan,
    # and Schuetze's "Introduction to Information Retrieval" book:
    # http://nlp.stanford.edu/IR-book/html/htmledition/the-bernoulli-model-1.html

    X = np.array([[0, 0, 0], [1, 1, 0], [0, 1, 0], [1, 0, 1], [0, 1, 0]])
    Y = np.array([0, 0, 1, 2, 2])

    # Fit Bernoulli NB w/ alpha = 1.0
    clf = BernoulliNB(alpha=1.0)
    clf.fit(X, Y)

    # Manually form the (log) numerator and denominator that
    # constitute P(feature presence | class)
    num = np.log(clf.feature_count_ + 1.0)
    denom = np.tile(np.log(clf.class_count_ + 2.0), (X.shape[1], 1)).T

    # Check manual estimate matches
    assert_array_almost_equal(clf.feature_log_prob_, (num - denom))


def test_bnb_scikit_parity():
    """
    Test that checks parity with scikit GaussianNB class
    """
    clf = BernoulliNB(alpha=2)
    clf.fit(X, y)

    clf_sk = SklearnBernoulliNB(alpha=2)
    clf_sk.fit(X, y)

    attribute_names = [
        "classes_",
        "class_count_",
        "feature_count_",
        "feature_log_prob_",
        "n_features_",
    ]

    for attribute_name in attribute_names:
        attribute = getattr(clf, attribute_name)
        attribute_sk = getattr(clf_sk, attribute_name)
        assert_array_almost_equal(attribute, attribute_sk)


def test_categoricalnb():
    # Check the ability to predict the training set.
    clf = CategoricalNB()
    clf.fit(X2, y2)
    y_pred = clf.predict(X2)
    assert_array_equal(y_pred, y2)
