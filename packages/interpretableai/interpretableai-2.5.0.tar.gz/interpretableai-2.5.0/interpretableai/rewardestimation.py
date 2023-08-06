from .iai import _IAI, _requires_iai_version, _iai_version_less_than
from .iaibase import (SupervisedLearner, ClassificationLearner,
                      RegressionLearner, GridSearch)
import warnings as _warnings


class CategoricalRewardEstimationLearner(SupervisedLearner):
    """Abstract type encompassing all learners for reward estimation with
    categorical treatments."""

    def fit_predict(self, *args, **kwargs):
        """Fit a reward estimation model on features `X`, treatments
        `treatments`, and outcomes `outcomes`, and return predicted
        counterfactual rewards for each observation along with the scores of
        the internal estimators during training.

        Julia Equivalent:
        `IAI.fit_predict! <https://docs.interpretable.ai/v2.1.0/RewardEstimation/reference/#IAI.fit_predict!-Tuple%7BLearner%7BIAIBase.CategoricalRewardEstimationTask%7D%7D>`

        Examples
        --------
        >>> lnr.fit_predict(X, treatments, outcomes)

        Compatibility
        -------------
        Requires IAI version 2.0 or higher.
        """
        _requires_iai_version("2.0.0", "fit_predict")
        return _IAI.fit_predict_convert(self._jl_obj, *args, **kwargs)

    def predict(self, *args, **kwargs):
        """Return counterfactual rewards estimated by the learner for each
        observation in the data given by `X`, `treatments` and `outcomes`.

        Julia Equivalent:
        `IAI.predict <https://docs.interpretable.ai/v2.1.0/RewardEstimation/reference/#IAI.predict-Tuple%7BCategoricalRewardEstimator%2CUnion%7BDataFrames.AbstractDataFrame%2C%2520AbstractArray%7Bvar%2522%23s39%2522%2C2%7D%2520where%2520var%2522%23s39%2522%253C%3AReal%7D%7D>`

        Examples
        --------
        >>> lnr.predict(X, treatments, outcomes)

        Compatibility
        -------------
        Requires IAI version 2.0 or higher.
        """
        _requires_iai_version("2.0.0", "predict")
        return _IAI.predict_convert(self._jl_obj, *args, **kwargs)

    def score(self, *args, **kwargs):
        """Calculate the scores of the internal estimators in the learner on
        the data given by `X`, `treatments` and `outcomes`.

        Returns a `Dict` with the following entries:

        - `'propensity'`: the score for the propensity estimator
        - `':outcome'`: a `dict` where the keys are the possible treatments,
                        and the values are the scores of the outcome estimator
                        corresponding to each treatment

        Julia Equivalent:
        `IAI.score <https://docs.interpretable.ai/v2.1.0/RewardEstimation/reference/#IAI.score-Tuple%7BCategoricalRewardEstimator%2CUnion%7BDataFrames.AbstractDataFrame%2C%2520AbstractArray%7Bvar%22%23s39%22%2C2%7D%2520where%2520var%22%23s39%22%3C%3AReal%7D%2CArray%7BT%2C1%7D%2520where%2520T%2CArray%7BT%2C1%7D%2520where%2520T%7D>`

        Examples
        --------
        >>> lnr.score(X, treatments, outcomes)

        Compatibility
        -------------
        Requires IAI version 2.1 or higher.
        """
        _requires_iai_version("2.1.0", "score")
        return _IAI.score_convert(self._jl_obj, *args, **kwargs)


class CategoricalRewardEstimator(CategoricalRewardEstimationLearner):
    """Learner for reward estimation with categorical treatments.

    Julia Equivalent:
    `IAI.CategoricalRewardEstimator <https://docs.interpretable.ai/v2.1.0/RewardEstimation/reference/#IAI.CategoricalRewardEstimator>`

    Examples
    --------
    >>> iai.CategoricalRewardEstimator(**kwargs)

    Parameters
    ----------
    Use keyword arguments to set parameters on the resulting learner. Refer to
    the Julia documentation for available parameters.

    Compatibility
    -------------
    Requires IAI version 2.0 or higher.
    """
    def __init__(self, *args, propensity_estimator=None,
                 outcome_estimator=None, **kwargs):
        _requires_iai_version("2.0.0", "CategoricalRewardEstimator")

        if _iai_version_less_than("2.1.0"):
            jl_obj = _IAI.RewardEstimator_convert(*args, **kwargs)
        else:
            if propensity_estimator:
                lnr = propensity_estimator
                if isinstance(lnr, GridSearch):
                    lnr = lnr.get_learner()
                if not isinstance(lnr, ClassificationLearner):
                    raise TypeError("`propensity_estimator` needs to be a " +
                                    "`ClassificationLearner`")
                propensity_estimator = propensity_estimator._jl_obj

            if outcome_estimator:
                lnr = outcome_estimator
                if isinstance(lnr, GridSearch):
                    lnr = lnr.get_learner()
                if not (isinstance(lnr, ClassificationLearner) or
                        isinstance(lnr, RegressionLearner)):
                    raise TypeError("`outcome_estimator` needs to be a " +
                                    "`ClassificationLearner` or " +
                                    "`RegressionLearner`")
                outcome_estimator = outcome_estimator._jl_obj

            jl_obj = _IAI.CategoricalRewardEstimator_convert(
                *args, propensity_estimator=propensity_estimator,
                outcome_estimator=outcome_estimator, **kwargs)

        super().__init__(jl_obj)


class EqualPropensityEstimator(ClassificationLearner):
    """Learner that estimates equal propensity for all treatments.

    For use with data from randomized experiments where treatments are known to
    be randomly assigned.

    Julia Equivalent:
    `IAI.EqualPropensityEstimator <https://docs.interpretable.ai/v2.1.0/RewardEstimation/reference/#IAI.EqualPropensityEstimator>`

    Examples
    --------
    >>> iai.EqualPropensityEstimator(**kwargs)

    Compatibility
    -------------
    Requires IAI version 2.1 or higher.
    """
    def __init__(self, *args, **kwargs):
        _requires_iai_version("2.1.0", "EqualPropensityEstimator")
        jl_obj = _IAI.EqualPropensityEstimator_convert(*args, **kwargs)
        super().__init__(jl_obj)


class NumericRewardEstimationLearner(SupervisedLearner):
    """Abstract type encompassing all learners for reward estimation with
    numeric treatments."""

    def fit_predict(self, *args, **kwargs):
        """Fit a reward estimation model on features `X`, treatments
        `treatments`, and outcomes `outcomes`, and return predicted
        counterfactual rewards for each observation under each treatment option
        in `treatment_candidates`, as well as the score of the internal outcome
        estimator.

        Julia Equivalent:
        `IAI.fit_predict! <https://docs.interpretable.ai/v2.1.0/RewardEstimation/reference/#IAI.fit_predict!-Tuple%7BLearner%7BIAIBase.NumericRewardEstimationTask%7D%7D>`

        Examples
        --------
        >>> lnr.fit_predict(X, treatments, outcomes, treatment_candidates)

        Compatibility
        -------------
        Requires IAI version 2.1 or higher.
        """
        _requires_iai_version("2.1.0", "fit_predict")
        return _IAI.fit_predict_convert(self._jl_obj, *args, **kwargs)

    def predict(self, *args, **kwargs):
        """Return counterfactual rewards estimated by the learner for each
        observation in the data given by `X` under each treatment option in
        `treatment_candidates`.

        Julia Equivalent:
        `IAI.predict <https://docs.interpretable.ai/v2.1.0/RewardEstimation/reference/#IAI.predict-Tuple%7BNumericRewardEstimator%2CUnion%7BDataFrames.AbstractDataFrame%2C%2520AbstractArray%7Bvar%22%23s39%22%2C2%7D%2520where%2520var%22%23s39%22%3C%3AReal%7D%2CArray%7BT%2C1%7D%2520where%2520T%7D>`

        Examples
        --------
        >>> lnr.predict(X, treatment_candidates)

        Compatibility
        -------------
        Requires IAI version 2.1 or higher.
        """
        _requires_iai_version("2.1.0", "predict")
        return _IAI.predict_convert(self._jl_obj, *args, **kwargs)

    def score(self, *args, **kwargs):
        """Calculate the scores of the internal estimator in the learner on
        the data given by `X`, `treatments` and `outcomes`.

        Julia Equivalent:
        `IAI.score <https://docs.interpretable.ai/v2.1.0/RewardEstimation/reference/#IAI.score-Tuple%7BNumericRewardEstimator%2CUnion%7BDataFrames.AbstractDataFrame%2C%2520AbstractArray%7Bvar%22%23s39%22%2C2%7D%2520where%2520var%22%23s39%22%3C%3AReal%7D%2CArray%7BT%2C1%7D%2520where%2520T%2CArray%7BT%2C1%7D%2520where%2520T%7D>`

        Examples
        --------
        >>> lnr.score(X, treatments, outcomes)

        Compatibility
        -------------
        Requires IAI version 2.1 or higher.
        """
        _requires_iai_version("2.1.0", "score")
        return _IAI.score_convert(self._jl_obj, *args, **kwargs)


class NumericRewardEstimator(NumericRewardEstimationLearner):
    """Learner for reward estimation with numeric treatments.

    Julia Equivalent:
    `IAI.NumericRewardEstimator <https://docs.interpretable.ai/v2.1.0/RewardEstimation/reference/#IAI.NumericRewardEstimator>`

    Examples
    --------
    >>> iai.NumericRewardEstimator(**kwargs)

    Parameters
    ----------
    Use keyword arguments to set parameters on the resulting learner. Refer to
    the Julia documentation for available parameters.

    Compatibility
    -------------
    Requires IAI version 2.1 or higher.
    """
    def __init__(self, *args, outcome_estimator=None, **kwargs):
        _requires_iai_version("2.1.0", "NumericRewardEstimator")

        if outcome_estimator:
            lnr = outcome_estimator
            if isinstance(lnr, GridSearch):
                lnr = lnr.get_learner()
            if not (isinstance(lnr, ClassificationLearner) or
                    isinstance(lnr, RegressionLearner)):
                raise TypeError("`outcome_estimator` needs to be a " +
                                "`ClassificationLearner` or " +
                                "`RegressionLearner`")
            outcome_estimator = outcome_estimator._jl_obj

        jl_obj = _IAI.NumericRewardEstimator_convert(
            *args, outcome_estimator=outcome_estimator, **kwargs)
        super().__init__(jl_obj)


def all_treatment_combinations(*args, **kwargs):
    """Return a `pandas.DataFrame` containing all treatment combinations of one
    or more treatment vectors, ready for use as `treatment_candidates` in
    `fit_predict!` or `predict`.

    Examples
    --------
    >>> iai.all_treatment_combinations(*args, **kwargs)

    Compatibility
    -------------
    Requires IAI version 2.1 or higher.
    """
    _requires_iai_version("2.1.0", "all_treatment_combinations")
    return _IAI.all_treatment_combinations_convert(*args, **kwargs)


def convert_treatments_to_numeric(*args, **kwargs):
    """Convert `treatments` from symbol/string format into numeric values.

    Examples
    --------
    >>> iai.convert_treatments_to_numeric(treatments)

    Compatibility
    -------------
    Requires IAI version 2.1 or higher.
    """
    _requires_iai_version("2.1.0", "convert_treatments_to_numeric")
    return _IAI.convert_treatments_to_numeric_convert(*args, **kwargs)


# DEPRECATED


class RewardEstimationLearner(CategoricalRewardEstimationLearner):
    """Abstract type encompassing all learners for reward estimation with
    categorical treatments.

    This class was deprecated and renamed to CategoricalRewardEstimationLearner
    in interpretableai 2.3.0. This is for consistency with the IAI v2.1.0 Julia
    release.
    """


class RewardEstimator(CategoricalRewardEstimator, RewardEstimationLearner):
    """Learner for reward estimation with categorical treatments.

    This class was deprecated and renamed to CategoricalRewardEstimator in
    interpretableai 2.3.0. This is for consistency with the IAI v2.1.0 Julia
    release.
    """
    def __init__(self, *args, **kwargs):
        _warnings.warn(
            "'RewardEstimator' is deprecated, use " +
            "'CategoricalRewardEstimator'",
            FutureWarning
        )
        super().__init__(*args, **kwargs)
