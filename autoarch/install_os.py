#!/usr/bin/python
"""
This script will install my arch linux
"""
import getpass
import platform
import tempfile

from plumbum import local, FG
from plumbum.machines import LocalCommand

from autoarch import get_root

as_root = get_root()

BASE_PACKAGES = [
    'man-db',
    'man-pages',
    'postgresql-libs',
    'seahorse',
    'nemo-seahorse',
    'gnome-keyring',
    'libsecret',
    'networkmanager-openconnect',
    'netdata',
    'python-pip',
    'cronie',
    'exfat-utils',
    'ntfs-3g',
    # 'linux-headers',
]

GUI_PACKAGES = [
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
    # 'evince',
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
    'usbutils',
    'github-cli',
    'python-poetry',
]

EXTRA_PACKAGES = [
    'gparted',
    'playerctl',
    'v4l2loopback-utils',
    'v4l2loopback-dkms',
    'redshift',
    'baobab',
    'ttf-jetbrains-mono',
]

PACMANS = [
    *BASE_PACKAGES,
    *GUI_PACKAGES,
    *CLI_PACAKGES,
    *EXTRA_PACKAGES,
]

AURS_ROOT = "$HOME/src/aur"
AURS = ['yay']

YAYS_BASE = [
    'otpclient',
    'kopia-bin',
    'kopia-ui-bin',
    'lightdm-settings',
    'remmina-plugin-folder',
    'remmina-plugin-rdesktop',
    'hplip',
    'mdatp',
]

YAYS_GQRX = [
    'gqrx',
    'mbelib',
    'libsndfile',
    'itpp',
]

YAYS_OPTIONALS = [
    'spotify',
    'ocenaudio-bin',
    'hexchat',
    'krita',
    'gimp',
    'obs-studio',
    'vlc',
    'variety',
    'flameshot',
    'evince',
    'onlyoffice',
    'caprine',
]

YAYS_CAMERA = [
    'webcamoid',
    'guvcview',
]

YAYS_DEV_TOOLS = [
    'jetbrains-toolbox',
    'sublime-text-4',
    'bcompare',
    'bcompare-cinnamon',
    'apachedirectorystudio',
    'pyenv',
    'pyenv-virtualenv',
    'ttf-meslo-nerd-font-powerlevel10k',
    'zsh-theme-powerlevel10k',
    'maven',
    'dbeaver',
    'keepassxc',
    'adobe-source-code-pro-fonts',
    'git',
    'sshpass',
    '1password',
]

YAYS = [
    *YAYS_BASE,
    *YAYS_GQRX,
    *YAYS_OPTIONALS,
    *YAYS_CAMERA,
    *YAYS_DEV_TOOLS,
    # 'st',
    # 'lightdm-gdmflexiserver',
    # 'youtube-dl',
    # 'brother-cups-wrapper-common',
    # 'libreoffice',
    # 'geos',
    # 'gdal',
    # 'papirus-icon-theme',
]

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


def install_base():
    update_pgp_keys()
    install_pacmans()
    enable_services()
    install_aurs()
    install_yay_packages()
    set_locale()


def enable_services():
    systemctl = local['systemctl']
    # _ = as_root[systemctl['enable', 'cups']] & FG
    _ = as_root[systemctl['enable', 'lightdm']] & FG
    _ = as_root[systemctl['enable', 'cronie']] & FG
    _ = as_root[systemctl['enable', 'netdata']] & FG
    _ = as_root[systemctl['enable', 'docker']] & FG


def install_pacmans():
    pacman = local['pacman']
    usermod = local['usermod']
    _ = as_root[pacman['-S', '--noconfirm', PACMANS]] & FG
    _ = as_root[usermod['-aG', 'docker', USER]] & FG


def update_pgp_keys():
    pacman_key = local["pacman-key"]
    _ = as_root[pacman_key['--populate', 'archlinux']] & FG


def set_locale():
    ln = local['ls']
    xdg_user_dirs_update = local['xdg_user_dirs_update']
    rm = local['rm']

    _ = as_root[ln['-sf', '/usr/share/zoneinfo/America/Montreal', '/etc/localtime']] & FG
    write_file(LC_GEN, '/etc/locale.gen')
    _ = as_root["locale-gen"] & FG
    write_file(LC_FR_CA, '/etc/locale.conf')
    write_file(VCON_KEYMAP, '/etc/vconsole.conf')


def install_aurs():
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


def install_yay_packages():
    yay = local['yay']
    _ = yay['-S', '--noconfirm', YAYS] & FG


def slick_greeter():
    sed = local['sed']
    ql = LocalCommand.QUOTE_LEVEL
    LocalCommand.QUOTE_LEVEL = 3
    _ = as_root[sed[
        '-i', "s/^#greeter-session=.*$/greeter-session=lightdm-slick-greeter/g", '/etc/lightdm/lightdm.conf']] & FG
    LocalCommand.QUOTE_LEVEL = ql


if __name__ == "__main__":
    main()
