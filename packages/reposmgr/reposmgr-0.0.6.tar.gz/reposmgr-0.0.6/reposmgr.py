#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Script to manage (actually only to read) repos file, and construct various
# informations from it.
#
# IMPORTANT: keep it simple, DON'T USE ANYTHING APART FROM STANDARD LIBRARY.
import os
import sys
from collections import namedtuple, OrderedDict


REPOS_ROOT         = os.environ.get('REPOS_ROOT', os.getcwd())
DEFAULT_REPOS_FILE = os.environ.get('REPOS_FILE', os.path.abspath('%s/.repos' % os.getcwd()))
ACCESS_TOKEN_FILE  = os.environ.get('ACCESS_TOKEN_FILE', '')
ACCESS_TOKEN       = None
PROPERTY_NAMES     = ['name', 'url', 'relative_path', 'is_main']
ALL_PROPERTY_NAMES = PROPERTY_NAMES + ['path', 'clone_url']


def log(msg):
    print (msg)


def get_access_token():
    global ACCESS_TOKEN
    if ACCESS_TOKEN:
        return ACCESS_TOKEN
    if not ACCESS_TOKEN_FILE:
        return None
    if not os.path.exists(ACCESS_TOKEN_FILE):
        return None
    with open(ACCESS_TOKEN_FILE, 'r') as fd:
        ACCESS_TOKEN = fd.read().strip()
    return ACCESS_TOKEN


class Repo(namedtuple('Repo', PROPERTY_NAMES)):
    @property
    def path(self):
        return '{repos_root}/{r.relative_path}'.format(repos_root=REPOS_ROOT, r=self)

    @property
    def clone_url(self):
        token = get_access_token()
        if not token:
            if self.url.startswith('git@'):
                return '{r.url}'.format(r=self)
            return 'https://{r.url}'.format(r=self)
        return 'https://{token}:{token}@{r.url}'.format(token=token, r=self)


def deserialize(row, is_main=False):
    name, the_rest = row.split('=')
    repo_url, relative_path = the_rest.rsplit(':', 1)
    return Repo(name, repo_url, relative_path, is_main)


def serialize(repo, append_new_line=False):
    new_line = '\n' if append_new_line else ''
    return u'{r.name}={r.url}:{r.path}{new_line}'.format(r=repo, new_line=new_line)


def load_repos(filepath=DEFAULT_REPOS_FILE):
    with open(filepath, 'r') as fd:
        data = []
        for n, row in enumerate(fd.readlines()):
            row = row.strip()
            if not row:
                continue
            is_main = n == 0
            data.append(deserialize(row.strip(), is_main))
        return OrderedDict((r.name, r) for r in data)


def get_properties(repos, repo_name, prop_names, separator=' '):
    result = []
    repo = repos[repo_name]
    for name in prop_names:
        result.append(getattr(repo, name))
    return separator.join(result)


# sanity check
def ensure_valid_operation_name(name):
    if name not in OPERATIONS:
        sys.stderr.write('[ERROR] "{name}" is not valid operation name ({operations})\n'.format(
            name=name,
            operations=', '.join(OPERATIONS.keys()),
        ))
        sys.exit(1)


def ensure_correct_names(prop_names, possible_names):
    for pname in prop_names:
        msg = '%s not in %s' % (pname, possible_names)
        if pname not in possible_names:
            sys.stderr.write('[ERROR] Wrong property name: %s\n' % msg)
            sys.exit(1)
# end / sanity check


# operations
def display_repo_property(repo_name, prop_names):
    repos = load_repos()
    log(get_properties(repos, repo_name, prop_names))


def display_all():
    repos = load_repos()
    for repo in repos.values():
        log(get_properties(repos, repo.name, ['name', 'url', 'path'], separator='\t'))


def display_properties(prop_names):
    repos = load_repos()
    for repo in repos.values():
        log(get_properties(repos, repo.name, prop_names, separator='\t'))


def display_main_repo():
    repos = load_repos()
    for repo in repos.values():
        if repo.is_main:
            log(repo.name)
            break
# end / operations


OPERATIONS = {
    'repo_property': display_repo_property,
    'display_all': display_all,
    'properties': display_properties,
    'main_repo': display_main_repo,
}


def format_usage(script_name):
    msg = ('\n'.join([
        'Usage:',
        '',
        '  # Display all stored info about repositories',
        '  {script_name} display_all',
        '',
        '  # Display given repo property',
        '  {script_name} repo_property <repo-name> [{properties}]',
        '',
        '  # Display given properties of all stored repos',
        '  {script_name} properties [{properties}]',
    ]))
    msg = msg.format(script_name=os.path.basename(script_name),
                     properties=','.join(ALL_PROPERTY_NAMES))
    return msg


def main():
    script_name, args = sys.argv[0], sys.argv[1:]
    if len(args) == 0:
        sys.stderr.write('%s\n' % format_usage(script_name))
        sys.exit(1)

    operation_name = args[0]
    ensure_valid_operation_name(operation_name)

    if operation_name == 'display_all':
        display_all()
        sys.exit(0)

    if operation_name == 'main_repo':
        display_main_repo()
        sys.exit(0)

    if operation_name == 'repo_property':
        if len(args) != 3:
            sys.stderr.write((
                '[ERROR]: not enough arguments for "%s"\n'
                '\n'
                '%s'
                '\n'
            ) % (operation_name, format_usage(script_name)))
            sys.exit(1)
        __, repo_name, props = args
        props = props.split(',')
        ensure_correct_names(props, ALL_PROPERTY_NAMES)
        display_repo_property(repo_name, props)
        sys.exit(0)

    if operation_name == 'properties':
        if len(args) != 2:
            sys.stderr.write((
                '[ERROR]: not enough arguments for "%s"\n'
                '\n'
                '%s'
                '\n'
            ) % (operation_name, format_usage(script_name)))
            sys.exit(1)
        __, props = args
        props = props.split(',')
        ensure_correct_names(props, ALL_PROPERTY_NAMES)
        display_properties(props)
        sys.exit(0)


if __name__ == '__main__':
    main()
