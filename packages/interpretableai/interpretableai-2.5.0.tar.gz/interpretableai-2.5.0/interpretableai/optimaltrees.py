from .iai import _IAI, _iai_version_less_than, _requires_iai_version
from .iaitrees import (TreeLearner, ClassificationTreeLearner,
                       RegressionTreeLearner, SurvivalTreeLearner,
                       PrescriptionTreeLearner, PolicyTreeLearner)
import warnings as _warnings


class OptimalTreeLearner(TreeLearner):
    """Abstract type encompassing all optimal tree learners."""
    pass


class OptimalTreeClassifier(OptimalTreeLearner, ClassificationTreeLearner):
    """Learner for training Optimal Classification Trees.

    Julia Equivalent:
    `IAI.OptimalTreeClassifier <https://docs.interpretable.ai/v2.1.0/OptimalTrees/reference/#IAI.OptimalTreeClassifier>`

    Examples
    --------
    >>> iai.OptimalTreeClassifier(**kwargs)

    Parameters
    ----------
    Use keyword arguments to set parameters on the resulting learner. Refer to
    the Julia documentation for available parameters.
    """
    def __init__(self, *args, **kwargs):
        jl_obj = _IAI.OptimalTreeClassifier_convert(*args, **kwargs)
        super().__init__(jl_obj)


class OptimalTreeRegressor(OptimalTreeLearner, RegressionTreeLearner):
    """Learner for training Optimal Regression Trees.

    Julia Equivalent:
    `IAI.OptimalTreeRegressor <https://docs.interpretable.ai/v2.1.0/OptimalTrees/reference/#IAI.OptimalTreeRegressor>`

    Examples
    --------
    >>> iai.OptimalTreeRegressor(**kwargs)

    Parameters
    ----------
    Use keyword arguments to set parameters on the resulting learner. Refer to
    the Julia documentation for available parameters.
    """
    def __init__(self, *args, **kwargs):
        jl_obj = _IAI.OptimalTreeRegressor_convert(*args, **kwargs)
        super().__init__(jl_obj)


class OptimalTreeSurvivalLearner(OptimalTreeLearner, SurvivalTreeLearner):
    """Learner for training Optimal Survival Trees.

    Julia Equivalent:
    `IAI.OptimalTreeSurvivalLearner <https://docs.interpretable.ai/v2.1.0/OptimalTrees/reference/#IAI.OptimalTreeSurvivalLearner>`

    Examples
    --------
    >>> iai.OptimalTreeSurvivalLearner(**kwargs)

    Parameters
    ----------
    Use keyword arguments to set parameters on the resulting learner. Refer to
    the Julia documentation for available parameters.
    """
    def __init__(self, *args, **kwargs):
        if _iai_version_less_than("2.0.0"):
            jl_obj = _IAI.OptimalTreeSurvivor_convert(*args, **kwargs)
        else:
            jl_obj = _IAI.OptimalTreeSurvivalLearner_convert(*args, **kwargs)
        super().__init__(jl_obj)


class OptimalTreeSurvivor(OptimalTreeSurvivalLearner):
    """Learner for training Optimal Survival Trees.

    This class was deprecated and renamed to OptimalTreeSurvivalLearner in
    interpretableai 2.0.2. This is for consistency with the IAI v2.0.0 Julia
    release.
    """
    def __init__(self, *args, **kwargs):
        _warnings.warn(
            "'OptimalTreeSurvivor' is deprecated, use " +
            "'OptimalTreeSurvivalLearner'",
            FutureWarning
        )
        super().__init__(*args, **kwargs)


class OptimalTreePrescriptionMinimizer(OptimalTreeLearner,
                                       PrescriptionTreeLearner):
    """Learner for training Optimal Prescriptive Trees where the prescriptions
    should aim to minimize outcomes.

    Julia Equivalent:
    `IAI.OptimalTreePrescriptionMinimizer <https://docs.interpretable.ai/v2.1.0/OptimalTrees/reference/#IAI.OptimalTreePrescriptionMinimizer>`

    Examples
    --------
    >>> iai.OptimalTreePrescriptionMinimizer(**kwargs)

    Parameters
    ----------
    Use keyword arguments to set parameters on the resulting learner. Refer to
    the Julia documentation for available parameters.
    """
    def __init__(self, *args, **kwargs):
        jl_obj = _IAI.OptimalTreePrescriptionMinimizer_convert(*args, **kwargs)
        super().__init__(jl_obj)


class OptimalTreePrescriptionMaximizer(OptimalTreeLearner,
                                       PrescriptionTreeLearner):
    """Learner for training Optimal Prescriptive Trees where the prescriptions
    should aim to maximize outcomes.

    Julia Equivalent:
    `IAI.OptimalTreePrescriptionMaximizer <https://docs.interpretable.ai/v2.1.0/OptimalTrees/reference/#IAI.OptimalTreePrescriptionMaximizer>`

    Examples
    --------
    >>> iai.OptimalTreePrescriptionMaximizer(**kwargs)

    Parameters
    ----------
    Use keyword arguments to set parameters on the resulting learner. Refer to
    the Julia documentation for available parameters.
    """
    def __init__(self, *args, **kwargs):
        jl_obj = _IAI.OptimalTreePrescriptionMaximizer_convert(*args, **kwargs)
        super().__init__(jl_obj)


class OptimalTreePolicyMinimizer(OptimalTreeLearner, PolicyTreeLearner):
    """Learner for training Optimal Policy Trees where the policy
    should aim to minimize outcomes.

    Julia Equivalent:
    `IAI.OptimalTreePolicyMinimizer <https://docs.interpretable.ai/v2.1.0/OptimalTrees/reference/#IAI.OptimalTreePolicyMinimizer>`

    Examples
    --------
    >>> iai.OptimalTreePolicyMinimizer(**kwargs)

    Parameters
    ----------
    Use keyword arguments to set parameters on the resulting learner. Refer to
    the Julia documentation for available parameters.

    Compatibility
    -------------
    Requires IAI version 2.0 or higher.
    """
    def __init__(self, *args, **kwargs):
        _requires_iai_version("2.0.0", "OptimalTreePolicyMinimizer")
        jl_obj = _IAI.OptimalTreePolicyMinimizer_convert(*args, **kwargs)
        super().__init__(jl_obj)


class OptimalTreePolicyMaximizer(OptimalTreeLearner, PolicyTreeLearner):
    """Learner for training Optimal Policy Trees where the policy
    should aim to maximize outcomes.

    Julia Equivalent:
    `IAI.OptimalTreePolicyMaximizer <https://docs.interpretable.ai/v2.1.0/OptimalTrees/reference/#IAI.OptimalTreePolicyMaximizer>`

    Examples
    --------
    >>> iai.OptimalTreePolicyMaximizer(**kwargs)

    Parameters
    ----------
    Use keyword arguments to set parameters on the resulting learner. Refer to
    the Julia documentation for available parameters.

    Compatibility
    -------------
    Requires IAI version 2.0 or higher.
    """
    def __init__(self, *args, **kwargs):
        _requires_iai_version("2.0.0", "OptimalTreePolicyMaximizer")
        jl_obj = _IAI.OptimalTreePolicyMaximizer_convert(*args, **kwargs)
        super().__init__(jl_obj)
