# Copyright (c) 2019 Qumulo, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

# XXX: Please add types to the functions in this file. Static type checking in
# Python prevents bugs!
# mypy: ignore-errors


import qumulo.lib.request as request
from qumulo.lib.uri import UriBuilder
from qumulo.rest.auth import find_identity

# Statically defined roles
ADMINISTRATOR_ROLE_NAME = 'Administrators'
ADMIN_OBSERVER_ROLE_NAME = 'Observers'


@request.request
def list_roles(conninfo, credentials):
    method = 'GET'
    uri = '/v1/auth/roles/'
    return request.rest_request(conninfo, credentials, method, uri)


@request.request
def list_role(conninfo, credentials, role_name):
    method = 'GET'
    uri = UriBuilder(path='/v1/auth/roles/')
    uri.add_path_component(role_name)
    return request.rest_request(conninfo, credentials, method, str(uri))


@request.request
def create_role(conninfo, credentials, role_name, description, privileges=()):
    method = 'POST'
    uri = '/v1/auth/roles/'
    return request.rest_request(
        conninfo,
        credentials,
        method,
        uri,
        body=dict(
            name=role_name, description=description, privileges=list(privileges),
        ),
    )


@request.request
def modify_role(
    conninfo, credentials, role_name, description=None, privileges=None, if_match=None
):
    method = 'PATCH'
    uri = UriBuilder(path='/v1/auth/roles/')
    uri.add_path_component(role_name)
    body = {}
    if description is not None:
        body['description'] = description
    if privileges is not None:
        body['privileges'] = list(privileges)
    return request.rest_request(
        conninfo, credentials, method, str(uri), body=body, if_match=if_match
    )


@request.request
def delete_role(conninfo, credentials, role_name):
    method = 'DELETE'
    uri = UriBuilder(path='/v1/auth/roles/')
    uri.add_path_component(role_name)
    return request.rest_request(conninfo, credentials, method, str(uri))


@request.request
def list_members(conninfo, credentials, role_name, limit=None, after=None):
    method = 'GET'
    uri = UriBuilder(path='/v1/auth/roles/')
    uri.add_path_component(role_name)
    uri.add_path_component('members')

    if limit is not None:
        uri.add_query_param('limit', limit)

    if after is not None:
        uri.add_query_param('after', after)

    return request.rest_request(conninfo, credentials, method, str(uri))


@request.request
def list_all_members(conninfo, credentials, role_name, limit=None):
    method = 'GET'
    uri = UriBuilder(path='/v1/auth/roles/')
    uri.add_path_component(role_name)
    uri.add_path_component('members')

    def get_members(uri):
        return request.rest_request(conninfo, credentials, method, str(uri))

    return request.PagingIterator(uri, get_members, page_size=limit)


@request.request
def add_member(conninfo, credentials, role_name, **attrs):
    """
    Add a member to role @p role_name. At least one argument other
    than @p domain must be specified. If multiple are specified, they must
    represent the same identity.
    @p role_name The name of the role being assigned to.
    @p domain The domain the identity is in.  LOCAL_DOMAIN, WORLD_DOMAIN,
        POSIX_USER_DOMAIN, POSIX_GROUP_DOMAIN, or AD_DOMAIN.
    @p auth_id The identifier used internally by qsfs.
    @p uid A posix UID
    @p gid A posix GID
    @p sid A SID.
    @p name A name of a cluster-local, AD, or LDAP user.  May be an unqualified
        login name, qualified with netbios name (e.g. DOMAIN\\user), a
        universal principal name (e.g. user@domain.example.com), or an LDAP
        distinguished name (e.g CN=John Doe,OU=users,DC=example,DC=com).
    """
    method = 'POST'
    uri = UriBuilder(path='/v1/auth/roles/')
    uri.add_path_component(role_name)
    uri.add_path_component('members')
    return request.rest_request(conninfo, credentials, method, str(uri), body=attrs)


@request.request
def remove_member(conninfo, credentials, role_name, **attrs):
    """
    Remove a member from role @p role_name. At least one argument other
    than @p domain must be specified. If multiple are specified, they must
    represent the same identity.
    @p role_name The name of the role being assigned to.
    @p domain The domain the identity is in.  LOCAL_DOMAIN, WORLD_DOMAIN,
        POSIX_USER_DOMAIN, POSIX_GROUP_DOMAIN, or AD_DOMAIN.
    @p auth_id The identifier used internally by qsfs.
    @p uid A posix UID
    @p gid A posix GID
    @p sid A SID.
    @p name A name of a cluster-local, AD, or LDAP user.  May be an unqualified
        login name, qualified with netbios name (e.g. DOMAIN\\user), a
        universal principal name (e.g. user@domain.example.com), or an LDAP
        distinguished name (e.g CN=John Doe,OU=users,DC=example,DC=com).
    """
    identity = find_identity(conninfo, credentials, **attrs)
    auth_id = identity.data['auth_id']

    method = 'DELETE'
    uri = UriBuilder(path='/v1/auth/roles/')
    uri.add_path_component(role_name)
    uri.add_path_component('members')
    uri.add_path_component(auth_id)
    return request.rest_request(conninfo, credentials, method, str(uri))


@request.request
def list_privileges(conninfo, credentials):
    method = 'GET'
    uri = '/v1/auth/privileges/'
    return request.rest_request(conninfo, credentials, method, uri)
