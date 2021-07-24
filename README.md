# discordpy_i18n
Multilingual supporting command system based on discord.ext.commands
Currently, this project is WIP (working in progress).
All PRs are welcome :D

## How to install
```shell
pip install discord.py-i18n
```

## How to use (Draft)
```toml
# lang/en-US.lang
[commands]
  [commands.hello]
  name="hello"
  aliases=["hi", "greeting"]
[text]
  [text.hello]
  value="Hello!"
```
```toml
# lang/ko-KR.lang
[commands]
  [commands.hello]
  name="안녕"
  aliases=["반가워", "인사"]
[text]
  [text.hello]
  value="안녕하세요!"
```
```python
# main.py
from discord.ext import commands
from discord_i18n import LocaleManager    # Locale manager object (singleton).


LocaleManager().load_locales(path='./lang')   # Load all language translation files in `lang/` directory. translation files will be named `(locale).lang`, containing toml format.
                                              # In this situation, it will load `lang/en-US.lang`, `lang/ko-KR.lang`
class I18NCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @LocaleManager().command(key='hello')     # Create command object with locale support. `key` will be the key of command in translation files. This coammand will have all traslated texts as `Command.aliases`
    async def hello(ctx):
        await ctx.send(LocaleManager.get_locale('ko-KR').hello)   # Currently thinking of using Locale (class) to get translated text in certain locale. 

bot = commands.Bot(command_prefix='!')
bot.load_cog(I18NCommands(bot))

bot.run('TOKEN')
```
### In en-US
> User : !hello
> 
> Bot : Hello!
### In ko-KR
> User : !안녕
> 
> Bot : 안녕하세요!
