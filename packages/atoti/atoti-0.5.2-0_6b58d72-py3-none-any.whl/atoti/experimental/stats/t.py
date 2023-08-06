"""Student’s t distribution.

For more information read:

    * `scipy.stats.t <https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.t.html>`_
    * `The Student’s t Wikipedia page <https://en.wikipedia.org/wiki/Student%27s_t-distribution>`_

"""

from ..._measures.calculated_measure import CalculatedMeasure, Operator
from ...measure import Measure, _convert_to_measure
from ._utils import NumericMeasureLike, ensure_strictly_positive


def pdf(point: Measure, *, degrees_of_freedom: NumericMeasureLike) -> Measure:
    r"""Probability density function for a Student’s t distribution.

    The pdf of a Student's t-distribution is:

    .. math::

        \operatorname {pdf}(x)=\frac {\Gamma (\frac {\nu +1}{2})}{\sqrt {\nu \pi }\,\Gamma (\frac {\nu }{2})} \left(1+\frac {x^{2}}{\nu }\right)^{-\frac {\nu +1}{2}}

    where :math:`\nu` is the number of degrees of freedom and :math:`\Gamma` is the gamma function.

    Args:
        point: The point where the function is evaluated.
        degrees_of_freedom: The number of degrees of freedom.
            Must be positive.

    See Also:
        `The Student’s t Wikipedia page <https://en.wikipedia.org/wiki/Student%27s_t-distribution>`_

    """
    ensure_strictly_positive(degrees_of_freedom, "degrees_of_freedom")
    return CalculatedMeasure(
        Operator("student_density", [point, _convert_to_measure(degrees_of_freedom)])
    )


def cdf(point: Measure, *, degrees_of_freedom: NumericMeasureLike) -> Measure:
    """Cumulative distribution function for a Student’s t distribution.

    Args:
        point: The point where the function is evaluated.
        degrees_of_freedom: The number of degrees of freedom.
            Must be positive.

    See Also:
        `The Student’s t Wikipedia page <https://en.wikipedia.org/wiki/Student%27s_t-distribution>`_

    """
    ensure_strictly_positive(degrees_of_freedom, "degrees_of_freedom")
    return CalculatedMeasure(
        Operator(
            "student_cumulative_probability",
            [point, _convert_to_measure(degrees_of_freedom)],
        )
    )


def ppf(point: Measure, *, degrees_of_freedom: NumericMeasureLike) -> Measure:
    """Percent point function for a Student’s t distribution.

    Also called inverse cumulative distribution function.

    Args:
        point: The point where the function is evaluated.
        degrees_of_freedom: The number of degrees of freedom.
            Must be positive.

    See Also:
        `The Student’s t Wikipedia page <https://en.wikipedia.org/wiki/Student%27s_t-distribution>`_

    """
    ensure_strictly_positive(degrees_of_freedom, "degrees_of_freedom")
    return CalculatedMeasure(
        Operator(
            "student_ppf",
            [point, _convert_to_measure(degrees_of_freedom)],
        )
    )
