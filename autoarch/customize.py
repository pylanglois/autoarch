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

BASE_PACKAGES = [
    'man-db',
    'man-pages',
    'git',
    'usbutils',
    'postgresql-libs',
    'sshpass',
    'seahorse',
    'nemo-seahorse',
    'gnome-keyring',
    'libsecret',
    'networkmanager-openconnect',
    'netdata',
    'python-pip',
    'cronie',
    'p7zip',
    'linux-headers',
]

GUI_PACKAGES = [
    'cups',
    'xorg-server-xephyr',
    'cinnamon',
    'cinnamon-translations',
    'chromium',
    'gnome-system-monitor',
    'gnome-calculator',
    'system-config-printer',
    'lightdm',
    'lightdm-slick-greeter',
    'nemo-fileroller',
    'xdg-user-dirs',
    'vlc',
    'adobe-source-code-pro-fonts',
    'evince',
]

CLI_PACAKGES = [
    'zsh',
    'byobu',
    'htop',
    'bmon',
    'nmap',
    'sshfs',
    'sysstat',
    'whois',
    'rclone',
    'wget',
    's3cmd',
    'jre-openjdk',
    'docker',
    'p7zip',
    'github-cli',
    'python-poetry',
]

EXTRA_PACKAGES = [
    'variety',
    'gparted',
    'flameshot',
    'cheese',
    'playerctl',
    'obs-studio',
    'v4l2loopback-utils',
    'v4l2loopback-dkms',
    'dbeaver',
    'keepassxc',
    'redshift',
    'baobab',
    'gnuradio',
    'gnuradio-companion',
    'gnuradio-osmosdr',
    'krita',
    'gimp',
    'blender',
    'ttf-jetbrains-mono',
    'eog',
    'darktable',
    'nomacs',
    'mousetweaks',
]

AURS_ROOT = "$HOME/src/aur"
AURS = ['yay']
YAYS = [
    'timeshift',
    'sublime-text-4',
    'otpclient',
    'jetbrains-toolbox',
    'bcompare',
    'bcompare-cinnamon',
    'kopia-bin',
    'kopia-ui-bin',
    'apachedirectorystudio',
    'lightdm-settings',
    'hplip',
    'pyenv',
    'pyenv-virtualenv',
    'ttf-meslo-nerd-font-powerlevel10k',
    'zsh-theme-powerlevel10k',
    'spotify',
    'st',
    'lightdm-gdmflexiserver',
    'ocenaudio',
    'gqrx',
    'mbelib',
    'libsndfile',
    'itpp',
    'portaudio',
    'remmina-plugin-folder',
    'remmina-plugin-rdesktop',
    'youtube-dl',
    'gqrx',
    'brother-cups-wrapper-common',
    'tuxguitar',
    'soundfont-fluid',
    'fluidsynth',
    'libreoffice',
    'webcamoid',
    'guvcview',
    'geos',
    'gdal',
    'maven',
    'papirus-icon-theme',
]

PYTHON_VERSION = {
    '3.10.2': 'd310',
    '3.9.10': 'd39',
    '3.8.12': 'd38',
    '3.7.12': 'd37',
}

USER = getpass.getuser()
HOSTNAME = platform.node()

LANG = 'fr_CA.UTF-8'

LC_FR_CA = f"""
    LANG={LANG}
    LANGUAGE={LANG}
    LC_ADDRESS={LANG}
    LC_COLLATE={LANG}
    LC_CTYPE={LANG}
    LC_IDENTIFICATION={LANG}
    LC_MEASUREMENT={LANG}
    LC_MESSAGES={LANG}
    LC_MONETARY={LANG}
    LC_NAME={LANG}
    LC_NUMERIC={LANG}
    LC_PAPER={LANG}
    LC_TELEPHONE={LANG}
    LC_TIME={LANG}
    LC_ALL={LANG}
    """

LC_GEN = f"""
    {LANG} UTF-8
    en_US.UTF-8 UTF-8
    """

KEYMAP = 'cf'
VCON_KEYMAP = f"KEYMAP={KEYMAP}"


def main():
    install_base()
    slick_greeter()
    kopia_restore()
    restore_dconf()
    restore_crontab()
    create_timeshift_snapshot()


def create_timeshift_snapshot():
    timeshift = local["timeshift"]
    _ = as_root[timeshift['--create', '--comments', 'First backup - autoarch', '--tags', 'D']] & FG


def restore_dconf():
    dconf = local["dconf"]
    _ = (dconf['load', '/'] < local.env.expand('$HOME/.config/dconf/dconf.ini')) & FG


def restore_crontab():
    crontab = local["crontab"]
    _ = crontab[f"{local.env.expand('$HOME/.config/crontab/crontab')}"] & FG


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


def kopia_restore():
    kopia = local['kopia']
    kopia_config = local.path(local.env.expand("~/.config/kopia"))
    ok_to_restore = 'y'
    if not kopia_config.exists():
        ok_to_restore = input('Kopia configuration is not there! Continue? [y/N]')

    if ok_to_restore.lower() == 'y':
        snapshots = json.loads(kopia['snapshot', 'list', '--json']())
        _ = kopia['restore', '--parallel=16', snapshots[-1]['id'], local.env.expand('$HOME')] & FG


def install_base():
    update_pgp_keys()
    install_pacmans()
    enable_services()
    install_aur()
    install_yay()
    install_theme()
    set_locale()
    install_python()


def enable_services():
    systemctl = local['systemctl']
    _ = as_root[systemctl['enable', 'cups']] & FG
    _ = as_root[systemctl['enable', 'lightdm']] & FG
    _ = as_root[systemctl['enable', 'cronie']] & FG
    _ = as_root[systemctl['enable', 'netdata']] & FG
    _ = as_root[systemctl['enable', 'docker']] & FG
    _ = as_root[systemctl['enable', 'avahi-daemon']] & FG


def install_pacmans():
    pacman = local['pacman']
    usermod = local['usermod']
    _ = as_root[pacman['-S', '--noconfirm', BASE_PACKAGES, GUI_PACKAGES, CLI_PACAKGES, EXTRA_PACKAGES]] & FG
    _ = as_root[usermod['-aG', 'docker', USER]] & FG


def update_pgp_keys():
    pacman_key = local["pacman-key"]
    _ = as_root[pacman_key['--populate', 'archlinux']] & FG


def install_python():
    pyenv = local['pyenv']
    for version, venv in PYTHON_VERSION.items():
        _ = pyenv['install', '-f', version] & FG
        _ = pyenv['virtualenv', '-f', version, venv] & FG


def slick_greeter():
    mkdir = local['mkdir']
    chmod = local['chmod']
    groupadd = local['groupadd']
    usermod = local['usermod']
    setfacl = local['setfacl']
    sed = local['sed']

    variety_folder = "/usr/local/share/variety-data"

    _ = as_root[mkdir['-p', variety_folder]] & FG
    _ = as_root[chmod['g+w', variety_folder]] & FG
    _ = as_root[groupadd['-f', 'variety']] & FG
    _ = as_root[usermod['-aG', 'variety', USER]] & FG
    _ = as_root[setfacl['-dm', 'g:variety:rwX', variety_folder]] & FG
    _ = as_root[setfacl['-m', 'g:variety:rwX', variety_folder]] & FG
    _ = as_root[mkdir['-p', f'{variety_folder}/{USER}']] & FG

    ql = LocalCommand.QUOTE_LEVEL
    LocalCommand.QUOTE_LEVEL = 3
    _ = as_root[sed[
        '-i', "s/^#greeter-session=.*$/greeter-session=lightdm-slick-greeter/g", '/etc/lightdm/lightdm.conf']] & FG
    LocalCommand.QUOTE_LEVEL = ql


def install_theme():
    git = local['git']
    cp = local['cp']
    gtk_css_path = local.env.expand('$HOME/.config/gtk-3.0')
    create_folders(['$HOME/.themes', gtk_css_path])
    with tempfile.TemporaryDirectory() as dir_name:
        _ = git['clone', '--depth=1', '--filter=blob:none', '--sparse',
                'https://github.com/linuxmint/cinnamon-spices-themes.git', f'{dir_name}/themes',] & FG
        with local.cwd(f'{dir_name}/themes'):
            _ = git['sparse-checkout', 'set', 'Adapta-Nokto/files/Adapta-Nokto'] & FG
            _ = cp['-frv', f'{dir_name}/themes/Adapta-Nokto/files/Adapta-Nokto', gtk_css_path] & FG

    gtk_patch_path = pkg_resources.path('autoarch.files', f'.config_gtk-3.0_gtk.css')
    _ = cp['-frv', gtk_patch_path, f"{gtk_css_path}/gtk.css"] & FG


def set_locale():
    ln = local['ls']
    xdg_user_dirs_update = local['xdg_user_dirs_update']
    rm = local['rm']

    _ = as_root[ln['-sf', '/usr/share/zoneinfo/America/Montreal', '/etc/localtime']] & FG
    write_file(LC_GEN, '/etc/locale.gen')
    _ = as_root["locale-gen"] & FG
    write_file(LC_FR_CA, '/etc/locale.conf')
    write_file(VCON_KEYMAP, '/etc/vconsole.conf')
    _ = xdg_user_dirs_update & FG
    _ = rm['-fr', f"{local.env.expand('$HOME')}/Desktop"]
    _ = rm['-fr', f"{local.env.expand('$HOME')}/Downloads"]
    _ = rm['-fr', f"{local.env.expand('$HOME')}/Pictures"]
    _ = rm['-fr', f"{local.env.expand('$HOME')}/Templates"]
    _ = rm['-fr', f"{local.env.expand('$HOME')}/Music"]
    _ = rm['-fr', f"{local.env.expand('$HOME')}/Public"]


def install_aur():
    git = local['git']
    makepkg = local['makepkg']
    create_folders([AURS_ROOT])
    with local.cwd(local.env.expand(AURS_ROOT)):
        for aur in AURS:
            aur_dir = local.path(local.env.expand(f"{AURS_ROOT}/{aur}"))
            if not aur_dir.exists():
                _ = git['clone', f"https://aur.archlinux.org/{aur}.git", f"{aur_dir}"] & FG
            with local.cwd(aur_dir):
                _ = makepkg['-si', '--noconfirm'] & FG


def install_yay():
    yay = local['yay']
    _ = yay['-S', '--noconfirm', YAYS] & FG


if __name__ == "__main__":
    main()
