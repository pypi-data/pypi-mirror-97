import sys

import click
from tabulate import tabulate

from . import main
from .pretty import print_info, print_warn, print_error
from ..session import Session


@main.group()
def dotfile():
    '''Provides dotfile operations.'''


@dotfile.command()
@click.argument('path', metavar='PATH')
@click.option('--perm', 'permission',
             help='Linux permission represented in octal number (e.g. 755) '
                  'Defaults to 755 if not specified')
@click.option('-f', '--file', 'dotfile_path',
              help='Path to dotfile to upload. '
                   'If not specified, client will try to read file from STDIN. ')
@click.option('-o', '--owner', '--owner-access-key', 'owner_access_key', metavar='ACCESS_KEY',
              help='Set the owner of the target session explicitly.')
def create(path, permission, dotfile_path, owner_access_key):
    '''
    Store dotfile to Backend.AI Manager.
    Dotfiles will be automatically loaded when creating kernels.

    PATH: Where dotfiles will be created when starting kernel
    '''

    if dotfile_path:
        with open(dotfile_path, 'r') as fr:
            body = fr.read()
    else:
        body = ''
        for line in sys.stdin:
            body += (line + '\n')
    with Session() as session:
        try:
            if not permission:
                permission = '755'
            dotfile_ = session.Dotfile.create(body, path, permission,
                                              owner_access_key=owner_access_key)
            print_info(f'Dotfile {dotfile_.path} created and ready')
        except Exception as e:
            print_error(e)
            sys.exit(1)


@dotfile.command()
@click.argument('path', metavar='PATH')
@click.option('-o', '--owner', '--owner-access-key', 'owner_access_key', metavar='ACCESS_KEY',
              help='Specify the owner of the target session explicitly.')
def get(path, owner_access_key):
    '''
    Print dotfile content
    '''
    with Session() as session:
        try:
            dotfile_ = session.Dotfile(path, owner_access_key=owner_access_key)
            body = dotfile_.get()
            print(body['data'])
        except Exception as e:
            print_error(e)
            sys.exit(1)


@dotfile.command()
def list():
    '''
    List all availabe dotfiles by user.
    '''
    fields = [
        ('Path', 'path', None),
        ('Data', 'data', lambda v: v[:30].splitlines()[0]),
        ('Permission', 'permission', None),
    ]
    with Session() as session:
        try:
            resp = session.Dotfile.list_dotfiles()
            if not resp:
                print('There is no dotfiles created yet.')
                return
            rows = (
                tuple(
                    item[key] if transform is None else transform(item[key])
                    for _, key, transform in fields
                )
                for item in resp
            )
            hdrs = (display_name for display_name, _, _ in fields)
            print(tabulate(rows, hdrs))
        except Exception as e:
            print_error(e)
            sys.exit(1)


@dotfile.command()
@click.argument('path', metavar='PATH')
@click.option('--perm', 'permission',
             help='Linux permission represented in octal number (e.g. 755) '
                  'Defaults to 755 if not specified')
@click.option('-f', '--file', 'dotfile_path',
              help='Path to dotfile to upload. '
                   'If not specified, client will try to read file from STDIN. ')
@click.option('-o', '--owner', '--owner-access-key', 'owner_access_key', metavar='ACCESS_KEY',
              help='Specify the owner of the target session explicitly.')
def update(path, permission, dotfile_path, owner_access_key):
    '''
    Update dotfile stored in Backend.AI Manager.
    '''

    if dotfile_path:
        with open(dotfile_path, 'r') as fr:
            body = fr.read()
    else:
        body = ''
        for line in sys.stdin:
            body += (line + '\n')
    with Session() as session:
        try:
            if not permission:
                permission = '755'
            dotfile_ = session.Dotfile(path, owner_access_key=owner_access_key)
            dotfile_.update(body, permission)
            print_info(f'Dotfile {dotfile_.path} updated')
        except Exception as e:
            print_error(e)
            sys.exit(1)


@dotfile.command()
@click.argument('path', metavar='PATH')
@click.option('-f', '--force', type=bool, is_flag=True,
              help='Delete dotfile without confirmation.')
@click.option('-o', '--owner', '--owner-access-key', 'owner_access_key', metavar='ACCESS_KEY',
              help='Specify the owner of the target session explicitly.')
def delete(path, force, owner_access_key):
    '''
    Delete dotfile from Backend.AI Manager.
    '''
    with Session() as session:
        dotfile_ = session.Dotfile(path, owner_access_key=owner_access_key)
        if not force:
            print_warn('Are you sure? (y/[n])')
            result = input()
            if result.strip() != 'y':
                print_info('Aborting.')
                exit()
        try:
            dotfile_.delete()
            print_info(f'Dotfile {dotfile_.path} deleted')
        except Exception as e:
            print_error(e)
            sys.exit(1)
