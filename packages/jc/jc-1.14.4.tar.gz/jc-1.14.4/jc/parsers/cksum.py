"""jc - JSON CLI output utility `cksum` command output parser

This parser works with the following checksum calculation utilities:
- `sum`
- `cksum`

Usage (cli):

    $ cksum file.txt | jc --cksum

    or

    $ jc cksum file.txt

Usage (module):

    import jc.parsers.cksum
    result = jc.parsers.cksum.parse(cksum_command_output)

Compatibility:

    'linux', 'darwin', 'cygwin', 'aix', 'freebsd'

Examples:

    $ cksum * | jc --cksum -p
    [
      {
        "filename": "__init__.py",
        "checksum": 4294967295,
        "blocks": 0
      },
      {
        "filename": "airport.py",
        "checksum": 2208551092,
        "blocks": 3745
      },
      {
        "filename": "airport_s.py",
        "checksum": 1113817598,
        "blocks": 4572
      },
      ...
    ]
"""
import jc.utils


class info():
    version = '1.0'
    description = 'cksum command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Parses cksum and sum program output'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'aix', 'freebsd']
    magic_commands = ['cksum', 'sum']


__version__ = info.version


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data with the following schema:

        [
          {
            "filename":     string,
            "checksum":     integer,
            "blocks":       integer
          }
        ]
    """

    for entry in proc_data:
        int_list = ['checksum', 'blocks']
        for key in int_list:
            if key in entry:
                try:
                    entry[key] = int(entry[key])
                except (ValueError):
                    entry[key] = None
    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = []

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            item = {
                'filename': line.split(maxsplit=2)[2],
                'checksum': line.split(maxsplit=2)[0],
                'blocks': line.split(maxsplit=2)[1]
            }
            raw_output.append(item)

    if raw:
        return raw_output
    else:
        return process(raw_output)
