import re
import SimpleBot


def simple_respond(t, sender):
    if re.search('^[Ss]ay\s[\w\s]+', t.body):
        msg = SimpleBot.Message('saying ' + ' '.join(t.body.split()[1:]))
        sender.send(msg)
    elif re.search('[Ss][Pp][Ee][Ll][Ll]\s[Ii].[Uu][Pp]', t.body):
        sender.send(SimpleBot.Message('HOLD THE MAYO'))
    return True


templates = {
    '^[Ss]ay\s[\w\s]+':simple_respond,
    '[Ss][Pp][Ee][Ll][Ll]\s[Ii].[Uu][Pp]':simple_respond
}