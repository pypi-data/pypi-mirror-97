import datetime
from typing import Any, Collection, Mapping, Union, cast

from ._vendor.atotipy4j.java_collections import JavaArray, JavaMap, ListConverter
from ._vendor.atotipy4j.java_gateway import JavaClass, JavaGateway, JavaObject


# No type stubs for py4j, so we ignore this error
def to_java_object_array(gateway: JavaGateway, seq: Collection[Any]) -> JavaArray:
    """Transform the Python collection into a Java array of strings.

    Args:
        gateway: the Java Gateway.
        seq: The collection to convert.

    """
    return to_typed_java_array(gateway, gateway.jvm.Object, seq)


def to_java_map(gateway: JavaGateway, dictionary: Mapping[Any, Any]) -> JavaMap:
    """Convert a Python dict to a JavaMap."""
    return _to_typed_java_map(gateway, "java.util.HashMap", dictionary)


def _to_typed_java_map(
    gateway: JavaGateway, clazz: str, to_convert: Mapping[Any, Any]
) -> JavaMap:
    """Convert to a map of the given type."""
    map_type = JavaClass(clazz, gateway._gateway_client)
    java_map = cast(JavaMap, map_type())
    for key in to_convert.keys():
        java_map[key] = as_java_object(gateway, to_convert[key])
    return java_map


def to_java_string_array(gateway: JavaGateway, seq: Collection[str]) -> JavaArray:
    """Transform the Python collection into a Java array of strings."""
    return to_typed_java_array(gateway, gateway.jvm.String, seq)


def to_java_map_list(gateway: JavaGateway, seq: Collection[Mapping[Any, Any]]) -> Any:
    """Transform the Python collection into a Java list of maps."""
    return ListConverter().convert(
        [to_java_map(gateway, elem) for elem in seq], gateway._gateway_client
    )


def to_java_object_list(gateway: JavaGateway, seq: Collection[Any]) -> Any:
    """Transform the Python collection into a Java list of object."""
    return ListConverter().convert(
        [as_java_object(gateway, e) for e in seq], gateway._gateway_client
    )


def to_typed_java_array(
    gateway: JavaGateway, array_type: Any, seq: Collection[Any]
) -> JavaArray:
    """Transform to Java array of given type."""
    array = cast(JavaArray, gateway.new_array(array_type, len(seq)))
    if seq:
        for index, elem in enumerate(seq):
            array[index] = as_java_object(gateway, elem)
    return array


def to_java_object_array_array(
    gateway: JavaGateway, rows: Collection[Collection[Any]]
) -> JavaArray:
    """Transform the 2D Python collection into a 2D Java collection of Objects."""
    length = 0
    java_rows = []
    for row in rows:
        length = len(row)
        java_rows.append(to_java_object_array(gateway, row))
    row_count = len(rows)
    array = cast(JavaArray, gateway.new_array(gateway.jvm.Object, row_count, length))
    for index, elem in enumerate(java_rows):
        array[index] = elem
    return array


def to_java_date(
    gateway: JavaGateway, date: Union[datetime.date, datetime.datetime]
) -> JavaObject:
    """Transform the Python date into a Java one."""
    if isinstance(date, datetime.datetime):
        if not date.tzinfo:
            return gateway.jvm.java.time.LocalDateTime.of(  # type: ignore
                date.year,
                date.month,
                date.day,
                date.hour,
                date.minute,
                date.second,
                date.microsecond * 1000,
            )
        raise NotImplementedError()
    if isinstance(date, datetime.date):
        # LocalDate of(int year, int month, int dayOfMonth)
        return gateway.jvm.java.time.LocalDate.of(date.year, date.month, date.day)  # type: ignore
    raise ValueError(f"Expected a date but got {date}")


def as_java_object(gateway: JavaGateway, arg: Any) -> Any:
    """Try to convert the arg to a java argument.

    Args:
        gateway: the Java gateway
        arg: the argument to convert.

    """
    if isinstance(arg, (datetime.date, datetime.datetime)):
        return to_java_date(gateway, arg)
    if isinstance(arg, list):
        # Convert to Vector
        vector_package = gateway.jvm.com.qfs.vector.array.impl  # type: ignore
        if all(isinstance(x, float) for x in arg):
            array = to_typed_java_array(gateway, gateway.jvm.double, arg)
            return vector_package.ArrayDoubleVector(array)  # type: ignore
        if all(isinstance(x, int) for x in arg):
            array = to_typed_java_array(gateway, gateway.jvm.long, arg)
            return vector_package.ArrayLongVector(array)  # type: ignore
        array = to_java_object_array(gateway, arg)
        return vector_package.ArrayObjectVector(array)  # type: ignore
    return arg


def to_python_dict(java_map: JavaMap) -> dict:
    """Convert a Java map to a python dict.

    Args:
        java_map: the java map to convert

    Returns:
        The Python dict equivalent of the map
    """
    dic: dict = {}
    for k in java_map.keySet().toArray():  # type: ignore
        dic[k] = java_map[k]
    return dic


def to_python_list(list_to_convert: JavaObject) -> list:
    """Convert a Java list to a python list.

    Args:
        list_to_convert: the java list to convert

    Returns:
        The Python list equivalent of the Java list

    """
    # ignore types when calling a Java function
    return list(list_to_convert.toArray())  # type: ignore
