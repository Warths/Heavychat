from minecraftTellrawGenerator import MinecraftTellRawGenerator as mctellraw
from conf import PREFIX


def get_command_tellraw(text):
    tellraws = []
    tellraws.append(mctellraw(text='['))
    tellraws.append(mctellraw(text='HeavyChat', color='dark_red'))
    tellraws.append(mctellraw(text='] ▶▶ '))
    tellraws.append(mctellraw(text=text))
    return get_tellraw(tellraws)

def get_tellraw(tellraws):
    tellraw = '["",'
    for values in tellraws:
        tellraw += str(values) + ', '
    tellraw = tellraw[0:-2] + ']'
    return tellraw

def get_options_tellraw(nickname):
    tellraws = []
    tellraws.append(mctellraw(text='☰ Options pour %s ' % nickname,
                              hover=mctellraw(text='Modération rapide'),
                              italic=True))
    tellraws.append(mctellraw(text='[Timeout]',
                              color='gray',
                              hover=mctellraw(text='Expulser 10 minutes'),
                              click='%s/timeout %s' % (PREFIX, nickname),
                              italic=True))
    tellraws.append(mctellraw(text=', ',
                              italic=True))
    tellraws.append(mctellraw(text='[Purge]',
                              color='gray',
                              hover=mctellraw(text='Supprimer les message récents'),
                              click='%s/timeout %s 1' % (PREFIX, nickname),
                              italic=True))
    tellraws.append(mctellraw(text=', ',
                              italic=True))
    tellraws.append(mctellraw(text='[Unban]',
                              color='gray',
                              hover=mctellraw(text='Révoquer un ban/timeout'),
                              click='%s/unban %s' % (PREFIX, nickname),
                              italic=True))
    tellraws.append(mctellraw(text=', ',
                              italic=True))
    tellraws.append(mctellraw(text='[Permit]',
                              color='gray',
                              hover=mctellraw(text='Autoriser un lien (!permit)'),
                              click='%s!permit %s ' % (PREFIX, nickname),
                              italic=True))
    tellraws.append(mctellraw(text='. ',
                              italic=True))
    return get_tellraw(tellraws)
