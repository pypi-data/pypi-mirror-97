from enum import unique, Enum


@unique
class DataType(Enum):
	String = 1
	Object = 2
	OneOf = 3
	Array = 4
	Integer =5
	Float = 6
	Boolean = 7