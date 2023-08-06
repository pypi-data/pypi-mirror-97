from typing import Optional

import click
from tabulate import tabulate

from montecarlodata.common.user import UserService
from montecarlodata.config import Config
from montecarlodata.errors import manage_errors
from montecarlodata.integrations.onboarding.fields import GQL_TO_FRIENDLY_CONNECTION_MAP


class OnboardingStatusService:
    _INTEGRATION_FRIENDLY_HEADERS = ['Integration', 'ID', 'Created on (UTC)']

    def __init__(self, config: Config, user_service: Optional[UserService] = None):
        self._abort_on_error = True
        self._user_service = user_service or UserService(config=config)

    @manage_errors
    def display_integrations(self, headers: Optional[str] = 'firstrow', table_format: Optional[str] = 'fancy_grid'):
        """
        Display active integrations in an easy to read table. E.g.
        ╒══════════════════╤══════════════════════════════════════╤══════════════════════════════════╕
        │ Integration      │ ID                                   │ Created on (UTC)                 │
        ╞══════════════════╪══════════════════════════════════════╪══════════════════════════════════╡
        │ Hive (metastore) │ 1023721b-e639-44ed-9838-e1f669d3fc85 │ 2020-05-09T01:49:52.806602+00:00 │
        ╘══════════════════╧══════════════════════════════════════╧══════════════════════════════════╛
        """
        table = [self._INTEGRATION_FRIENDLY_HEADERS]
        for warehouse in self._user_service.warehouses or [{}]:
            connections = warehouse.get('connections')
            for connection in connections or []:
                table.append(
                    [
                        GQL_TO_FRIENDLY_CONNECTION_MAP.get(connection['type'].lower().replace('_', '-'),
                                                           connection['type']),
                        connection['uuid'],
                        connection['createdOn']
                    ]
                )  # order by the friendly headers, defaulting to gql response if not found
        click.echo(tabulate(table, headers=headers, tablefmt=table_format))
