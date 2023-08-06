import re
import logging


from sevenbridges.errors import SbgError, ReadOnlyPropertyError
from sevenbridges.meta.comp_mutable_dict import CompoundMutableDict
from sevenbridges.meta.resource import Resource
from sevenbridges.models.file import File


logger = logging.getLogger(__name__)


# noinspection PyProtectedMember
class Logs(CompoundMutableDict, Resource):
    """
    Task output resource.
    """
    _name = 'logs'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __getitem__(self, item):
        try:
            log = self._parent._data[self._name][item]
            match = re.match(r'.*files/(.*)/.*', log)
            if match:
                file_id = match.groups()[0]
                return File(id=file_id, api=self._api)
            else:
                raise SbgError(f'Unable to fetch {item} log file!')
        except Exception as e:
            logger.debug(
                'Failed to retrieve log file due to an error: %s', str(e)
            )

    def __setitem__(self, key, value):
        raise ReadOnlyPropertyError('Can not modify read only properties.')
