from assetic.models.requestor_representation import RequestorRepresentation
import warnings
import six
class Assetic3IntegrationRepresentationsRequestorRepresentation(RequestorRepresentation):
	def __init__(self, **kwargs):
		warnings.warn('The "Assetic3IntegrationRepresentationsRequestorRepresentation" class is deprecated, use "RequestorRepresentation" instead',stacklevel=2)
		super(RequestorRepresentation, self).__init__()
		for attr, _ in six.iteritems(self.swagger_types):
			val = None
			if attr in kwargs:
				val = kwargs[attr]
			setattr(self, "_" + attr, val) 
