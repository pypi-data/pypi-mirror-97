import difflib


def binary_diff(accepted, received):
    diff = difflib.diff_bytes(
        difflib.unified_diff,
        [accepted.data],
        [received.data],
        lineterm=b"")
    return b'\n'.join(diff)


def extension(extension_point):
    extension_point.add(
        name='binary',
        description='Differ for binary files.',
        activate=lambda _full, _ext: binary_diff)
