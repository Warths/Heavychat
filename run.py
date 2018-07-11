from irc.irc import Irc
from colorspace.colorspace import Colorspace
from mc_server.server import Server
from mc_server.tellraw import Tellraw
import mc_server.commands as cmd
from config import PASS, NICKNAME, CREDENTIALS
from conf import LOG_PATH, SCREEN_NAME, DEFAULT_CHANNEL, DEFAULT_SELECTOR, PREFIX, COMMAND, ALLOWED_CHANNELS
import time


def invalid():
    message = cmd.get_command_tellraw('Commande invalide, %s%s help pour plus d\'informations' %(PREFIX, COMMAND))
    server.send('/tellraw ' + event.player + ' ' + message)


def mc_send(tellraw, target=None, force=False):
    if not configuration['toggle'] and not force:
        return
    if target is not None:
        selector_list = [target]
    else:
        selector_list = ['@a'] if '@a' in configuration['selector'] else configuration['selector']
    for selector in selector_list:
        server.send('/tellraw ' + str(selector) + ' ' + str(tellraw))

configuration = {'toggle': True, 'selector': DEFAULT_SELECTOR, 'currentchannel': DEFAULT_CHANNEL}
server = Server(SCREEN_NAME, LOG_PATH)
mc_send(cmd.get_command_tellraw("Lancement d'HeavyChat 2.0"), force=True)
bot = Irc(NICKNAME, PASS, DEFAULT_CHANNEL)
mc_send(cmd.get_command_tellraw("Client IRC Heavyprojectbot lancé"), force=True)
users = {}
for element in CREDENTIALS:
    users[element] = Irc(CREDENTIALS[element]['nickname'], CREDENTIALS[element]['oauth'], DEFAULT_CHANNEL)
    mc_send(cmd.get_command_tellraw('Client IRC %s lancé' % element), force=True)
mc_send(cmd.get_command_tellraw("HeavyChat - Initialisé"), force=True)
colorspace = Colorspace()


while True:
    for event in bot.get_message():
        if event.type == 'PRIVMSG' and configuration['toggle']:
            message = Tellraw(event, colorspace.get_mc_color(event.tags['color']))
            if not message.contain_link:
                mc_send(message.get_tellraw())
    for event in server.get_events():
        if event.type == 'TO_TWITCH' and event.player in users:
            users[event.player].send_message(event.content)
        elif event.type == 'COMMAND' and event.player in users:
            if len(event.arg) == 1 and event.arg[0].lower() == 'toggle':
                configuration['toggle'] = not configuration['toggle']
                mc_send(cmd.get_command_tellraw("Affichage des messages Twitch %s"
                                                % ('activé' if configuration['toggle'] else 'désactivé')), force=True)
            elif len(event.arg) == 1 and event.arg[0].lower() == 'help':
                mc_send(cmd.get_command_tellraw("Guide d'utilisation d'HeavyChat"), target=event.player, force=True)
                mc_send(cmd.get_command_tellraw("Canal actuel : %s") % configuration['currentchannel'], target=event.player, force=True)
                mc_send(cmd.get_command_tellraw("==== Commandes ===="), target=event.player, force=True)
                mc_send(cmd.get_command_tellraw("Activer/désactiver HeavyChat"), target=event.player, force=True)
                mc_send(cmd.get_command_tellraw("%s%s toggle") % (PREFIX, COMMAND), target=event.player, force=True)
                mc_send(cmd.get_command_tellraw("Switcher le bot sur un autre canal:"), target=event.player, force=True)
                mc_send(cmd.get_command_tellraw("%s%s switch <arg1>") %(PREFIX, COMMAND), target=event.player, force=True)
                mc_send(cmd.get_command_tellraw("Modifier les destinataires d'HeavyChat :"), target=event.player, force=True)
                mc_send(cmd.get_command_tellraw("%s%s selector [set|add|del] <arg1> <arg2> ..") % (PREFIX, COMMAND), target=event.player, force=True)
                mc_send(cmd.get_command_tellraw("Lister les destinataires d'HeavyChat"), target=event.player, force=True)
                mc_send(cmd.get_command_tellraw("%s%s selector list"), target=event.player, force=True)
                mc_send(cmd.get_command_tellraw("Message Twitch rapide"), target=event.player, force=True)
                mc_send(cmd.get_command_tellraw("%s<contenu du message>" % PREFIX), target=event.player, force=True)
            elif len(event.arg) == 2 and event.arg[0].lower() == 'switch':
                if event.arg[1].lower() in ALLOWED_CHANNELS:
                    mc_send(cmd.get_command_tellraw("Changement de canal vers %s.." % event.arg[1]))
                    bot.switch_channel(event.arg[1])
                    for user_bot in users:
                        users[user_bot].switch_channel(event.arg[1])
                    mc_send(cmd.get_command_tellraw("Connecté : %s." % event.arg[1]))
                else:
                    mc_send(cmd.get_command_tellraw("Connection échouée : le canal %s n'est pas autorisé." % event.arg[1]))
            elif len(event.arg) >= 2 and event.arg[0].lower() == 'selector':
                if len(event.arg) > 2:
                    if event.arg[1] == 'set':
                        configuration['selector'] = []
                        for args in event.arg[2:]:
                            configuration['selector'].append(args.lower())
                    elif event.arg[1] == 'add':
                        for args in event.arg[2:]:
                            configuration['selector'].append(args.lower())
                    elif event.arg[1] == 'del':
                        for args in event.arg[2:]:
                            if args.lower() in configuration['selector']:
                                configuration['selector'].remove(args.lower())
                elif event.arg[1] == 'list':
                    mc_send(cmd.get_command_tellraw('Liste des sélecteurs :'))
                    mc_send(cmd.get_command_tellraw(str(configuration['selector'])))
            elif len(event.arg) == 2 and event.arg[0] == 'options':
                mc_send(cmd.get_options_tellraw(event.arg[1]), force=True, target=event.player)
            else:
                invalid()
    time.sleep(0.05)


