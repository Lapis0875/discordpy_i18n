from typing import List, Dict, Optional, Final, Union

from discord_i18n.type_hints import TOML


__all__ = ('LocaleCommand', 'LocaleCommandGroup', 'parse_locale_command', 'LocaleText', 'LocaleTextGroup', 'parse_locale_text', 'Locale')


# TOML keys
KEY: Final[str] = 'key'
NAME: Final[str] = 'name'
ALIASES: Final[str] = 'aliases'
DESCRIPTION: Final[str] = 'description'
VALUE: Final[str] = 'value'
SUBCOMMANDS: Final[str] = 'subcommands'
COMMAND: Final[str] = 'commands'
TEXT: Final[str] = 'texts'


class LocaleCommand:
    __slots__ = ('locale', 'key', 'name', 'aliases', 'description')
    locale: 'Locale'
    key: str
    name: str
    aliases: List[str]
    description: Optional[str]

    def __init__(
            self,
            locale: 'Locale',
            key: str,
            name: str,
            aliases: List[str],
            description: Optional[str] = None
    ):
        self.locale = locale
        self.key = key
        self.name = name
        self.aliases = aliases
        self.description = description

    def __repr__(self):
        return f'LocaleCommandGroup(' \
               f'key={self.key}, ' \
               f'name={self.name}, ' \
               f'aliases={self.aliases}, ' \
               f'description={self.description})'


class LocaleCommandGroup(LocaleCommand):
    __slots__ = ('subcommands',)
    subcommands: Dict[str, LocaleCommand]

    def __init__(
            self,
            locale: 'Locale',
            key: str,
            name: str,
            aliases: List[str],
            subcommands: Dict[str, LocaleCommand],
            description: Optional[str] = None
    ):
        super(LocaleCommandGroup, self).__init__(locale, key, name, aliases, description)
        self.subcommands = subcommands

    def __repr__(self):
        return f'LocaleCommandGroup(' \
               f'key={self.key}, ' \
               f'name={self.name}, ' \
               f'aliases={self.aliases}, ' \
               f'subcommands={len(self.subcommands)}, ' \
               f'description={self.description})'


def parse_locale_command(locale: 'Locale', key: str, command_or_group: TOML) -> Union[LocaleCommand, LocaleCommandGroup]:
    name: str = command_or_group.pop(NAME)
    aliases: List[str] = command_or_group.pop(ALIASES)
    description: Optional[str] = command_or_group.pop(DESCRIPTION) if DESCRIPTION in command_or_group else None

    if len(command_or_group) == 0:
        return LocaleCommand(locale, key, name, aliases, description)
    else:
        # leftovers are subcommands
        subcommands: Dict[str, LocaleCommand] = dict(map(
            lambda key_content: (key_content[0], parse_locale_command(locale, *key_content)),
            command_or_group.items()
        ))
        return LocaleCommandGroup(locale, key, name, aliases, subcommands, description)


class LocaleText:
    __slots__ = ('locale', 'key', 'value')
    locale: 'Locale'
    key: str
    value: str

    @classmethod
    def parse(cls, locale: 'Locale', locale_key: str, locale_content: TOML):
        return cls(
            locale=locale,
            key=locale_key,
            value=locale_content[VALUE]
        )

    def __init__(self, locale: 'Locale', key: str, value: str):
        self.locale = locale
        self.key = key
        self.value = value

    def __repr__(self):
        return f'LocaleText(key={self.key}, value={self.value})'


class LocaleTextGroup:
    locale: 'Locale'
    key: str

    def __init__(self, locale: 'Locale', key: str):
        self.locale = locale
        self.key = key
        self.items: Dict[str, Union[LocaleText, LocaleTextGroup]] = {}

    def add_item(self, key: str, text: Union[LocaleText, 'LocaleTextGroup']):
        if not isinstance(text, (LocaleText, LocaleTextGroup)):
            raise TypeError(f'Parameter `text` must be either LocaleText or LocaleTextGroup, not {type(text)}')
        self.items[key] = text

    def __repr__(self):
        return f'LocaleTextGroup(key={self.key}, items={len(self.items)})'


def parse_locale_text(locale: 'Locale', key: str, content: TOML) -> Union[LocaleText, LocaleTextGroup]:
    if VALUE in content:
        # LocaleText
        return LocaleText(locale, key, content.pop(VALUE))
    else:
        # LocaleTextGroup
        group = LocaleTextGroup(locale, key)
        group.items = dict(map(
            lambda key_content: (key_content[0], parse_locale_text(locale, *key_content)),
            content.items()
        ))
        return group


class Locale:
    name: str
    commands: Dict[str, Union[LocaleCommand, LocaleCommandGroup]]
    texts: Dict[str, Union[LocaleText, LocaleTextGroup]]

    def __init__(self, name: str):
        self.name = name
        self.commands = {}
        self.texts = {}

    def load(self, locale_content: TOML):
        self.commands = dict(map(
            lambda key_content: (key_content[0], parse_locale_command(self, *key_content)),
            locale_content[COMMAND].items()
        ))

        self.texts = dict(map(
            lambda key_content: (key_content[0], parse_locale_text(self, *key_content)),
            locale_content[TEXT].items()
        ))

    def __repr__(self):
        return f'Locale(name={self.name}, commands={len(self.commands)}, texts={len(self.texts)})'

    def get_translated_command(self, key: str) -> Optional[Union[LocaleCommand, LocaleCommandGroup]]:
        return self.commands.get(key)

    def get_translated_text(self, key: str) -> Optional[Union[LocaleText, LocaleTextGroup]]:
        return self.texts.get(key)
