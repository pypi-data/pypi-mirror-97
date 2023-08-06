'''Classes to make up play script object.
'''
import re
from enum import Enum


class PScLineType(Enum):
    '''Types for PScLine.
    '''
    TITLE = 0                   # Title
    AUTHOR = 1                  # Author name
    CHARSHEADLINE = 2           # Headline of character list
    CHARACTER = 3               # Character
    H1 = 4                      # Headline of scene (level 1)
    H2 = 5                      # Headline of scene (level 2)
    H3 = 6                      # Headline of scene (level 3)
    DIRECTION = 7               # Direction
    DIALOGUE = 8                # Dialogue
    ENDMARK = 9                 # End mark
    COMMENT = 10                # Comment
    EMPTY = 11                  # Empty line
    CHARACTER_CONTINUED = 12    # Following lines of Character
    DIRECTION_CONTINUED = 13    # Following lines of Direction
    DIALOGUE_CONTINUED = 14     # Following lines of Dialogue
    COMMENT_CONTINUED = 15      # Foloowing lines of Comment


class PScLine:
    '''Line in PSc lines.
    '''
    # Opening and closing brackets for text in dialogue lines.
    # More than one characters can be set and matched as each.
    # In addition, space character is used as name-text delimiter implicitly.
    dlg_brackets = ('「', '」')

    def __init__(self, line_type, name=None, text=None):
        '''Constructor.

        Parameters
        ----------
        line_type : playscript.PScLineType
        name : str
        text : str
        '''
        try:
            self.type = PScLineType(line_type)
        except ValueError:
            raise TypeError(
                'Argument "line_type" should be a PScLineType member.')

        if line_type in (PScLineType.CHARACTER, PScLineType.DIALOGUE):
            if not name:
                raise ValueError(
                    'Argument "name" is required '
                    'for type CHARACTER or DIALOGUE.')

        if line_type not in (PScLineType.EMPTY, PScLineType.CHARACTER):
            if not text:
                raise ValueError(
                    'Argument "text" is required '
                    'for the other types than EMPTY or CHARACTER.')

        if name:
            self.name = name
        if text:
            self.text = text

    @classmethod
    def from_text(cls, line_type, text, *, default_name='*',
                  dlg_brackets=None):
        '''Make PScLine object from PScLineType and a text.

        Parameters
        ----------
        line_type : playscript.PScLineType
        text : str
            Input text that the PScLine object is made from.
        default_name : str
            Used as name if no space or bracket in text.
        dlg_brackets : list-like[str]
            Tuple/list of opening bracket chars and closing bracket chars.

        Returns
        -------
        line : playscript.PScLine
        '''
        # Delimiter of name and text in character lines.
        chr_delimiter = re.compile(r'\s+')

        if not dlg_brackets:
            dlg_brackets = cls.dlg_brackets

        # Delimiter of name and text in dialogue lines.
        dlg_delimiter = re.compile(f'\\s*[\\s{dlg_brackets[0]}]')

        text = text.strip()

        if line_type == PScLineType.CHARACTER:
            # Split text to name and text.
            if not chr_delimiter.search(text):
                name, text = text, ''
            else:
                name, text = chr_delimiter.split(text, maxsplit=1)
            return cls(line_type, name=name, text=text)

        if line_type == PScLineType.DIALOGUE:
            name = ''
            # Split text to name and text.
            if dlg_delimiter.search(text):
                name, text = dlg_delimiter.split(text, maxsplit=1)

            if not name:
                name = default_name

            # Remove closing bracket at end.
            if text[-1] in dlg_brackets[1]:
                text = text[:-1]

            return cls(line_type, name=name, text=text)

        # TODO: line_type が数字や文字列だった場合に対応する。

        return cls(line_type, text=text)


class PSc:
    '''Play script.
    '''
    def __init__(self, title='', author='', chars=[], lines=[]):
        '''Constructor.

        Parameters
        ----------
        title : str
        author : str
        chars : list-like[str]
        lines : list-like[str]
        '''
        self.title = title
        self.author = author
        self.chars = chars
        # lines could be a generator while self.lines should be a list.
        self.lines = list(lines)

    @classmethod
    def from_lines(cls, lines):
        '''Make PSc object from PScLine objects.

        Parameters
        ----------
        lines : list-like[playscript.PScLine]

        Returns
        -------
        script : playscript.PSc
        '''
        return cls(lines=lines)

    @classmethod
    def lines_from_types_and_texts(cls, line_types, texts):
        '''Make PScLine list from line types and source texts.

        Parameters
        ----------
        line_types : list-like[playscript.PScLineType]
        texts : list-like[str]

        Returns
        -------
        lines : list[playscript.PScLine]
        '''
        lines = []
        for line_type, text in zip(line_types, texts):
            line = PScLine.from_text(line_type, text)
            lines.append(line)
        return lines
