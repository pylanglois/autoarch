#!/usr/bin/python
"""
This script will install my arch linux
"""
import importlib.resources as pkg_resources
import getpass
import platform
import tempfile
import json
from plumbum import local, FG
from plumbum.machines import LocalCommand
from autoarch import get_root

as_root = get_root()

PYTHON_VERSION = {
    '3.11.2': 'd311',
    '3.10.10': 'd310',
    '3.9.16': 'd39',
}

USER = getpass.getuser()


def write_file(content, filename):
    cp = local['cp']
    with tempfile.NamedTemporaryFile(mode='w+') as tmp:
        tmp.write(content)
        tmp.seek(0)
        _ = as_root[cp['-f', filename, f"{filename}.bk"]] & FG
        _ = as_root[cp['-f', tmp.name, filename]] & FG


def create_folders(folder_list):
    if not isinstance(folder_list, list):
        raise Exception("folder_list needs to be a list of folder.")
    for folder in folder_list:
        folder_path = local.path(local.env.expand(folder))
        if not folder_path.exists():
            folder_path.mkdir()


def main():
    kopia_config = local.path(local.env.expand("~/.config/kopia"))
    ok_to_restore = 'y'
    if not kopia_config.exists():
        ok_to_restore = input('Kopia configuration is not there! Continue? [y/N]')

    if ok_to_restore.lower() == 'y':
        xdg_folders()
        remove_titlebar()
        variety()
        kopia_restore()
        restore_dconf()
        restore_crontab()


def xdg_folders():
    xdg_user_dirs_update = local['xdg_user_dirs_update']
    rm = local['rm']

    _ = xdg_user_dirs_update & FG
    _ = rm['-fr', f"{local.env.expand('$HOME')}/Desktop"]
    _ = rm['-fr', f"{local.env.expand('$HOME')}/Downloads"]
    _ = rm['-fr', f"{local.env.expand('$HOME')}/Pictures"]
    _ = rm['-fr', f"{local.env.expand('$HOME')}/Templates"]
    _ = rm['-fr', f"{local.env.expand('$HOME')}/Music"]
    _ = rm['-fr', f"{local.env.expand('$HOME')}/Public"]


def remove_titlebar():
    cp = local['cp']
    gtk_css_path = local.env.expand('$HOME/.config/gtk-3.0')
    create_folders([gtk_css_path])
    gtk_patch_path = pkg_resources.path('autoarch.files', f'.config_gtk-3.0_gtk.css')
    _ = cp['-frv', gtk_patch_path, f"{gtk_css_path}/gtk.css"] & FG


def variety():
    mkdir = local['mkdir']
    chmod = local['chmod']
    groupadd = local['groupadd']
    usermod = local['usermod']
    setfacl = local['setfacl']

    variety_folder = "/usr/local/share/variety-data"

    _ = as_root[mkdir['-p', variety_folder]] & FG
    _ = as_root[chmod['g+w', variety_folder]] & FG
    _ = as_root[groupadd['-f', 'variety']] & FG
    _ = as_root[usermod['-aG', 'variety', USER]] & FG
    _ = as_root[setfacl['-dm', 'g:variety:rwX', variety_folder]] & FG
    _ = as_root[setfacl['-m', 'g:variety:rwX', variety_folder]] & FG
    _ = as_root[mkdir['-p', f'{variety_folder}/{USER}']] & FG


def kopia_restore():
    kopia = local['kopia']
    snapshots = json.loads(kopia['snapshot', 'list', '--json']())
    _ = kopia['restore', '--parallel=16', snapshots[-1]['id'], local.env.expand('$HOME')] & FG


def restore_dconf():
    dconf = local["dconf"]
    _ = (dconf['load', '/'] < local.env.expand('$HOME/.config/dconf/dconf.ini')) & FG


def restore_crontab():
    crontab = local["crontab"]
    _ = crontab[f"{local.env.expand('$HOME/.config/crontab/crontab')}"] & FG


def install_python():
    pyenv = local['pyenv']
    for version, venv in PYTHON_VERSION.items():
        _ = pyenv['install', '-f', version] & FG
        _ = pyenv['virtualenv', '-f', version, venv] & FG


if __name__ == "__main__":
    main()
