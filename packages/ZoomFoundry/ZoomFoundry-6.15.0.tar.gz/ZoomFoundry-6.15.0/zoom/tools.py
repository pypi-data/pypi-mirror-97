"""
    zoom.tools
"""

import datetime
import logging
import os
import uuid

import sass as libsass
from markdown import Markdown
from pypugjs.ext.html import process_pugjs as pug
from zoom.response import RedirectResponse
import zoom.helpers
from zoom.helpers import abs_url_for, url_for_page, url_for
from zoom.utils import trim, dedup
from zoom.render import apply_helpers

# Needed for access to zoom.system, which is circular if imported directly
# here.
import zoom

one_day = datetime.timedelta(1)
one_week = one_day * 7
one_hour = datetime.timedelta(hours=1)
one_minute = datetime.timedelta(minutes=1)


def now():
    """Return the current datetime"""
    return datetime.datetime.now()


def today():
    """Return the current date

    >>> today() == datetime.date.today()
    True
    """
    return datetime.date.today()


def yesterday(any_date=None):
    """Return date for yesterday

    >>> yesterday(datetime.date(2017, 12, 4))
    datetime.date(2017, 12, 3)

    >>> yesterday(datetime.date(2017, 1, 1))
    datetime.date(2016, 12, 31)
    """
    return (any_date or today()) - one_day


def tomorrow(any_date=None):
    """Return date for tomorrow

    >>> tomorrow(datetime.date(2017, 12, 3))
    datetime.date(2017, 12, 4)

    >>> tomorrow(datetime.date(2016, 12, 31))
    datetime.date(2017, 1, 1)
    """
    return (any_date or today()) + one_day


def first_day_of_the_month(any_date):
    """returns the first day of the month for any date

    >>> first_day_of_the_month(datetime.date(2016, 12, 31))
    datetime.date(2016, 12, 1)
    """
    return datetime.date(any_date.year, any_date.month, 1)


def last_day_of_the_month(any_date):
    """returns the last day of the month for any date

    >>> last_day_of_the_month(datetime.date(2016, 2, 1))
    datetime.date(2016, 2, 29)

    >>> last_day_of_the_month(datetime.datetime(2016, 2, 1, 1, 1, 1))
    datetime.date(2016, 2, 29)
    """
    next_month = any_date.replace(day=28) + datetime.timedelta(days=4)
    return first_day_of_the_month(next_month) - one_day


def first_day_of_next_month(any_date):
    """returns the first day of next month for any date

    >>> first_day_of_next_month(datetime.date(2016, 2, 1))
    datetime.date(2016, 3, 1)
    """
    return last_day_of_the_month(any_date) + one_day


def last_day_of_next_month(any_date):
    """returns the last day of next month for any date

    >>> last_day_of_next_month(datetime.date(2016, 2, 1))
    datetime.date(2016, 3, 31)
    """
    return last_day_of_the_month(first_day_of_next_month(any_date))


def first_day_of_last_month(any_date):
    """Returns the first day of last month for any date

    >>> first_day_of_last_month(datetime.date(2016, 1, 21))
    datetime.date(2015, 12, 1)
    """
    return first_day_of_the_month(last_day_of_last_month(any_date))


def last_day_of_last_month(any_date):
    """Returns the first day of last month for any date

    >>> last_day_of_last_month(datetime.date(2016, 1, 21))
    datetime.date(2015, 12, 31)
    """
    return first_day_of_the_month(any_date) - one_day


def this_month(any_date):
    """Returns date range for last month for any date

    >>> this_month(datetime.date(2016, 1, 21))
    (datetime.date(2016, 1, 1), datetime.date(2016, 1, 31))
    """
    return (first_day_of_the_month(any_date), last_day_of_the_month(any_date))


def next_month(any_date):
    """Returns date range for next month for any date

    >>> next_month(datetime.date(2016, 1, 21))
    (datetime.date(2016, 2, 1), datetime.date(2016, 2, 29))
    """
    return (first_day_of_next_month(any_date), last_day_of_next_month(any_date))


def last_month(any_date):
    """Returns date range for last month for any date

    >>> last_month(datetime.date(2016, 1, 21))
    (datetime.date(2015, 12, 1), datetime.date(2015, 12, 31))
    """
    return (first_day_of_last_month(any_date), last_day_of_last_month(any_date))


def how_long(time1, time2):
    """Returns a string that describes the difference between two times.

    >>> import time
    >>> now = now()

    >>> how_long(now, now)
    'a moment'

    >>> how_long(now, now + one_minute / 3)
    '20 seconds'

    >>> how_long(now, now + one_hour / 3)
    '20 minutes'

    >>> how_long(now, now + one_hour)
    '1 hour'

    >>> how_long(now, now + one_day / 3)
    '8 hours'

    >>> how_long(now, now + one_day)
    '1 day'

    >>> how_long(now, now + 2 * one_day)
    '2 days'

    >>> how_long(now, now + 15 * one_day)
    '2 weeks'

    >>> how_long(now, now + 35 * one_day)
    'over a month'

    >>> how_long(now, now + 65 * one_day)
    'over 2 months'

    >>> how_long(now, now + 361 * one_day)
    'almost a year'

    >>> how_long(now, now + 20 * one_minute)
    '20 minutes'

    >>> how_long(now, now + 2 * 365 * one_day)
    'almost two years'

    >>> how_long(now, now + 3.25 * 365 * one_day)
    'over 3 years'

    >>> how_long(now, now + 1.25 * 365 * one_day)
    'over a year'

    >>> how_long(today(), tomorrow(today()))
    '1 day'

    >>> how_long(today(), now + one_week)
    '7 days'

    >>> how_long(now, time.time())
    'a moment'

    >>> failed = False
    >>> try:
    ...    how_long(now, None)
    ... except TypeError:
    ...    failed = True
    >>> failed
    True

    """
    #pylint: disable=R0912

    def as_datetime(anytime):
        """Convert value to datetime"""
        if isinstance(anytime, datetime.datetime):
            return anytime
        elif isinstance(anytime, datetime.date):
            return datetime.datetime(anytime.year, anytime.month, anytime.day)
        elif anytime is None:
            msg = 'date, datetime or timestamp required (None passed)'
            raise TypeError(msg)
        else:
            return datetime.datetime.fromtimestamp(anytime)

    diff = as_datetime(time2) - as_datetime(time1)

    if diff.days > 365*2:
        result = 'over %d years' % (diff.days / 365)
    elif diff.days > 365*1.75:
        result = 'almost two years'
    elif diff.days > 365:
        result = 'over a year'
    elif diff.days > 360:
        result = 'almost a year'
    elif diff.days > 60:
        result = 'over %d months' % (diff.days / 30)
    elif diff.days > 30:
        result = 'over a month'
    elif diff.days > 14:
        result = '%d weeks' % (diff.days / 7)
    elif diff.days > 1:
        result = '%d days' % diff.days
    elif diff.days == 1:
        result = '1 day'
    elif diff.seconds > 7200:
        result = '%d hours' % int(diff.seconds / 3600)
    elif int(diff.seconds) >= 3600:
        result = '1 hour'
    elif diff.seconds > 60:
        result = '%d minutes' % int(diff.seconds / 60)
    elif diff.seconds > 0:
        result = '%d seconds' % int(diff.seconds)
    else:
        result = 'a moment'
    return result

def how_long_ago(anytime, since=None):
    """
    Returns a string that describes the difference between any time and now.

    >>> now = now()

    >>> how_long_ago(now - datetime.timedelta(1) * 2)
    '2 days ago'

    >>> how_long_ago(now + 20 * one_minute)
    '19 minutes from now'

    >>> how_long_ago(now - 20 * one_minute)
    '20 minutes ago'

    >>> how_long_ago(now - 20 * one_minute, now - 10 * one_minute)
    '10 minutes ago'

    """

    def as_datetime(anytime):
        """Convert value to datetime"""
        if isinstance(anytime, datetime.datetime):
            return anytime
        elif isinstance(anytime, datetime.date):
            return datetime.datetime(anytime.year, anytime.month, anytime.day)
        elif anytime is None:
            msg = 'date, datetime or timestamp required (None passed)'
            raise TypeError(msg)
        else:
            return datetime.datetime.fromtimestamp(anytime)

    right_now = since or now()
    if as_datetime(anytime) < right_now:
        return how_long(anytime, right_now) + ' ago'
    else:
        return how_long(right_now, anytime) + ' from now'


def is_listy(obj):
    """test to see if an object will iterate like a list

    >>> is_listy([1,2,3])
    True

    >>> is_listy(set([3,4,5]))
    True

    >>> is_listy((3,4,5))
    True

    >>> is_listy(dict(a=1, b=2))
    False

    >>> is_listy('123')
    False
    """
    return isinstance(obj, (list, tuple, set))


def ensure_listy(obj):
    """ensure object is wrapped in a list if it can't behave like one

    >>> ensure_listy('not listy')
    ['not listy']

    >>> ensure_listy(['already listy'])
    ['already listy']

    >>> ensure_listy([])
    []
    """
    if is_listy(obj):
        return obj
    return [obj]


class Redirector(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def render(self, request):
        """render redirect"""

        location = url_for(*self.args, **self.kwargs)
        location = zoom.render.render(location)
        location = abs_url_for(location)
        location = zoom.render.render(location)

        logger = logging.getLogger(__name__)
        logger.debug('redirecting to: %r', location)
        return RedirectResponse(location)



def redirect_to(*args, **kwargs):
    """Return a redirect response for a URL."""
    return Redirector(*args, **kwargs)


def partial(*args, **kwargs):
    """Return a partial HTML response."""
    content = zoom.Component(*args, **kwargs)
    return zoom.response.HTMLResponse(content.render())


def home(view=None):
    """Redirect to application home.

    """
    if view:
        return redirect_to(url_for_page(view))
    return redirect_to(url_for_page())


def unisafe(val):
    """safely convert to unicode

    >>> unisafe(None)
    ''

    >>> unisafe(b'123')
    '123'

    >>> unisafe(
    ...     b'\\xe3\\x81\\x93\\xe3\\x82\\x93\\xe3\\x81\\xab\\xe3\\x81'
    ...     b'\\xa1\\xe3\\x81\\xaf\\xe4\\xb8\\x96\\xe7\\x95\\x8c'
    ... )
    'こんにちは世界'

    >>> unisafe(1)
    '1'

    """
    if val is None:
        return ''
    elif isinstance(val, bytes):
        try:
            val = val.decode('utf-8')
        except:
            val = val.decode('Latin-1')
    elif not isinstance(val, str):
        val = str(val)
    return val


def websafe(content):
    """Return htmlquoted version of content

    >>> websafe(b'This could be <problematic>')
    'This could be &lt;problematic&gt;'
    """
    return hide_helpers(htmlquote(unisafe(content)))


def htmlquote(text):
    """Encodes `text` for raw use in HTML.

    >>> htmlquote(u"<'&\\">")
    '&lt;&#39;&amp;&quot;&gt;'

    >>> htmlquote("<'&\\">")
    '&lt;&#39;&amp;&quot;&gt;'
    """
    replacements = (
        ('&', '&amp;'),
        ('<', '&lt;'),
        ('>', '&gt;'),
        ("'", '&#39;'),
        ('"', '&quot;'),
    )
    for replacement in replacements:
        text = text.replace(*replacement)
    return text


def get_markdown_converter():
    """Return a configured markdown converter

    >>> markdown("a [[wikilink]] test")
    '<p>a <a class="wikilink" href="wikilink.html">wikilink</a> test</p>'

    >>> markdown("a [[wikilink.html]] test")
    '<p>a [[wikilink.html]] test</p>'
    """
    def make_page_name(text):
        result = []
        for c in text.lower():
            if c in 'abcdefghijklmnopqrstuvwxyz01234567890.-/':
                result.append(c)
            elif c == ' ':
                result.append('-')
        text = ''.join(result)
        if text.endswith('.html'):
            text = text[:-5]
        return text

    def url_builder(label, base, end):
        return make_page_name(label) + '.html'

    markdown_logger = logging.getLogger('MARKDOWN')
    markdown_logger.setLevel(logging.WARNING)

    extras = ['tables', 'def_list', 'wikilinks', 'toc']
    configs = {'wikilinks': [('build_url', url_builder)]}
    converter = Markdown(extensions=extras, extension_configs=configs)
    return converter


markdown_converter = get_markdown_converter()  # TODO: decorator instead?


def markdown(content):
    """Transform content with markdown

    >>> markdown('this **is** bold')
    '<p>this <strong>is</strong> bold</p>'
    """
    return markdown_converter.convert(trim(content))


def load(pathname, encoding='utf-8'):
    """Read a file and return the contents"""

    logger = logging.getLogger(__name__)
    logger.debug('load %r', pathname)
    with open(pathname, encoding=encoding) as reader:
        return reader.read()

def safe_format(__content, *args, **kwargs):
    """
    Perform a brace-style string format, leaving double curly braces
    unchanged (they would normally be treated as an escape of a single brace).

    >>> '{{a}} {b}'.format(b=1)
    '{a} 1'
    >>> safe_format('{{a}} {b}', b=1)
    '{{a}} 1'
    """
    # XXX: This approach trades runtime efficiency for implementation
    # simplicity. It could be improved in the future.

    # Create (functionally) universally unique tokens to replace double curly
    # braces during the format.
    open_helper = uuid.uuid4().hex
    close_helper = uuid.uuid4().hex

    # Swap double curly braces for their tokens, format, then restore them.
    content = close_helper.join(open_helper.join(
        __content.split('{{')
    ).split('}}'))
    content = content.format(*args, **kwargs)
    content = '{{'.join('}}'.join(content.split(
        close_helper
    )).split(open_helper))
    return content


def apply_helpers_and_format(template, *args, **kwargs):
    """
    Apply keyword arguments as Zoom helpers to `template`, then all provided
    arguments except for `template` as standard brace-style format parameters,
    in that order.

    Missing format parameters result in a `KeyError`, while un-matched helpers
    are left as is (presumably to be filled later in the request).

    >>> apply_helpers_and_format('{{a}} {{b "B"}} {c} {{d}}', a='A', c='C')
    'A B C {{d}}'

    >>> apply_helpers_and_format('{{a}} {{b "B"}} {c} {{d}}', a='A', c='C', d='{{e}}', e='{{a}}')
    'A B C A'

    >>> apply_helpers_and_format('{a}')
    Traceback (most recent call last):
        ...
    KeyError: 'a'

    """
    after_helpers = apply_helpers(template, None, [kwargs])
    return safe_format(after_helpers, *args, **kwargs)


def load_content(pathname, *args, **kwargs):
    """
    Load the content template from the given file, then apply the remaining
    arguments as helpers and standard brace-style format parameters. See
    `zoom.tools.apply_helpers_and_format()` for behaviour.
    """
    isfile = os.path.isfile

    if not isfile(pathname):
        for extension in ['html', 'md', 'txt', 'pug']:
            if isfile(pathname + '.' + extension):
                pathname = pathname + '.' + extension
                break

    template = load(pathname)
    if template:
        content = apply_helpers_and_format(template, *args, **kwargs)
        if pathname.endswith('.html'):
            result = content
        elif pathname.endswith('.pug'):
            basedir = os.path.realpath(os.path.split(pathname)[0])
            result = pug(content, options=dict(basedir=basedir))
        else:
            result = markdown(content)
        return result
    return ''


def load_template(name, default=None):
    """
    Load a template from the theme folder.

    Templates usually have .html file extensions and this module
    will assume that's what is desired unless otherwise specified.
    """

    def find_template(name):
        for path in templates_paths:
            if os.path.exists(path) and (name in os.listdir(path)):
                return os.path.join(path, name)
        name_lower = name.lower()
        for path in templates_paths:
            if os.path.exists(path):
                for filename in os.listdir(path):
                    if filename.lower() == name_lower:
                        return os.path.join(path, filename)

    def load_template_file(name, default):
        pathname = find_template(name)
        if pathname:
            if os.path.exists(pathname):

                if site.theme_comments == 'path':
                    source = pathname
                elif site.theme_comments == 'name':
                    source = name[:-5]
                else:
                    source = None

                t = load(pathname)

                if source and pathname[-5:].lower() == '.html':
                    result = (
                        '\n'
                        '<!-- source: %s -->\n'
                        '%s\n'
                        '<!-- end source: %s -->\n' % (source, t, source)
                    )
                else:
                    result = t
                return result

        logger = logging.getLogger(__name__)
        if default is None:
            logger.warning('template missing: %r', name)
        logger.debug('templates paths: %r', templates_paths)

        if default:
            return default

        if site.theme_comments == 'path':
            comment = '%r missing in %r ' % (name, templates_paths)
        elif site.theme_comments == 'name':
            comment = 'missing %r ' % (name)
        else:
            comment = 'missing '

        return default or '<!-- template %s-->' % comment

    site = zoom.system.request.site

    app = getattr(zoom.system.request, 'app', None)
    app_templates_paths = app.templates_paths if app else []

    templates_paths = dedup(app_templates_paths + site.templates_paths)

    if not '.' in name:
        name = name + '.html'

    if '/' in name or '\\' in name:
        raise Exception(
            'Unable to use specified template path.  '
            'Templates are located in theme folders.'
        )

    return site.templates.setdefault(name, load_template_file(name, default))

def get_template(template_name='default', theme='default'):
    """Get site template"""

    logger = logging.getLogger(__name__)
    path = zoom.system.site.themes_path
    isfile = os.path.isfile

    pathname = os.path.realpath(
        os.path.join(path, theme, template_name + '.html')
    )
    alt_pathname = pathname.endswith('.html') and pathname[:-4] + 'pug'
    default_pathname = os.path.realpath(
        os.path.join(
            zoom.tools.zoompath(
                'zoom/_assets/web/themes/default',
                template_name + '.pug'
            )
        )
    )
    logger.debug('default_pathname: %r', alt_pathname)

    if isfile(pathname):
        logger.debug('get_template %r', pathname)
        with open(pathname, 'rb') as reader:
            return reader.read().decode('utf8')

    elif alt_pathname and isfile(alt_pathname):
        basedir = os.path.split(alt_pathname)[0]
        logger.debug('get_template %r', alt_pathname)
        logger.debug('basedir %r', basedir)
        with open(alt_pathname, 'rb') as reader:
            return zoom.tools.pug(reader.read().decode('utf8'), basedir=basedir)

    elif default_pathname and isfile(default_pathname):
        basedir = os.path.split(default_pathname)[0]
        logger.debug('get_template %r', default_pathname)
        logger.debug('basedir %r', basedir)
        with open(default_pathname, 'rb') as reader:
            return zoom.tools.pug(reader.read().decode('utf8'), basedir=basedir)

    else:
        if template_name == 'default':
            logger.error('default template %s missing', pathname)
            raise zoom.exceptions.ThemeTemplateMissingException(
                'Default template missing %r' % pathname
            )
        return get_template('default', theme)

def zoompath(*args):
    """Returns the location of a standard Zoom asset

    >>> import os
    >>> theme_path = zoompath('zoom', '_assets', 'web', 'themes', 'default')
    >>> os.path.exists(theme_path)
    True

    """
    realpath = os.path.realpath
    dirname = os.path.dirname
    join = os.path.join
    return realpath(join(realpath(dirname(zoom.__file__)), '..', *args))


def hide_helpers(content):
    """prevent helper requests from being filled"""
    return content.replace('{{', '[[raw!').replace('}}', '-raw]]')


def restore_helpers(content):
    """Restores content helpers to their usual form"""
    return content.replace('[[raw!', '{{').replace('-raw]]', '}}')


def sass(text):
    """Convert SASS to CSS

    >>> tpl = '''
    ... .fancy
    ...   color: red
    ... '''
    >>> sass(tpl)
    '.fancy {\\n  color: red; }\\n'

    """
    if text.endswith('.sass'):
        out = libsass.compile(filename=text)
    else:
        out = libsass.compile(string=text, indented=True)
    return out
