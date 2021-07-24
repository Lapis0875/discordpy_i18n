from functools import reduce
from typing import Dict, Optional
from os import listdir

import tomli
from discord.ext import commands

from .design_pattern import Singleton
from .locale import Locale, LocaleCommandGroup, LocaleCommand
from .type_hints import TOML


__all__ = ('LocaleManager', )


class LocaleManager(Singleton):
    """Singleton object to manage and utilize locales."""
    def __init__(self, lang_path: str = './lang'):
        self.lang_path: str = lang_path
        self.locales: Dict[str, Locale] = {}
        self.command_aliases: Dict[str, list[str]] = {}

    def add_locale(self, locale: Locale):
        if not isinstance(locale, Locale):
            raise TypeError(f'locale must be an instance of class `Locale`, not {type(locale)}')
        self.locales[locale.name] = locale

    def load(self):
        print(listdir(self.lang_path))
        for locale_file in filter(lambda f: f.split('.')[-1] == 'lang', listdir(self.lang_path)):
            locale_name: str = locale_file[:-5]
            with open(f'{self.lang_path}/{locale_file}', mode='rt', encoding='utf-8') as f:
                content: TOML = tomli.load(f)
                locale = Locale(locale_name)
                locale.load(content)
                self.add_locale(locale)

    def merge_command_aliases(self, locale: Locale):
        for command_key, command in locale.commands.items():
            if command_key not in self.command_aliases:
                self.command_aliases[command_key] = []
            self.command_aliases[command_key] += command.aliases
            if isinstance(command, LocaleCommandGroup):
                self.flatten_group_command_aliases(command_key, command.subcommands)

    def flatten_group_command_aliases(self, group_key, subcommands: Dict[str, LocaleCommand]):
        for subcommand_key, subcommand in subcommands.items():
            flatten_subcommand_key = f'{group_key}.{subcommand_key}'
            if flatten_subcommand_key not in self.command_aliases:
                self.command_aliases[flatten_subcommand_key] = []
            self.command_aliases[flatten_subcommand_key] += subcommand.aliases
            if isinstance(subcommand, LocaleCommandGroup):
                self.flatten_group_command_aliases(subcommand_key, subcommand.subcommands)

    def get_locale(self, name: str) -> Optional[Locale]:
        return self.locales.get(name)

    def command(self, key: str):
        return commands.command(key, aliases=self.command_aliases[key])
