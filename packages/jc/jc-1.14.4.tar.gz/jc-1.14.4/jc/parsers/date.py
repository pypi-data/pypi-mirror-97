"""jc - JSON CLI output utility `date` command output parser

Usage (cli):

    $ date | jc --date

    or

    $ jc date

Usage (module):

    import jc.parsers.date
    result = jc.parsers.date.parse(date_command_output)

Compatibility:

    'linux', 'darwin', 'freebsd'

Examples:

    $ date | jc --date -p
    {
      "year": 2020,
      "month_num": 7,
      "day": 31,
      "hour": 16,
      "minute": 48,
      "second": 11,
      "period": null,
      "month": "Jul",
      "weekday": "Fri",
      "weekday_num": 6,
      "timezone": "PDT"
    }

    $ date | jc --date -p -r
    {
      "year": "2020",
      "month": "Jul",
      "day": "31",
      "weekday": "Fri",
      "hour": "16",
      "minute": "50",
      "second": "01",
      "timezone": "PDT"
    }
"""
import jc.utils


class info():
    version = '1.1'
    description = 'date command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'freebsd']
    magic_commands = ['date']


__version__ = info.version


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data with the following schema:

        {
          "year":         integer,
          "month_num":    integer,
          "day":          integer,
          "hour":         integer,
          "minute":       integer,
          "second":       integer,
          "period":       string,
          "month":        string,
          "weekday":      string,
          "weekday_num":  integer,
          "timezone":     string
        }
    """
    month_map = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12
    }

    weekday_map = {
        "Sun": 1,
        "Mon": 2,
        "Tue": 3,
        "Wed": 4,
        "Thu": 5,
        "Fri": 6,
        "Sat": 7
    }

    if proc_data:
        return {
            "year": int(proc_data['year']),
            'month_num': month_map[proc_data['month']],
            "day": int(proc_data['day']),
            "hour": int(proc_data['hour']),
            "minute": int(proc_data['minute']),
            "second": int(proc_data['second']),
            "period": proc_data['period'] if 'period' in proc_data else None,
            "month": proc_data['month'],
            "weekday": proc_data['weekday'],
            "weekday_num": weekday_map[proc_data['weekday']],
            "timezone": proc_data['timezone']
        }
    else:
        return {}


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = {}

    if jc.utils.has_data(data):
        data = data.replace(':', ' ')
        split_data = data.split()

        # date v8.32 uses a different format depending on locale, so need to support LANG=en_US.UTF-8
        if len(split_data) == 9 and ('AM' in split_data or 'am' in split_data or 'PM' in split_data or 'pm' in split_data):
            raw_output = {
                "year": split_data[8],
                "month": split_data[1],
                "day": split_data[2],
                "weekday": split_data[0],
                "hour": split_data[3],
                "minute": split_data[4],
                "second": split_data[5],
                "period": split_data[6],
                "timezone": split_data[7]
            }
        else:
            # standard LANG=C date output
            raw_output = {
                "year": split_data[7],
                "month": split_data[1],
                "day": split_data[2],
                "weekday": split_data[0],
                "hour": split_data[3],
                "minute": split_data[4],
                "second": split_data[5],
                "timezone": split_data[6]
            }

    if raw:
        return raw_output
    else:
        return process(raw_output)
