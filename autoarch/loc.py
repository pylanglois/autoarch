#!/usr/bin/python
import tempfile

from plumbum import local, FG

from autoarch import get_root

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


def write_file(content, filename):
    cp = local["cp"]
    as_root = get_root()

    with tempfile.NamedTemporaryFile(mode='w+') as tmp:
        tmp.write(content)
        tmp.seek(0)
        as_root[cp['-f', filename, f"{filename}.bk"]] & FG
        as_root[cp['-f', tmp.name, filename]] & FG


def set_locale():
    as_root = get_root()
    ln = local["ln"]

    as_root[ln['-sf', '/usr/share/zoneinfo/America/Montreal', '/etc/localtime']] & FG
    write_file(LC_GEN, '/etc/locale.gen')
    as_root["locale-gen"] & FG
    write_file(LC_FR_CA, '/etc/locale.conf')
    write_file(VCON_KEYMAP, '/etc/vconsole.conf')


if __name__ == "__main__":
    set_locale()
