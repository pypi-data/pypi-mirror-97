from dataclasses import dataclass

_LOCAL_DATE = "LocalDate"
_LOCAL_DATE_TIME = "LocalDateTime"
_ZONED_DATE_TIME = "ZonedDateTime"


@dataclass(frozen=True)
class DataType:
    """atoti Type."""

    java_type: str
    """Name of the associated Java literal type."""

    nullable: bool
    """Whether the objects of this type can be ``None``.

    Elements within array types cannot be ``None`` and must share the same scalar type.
    """

    def __str__(self) -> str:
        if self.nullable:
            return f"{self.java_type} (nullable)"
        return self.java_type


def local_date(java_format: str, nullable: bool = False):
    """Create a date type with the given Java date format."""
    return DataType(f"{_LOCAL_DATE}[{java_format}]", nullable)


def local_date_time(java_format: str, nullable: bool = False):
    """Create a datetime type with the given Java datetime format."""
    return DataType(f"{_LOCAL_DATE_TIME}[{java_format}]", nullable)


BOOLEAN = DataType("boolean", False)
NULLABLE_BOOLEAN = DataType("boolean", True)
STRING = DataType("string", False)
INT = DataType("int", False)
NULLABLE_INT = DataType("int", True)
INT_ARRAY = DataType("int[]", True)
LONG = DataType("long", False)
NULLABLE_LONG = DataType("long", True)
LONG_ARRAY = DataType("long[]", True)
FLOAT = DataType("float", False)
NULLABLE_FLOAT = DataType("float", True)
FLOAT_ARRAY = DataType("float[]", True)
DOUBLE = DataType("double", False)
NULLABLE_DOUBLE = DataType("double", True)
DOUBLE_ARRAY = DataType("double[]", True)
OBJECT = DataType("object", False)
NULLABLE_OBJECT = DataType("object", True)
LOCAL_DATE = local_date("yyyy-MM-dd")
LOCAL_DATE_TIME = local_date_time("yyyy-MM-dd'T'HH:mm:ss")
PYTHON_DOUBLE_LIST = DataType("atoti_list_double[][,]", True)
PYTHON_FLOAT_LIST = DataType("atoti_list_float[][,]", True)
PYTHON_LONG_LIST = DataType("atoti_list_long[][,]", True)
PYTHON_INT_LIST = DataType("atoti_list_int[][,]", True)
NUMPY_DOUBLE_ARRAY = DataType("atoti_numpy_double[][ ]", True)
NUMPY_FLOAT_ARRAY = DataType("atoti_numpy_float[][ ]", True)
NUMPY_LONG_ARRAY = DataType("atoti_numpy_long[][ ]", True)
NUMPY_INT_ARRAY = DataType("atoti_numpy_int[][ ]", True)

_ARRAYS = (
    INT_ARRAY,
    LONG_ARRAY,
    DOUBLE_ARRAY,
    FLOAT_ARRAY,
    PYTHON_DOUBLE_LIST,
    PYTHON_LONG_LIST,
    PYTHON_INT_LIST,
    NUMPY_DOUBLE_ARRAY,
    NUMPY_LONG_ARRAY,
    NUMPY_INT_ARRAY,
)


def _is_temporal(data_type: DataType):
    """Whether the type is temporal or not."""
    return (
        data_type.java_type.startswith(_LOCAL_DATE)
        or data_type.java_type.startswith(_LOCAL_DATE_TIME)
        or data_type.java_type.startswith(_ZONED_DATE_TIME)
    )
