import re
import templates
import SimpleBot
msg = SimpleBot.Message('SPELL ICUP')
for k in templates.rules_templates.keys():
    if re.search(k, msg.body):
        res = templates.rules_templates[k](msg)
        print(res)