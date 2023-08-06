"""
    fills templates
"""

import re

parts_re = (
    r"""(\w+)\s*=\s*"([^"]*)"|"""
    r"""(\w+)\s*=\s*'([^']*)'|"""
    r"""(\w+)\s*=\s*([^\s]+)\s*|"""
    r""""([^"]*)"|"""
    r"""'([^']*)'|"""
    r"""(\w+)"""
)
tag_parts = re.compile(parts_re)

name_re = '[a-z0-9_.]+'
pattern_tpl = r'%s(' + name_re + r')\s*(.*?)%s'
patterns = {}


def _fill(tag_start, tag_end, text, callback):
    """do the actual work of filling in tags

    >>> def filler(name, *args, **kwargs):
    ...     if name == 'name':
    ...         return 'Joe'
    >>> _fill('<dz:', '>', 'Hello <dz:name>!', filler)
    'Hello Joe!'

    """

    def replace_tag(match):
        """replace a tag"""

        name = match.groups(1)[0].lower()
        rest = match.group(0)[len(name)+len(tag_start):-len(tag_end)]
        parts = tag_parts.findall(rest)
        keywords = dict(
            a and (a, b) or c and (c, d) or e and (e, f)
            for (a, b, c, d, e, f, g, h, i) in parts
            if a or c or e
        )
        args = [
            h or i or g or ""
            for (a, _, c, _, e, _, g, h, i) in parts
            if not (a or c or e)
        ]

        result = callback(name, *args, **keywords)
        if result is None:
            result = match.group(0)
        return str(result)

    tags = (tag_start, tag_end)
    if tags not in patterns:
        patterns[tags] = re.compile(
            pattern_tpl % (tag_start, tag_end),
            re.IGNORECASE
        )
    innerre = patterns[tags]

    result = []
    lastindex = 0

    for outermatch in re.finditer("<!--.*?-->", text):
        text_between = text[lastindex:outermatch.start()]
        new_text = innerre.sub(replace_tag, text_between)
        result.append(new_text)
        lastindex = outermatch.end()
        result.append(outermatch.group())
    text_after = text[lastindex:]
    result.append(innerre.sub(replace_tag, text_after))

    return ''.join(x for x in result)


def fill(text, callback):
    """fill tags in the double handlebars style

    >>> def filler(name, *args, **kwargs):
    ...     if name == 'name':
    ...         name = kwargs.get('language')=='french' and 'Jacques' or 'James'
    ...         if 'upper' in args:
    ...             return name.upper()
    ...         elif 'lower' in args:
    ...             return name.lower()
    ...         else:
    ...             return name
    ...
    >>> fill('Hello {{name}}!', filler)
    'Hello James!'
    >>> fill('Hello {{name language=\"french\"}}!', filler)
    'Hello Jacques!'
    >>> fill('Hello {{name upper}}!', filler)
    'Hello JAMES!'
    >>> fill('Hello {{name lower language=\"french\"}}!', filler)
    'Hello jacques!'
    >>> fill('Hello {{name lower language=french}}!', filler)
    'Hello jacques!'
    >>> fill('Hello {{name}}!', lambda a: None )
    'Hello {{name}}!'

    >>> values = {}
    >>> fill('Hello {{name}}!', values.get )
    'Hello {{name}}!'
    >>> fill('Hello {{name "World"}}!', values.get )
    'Hello World!'
    >>> values['name'] = 'Pat'
    >>> fill('Hello {{name "World"}}!', values.get )
    'Hello Pat!'
    >>> del values['name']
    >>> fill('Hello{{name ""}}!', values.get )
    'Hello!'

    >>> class Thing:
    ...     name = 'Widget'
    >>> thing = Thing()
    >>> thing.name
    'Widget'
    >>> def fill_this(template, *args, **kwargs):
    ...     def filler(name, *a, **k):
    ...         tpl = ('{'+name+'}')
    ...         result = tpl.format(*args, **kwargs)
    ...         return result
    ...     return fill(template, filler)
    >>> fill_this('A {{thing.name}}, {{person}}!', thing=thing, person='Ann')
    'A Widget, Ann!'

    """
    return dzfill(_fill('{{', '}}', text, callback), callback)


def custom_fill(tag_start, tag_end, text, callback):
    """fill tags in a custom style

    >>> def fill2(*args, **kwargs):
    ...     return custom_fill('\$\(\( ', '\)\)', *args, **kwargs)
    >>> def callback(name, *args, **kwargs):
    ...     return dict(first_name='Sam', last_name='Jones').get(name, 'unknown')
    >>> fill2('Hello $(( first_name ))', callback)
    'Hello Sam'
    >>> fill2('Hello $(( first_name )) $(( last_name ))', callback)
    'Hello Sam Jones'
    """
    return _fill(tag_start, tag_end, text, callback)


def dzfill(text, callback):
    """fill tags in the <dz: style"""
    return _fill('<dz:', '>', text, callback)

def dollar_fill(text, callback):
    """fill templates in the dollar style"""
    start, end = '\$\(\(\s*?', '\s*?\)\)'
    return custom_fill(start, end, text, callback)
