import textwrap
from typing import Iterable, Sequence

from .base import api_function, BaseFunction
from ..request import Request
from ..session import api_session

__all__ = (
    'Group',
)


class Group(BaseFunction):
    """
    Provides a shortcut of :func:`Group.query()
    <ai.backend.client.admin.Admin.query>` that fetches various group information.

    .. note::

      All methods in this function class require your API access key to
      have the *admin* privilege.
    """

    @api_function
    @classmethod
    async def list(cls, domain_name: str,
                   fields: Iterable[str] = None) -> Sequence[dict]:
        """
        Fetches the list of groups.

        :param domain_name: Name of domain to list groups.
        :param fields: Additional per-group query fields to fetch.
        """
        if fields is None:
            fields = ('id', 'name', 'description', 'is_active',
                      'created_at', 'domain_name',
                      'total_resource_slots', 'allowed_vfolder_hosts',
                      'integration_id')
        query = textwrap.dedent("""\
            query($domain_name: String) {
                groups(domain_name: $domain_name) {$fields}
            }
        """)
        query = query.replace('$fields', ' '.join(fields))
        variables = {'domain_name': domain_name}
        rqst = Request(api_session.get(), 'POST', '/admin/graphql')
        rqst.set_json({
            'query': query,
            'variables': variables,
        })
        async with rqst.fetch() as resp:
            data = await resp.json()
        return data['groups']

    @api_function
    @classmethod
    async def detail(cls, gid: str, fields: Iterable[str] = None) -> Sequence[dict]:
        """
        Fetch information of a group with group ID.

        :param gid: ID of the group to fetch.
        :param fields: Additional per-group query fields to fetch.
        """
        if fields is None:
            fields = ('id', 'name', 'description', 'is_active', 'created_at', 'domain_name',
                      'total_resource_slots', 'allowed_vfolder_hosts', 'integration_id')
        query = textwrap.dedent("""\
            query($gid: UUID!) {
                group(id: $gid) {$fields}
            }
        """)
        query = query.replace('$fields', ' '.join(fields))
        variables = {'gid': gid}
        rqst = Request(api_session.get(), 'POST', '/admin/graphql')
        rqst.set_json({
            'query': query,
            'variables': variables,
        })
        async with rqst.fetch() as resp:
            data = await resp.json()
        return data['group']

    @api_function
    @classmethod
    async def create(cls, domain_name: str, name: str, description: str = '',
                     is_active: bool = True, total_resource_slots: str = None,
                     allowed_vfolder_hosts: Iterable[str] = None,
                     integration_id: str = None,
                     fields: Iterable[str] = None) -> dict:
        """
        Creates a new group with the given options.
        You need an admin privilege for this operation.
        """
        if fields is None:
            fields = ('id', 'domain_name', 'name',)
        query = textwrap.dedent("""\
            mutation($name: String!, $input: GroupInput!) {
                create_group(name: $name, props: $input) {
                    ok msg group {$fields}
                }
            }
        """)
        query = query.replace('$fields', ' '.join(fields))
        variables = {
            'name': name,
            'input': {
                'description': description,
                'is_active': is_active,
                'domain_name': domain_name,
                'total_resource_slots': total_resource_slots,
                'allowed_vfolder_hosts': allowed_vfolder_hosts,
                'integration_id': integration_id,
            },
        }
        rqst = Request(api_session.get(), 'POST', '/admin/graphql')
        rqst.set_json({
            'query': query,
            'variables': variables,
        })
        async with rqst.fetch() as resp:
            data = await resp.json()
        return data['create_group']

    @api_function
    @classmethod
    async def update(cls, gid: str, name: str = None, description: str = None,
                     is_active: bool = None, total_resource_slots: str = None,
                     allowed_vfolder_hosts: Iterable[str] = None,
                     integration_id: str = None,
                     fields: Iterable[str] = None) -> dict:
        """
        Update existing group.
        You need an admin privilege for this operation.
        """
        query = textwrap.dedent("""\
            mutation($gid: UUID!, $input: ModifyGroupInput!) {
                modify_group(gid: $gid, props: $input) {
                    ok msg
                }
            }
        """)
        variables = {
            'gid': gid,
            'input': {
                'name': name,
                'description': description,
                'is_active': is_active,
                'total_resource_slots': total_resource_slots,
                'allowed_vfolder_hosts': allowed_vfolder_hosts,
                'integration_id': integration_id,
            },
        }
        rqst = Request(api_session.get(), 'POST', '/admin/graphql')
        rqst.set_json({
            'query': query,
            'variables': variables,
        })
        async with rqst.fetch() as resp:
            data = await resp.json()
        return data['modify_group']

    @api_function
    @classmethod
    async def delete(cls, gid: str):
        """
        Inactivates the existing group. Does not actually delete it for safety.
        """
        query = textwrap.dedent("""\
            mutation($gid: UUID!) {
                delete_group(gid: $gid) {
                    ok msg
                }
            }
        """)
        variables = {'gid': gid}
        rqst = Request(api_session.get(), 'POST', '/admin/graphql')
        rqst.set_json({
            'query': query,
            'variables': variables,
        })
        async with rqst.fetch() as resp:
            data = await resp.json()
        return data['delete_group']

    @api_function
    @classmethod
    async def purge(cls, gid: str):
        """
        Delete the existing group. This action cannot be undone.
        """
        query = textwrap.dedent("""\
            mutation($gid: UUID!) {
                purge_group(gid: $gid) {
                    ok msg
                }
            }
        """)
        variables = {'gid': gid}
        rqst = Request(api_session.get(), 'POST', '/admin/graphql')
        rqst.set_json({
            'query': query,
            'variables': variables,
        })
        async with rqst.fetch() as resp:
            data = await resp.json()
        return data['purge_group']

    @api_function
    @classmethod
    async def add_users(cls, gid: str, user_uuids: Iterable[str],
                        fields: Iterable[str] = None) -> dict:
        """
        Add users to a group.
        You need an admin privilege for this operation.
        """
        query = textwrap.dedent("""\
            mutation($gid: UUID!, $input: ModifyGroupInput!) {
                modify_group(gid: $gid, props: $input) {
                    ok msg
                }
            }
        """)
        variables = {
            'gid': gid,
            'input': {
                'user_update_mode': 'add',
                'user_uuids': user_uuids,
            },
        }
        rqst = Request(api_session.get(), 'POST', '/admin/graphql')
        rqst.set_json({
            'query': query,
            'variables': variables,
        })
        async with rqst.fetch() as resp:
            data = await resp.json()
        return data['modify_group']

    @api_function
    @classmethod
    async def remove_users(cls, gid: str, user_uuids: Iterable[str],
                           fields: Iterable[str] = None) -> dict:
        """
        Remove users from a group.
        You need an admin privilege for this operation.
        """
        query = textwrap.dedent("""\
            mutation($gid: UUID!, $input: ModifyGroupInput!) {
                modify_group(gid: $gid, props: $input) {
                    ok msg
                }
            }
        """)
        variables = {
            'gid': gid,
            'input': {
                'user_update_mode': 'remove',
                'user_uuids': user_uuids,
            },
        }
        rqst = Request(api_session.get(), 'POST', '/admin/graphql')
        rqst.set_json({
            'query': query,
            'variables': variables,
        })
        async with rqst.fetch() as resp:
            data = await resp.json()
        return data['modify_group']
