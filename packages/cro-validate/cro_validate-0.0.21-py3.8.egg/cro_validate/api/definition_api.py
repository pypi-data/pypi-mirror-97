import cro_validate.classes.definition_classes as Definitions
import cro_validate.classes.util_classes as Utils
from cro_validate.enum import DataType


def get(definition_or_name):
	'''returns :ref:`Definition` instance.
	'''
	return Definitions.Index.get(definition_or_name)


def exists(name):
	return Definitions.Index.exists(name)


def as_dict():
	return Definitions.Index.as_dict()


def to_json_dict():
	return Definitions.Index.to_json_dict()


def from_json_dict(root):
	return Definitions.Index.from_json_dict(root)


def register_data_type_rule(data_type, rule, exceptions=[]):
	return Definitions.Index.register_data_type_rule(data_type, rule, exceptions)


def register_data_format_rule(data_format, rule, exceptions=[]):
	return Definitions.Index.register_data_format_rule(data_format, rule, exceptions)


def register_definition(
 			name=Utils.Empty,
			aliases=Utils.Empty,
			description=Utils.Empty,
			data_type=Utils.Empty,
			data_format=Utils.Empty,
			default_value=Utils.Empty,
			examples=Utils.Empty,
			nullable=Utils.Empty,
			deprecated=Utils.Empty,
			internal=Utils.Empty,
			rules=Utils.Empty,
			meta=Utils.Empty,
			dependency_resolver=Utils.Empty
		):
	result = Definitions.Index.register_definition(
			name=name,
			aliases=aliases,
			description=description,
			data_type=data_type,
			data_format=data_format,
			default_value=default_value,
			examples=examples,
			nullable=nullable,
			deprecated=deprecated,
			internal=internal,
			rules=rules,
			meta=meta,
			dependency_resolver=dependency_resolver
		)
	return result


def ensure_alias(name, alias):
	Definitions.Index.ensure_alias(name, alias)


def list_definitions():
	results = Definitions.Index.list_definitions()
	return results


def list_dependent_definitions(definition_name):
	results = Definitions.Index.list_dependent_definitions(definition_name)
	return results


def list_fields(name_or_definition):
	definition = name_or_definition
	if not isinstance(definition, Definitions.Definition):		
		definition = get(str(name_or_definition))
	return definition.list_fields()


def validate_input(
			definition_or_name,
			value,
			field_fqn=None,
			field_name=None,
			dependent_values={},
			**rules_kw
		):
	results = Definitions.Index.validate_input(
			None,
			field_fqn,
			field_name,
			definition_or_name,
			value,
			dependent_values,
			**rules_kw
		)
	return results


def clear():
	Definitions.Index.clear()