from plumbum.cmd import sudo

AS_ROOT = None


def get_root():
    global AS_ROOT
    if not AS_ROOT:
        AS_ROOT = sudo["-u", 'root']
    return AS_ROOT
