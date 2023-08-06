

class DependentDefinitionResolver:
	def list_dependent_definition_names(self, fqn):
		raise NotImplementedError()

	def get_dependent_definition(self, fqn, dependent_values):
		raise NotImplementedError()

	def list_dependency_fields(self, fqn):
		raise NotImplementedError()


class DefaultDefinitionDependencyResolver(DependentDefinitionResolver):
	def list_dependent_definition_names(self, fqn):
		return []

	def to_json_dict(self):
		return {}

	def get_dependent_definition(self, fqn, dependent_values):
		return None

	def list_dependency_fields(self, fqn):
		return []

	def to_json_dict(self):
		return {}


class _OneOfResolverPlayback:
	def __init__(self, fqn, dependency_state, dependent_definition_name):
		self.fqn = fqn
		self.dependency_state = dependency_state
		self.dependent_definition_name = dependent_definition_name

	def to_json_dict(self):
		return {
				'fqn': self.fqn,
				'dependency_state': self.dependency_state,
				'dependent_definition_name': self.dependent_definition_name
			}


class OneOfResolver(DependentDefinitionResolver):
	def __init__(self, playback=[]):
		self._dependencies = set()
		self._dependency_idx = {}
		self._dependency_order = []
		self._permutations = []
		self._serialize_playback = []
		for entry in playback:
			self.index_dependent_definition(
					entry['fqn'],
					entry['dependency_state'],
					entry['dependent_definition_name']
				)

	def to_json_dict(self):
		return {
				'playback': [entry.to_json_dict() for entry in self._serialize_playback]
			}

	def _update_dependency_idx_order(self, fqn, keys):
		diff = self._dependencies.difference(keys)
		if len(diff) > 0:
			raise Config.exception_factory.create_internal_error(fqn, 'Permutation keys must match dependencies.')
		self._dependencies.update([k for k in keys])
		for k in keys:
			if k in self._dependency_order:
				continue
			self._dependency_order.append(k)
		self._dependency_order.sort()

	def _index_permutation(self, fqn, permutation, value):
		self._permutations.append(permutation)
		idx = self._dependency_idx
		for k in self._dependency_order[:-1]:
			state = permutation[k]
			if state not in idx:
				idx[state] = {}
			idx = idx[state]
		state = permutation[self._dependency_order[-1]]
		if state in idx:
			raise Config.exception_factory.create_internal_error(fqn, 'Cannot re-index a permutation.')
		idx[state] = value

	def _get_permutation_value(self, fqn, permutation):
		idx = self._dependency_idx
		last_index = len(self._dependency_order) - 1
		for i in range(len(self._dependency_order)):
			k = self._dependency_order[i]
			if k not in permutation:
				raise Config.exception_factory.create_internal_error(
						fqn,
						'k not in permutation ({0})'.fromat(permutation)
					)
			state = permutation[k]
			if state not in idx:
				raise Config.exception_factory.create_internal_error(
						fqn,
						'Unknown permutation value (k={0} p={2}).'.format(k, state, permutation)
					)
			if i == last_index:
				return idx[state]
			idx = idx[state]
		return None

	def list_dependent_definition_names(self, fqn):
		result = set()
		for p in self._permutations:
			name = self._get_permutation_value(fqn, p)
			result.add(name)
		return result

	def index_dependent_definition(self, fqn, dependency_state, dependent_definition_name):
		self._update_dependency_idx_order(fqn, dependency_state.keys())
		self._index_permutation(fqn, dependency_state, dependent_definition_name)
		self._serialize_playback.append(_OneOfResolverPlayback(fqn, dependency_state, dependent_definition_name))

	def get_dependent_definition(self, fqn, dependent_values):
		name = self._get_permutation_value(fqn, dependent_values)
		return name

	def list_dependency_fields(self, fqn):
		return self._dependencies
