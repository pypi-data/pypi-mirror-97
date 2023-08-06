"""Differ extension for JSON data.
"""

from functools import partial
import json

import fitb
import graphtage


def json_diff(extension_config, accepted, received):
    accepted_text = accepted.data.decode(
        extension_config['encoding'])
    accepted_tree = graphtage.json.build_tree(
        json.loads(accepted_text)) 

    received_text = received.data.decode(
        extension_config['encoding'])
    received_tree = graphtage.json.build_tree(
        json.loads(received_text)) 
 
    diff = accepted_tree.diff(received_tree)
    with graphtage.DEFAULT_PRINTER as p:
        graphtage.json.JSONFormatter.DEFAULT_INSTANCE.print(p, diff)


def extension(extension_point):
    extension_point.add(
        name='json',
        description='Differ for json data.',
        config_options=(fitb.Option(
            'encoding', 'Encoding of JSON data', 'utf-8'),),
        activate=lambda full, ext: partial(json_diff, ext))
