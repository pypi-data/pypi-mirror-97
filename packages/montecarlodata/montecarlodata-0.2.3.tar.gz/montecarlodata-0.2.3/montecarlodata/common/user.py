from dataclasses import dataclass
from typing import Optional

from montecarlodata.config import Config
from montecarlodata.errors import complain_and_abort
from montecarlodata.queries.user import GET_USER_QUERY
from montecarlodata.utils import GqlWrapper


@dataclass
class User:
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserService:
    def __init__(self, config: Config, request_wrapper: Optional[GqlWrapper] = None):
        self._config = config
        self._request_wrapper = request_wrapper or GqlWrapper(mcd_id=config.mcd_id, mcd_token=config.mcd_token)

        self._user = self._request_wrapper.make_request(GET_USER_QUERY)  # get user info
        self._set_user_props()

    @property
    def user(self) -> User:
        """
        Returns basic user properties
        """
        return User(first_name=self._user['getUser'].get('firstName'), last_name=self._user['getUser'].get('lastName'))

    def _set_user_props(self) -> None:
        """
        Set relevant user props like DC and warehouse to instance
        """
        self.collectors = self._user['getUser']['account'].get('dataCollectors', [{}])
        self.active_collector = self.collectors[self._get_active_collector()]
        self.warehouses = self.active_collector.get('warehouses')

    def _get_active_collector(self) -> Optional[int]:
        """
        Get active collector - currently only one active collector per account is supported. Abort if None are found
        """
        for idx, collector in enumerate(self.collectors):
            if collector.get('active'):
                return idx
        complain_and_abort('No active collector found')
