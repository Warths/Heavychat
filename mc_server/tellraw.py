from minecraftTellrawGenerator import MinecraftTellRawGenerator as mctellraw
from conf import SUB_BADGES, BITS_BADGES, PREFIX, PREVENT_LINK
import re
import random
import string

class Tellraw:
    def __init__(self, twitch_message, color):
        self.message = twitch_message.content
        self.channel = twitch_message.channel[1:].capitalize()
        self.tags = twitch_message.tags
        self.message = self.gogole(self.message)
        self.message = self.message.replace('"', "''")
        self.color = color
        if PREVENT_LINK:
            self.contain_link = self.link_filter()
        else:
            self.contain_link = False
        self.tellraw_list = []
        if SUB_BADGES['activated'] and int(self.tags['subscriber']) > 0:
            self.tellraw_list.append(self.sub_badge())
            self.tellraw_list.append(self.space())
        if BITS_BADGES['activated'] and 'bits' in self.tags['@badges']:
            self.tellraw_list.append(self.bits_badge())
            self.tellraw_list.append(self.space())
        self.tellraw_list.append(self.nickname_mod())
        self.tellraw_list.append(self.closing())

    def gogole(self, message):
        if 'don' in message and 'ACTION' in message:
            gogole_string = ["Ma maman va me disputer si elle sait que je ne suis pas au lit.",
                             "Mon papa et ma maman, ils sont frère et soeur, c'est normal ?",
                             "J'essaie d'être intelligent. C'est vraiment dur...",
                             "Ca vient quand la puberté ? Je complexe, ca doit venir avant 15 ans non ?",
                             "Je te souhaite le meilleur.",
                             "Ma maman dit que je ne devrais pas sucer mon pouce à cet âge.",
                             "J'ai raté mon brevet, car ma passion c'est spammer sur les tchats. Je suis tellement seul.",
                             "%s, tu es mon idéal masculin.. J'dis pas que j'aime les hommes, mais tu me fais de l'effet."
                             % self.channel,
                             "J'ai toujours admiré %s en secret.. J'ai son poster dans ma chambre." % self.channel,
                             "Ma passion ne se résume qu'à une seule chose : me nourrir des produits de mon corps !",
                             "Être avec vous me fait ressentir un profond manque de confiance en moi.. "
                             "Vous êtes tous tellement intelligents !",
                             "Pour la Nasa, l'espace est une priorité. Ils veulent m'y envoyer..",
                             "J'adore mettre des cornichons dans mon nez, ça donne du gouts à ce que je mange.",
                             "Mon légume préféré, c'est l'aubergine ! Pourquoi ? On a tous droit à nos petits secrets.. ;)",
                             "Ma maman m'a dit que z'étais SHPECHIAL.",
                             "%s !! ..J'apprécie les fruits, en sirop." % self.channel,
                             "La différence fondamentale entre une brique et moi, c'est que je m'appelle %s" % self.tags['display-name'],
                             "Comment vous faites vos lacets ? Je trouve ca vraiment très compliqué ..",
                             "Ce truc sous mon nombril, vous croyez que c'est une excroissance graisseuse ?",
                             "Mon test de QI sur internet affiche %s ! Ca fait combien ? J'ai pas assez de doigts."
                             % random.randint(70, 90),
                             "Si vous avez des problèmes pour vous intégrer en société.. Vous n'êtes pas seuls.",
                             "J'ai des poils qui poussent un peu partout, je deviens grand !",
                             "Au moins, sur internet, quand je me comporte bêtement, personne ne sait qui je suis.",
                             "Quelle vie on mène, tout de même, quand on a 47 chromosomes !"]
            message = gogole_string[random.randint(0, len(gogole_string) - 1)]
            return message
        else:
            return message

    def bits_badge(self):
        bold = False
        bits_amount = int(self.tags['@badges']['bits'])
        hover = 'Bits (%s !)' % bits_amount
        if bits_amount == 1:
            bits = '▲'
            color = 'light_gray'
        elif bits_amount == 100:
            bits = '✦'
            color = 'light_purple'
            bold = True
        elif bits_amount == 1000:
            bits = '⬟'
            color = 'green'
        elif bits_amount == 5000:
            bits = '⬢'
            color = 'aqua'
        elif bits_amount == 10000:
            bits = '★'
            color = 'red'
        elif bits_amount == 25000:
            bits = '★'
            color = 'light_purple'
        elif bits_amount == 50000:
            bits = '★'
            color = 'gold'
        elif bits_amount == 75000:
            bits = '★'
            color = 'green'
        elif bits_amount == 100000:
            bits = '✮'
            color = 'yellow'
        elif bits_amount == 200000:
            bits = '✮'
            color = 'light_gray'
            bold = True
        elif bits_amount == 300000:
            bits = '✮'
            color = 'light_purple'
            bold = True
        elif bits_amount == 400000:
            bits = '✮'
            color = 'green'
            bold = True
        elif bits_amount == 500000:
            bits = '✯'
            color = 'aqua'
            bold = True
        elif bits_amount == 600000:
            bits = '✯'
            color = 'red'
            bold = True
        elif bits_amount == 700000:
            bits = '✯'
            color = 'dark_purple'
            bold = True
        elif bits_amount == 800000:
            bits = '✯'
            color = 'gold'
            bold = True
        elif bits_amount == 900000:
            bits = '✯'
            color = 'dark_green'
            bold = True
        else:
            bits = '✯'
            color = 'yellow'
            bold = True
        if not BITS_BADGES['color']:
            color = 'white'
        tellraw = mctellraw(
            text=bits,
            color=color,
            bold=bold,
            hover=mctellraw(text=hover, italic=True, color='light_gray')
        )
        return tellraw

    def sub_badge(self):
        italic = False
        bold = False
        underlined = False
        sub_duration = int(self.tags['@badges']['subscriber'])
        hover = 'Abonné (%s+ mois)' % sub_duration
        if sub_duration == 0:
            sub = 'Sub'
            color = 'gold'
            hover = 'Abonné récent !'
        elif sub_duration == 3:
            sub = 'SUB'
            color = 'gold'
        elif sub_duration == 6:
            sub = 'SUB'
            color = 'yellow'
        elif sub_duration == 12:
            sub = 'SUB'
            color = 'aqua'
        elif sub_duration == 24:
            sub = 'SUB'
            color = 'light_purple'
        else:
            sub = 'SUB'
            color = 'light_purple'
            underlined = True
            bold = True
        if not SUB_BADGES['color']:
            color = 'white'
        tellraw = mctellraw(
            text=sub,
            color=color,
            italic=italic,
            bold=bold,
            underlined=underlined,
            hover=mctellraw(text=hover, italic=True, color='light_gray')
        )
        return tellraw

    @staticmethod
    def space():
        tellraw = mctellraw(
            text=' ',
            color='white',
        )
        return tellraw

    def nickname_mod(self):
        tellraw = mctellraw(
            text=self.tags['display-name'],
            color=self.color,
            click='%sheavychat options %s ' % (PREFIX, self.tags['display-name']),
            insertion=PREFIX + '/timeout ' + self.tags['display-name'],
            hover=mctellraw(text='Expulser %s 10 minutes (Shift clic pour plus d\'options)' % self.tags['display-name'], italic=True)
        )
        return tellraw


    def closing(self):
        tellraw = mctellraw(
            text=': %s' % self.message,
            color='white',
        )
        return tellraw

    def get_tellraw(self):
        tellraw = '["",'
        for values in self.tellraw_list:
            tellraw += str(values) + ', '
        tellraw = tellraw[0:-2] + ']'
        return tellraw


    def link_filter(self):
        if '.' in self.message and self.tags['mod'] is not '1':
            if re.search('^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$',
                         self.message):
                return True
        return False
