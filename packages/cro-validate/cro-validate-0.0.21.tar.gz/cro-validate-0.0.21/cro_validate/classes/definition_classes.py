import importlib, collections

from enum import Enum
from cro_validate.enum import DataType
from cro_validate.classes.configuration_classes import Config
import cro_validate.classes.parameter_classes as Parameters
import cro_validate.classes.schema_classes as Schemas
import cro_validate.classes.name_strategy_classes as NameStrategies
import cro_validate.classes.util_classes as Utils
import cro_validate.classes.dependency_classes as Dependencies


class Meta:
	def initialize(self, definition, **kw):
		raise NotImplementedError()


class DefaultDefinitionMeta(Meta):
	component_name_strategy = NameStrategies.DefaultComponentNameStrategy()
	schema_name = None
	component_name = None

	def __init__(self, component_name_strategy=Utils.Empty):
		if not Utils.Empty.isempty(component_name_strategy):
			self.component_name_strategy = component_name_strategy
		

	def initialize(self, definition, component_name_suffix='Model', display_name=None):
		if definition.is_object():
			self.schema_name = definition.data_format.model_name
			self.component_name = self.schema_name
		elif definition.is_array():
			self.component_name = definition.data_format
		else:
			self.component_name = self.component_name_strategy.create_name(definition, component_name_suffix, display_name)


class Definition:
	name = None
	aliases = []
	description = ''
	data_type = DataType.String
	data_format = None
	default_value = Utils.Empty
	examples = None
	nullable = False
	deprecated = False
	internal = False
	rules = []
	meta = DefaultDefinitionMeta()
	dependency_resolver = Dependencies.DefaultDefinitionDependencyResolver()

	def to_json_dict(self):
		def _is_default(name, value):
			class_value = getattr(self.__class__, name)
			if class_value == value:
				return True
			return False
		def _set(target, name, value):
			if _is_default(name, value):
				return
			target[name] = value		
		dependency_resolver_type = Utils.ClassName.class_fqn(self.dependency_resolver)
		fmt = None
		if self.data_format is not None:
			if isinstance(self.data_format, Enum):
				fmt = self.data_format.name
			elif isinstance(self.data_format, Schemas.Schema):
				fmt = self.data_format.to_json_dict()
			elif isinstance(self.data_format, set):
				fmt = [f for f in self.data_format]
				fmt.sort()
			else:
				fmt = self.data_format
		fmt_type = Utils.ClassName.class_fqn(self.data_format)
		default_value_type = Utils.ClassName.class_fqn(self.default_value)
		aliases = [a for a in self.aliases]
		aliases.sort()
		result = {}
		_set(result, 'aliases', aliases)
		_set(result, 'description', self.description)
		_set(result, 'data_type', self.data_type.name)
		_set(result, 'data_format', fmt)
		_set(result, 'default_value', self.default_value)
		_set(result, 'examples', self.examples)
		_set(result, 'nullable', self.nullable)
		_set(result, 'deprecated', self.deprecated)
		_set(result, 'internal', self.internal)
		_set(result, 'rules', [{'type':Utils.ClassName.class_fqn(r), 'config':r.to_json_dict()} for r in self.rules])
		types = {
				'default_value': default_value_type,
				'data_format': fmt_type
			}
		result = {k: result[k] for k in result if not _is_default(k, result[k])}
		for k in types:
			t = types[k]
			if k in result:
				result[k + '_type'] = t
		return result

	def __init__(
				self,
				name,
				aliases,
				description,
				data_type,
				data_format,
				default_value,
				examples,
				nullable,
				deprecated,
				internal,
				rules,
				meta,
				dependency_resolver
			):
		def _set_member(name, value):
			if Utils.Empty.isempty(value):
				return
			setattr(self, name, value)
		_set_member('name', name)
		_set_member('aliases', aliases)
		_set_member('description', description)
		_set_member('data_type', data_type)
		_set_member('data_format', data_format)
		_set_member('default_value', default_value)
		_set_member('examples', examples)
		_set_member('nullable', nullable)
		_set_member('deprecated', deprecated)
		_set_member('internal', internal)
		_set_member('dependencies', set())
		_set_member('rules', rules)
		_set_member('meta', meta)
		_set_member('dependency_resolver', dependency_resolver)
		# Name
		######
		self.name = Config.definition_name_strategy.create_name(self, self.name)
		if self.name is None:
			Config.exception_factory.create_input_error(
					'<unset>', 'Definition name cannot be None (description={0})'.format(self.description)
				)
		# Aliases
		#########
		if isinstance(aliases, str):
			self.aliases = {aliases}
		# Nullable
		##########
		if self.default_value is None:
			self.nullable = True
		# Default Value
		###############
		if Utils.Empty.isempty(self.default_value):
			if self.nullable is True:
				self.default_value = None
		# Data Format
		#############
		if self.is_object() and isinstance(self.data_format, str):
			format_definition = Index.get(self.data_format)
			self.data_format = format_definition.data_format
		elif self.data_type is DataType.OneOf:
			self.data_format = self.dependency_resolver.list_dependent_definition_names(self.name)
		# Validator
		###########
		if self.is_object():
			self.validator = self._get_obj_validator()
		elif self.is_array():
			self.validator = self._validate_array	
		else:
			self.validator = self._assign_value
		# Dependencies
		##############
		self.dependencies = set(self.dependency_resolver.list_dependency_fields(self.name))
		# Examples
		##########
		if not self.examples:
			self.examples = Config.default_examples_provider.get_examples(self)
		if not self.is_object() and not self.is_array():
			if not self.examples:
				raise Config.exception_factory.create_input_error(self.name, 'Missing examples')
		# Meta
		######
		self.meta.initialize(self)

	def _get_obj_model_validator(self):
		display_name = self.data_format.model_name
		if self.data_format.display_name is not None:
			display_name = str(self.data_format.display_name)
		validator = Schemas.ModelValidator(
				name=display_name,
				allow_unknown_fields=self.data_format.allow_unknown_fields,
				case_sensitive=self.data_format.case_sensitive
			)
		required = set()
		optional = set()
		ignored = set()
		unvalidated = set()
		definition_names = {}
		input_names = {}
		output_names = {}
		dependencies = {}
		default_values = {}
		fields = self.list_fields()
		for name in fields:
			field_definition = fields[name]
			if field_definition is None:
				field_definition = Schemas.Field()
			if field_definition.required:
				required.add(name)
			else:
				optional.add(name)
			if field_definition.ignored:
				ignored.add(name)
			if field_definition.unvalidated:
				unvalidated.add(name)
			if field_definition.definition_name:
				definition_names[name] = field_definition.definition_name
			if field_definition.output_name:
				output_names[name] = field_definition.output_name
			if field_definition.input_name:
				input_names[name] = field_definition.input_name
			if not Utils.Empty.isempty(field_definition.default_value):
				default_values[name] = field_definition.default_value
			definition_name = name
			if field_definition.definition_name is not None:
				definition_name = field_definition.definition_name
			if field_definition.unvalidated is not True:
				dependencies[name] = Index.get(definition_name).dependencies
		validator.add_spec(
				required=required,
				optional=optional,
				ignored=ignored,
				unvalidated=unvalidated,
				definition_names=definition_names,
				input_names=input_names,
				output_names=output_names,
				dependencies=dependencies,
				default_values=default_values
			)
		return validator

	def _get_obj_validator(self):
		model_validator = self._get_obj_model_validator()
		validator = Schemas.Validator(
				self.name,
				model_validator
			)
		return validator

	def _validate_array(
				self,
				results,
				field_fqn,
				field_name,
				definition,
				value,
				dependent_values,
				**rules_kw):
		if isinstance(value, list):
			pass
		elif isinstance(value, set):
			value = [v for v in value]
		else:
			raise Config.exception_factory.create_input_error(field_fqn, 'Expected array, received: {0}'.format(type(value)))
		items = []
		i = 0
		for entry in value:
			item = Index.validate_input(None, field_fqn + '[' + str(i) + ']', field_name, self.data_format, entry, dependent_values)
			items.append(item[field_name])
			i = i + 1
		results[field_name] = items

	def _assign_value(
				self,
				results,
				field_fqn,
				field_name,
				definition,
				value,
				dependent_values,
				**rules_kw):
		results[field_name] = value

	def validate(
				self,
				results,
				field_fqn,
				field_name,
				definition,
				value,
				dependent_values,
				**rules_kw
			):
		'''
		The validate func
		'''
		try:
			results = Parameters.Index.ensure(results)
			if not self.validator:
				raise Config.exception_factory.create_internal_error(self.name, "Missing validator.")
			if field_name is None:
				field_name = self.name
			if field_fqn is None:
				field_fqn = field_name
				if self.data_type == DataType.Object:
					field_fqn = self.validator.model_validator.name
			dependent_definition_name = self.dependency_resolver.get_dependent_definition(
					field_fqn,
					dependent_values
				)
			if value is None:
				if self.nullable is True:
					results[field_name] = None
					return
				else:
					raise Config.exception_factory.create_input_error(field_fqn, 'Not nullable.')
			results[field_name] = value
			Index._eval_data_type_rules(
					results,
					field_fqn,
					field_name,
					self,
					**rules_kw
				)
			Index._eval_data_format_rules(
					results,
					field_fqn,
					field_name,
					self,
					**rules_kw
				)
			if dependent_definition_name is not None:
				Index.validate_input(
						results,
						field_fqn,
						field_name,
						dependent_definition_name,
						results[field_name],
						dependent_values,
						**rules_kw
					)
			else:
				self.validator(
						results,
						field_fqn,
						field_name,
						self,
						results[field_name],
						dependent_values,
						**rules_kw
					)
			for rule in self.rules:
				results[field_name] = rule.execute(field_fqn, results[field_name], **rules_kw)
			return results
		except Exception as ex:
			if self.internal:
				raise Config.exception_factory.create_internal_error(ex.source, ex.message)
			else:
				raise ex

	def has_default_value(self):
		if Utils.Empty.isempty(self.default_value):
			return False
		return True

	def get_default_value(self, name):
		if not self.has_default_value():
			raise Config.exception_factory.create_internal_error(self.name, 'No default value configured')
		return self.default_value

	def get_name(self):
		return self.name

	def get_data_type(self):
		return self.data_type

	def get_data_format(self):
		return self.data_format

	def get_description(self, delim=' ', cat_rules=False):
		result = self.description
		if cat_rules is True:
			if self.rules is not None and len(self.rules) > 0:
				result = result + delim + delim.join([rule.get_description() for rule in self.rules])
		return result

	def get_aliases(self):
		return self.aliases

	def is_array(self):
		if self.data_type == DataType.Array:
			return True
		return False

	def is_object(self):
		if self.data_type == DataType.Object:
			return True
		return False

	def is_primitive(self):
		if self.is_object() or self.is_array():
			return False
		return True

	def is_internal(self):
		return self.is_internal

	def is_nullable(self):
		return self.nullable

	def list_fields(self):
		if self.data_type is not DataType.Object:
			return {}
		model = self.data_format.model
		if model is None:
			raise Config.exception_factory.create_internal_error(self.data_format.model_name, 'Missing model')
		fields = {}
		if isinstance(model, dict):
			fields = model
		else:
			for name in dir(model):
				if name.startswith('_'):
					continue
				fields[name] = getattr(model, name)
		for k in fields:
			f = fields[k]
			if f.input_name is None:
				f.input_name = k
		return fields

	def get_boundaries(self):
		result = []
		for rule in self.rules:
			result.extend(rule.get_boundaries())
		if self.is_nullable() is not True:
			result.append(None)
		if self.is_object() is True:
			result.append([])
		if self.is_array() is True:
			result.append({})
		return result


class DefinitionJsonDeserializer:
	def _get_dict_value(self, idx, k, default_value=Utils.Empty):
		if k in idx:
			return idx[k]
		return default_value

	def _set(self, src, tgt, k, default_value=Utils.Empty):
		v = self._get_dict_value(src, k, default_value)
		if Utils.Empty.isempty(v):
			return
		if k == 'is_internal':
			k = 'internal'
		tgt[k] = v

	def _deserialize_schema_field(self, root, name, obj):
		kw = {}
		if 'default_value' in obj:
			if obj['default_value_type'] != 'cro_validate.classes.util_classes.Empty':
				kw['default_value'] = self._instantiate(obj['default_value_type'], obj['default_value'])
		kw['definition_name'] = name
		if 'definition_name' in obj and obj['definition_name'] is not None:
			kw['definition_name'] = obj['definition_name']
		if not Index.exists(kw['definition_name']):
			dependent_definition_profile = self.deserialize(root, kw['definition_name'])
			Index.register_definition(**dependent_definition_profile)
		self._set(obj, kw, 'dependencies')
		self._set(obj, kw, 'ignored')
		self._set(obj, kw, 'input_name')
		self._set(obj, kw, 'output_name')
		self._set(obj, kw, 'required')
		self._set(obj, kw, 'unvalidated')
		if 'dependencies' in kw and isinstance(kw['dependencies'], list):
			kw['dependencies'] = set(kw['dependencies'])
		field = Schemas.Field(**kw)
		return field
		
	def _deserialize_schema(self, root, obj, name):
		kw = {}
		self._set(obj, kw, 'allow_unknown_fields')
		self._set(obj, kw, 'case_sensitive')
		self._set(obj, kw, 'display_name')
		self._set(obj, kw, 'model')
		kw['model_name'] = name
		model = {}
		if 'model' in obj:
			for name in obj['model']:
				field = self._deserialize_schema_field(root, name, obj['model'][name])
				model[name] = field
		kw['model'] = model
		schema = Schemas.Schema(**kw)
		return schema

	def _instantiate(self, fqn, *args, **kw):
		module_name, class_name = Utils.ClassName.class_fqn_parts(fqn)
		if module_name == 'builtins' and class_name == 'NoneType':
			return None
		module = importlib.import_module(module_name)
		_class = getattr(module, class_name)
		if isinstance(_class, type(Enum)):
			result = _class[args[0]]
		else:
			result = _class(*args, **kw)
		return result

	def _deserialize_rule(self, root, obj):
		rule = self._instantiate(obj['type'], **obj['config'])
		return rule

	def deserialize(self, root, name):
		kw = {
			'name': Utils.Empty,
			'aliases': Utils.Empty,
			'description': Utils.Empty,
			'examples': Utils.Empty,
			'nullable': Utils.Empty,
			'deprecated': Utils.Empty,
			'internal': Utils.Empty,
			'data_type': Utils.Empty,
			'data_format': Utils.Empty,
			'default_value': Utils.Empty,
			'meta': Utils.Empty,
			'dependency_resolver': Utils.Empty,
			'rules': Utils.Empty
		}
		namespace = {k:k for k in root}
		for k in root:
			if 'aliases' not in root[k]:
				continue
			for k1 in root[k]['aliases']:
				namespace[k1] = k
		obj = root[namespace[name]]
		# Data Format
		#############
		if 'data_type' in obj:
			kw['data_type'] = DataType[obj['data_type']]
		if 'data_format' in obj:
			if obj['data_format_type'] == 'cro_validate.classes.schema_classes.Schema':
				kw['data_format'] = self._deserialize_schema(root, obj['data_format'], name)
			else:
				kw['data_format'] = self._instantiate(obj['data_format_type'], obj['data_format'])
		# Default Value
		###############
		if 'default_value' in obj:
			if obj['default_value_type'] == 'builtins.NoneType':
				kw['default_value'] = None
			elif obj['default_value_type'] != 'cro_validate.classes.util_classes.Empty':
				kw['default_value'] = self._instantiate(obj['default_value_type'], obj['default_value'])
		# Rules
		#######
		if 'rules' in obj:
			rules = []
			for rule in obj['rules']:
				rule_obj = self._deserialize_rule(obj, rule)
				rules.append(rule_obj)
			kw['rules'] = rules
		# Aliases
		#########
		if 'aliases' in obj:
			kw['aliases'] = set(obj['aliases'])
		# Simple
		########
		kw['name'] = name
		self._set(obj, kw, 'description', '')
		self._set(obj, kw, 'examples', [])
		self._set(obj, kw, 'nullable', False)
		self._set(obj, kw, 'deprecated', False)
		self._set(obj, kw, 'is_internal', False)
		return kw


class Index:
	_idx = {}
	_data_type_rules = {}
	_data_type_rule_exceptions = set()
	_data_format_rules = {}
	_data_format_rule_exceptions = set()

	def get(definition_or_name):
		if isinstance(definition_or_name, Definition):
			return definition_or_name
		definition_name = str(definition_or_name)
		resolved = Config.definition_name_resolver.resolve(Index._idx, definition_name)
		if resolved is None:
			raise Config.exception_factory.create_input_error(definition_name, 'Definition name resolution failed (Unknown definition name).')
		return Index._idx[resolved]

	def exists(name):
		resolved = Config.definition_name_resolver.resolve(Index._idx, name)
		if resolved is None:
			return False
		return True

	def as_dict():
		return Index._idx

	def to_json_dict():
		aliases = set()
		keys = [k for k in Index.as_dict()]
		keys.sort()
		for k in keys:
			definition = Index.get(k)
			aliases.update(definition.aliases)
		result = {k:Index.get(k).to_json_dict() for k in keys if k not in aliases}
		return result

	def from_json_dict(root):
		deserializer = DefinitionJsonDeserializer()
		for k in root:
			if Index.exists(k):
				continue
			profile = deserializer.deserialize(root, k)
			Index.register_definition(**profile)

	def register_definition(
				name,
				aliases,
				description,
				data_type,
				data_format,
				default_value,
				examples,
				nullable,
				deprecated,
				internal,
				rules,
				meta,
				dependency_resolver
			):
		definition = Definition(
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
		definition_name = definition.get_name()
		names = set()
		names.add(definition_name)
		if Utils.Empty.isempty(aliases):
			pass
		elif isinstance(aliases, str):
			names.add(aliases)
		else:
			names.update(aliases)
		for entry in names:
			if definition_name in Index._idx:
				raise Config.exception_factory.create_internal_error(definition_name, 'Input definiton already exists.')
		for entry in names:
			Index._idx[entry] = definition
		return definition

	def register_data_type_rule(data_type, rule, exceptions=[]):
		if data_type not in Index._data_type_rules:
			Index._data_type_rules[data_type] = []
		Index._data_type_rules[data_type].append(rule)
		Index._data_type_rule_exceptions.update(exceptions)

	def register_data_format_rule(data_format, rule, exceptions=[]):
		if data_format not in Index._data_format_rules:
			Index._data_format_rules[data_format] = []
		Index._data_format_rules[data_format].append(rule)
		Index._data_format_rule_exceptions.update(exceptions)

	def _eval_data_type_rules(
				results,
				field_fqn,
				field_name,
				definition,
				**rules_kw
			):
		data_type = definition.get_data_type()
		if data_type not in Index._data_type_rules:
			return
		if definition.get_name() in Index._data_type_rule_exceptions:
			return
		for rule in Index._data_type_rules[definition.get_data_type()]:
			results[field_name] = rule.execute(field_fqn, results[field_name], **rules_kw)

	def _eval_data_format_rules(
				results,
				field_fqn,
				field_name,
				definition,
				**rules_kw
			):
		data_format = definition.get_data_format()
		if not isinstance(data_format, collections.Hashable):
			# currently not supported; FUTURES
			return
		if data_format not in Index._data_format_rules:
			return
		if definition.get_name() in Index._data_format_rule_exceptions:
			return
		for rule in Index._data_format_rules[definition.get_data_format()]:
			results[field_name] = rule.execute(field_fqn, results[field_name], **rules_kw)

	def validate_input(
				validated,
				field_fqn,
				field_name,
				definition_or_name,
				value,
				dependent_values={},
				**rules_kw
			):
		definition = Index.get(definition_or_name)
		results = Parameters.Index.ensure(validated)
		definition.validate(results, field_fqn, field_name, definition, value, dependent_values, **rules_kw)
		return results

	def ensure_alias(name, alias):
		definition = Index.get(name)
		if alias not in Index._idx:
			Index._idx[alias] = definition

	def list_definitions():
		result = [k for k in Index._idx]
		result.sort()
		return result

	def list_dependent_definitions(definition_name):
		results = set()
		definition = Index.get(definition_name)
		if definition.data_type == DataType.Object:
			result = definition.validator.list_definition_names()
		elif definition.data_type == DataType.Array:
			results = Index.list_dependent_definitions(definition.data_format)
		return results

	def list_fields(name):
		definition = Index.get(name)
		if definition.data_type == DataType.Object:
			return definition.validator.list_field_names()
		return [name]

	def clear():
		Index._idx = {}