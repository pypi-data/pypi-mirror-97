"""
    admin model
"""

import logging
import uuid

import zoom
import zoom.mail
from zoom.context import context
from zoom.tools import today
from zoom.users import Users
from zoom.models import Groups


def get_user_group_options(site):
    """return options for a groups pulldown field"""
    user_groups = list(sorted(
        (group.link, group.key)
        for group in site.groups.find(**{'type': 'U'})
    ))
    return user_groups


def get_subgroups(db, groups):
    """get subgroups for a list of groups
    """

    def get_memberships(group, memberships, depth=0):
        """get group memberships"""
        result = set([group])
        if depth < 10:
            for grp, sgrp in memberships:
                if group == sgrp and grp not in result:
                    result |= get_memberships(grp, memberships, depth+1)
        return result

    all_subgroups = list(db(
        'SELECT group_id, subgroup_id FROM subgroups ORDER BY subgroup_id'
    ))

    memberships = set([])
    for group in groups:
        memberships |= get_memberships(group, all_subgroups)

    return memberships


def get_supergroups(db, groups):
    """get supergroups for a list of groups
    """

    def get_memberships(group, memberships, depth=0):
        """get group memberships"""
        result = set([group])
        if depth < 10:
            for grp, sgrp in memberships:
                if group == grp and sgrp not in result:
                    result |= get_memberships(sgrp, memberships, depth+1)
        return result

    all_subgroups = list(db(
        'SELECT group_id, subgroup_id FROM subgroups ORDER BY subgroup_id'
    ))

    memberships = set([])
    for group in groups:
        memberships |= get_memberships(group, all_subgroups)

    return memberships


def named_groups(db, group_ids):
    """Returns names for a list of group ids"""
    result = []
    for _id, name in db('SELECT id, name FROM `groups`'):
        if _id in group_ids:
            result.append(name)
    return result


def get_subgroup_options(db, group_id):
    cmd = """
    select name, id
    from `groups`
    where id <> %s and left(groups.name, 2) <> 'a_'
    """
    return list(
        (name, str(id))
        for name, id in db(cmd, group_id)
    )


def get_role_options(db, group_id):
    cmd = """
    select name, id
    from `groups`
    where id <> %s and left(groups.name, 2) <> 'a_'
    """
    return list(
        (name, str(id))
        for name, id in db(cmd, group_id)
    )


class AdminModel(object):

    def __init__(self, db):
        self.db = db
        self.logger = logging.getLogger(__name__)
        self.groups = Groups(db)

    def log(self, message, *args):
        self.logger.debug(message, *args)

    def get_user_options(self):
        return sorted(
            (user.link, user.user_id) for user in Users(self.db)
        )

    def get_subgroup_options(self, group_id):
        return sorted(
            (group.link, group.group_id)
            for group in self.groups.find(**{'type': 'U'})
            if group.group_id != group_id
        )

    def get_role_options(self, group_id):
        return sorted(
            (group.link, group.group_id)
            for group in self.groups.find(**{'type': 'U'})
            if group.group_id != group_id
        )

    def get_app_options(self):
        groups_lookup = {
            group.name: group.group_id
            for group in zoom.system.site.groups.find(type='A')
        }
        return sorted([
            (
                app.title,
                groups_lookup.get('a_' + app.name, 'a_' + app.name)
            ) for app in zoom.system.site.apps
        ], key=repr)

    def update_group_apps(self, record):
        """Post updated group apps"""

        # create groups for uninstalled apps
        new_groups_required = set(
            app_key for app_key in record['apps']
            if isinstance(app_key, str) and app_key.startswith('a_')
        )
        for group_name in new_groups_required:
            app_name = group_name[2:]
            zoom.system.site.groups.add_app(app_name)

        groups_lookup = {
            group.name: group.group_id
            for group in zoom.system.site.groups.find(type='A')
        }
        new_keys = set(
            groups_lookup.get(app_key, app_key)
            for app_key in record['apps']
        )

        group = record
        group.update_apps_by_id(new_keys)

    def update_group_relationships(self, record):
        group = record
        group.update_members_by_id(group['users'])
        group.update_subgroups_by_id(group['subgroups'])
        group.update_roles_by_id(group['roles'])
        self.update_group_apps(record)


def get_index_metrics(db):

    def count(where, *args):
        """Return the result of a count query"""
        return '{:,}'.format((list(db('select count(*) from ' + where, *args))[0][0]))

    def avg(metric, where, *args):
        """Return the result of a query that calculates an average"""
        value = list(db('select avg({}) from {}'.format(metric, where), *args))[0][0]
        return '{:,.1f}'.format(value) if value else '-'

    the_day = today()
    host = zoom.system.request.host

    num_users = count('users where status="A"')
    num_groups = count('groups where type="U"')
    num_requests = count('log where status="C" and server=%s and timestamp>=%s', host, the_day)
    num_errors = count('log where status="E" and server=%s and timestamp>=%s', host, the_day)
    avg_speed = avg('elapsed', 'log where status="C" and server=%s and timestamp>=%s and path<>"/login"', host, the_day)
    num_authorizations = count('audit_log where timestamp>=%s', the_day)

    metrics = [
        ('Users', '/admin/users', num_users),
        ('Groups', '/admin/groups', num_groups),
        ('Requests Today', '/admin/requests', num_requests),
        ('Errors Today', '/admin/errors', num_errors),
        ('Performance (ms)', '/admin/requests', avg_speed),
        ('Authorizations Today', '/admin/audit', num_authorizations)
    ]
    return metrics


def update_user_groups(record):
    logger = logging.getLogger(__name__)
    db = context.site.db
    record_id = record['_id']

    existing_groups = set(
        group_id for group_id, in
        db('select group_id from members where user_id=%s', record_id)
    )
    logger.debug('existing_groups: %r', existing_groups)

    updated_groups = set(record['memberships'])
    logger.debug('updated_groups: %r', updated_groups)

    if updated_groups != existing_groups:
        if existing_groups - updated_groups:
            logger.debug('deleting: %r', existing_groups - updated_groups)
            cmd = 'delete from members where user_id=%s and group_id in %s'
            db(cmd, record_id, existing_groups - updated_groups)
        if updated_groups - existing_groups:
            logger.debug('inserting: %r', updated_groups - existing_groups)
            cmd = 'insert into members (user_id, group_id) values (%s, %s)'
            values = updated_groups - existing_groups
            sequence = zip([record_id] * len(values), values)
            db.execute_many(cmd, sequence)
    else:
        logger.debug('members unchanged')


def update_group_relationships(record):
    admin = AdminModel(context.site.db)
    admin.update_group_relationships(record)


def send_invitation(user):
    """Send invitation email"""
    password = uuid.uuid4().hex[-10:]
    user.set_password(password)
    site = zoom.system.site
    body = zoom.tools.load_content(
        'welcome', user=user, site=site, password=password)
    subject = 'Welcome - ' + site.name
    zoom.mail.send(user.email, subject, body)
    zoom.alerts.success(f'invitation sent to {user.username}')


def send_password(user, password):
    """Send password reset email"""
    site = zoom.system.site
    body = zoom.tools.load_content(
        'reset', user=user, site=site, password=password)
    subject = 'Password reset - ' + site.name
    zoom.mail.send(user.email, subject, body)


def admin_crud_policy():
    """Authourization policy for Admin app collections
    """
    def _policy(item, user, action):
        """Policy rules for shared collection"""

        def can_crud(user):
            """Return True if user can crud this collection
            """
            return user.is_admin or user.is_member('authorizers')

        actions = {
            'create': can_crud,
            'read': can_crud,
            'update': can_crud,
            'delete': can_crud,
        }

        if action not in actions:
            raise Exception('action missing: {}'.format(action))

        return actions.get(action)(user)
    return _policy


class AdminCollection(zoom.collect.Collection):
    """Admin app Collection"""

    allows = admin_crud_policy()


class GroupsCollection(AdminCollection):

    @property
    def has_many_records(self):
        return False

