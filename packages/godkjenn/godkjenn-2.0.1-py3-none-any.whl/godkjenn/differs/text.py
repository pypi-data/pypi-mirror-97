import difflib
from functools import partial

import fitb


def text_diff(extension_config, accepted, received):
    accepted_text = accepted.data.decode(
        extension_config['encoding'])

    received_text = received.data.decode(
        extension_config['encoding'])

    from io import StringIO
    diff = difflib.unified_diff(
        list(StringIO(accepted_text)),
        list(StringIO(received_text)),
        lineterm="")

    return '\n'.join(diff)


def extension(extension_point):
    extension_point.add(
        name='text',
        description='Differ for text files.',
        config_options=(fitb.Option(
            'encoding', 'Encoding of files', 'utf-8'),),
        activate=lambda full, ext: partial(text_diff, ext))
