import discord_i18n

mananger = discord_i18n.LocaleManager()

mananger.load()

en = mananger.get_locale('en-US')
print(en)

hello_cmd = en.get_translated_command('hello')
print(hello_cmd)

user_groupcmd = en.get_translated_command('user')
print(user_groupcmd)

hello_text = en.get_translated_text('hello')
print(hello_text)

user_grouptext = en.get_translated_text('user')
print(user_grouptext)

user_info = user_grouptext.items['info']
print(user_info)
