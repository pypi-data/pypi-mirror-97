"""Chi-square distribution.

For more information read:

    * `scipy.stats.chi2 <https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2.html>`_
    * `The Chi-square Wikipedia page <https://en.wikipedia.org/wiki/Chi-square_distribution>`_

"""

from ..._measures.calculated_measure import CalculatedMeasure, Operator
from ...measure import Measure, _convert_to_measure
from ._utils import NumericMeasureLike, ensure_strictly_positive


def pdf(point: Measure, *, degrees_of_freedom: NumericMeasureLike) -> Measure:
    r"""Probability density function for a chi-square distribution.

    The pdf of the chi-square distribution with k degrees of freedom is

    .. math::

        \operatorname {pdf}(x)=\dfrac
          {x^{\frac {k}{2}-1}e^{-\frac {x}{2}}}
          {2^\frac {k}{2}\Gamma \left(\frac {k}{2}\right)}

    where :math:`\Gamma` is the `gamma function <https://en.wikipedia.org/wiki/Gamma_function>`_.

    Args:
        point: The point where the function is evaluated.
        degrees_of_freedom: The number of degrees of freedom.
            Must be positive.

    See Also:
        `The Chi-square Wikipedia page <https://en.wikipedia.org/wiki/Chi-square_distribution>`_

    """
    ensure_strictly_positive(degrees_of_freedom, "degrees_of_freedom")
    return CalculatedMeasure(
        Operator("chi2_density", [point, _convert_to_measure(degrees_of_freedom)])
    )


def cdf(point: Measure, *, degrees_of_freedom: NumericMeasureLike) -> Measure:
    r"""Cumulative distribution function for a chi-square distribution.

    The cdf of the chi-square distribution with k degrees of freedom is

    .. math::

        \operatorname {cdf}(x)=\dfrac {\gamma (\frac {k}{2},\,\frac {x}{2})}{\Gamma (\frac {k}{2})}

    where :math:`\Gamma` is the `gamma function <https://en.wikipedia.org/wiki/Gamma_function>`_
    and :math:`\gamma` the `lower incomplete gamma function <https://en.wikipedia.org/wiki/Incomplete_gamma_function>`_.

    Args:
        point: The point where the function is evaluated.
        degrees_of_freedom: The number of degrees of freedom.
            Must be positive.

    See Also:
        `The Chi-square Wikipedia page <https://en.wikipedia.org/wiki/Chi-square_distribution>`_

    """
    ensure_strictly_positive(degrees_of_freedom, "degrees_of_freedom")
    return CalculatedMeasure(
        Operator(
            "chi2_cumulative_probability",
            [point, _convert_to_measure(degrees_of_freedom)],
        )
    )


def ppf(point: Measure, *, degrees_of_freedom: NumericMeasureLike) -> Measure:
    """Percent point function for a chi-square distribution.

    Also called inverse cumulative distribution function.

    Args:
        point: The point where the function is evaluated.
        degrees_of_freedom: The number of degrees of freedom.
            Must be positive.

    See Also:
        `The Chi-square Wikipedia page <https://en.wikipedia.org/wiki/Chi-square_distribution>`_

    """
    ensure_strictly_positive(degrees_of_freedom, "degrees_of_freedom")
    return CalculatedMeasure(
        Operator(
            "chi2_ppf",
            [point, _convert_to_measure(degrees_of_freedom)],
        )
    )
