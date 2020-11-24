import itchat
from itchat.content import TEXT

@itchat.msg_register
def simple_reply(msg):
    if msg['Type'] == TEXT:
        return 'I received：%s' % msg['Content']
itchat.auto_login()
itchat.run()