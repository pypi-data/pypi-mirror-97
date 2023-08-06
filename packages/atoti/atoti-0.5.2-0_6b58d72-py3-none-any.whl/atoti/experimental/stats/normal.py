"""Normal distribution, also called Gaussian, Gauss or Laplace–Gauss distribution.

For more information read:

    * `scipy.stats.norm <https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.norm.html>`_
    * `The Normal distribution Wikipedia page <https://en.wikipedia.org/wiki/Normal_distribution>`_
"""


from ..._measures.calculated_measure import CalculatedMeasure, Operator
from ...measure import Measure, _convert_to_measure
from ._utils import NumericMeasureLike, ensure_strictly_positive


def pdf(
    point: Measure,
    *,
    mean: NumericMeasureLike = 0,
    standard_deviation: NumericMeasureLike = 1
) -> Measure:
    r"""Probability density function for a normal distribution.

    The pdf is given by the formula

    .. math::

        \operatorname {pdf}(x) = \frac{1}{ \sigma \sqrt{2 \pi} } e^{-\frac{1}{2} \left(\frac{x - \mu}{\sigma}\right)^{2}}

    Where :math:`\mu` is the mean (or expectation) of the distribution while :math:`\sigma` is its standard deviation.

    Args:
        point: The point where the function is evaluated.
        mean: The mean value of the distribution.
        standard_deviation: The standard deviation of the distribution.
            Must be positive.

    See Also:
        `General normal distribution <https://en.wikipedia.org/wiki/Normal_distribution#General_normal_distribution>`_ on Wikipedia.

    """
    ensure_strictly_positive(standard_deviation, "standard_deviation")
    return CalculatedMeasure(
        Operator(
            "normal_density",
            [point, _convert_to_measure(mean), _convert_to_measure(standard_deviation)],
        )
    )


def cdf(
    point: Measure, *, mean: NumericMeasureLike, standard_deviation: NumericMeasureLike
) -> Measure:
    r"""Cumulative distribution function for a normal distribution.

    The cdf is given by the formula

    .. math::

       \operatorname {cdf}(x) = \frac {1}{2}\left[1 + \operatorname {erf} \left(\frac {x-\mu }{\sigma {\sqrt {2}}}\right)\right]

    Where :math:`\mu` is the mean of the distribution, :math:`\sigma` is its standard deviation and :math:`\operatorname {erf}` the error function.

    Args:
        point: The point where the function is evaluated.
        mean: The mean value of the distribution.
        standard_deviation: The standard deviation of the distribution.
            Must be positive.

    See Also:
        `cdf of a normal distribution <https://en.wikipedia.org/wiki/Normal_distribution#Cumulative_distribution_function>`_ on Wikipedia

    """
    ensure_strictly_positive(standard_deviation, "standard_deviation")
    return CalculatedMeasure(
        Operator(
            "normal_cumulative_probability",
            [point, _convert_to_measure(mean), _convert_to_measure(standard_deviation)],
        )
    )


def ppf(
    point: Measure, *, mean: NumericMeasureLike, standard_deviation: NumericMeasureLike
) -> Measure:
    r"""Percent point function for a normal distribution.

    Also called inverse cumulative distribution function.

    The ppf is given by the formula

    .. math::

       \operatorname {ppf}(x) = \mu + \sigma \sqrt{2} \operatorname {erf} ^{-1}(2x-1)

    Where :math:`\mu` is the mean of the distribution, :math:`\sigma` is its standard deviation and :math:`\operatorname {erf}^{-1}` the inverse of the error function.

    Args:
        point: The point where the function is evaluated.
        mean: The mean value of the distribution.
        standard_deviation: The standard deviation of the distribution.
            Must be positive.

    See Also:
        `Quantile function of  a normal distribution <https://en.wikipedia.org/wiki/Normal_distribution#Quantile_function>`_ on Wikipedia

    """
    ensure_strictly_positive(standard_deviation, "standard_deviation")
    return CalculatedMeasure(
        Operator(
            "normal_ppf",
            [point, _convert_to_measure(mean), _convert_to_measure(standard_deviation)],
        )
    )
