import json

from .. import PScLineType, PScLine, PSc


class PScObjEncoder(json.JSONEncoder):
    '''Convert PSc object to a dict structure
    '''

    def default(self, obj):
        if isinstance(obj, PSc):
            return {
                'class': 'PSc',
                'title': obj.title,
                'author': obj.author,
                'chars': obj.chars,
                'lines': obj.lines,
            }
        else:
            return super().default(obj)


class PScLineObjEncoder(json.JSONEncoder):
    '''Convert PScLine object to a dict structure
    '''

    def default(self, obj):
        if isinstance(obj, PScLine):
            line_dict = {
                'class': 'PScLine',
                'type': obj.type.name,
            }
            if hasattr(obj, 'name'):
                line_dict['name'] = obj.name
            if hasattr(obj, 'text'):
                line_dict['text'] = obj.text
            return line_dict
        else:
            return super().default(obj)


class PScEncoder(PScObjEncoder, PScLineObjEncoder):
    '''Encode whole PSc object to a JSON string
    '''
    pass


def psc_dump(sc, fp, cls=PScEncoder, ensure_ascii=False, **kwargs):
    '''Serialize a PSc object and stream it to file-like object
    '''
    kwargs['cls'] = cls
    kwargs['ensure_ascii'] = ensure_ascii
    return json.dump(sc, fp, **kwargs)


def psc_dumps(sc, cls=PScEncoder, ensure_ascii=False, **kwargs):
    '''Serialize a PSc object to str object
    '''
    kwargs['cls'] = cls
    kwargs['ensure_ascii'] = ensure_ascii
    return json.dumps(sc, **kwargs)


def _psc_dict_hook(obj):
    '''Decode a dict with entry class:PSc into PSc object
    '''
    if type(obj) == dict and obj.get('class') == 'PSc':
        title = obj.get('title', '')
        author = obj.get('author', '')
        chars = obj.get('chars', [])
        lines = obj.get('lines', [])

        sc = PSc(title=title, author=author, chars=chars, lines=lines)
        return sc
    else:
        return obj


def _psc_line_dict_hook(obj):
    '''Decode a dict with entry class:PScLine into PScLine object
    '''
    if type(obj) == dict and obj.get('class') == 'PScLine':
        line_type = PScLineType[obj['type']]
        name = obj.get('name')
        text = obj.get('text')

        line = PScLine(line_type, name=name, text=text)
        return line
    else:
        return obj


def _psc_hook(obj):
    '''Decode any dict contained in encoded PSc object
    '''
    hooks = [_psc_dict_hook, _psc_line_dict_hook]
    for hook in hooks:
        obj = hook(obj)
    return obj


def psc_load(fp, object_hook=_psc_hook, **kwargs):
    '''Deserialize a stream from file-like object into PSc object
    '''
    kwargs['object_hook'] = object_hook
    return json.load(fp, **kwargs)


def psc_loads(s, object_hook=_psc_hook, **kwargs):
    '''Deserialize a str object into PSc object
    '''
    kwargs['object_hook'] = object_hook
    return json.loads(s, **kwargs)
