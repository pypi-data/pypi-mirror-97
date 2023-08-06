import logging
import datetime
import pytz
import dateutil
from dateutil.parser import parse as dateparser
import re
from collections import namedtuple

from mjooln.core.seed import Seed
from mjooln.core.glass import Glass

logger = logging.getLogger(__name__)


# TODO: Same date in all examples?
# TODO: Move examples to separate documentation page?


class ZuluError(Exception):
    pass


class Zulu(datetime.datetime, Seed, Glass):
    # TODO: Revise documentation
    # TODO: Round to millisecond etc. And floor. Check Arrow how its done
    # TODO: Move elf doc to elf method
    """Timezone aware datetime objects in UTC

    Create using constructor::

        Zulu() or Zulu.now()
            Zulu(2020, 5, 21, 20, 5, 31, 930343)

        Zulu(2020, 5, 12)
            Zulu(2020, 5, 12)

        Zulu(2020, 5, 21, 20, 5, 31)
            Zulu(2020, 5, 21, 20, 5, 31)

    Zulu.seed() is a string on the format ``<date>T<time>u<microseconds>Z``,
    and is \'designed\'
    to be file name and double click friendly, as well as easily recognizable
    within some string when using regular expressions.
    Printing a Zulu object returns seed, and Zulu can be created using
    from_seed()::

        z = Zulu(2020, 5, 12)
        print(z)
            20200512T000000u000000Z

        z.seed()
            '20200512T000000u000000Z'

        str(z)
            '20200512T000000u000000Z'

        Zulu.from_seed('20200512T000000u000000Z')
        z = Zulu(2020, 5, 12)

    For an ISO 8601 formatted string, use custom function::

        z = Zulu('20200521T202041u590718Z')
        z.iso()
            '2020-05-21T20:20:41.590718+00:00'

    Similarly, Zulu can be created from ISO string::

        Zulu.from_iso('2020-05-21T20:20:41.590718+00:00')
            Zulu(2020, 5, 21, 20, 20, 41, 590718)


    Inputs or constructors may vary, but Zulu objects are *always* UTC. Hence
    the name Zulu.

    Constructor also takes regular datetime objects, provided they have
    timezone info::

        dt = datetime.datetime(2020, 5, 23, tzinfo=pytz.utc)
        Zulu(dt)
            Zulu(2020, 5, 23, 0, 0, tzinfo=<UTC>)

        dt = datetime.datetime(2020, 5, 23, tzinfo=dateutil.tz.tzlocal())
        Zulu(dt)
            Zulu(2020, 5, 22, 22, 0, tzinfo=<UTC>)

    Zulu has element access like datetime, in addition to string convenience
    attributes::

        z = Zulu()
        print(z)
            20200522T190137u055918Z
        z.month
            5
        z.str.month
            '05'
        z.str.date
            '20200522'
        z.str.time
            '190137'

    Zulu has a delta convenience function for timedelta, as well as a function
    to add deltas directly to generate a new Zulu::

        Zulu.delta(hours=1)
            datetime.timedelta(seconds=3600)

        z = Zulu(2020, 1, 1)
        z.add(days=2)
            Zulu(2020, 1, 3)

    For more flexible ways to create a Zulu object, see :meth:`Zulu.elf`

    .. warning:: Elves are fickle and rude


    """

    _ZuluStr = namedtuple('ZuluStr', [
        'year',
        'month',
        'day',
        'hour',
        'minute',
        'second',
        'microsecond',
        'date',
        'time',
        'seed',
    ])

    _FORMAT = '%Y%m%dT%H%M%Su%fZ'
    REGEX = r'\d{8}T\d{6}u\d{6}Z'
    LENGTH = 23

    ISO_REGEX_STRING = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-' \
                       r'(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):' \
                       r'([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-]' \
                       r'(?:2[0-3]|[01][0-9]):[0-5][0-9])?$'
    ISO_REGEX = re.compile(ISO_REGEX_STRING)

    ############################################################################
    # String methods
    ############################################################################

    @classmethod
    def is_iso(cls, str_):
        # TODO: Use regex instead, and include check on timezone (optional)
        """Check if input string is
        `ISO 8601 <https://en.wikipedia.org/wiki/ISO_8601>`_

        Check is done using regex ``Zulu.ISO_REGEX``

        :param ts_str: Maybe an ISO formatted string
        :return: True if str_ is iso, False if not
        :rtype: bool
        """
        try:
            if cls.ISO_REGEX.match(str_) is not None:
                return True
        except:
            pass
        return False

    ############################################################################
    # Timezone methods
    ############################################################################

    @classmethod
    def all_timezones(cls):
        """
        Returns a list of all allowed timezone names

        Timezone \'local\' will return a datetime object with local timezone,
        but is not included in this list

        Wrapper for ``pytz.all_timezones``

        :return: List of timezones
        :rtype: list
        """
        return pytz.all_timezones

    @classmethod
    def _to_utc(cls, ts):
        return ts.astimezone(pytz.utc)

    @classmethod
    def _tz_from_name(cls, tz='utc'):
        if tz == 'local':
            tz = dateutil.tz.tzlocal()
        else:
            try:
                tz = pytz.timezone(tz)
            except pytz.exceptions.UnknownTimeZoneError as ue:
                raise ZuluError(f'Unknown timezone: \'{tz}\'. '
                                f'Use Zulu.all_timezones() for a list '
                                f'of actual timezones')
        return tz

    ############################################################################
    # Create methods
    ############################################################################

    @classmethod
    def now(cls,
            tz=None):
        """
        Overrides ``datetime.datetime.now()``. Equivalent to ``Zulu()``

        :raise ZuluError: If parameter ``tz`` has a value. Even if value is UTC
        :param tz: Do not use. Zulu is always UTC
        :return: Zulu
        """
        if tz:
            raise ZuluError(f'Zulu.now() does not allow input time zone info. '
                            f'Zulu is always UTC. Hence the name')
        return cls()

    @classmethod
    def _from_unaware(cls, ts, tz=None):
        if not tz:
            raise ZuluError('No timezone info. Set timezone to use '
                            'with \'tz=<timezone string>\'. \'local\' will '
                            'use local timezone info. Use '
                            'Zulu.all_timezones() for a list of actual '
                            'timezones')
        return ts.replace(tzinfo=cls._tz_from_name(tz))

    @classmethod
    def _elf(cls, ts, tz=None):
        # Takes a datetime.datetime object and adds the input tzinfo if
        # none is present
        if not ts.tzinfo:
            ts = cls._from_unaware(ts, tz=tz)
        return ts

    @classmethod
    def from_unaware(cls, ts, tz='utc'):
        """ Create Zulu from timezone unaware datetime

        :param ts: Unaware time stamp
        :type ts: datetime.datetime
        :param tz: Time zone, with 'utc' as default.
            'local' will use local time zone
        :return: Zulu
        :rtype: Zulu
        """
        if ts.tzinfo:
            raise ZuluError(f'Input datetime already has '
                            f'time zone info: {ts}. '
                            f'Use constructor or Zulu.elf()')
        else:
            ts = cls._from_unaware(ts, tz=tz)
        return cls(ts)

    @classmethod
    def from_unaware_local(cls, ts):
        """ Create Zulu from timezone unaware local timestamp

        :param ts: Timezone unaware datetime
        :type ts: datetime.datetime
        :return: Zulu
        :rtype: Zulu
        """
        return cls.from_unaware(ts, tz='local')

    @classmethod
    def from_unaware_utc(cls, ts):
        """ Create Zulu from timezone unaware UTC timestamp

        :param ts: Timezone unaware datetime
        :type ts: datetime.datetime
        :return: Zulu
        :rtype: Zulu
        """
        return cls.from_unaware(ts, tz='utc')

    @classmethod
    def _parse_iso(cls,
                   iso: str):
        ts = dateparser(iso)
        if ts.tzinfo and str(ts.tzinfo) == 'tzutc()':
            ts = ts.astimezone(pytz.utc)
        return ts

    @classmethod
    def from_iso(cls,
                 str_: str,
                 tz=None):
        """
        Create Zulu object from ISO 8601 string

        :param iso: ISO 8601 string
        :param tz: Timezone string to use if missing in ts_str
        :return: Zulu
        :rtype: Zulu
        """
        ts = cls._parse_iso(str_)
        if tz and not ts.tzinfo:
            ts = cls._from_unaware(ts, tz)
        elif ts.tzinfo and tz:
            raise ZuluError(f'Timezone info found in ISO string as well as '
                            f'input timezone argument (tz). Keep tz=None, '
                            f'or use Zulu.elf()')
        elif not tz and not ts.tzinfo:
            raise ZuluError('No timezone info in neither ISO string '
                            'nor tz argument')
        return cls(ts)

    @classmethod
    def _parse(cls,
               ts_str: str,
               pattern: str):
        return datetime.datetime.strptime(ts_str, pattern)

    @classmethod
    def parse(cls,
              ts_str: str,
              pattern: str,
              tz=None):
        """Parse time stamp string with the given pattern

        :param ts_str: Timestamp string
        :type ts_str: str
        :param pattern: Follows standard
            `python strftime reference <https://strftime.org/>`_
        :param tz: Timezone to use if timestamp does not have timezone info
        :return: Zulu
        """
        ts = cls._parse(ts_str, pattern)
        if not ts.tzinfo:
            ts = cls._from_unaware(ts, tz=tz)
        elif tz:
            raise ZuluError('Cannot have an input timezone argument when '
                            'input string already has timezone information')
        return cls(ts)

    @classmethod
    def from_seed(cls, str_: str):
        """
        Create Zulu object from Zulu seed

        :param str_: Zulu seed
        :return: Zulu
        :rtype: Zulu
        """
        if not cls.is_seed(str_):
            raise ZuluError(f'String is not Zulu seed: {str_}')
        ts = cls._parse(str_, cls._FORMAT)
        ts = cls._from_unaware(ts, tz='utc')
        return cls(ts)

    @classmethod
    def _from_epoch(cls, epoch):
        ts = datetime.datetime.utcfromtimestamp(epoch)
        return ts.replace(tzinfo=pytz.UTC)

    @classmethod
    def from_epoch(cls, epoch):
        """
        Create Zulu object from UNIX Epoch

        :param epoch: Unix epoch
        :type epoch: float
        :return: Zulu
        :rtype: Zulu
        """
        ts = cls._from_epoch(epoch)
        return cls(ts)

    @classmethod
    def _fill_args(cls, args):
        if len(args) < 8:
            # From date
            args = list(args)
            args += (8 - len(args)) * [0]
            if args[1] == 0:
                args[1] = 1
            if args[2] == 0:
                args[2] = 1
            args = tuple(args)

        if args[-1] not in [None, 0, pytz.utc]:
            raise ZuluError(f'Zulu can only be UTC. '
                            f'Invalid timezone: {args[-1]}')

        args = list(args)
        args[-1] = pytz.utc
        return tuple(args)



    @classmethod
    def elf(cls, *args, tz='local'):
        """General input Zulu constructor

        .. warning:: Elves are fickle and rude

        ``Zulu.elf()`` takes the same inputs as constructor, and also allows Zulu
        objects to pass through. If timeozone is missing it will assume the input
        timezone ``tz``, which is set to local as default

        It takes both seed strings and iso strings::

            Zulu.elf('20201112T213732u993446Z')
                Zulu(2020, 11, 12, 21, 37, 32, 993446)

            Zulu.elf('2020-11-12T21:37:32.993446+00:00')
                Zulu(2020, 11, 12, 21, 37, 32, 993446)

        It takes UNIX epoch::

            e = Zulu(2020, 1, 1).epoch()
            e
                1577836800.0
            Zulu.elf(e)
                Zulu(2020, 1, 1)

        It will guess the missing values if input integers are not a full date
        and/or time::

            Zulu.elf(2020)
                Zulu(2020, 1, 1)

            Zulu.elf(2020, 2)
                Zulu(2020, 2, 1)

            Zulu.elf(2020,1,1,10)
                Zulu(2020, 1, 1, 10, 0, 0)

        .. warning:: Elves are fickle and rude

        :param args: Input arguments
        :param tz: Time zone to assume if missing. 'local' will use local
            time zone. Use Zulu.all_timezones() for a list of actual
            timezones. Default is 'local'
        :return: Zulu
        """
        ts = None
        if len(args) == 0:
            return cls()
        elif len(args) > 1:
            args = cls._fill_args(args)
            ts = datetime.datetime(*args)
            if not ts.tzinfo:
                ts = cls._from_unaware(ts, tz)
        elif len(args) == 1:
            arg = args[0]
            if isinstance(arg, Zulu):
                return arg
            elif isinstance(arg, datetime.datetime):
                # Add timzone if missing
                ts = cls._elf(arg, tz=tz)
                return cls(ts)
            elif isinstance(arg, float):
                return cls.from_epoch(arg)
            elif isinstance(arg, int):
                # Instantiate as start of year
                return cls(arg, 1, 1)
            elif isinstance(arg, str):
                if cls.is_seed(arg):
                    return cls.from_seed(arg)
                elif cls.is_iso(arg):
                    ts = cls._parse_iso(arg)
                    # Add timzone if missing
                    ts = cls._elf(ts, tz=tz)
                else:
                    raise ZuluError(f'String is neither zulu, nor ISO: {arg}. '
                                    f'Use Zulu.parse() and enter the format '
                                    f'yourself')
            else:
                raise ZuluError(f'Found no way to interpret input '
                                f'argument as Zulu: {arg} [{type(arg)}]')
        return cls(ts)

    @classmethod
    def range(cls,
              start=None,
              n=10,
              delta=datetime.timedelta(hours=1)):
        """Generate a list of Zulu of fixed intervals

        .. warning:: Mainly for dev purposes. There are far better
            ways of creating a range of timestamps, such as using pandas.

        :param start: Start time Zulu, default is *now*
        :type start: Zulu
        :param n: Number of timestamps in range, with default 10
        :type n: int
        :param delta: Time delta between items, with default one hour
        :type delta: datetime.timedelta
        :return: [Zulu]
        """
        if not start:
            start = cls()
        return [Zulu.elf(start + x * delta) for x in range(n)]

    def __new__(cls, *args, **kwargs):
        if len(args) == 0 and len(kwargs) == 0:
            ts = datetime.datetime.utcnow()
            ts = ts.replace(tzinfo=pytz.UTC)
        elif len(args) == 1 and len(kwargs) == 0:
            arg = args[0]
            if isinstance(arg, str):
                raise ZuluError('Cannot instantiate Zulu with a string. Use '
                                'Zulu.from_iso(), Zulu.from_seed(), '
                                'Zulu.from_string() or Zulu.parse()')
            elif isinstance(arg, float):
                raise ZuluError(f'Cannot create Zulu object from a float: '
                                f'{arg}; If float is unix epoch, '
                                f'use Zulu.from_epoch()')
            elif isinstance(arg, Zulu):
                raise ZuluError(f'Input argument is already Zulu: {arg}. '
                                f'Use Zulu.elf() for a softer, but more '
                                f'fickle approach')
            elif isinstance(arg, datetime.datetime):
                ts = arg
                if not ts.tzinfo:
                    raise ZuluError('Cannot create Zulu from datetime if '
                                    'datetime object does not have timezone '
                                    'info. Use Zulu.from_unaware()')
                ts = ts.astimezone(pytz.UTC)
            else:
                raise ZuluError(f'Unable to interpret input argument: '
                                f'{arg} [{type(arg).__name__}]')
        else:
            # Handle input as regular datetime input (year, month, day etc)
            try:
                ts = datetime.datetime(*args)
            except TypeError as te:
                raise ZuluError from te
            # Add timezone info if missing (assume utc, of course)
            if not ts.tzinfo:
                ts = ts.replace(tzinfo=pytz.UTC)

        # Create actual object
        args = tuple([ts.year, ts.month, ts.day,
                      ts.hour, ts.minute, ts.second,
                      ts.microsecond, ts.tzinfo])
        self = super().__new__(cls, *args)
        seed = self.strftime(self._FORMAT)
        self.str = self._ZuluStr(
            year=seed[:4],
            month=seed[4:6],
            day=seed[6:8],
            hour=seed[9:11],
            minute=seed[11:13],
            second=seed[13:15],
            microsecond=seed[16:22],
            date=seed[:8],
            time=seed[9:15],
            seed=seed,
        )
        return self

    def __str__(self):
        return self.str.seed

    def __repr__(self):
        times = [self.hour, self.minute, self.second]
        has_micro = self.microsecond > 0
        has_time = sum(times) > 0
        nums = [self.year, self.month, self.day]
        if has_time or has_micro:
            nums += times
        if has_micro:
            nums += [self.microsecond]
        numstr = ', '.join([str(x) for x in nums])
        return f'Zulu({numstr})'

    def epoch(self):
        """
        Get UNIX epoch (seconds since January 1st 1970)

        Wrapper for ``datetime.datetime.timestamp()``

        :return: Seconds since January 1st 1970
        :rtype: float
        """
        return self.timestamp()

    @classmethod
    def from_str(cls, str_):
        if cls.is_seed(str_):
            return cls.from_seed(str_)
        elif cls.is_iso(str_):
            return cls.from_iso(str_)
        else:
            raise ZuluError(f'Unknown string format (neither seed nor iso): '
                            f'{str_}; '
                            f'Use Zulu.parse() to specify format pattern and '
                            f'timezone')

    def iso(self, full=False):
        # TODO: Implement full flag
        """Create `ISO 8601 <https://en.wikipedia.org/wiki/ISO_8601>`_ string

        Example::

            z = Zulu(2020, 5, 21)
            z.iso()
                '2020-05-21T00:00:00+00:00'

        :return: str
        """
        if full:
            raise ZuluError('Full isoformat not implemented. Full means it '
                            'has fixed length no matter the value. Is needed '
                            'for certain document database based tools')
        return self.isoformat()

    def format(self, pattern):
        """Format Zulu to string with the given pattern

        :param pattern: Follows standard
            `Python strftime reference <https://strftime.org/>`_
        :return: str
        """
        return self.strftime(pattern)

    def to_unaware(self):
        """
        Get timezone unaware datetime object in UTC

        :return: Timezone unaware datetime
        :rtype: datetime.datetime
        """
        return datetime.datetime.utcfromtimestamp(self.epoch())

    def to_tz(self, tz='local'):
        """ Create regular datetime with input timezone

        For a list of timezones use :meth:`.Zulu.all_timezones()`, which is a
        wrapper for

        :param tz: Time zone to use. 'local' will return the local time zone.
            Default is 'local'
        :return: datetime.datetime
        """
        ts_utc = datetime.datetime.utcfromtimestamp(self.epoch())
        ts_utc = ts_utc.replace(tzinfo=pytz.UTC)
        return ts_utc.astimezone(self._tz_from_name(tz))

    def to_local(self):
        """ Create regular datetime with local timezone

        :return: datetime.datetime
        """
        return self.to_tz(tz='local')

    @classmethod
    def delta(cls,
              days=0,
              hours=0,
              minutes=0,
              seconds=0,
              microseconds=0,
              weeks=0):
        """Wrapper for datetime.timedelta

        :param days: Number of days
        :param hours: Number of hours
        :param minutes: Number of minutes
        :param seconds: Number of seconds
        :param microseconds: Number of microseconds
        :param weeks: Number of weeks
        :return: datetime.timedelta
        """
        return datetime.timedelta(days=days,
                                  hours=hours,
                                  minutes=minutes,
                                  seconds=seconds,
                                  microseconds=microseconds,
                                  weeks=weeks)

    def add(self,
            days=0,
            hours=0,
            minutes=0,
            seconds=0,
            microseconds=0,
            weeks=0):
        """Adds the input to current Zulu object and returns a new one

        :param days: Number of days
        :param hours: Number of hours
        :param minutes: Number of minutes
        :param seconds: Number of seconds
        :param microseconds: Number of microseconds
        :param weeks: Number of weeks
        :return: Zulu
        """
        delta = self.delta(days=days,
                           hours=hours,
                           minutes=minutes,
                           seconds=seconds,
                           microseconds=microseconds,
                           weeks=weeks)
        return self + delta
