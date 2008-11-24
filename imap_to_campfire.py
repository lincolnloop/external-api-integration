#!/usr/bin/env python

import imaplib
from pinder import Campfire

IMAP_LOGIN = {
    'server': "imap.gmail.com",
    'user': "user@mydomain.com",
    'password': "secretpassword",
}
CAMPFIRE_LOGIN = {
    'subdomain': "mydomain", #http://mydomain.campfirenow.com
    'room': "My Room Name",
    'user': "campfire_user@mydomain.com",
    'password': "secretpassword2",
}


def imap_to_campfire(imap_login, campfire_login):
    """
    Checks IMAP inbox and posts info to Campfire.
    
    """
    # connect to IMAP
    i = imaplib.IMAP4_SSL(imap_login['server'])
    i.login(imap_login['user'], imap_login['password'])

    # connect to Campfire
    c = Campfire(campfire_login['subdomain'])
    c.login(campfire_login['user'], campfire_login['password'])
    room = c.find_room_by_name(campfire_login['room'])

    typ, data = i.select("INBOX")
    msg_total = int(data[0])
    #import pdb; pdb.set_trace()
    for msg_id in range(1, msg_total+1):
        typ, data = i.fetch(msg_id, "(BODY[HEADER.FIELDS (TO SUBJECT)])")
        #retrieve relative part of message
        msg_info = data[0][1]
        #archive message
        i.store(msg_id, "+FLAGS", r'(\Deleted)')
    
        #post to Campfire
        room.paste("*New Message*\r\n%s" % msg_info)
    
    i.close()
    i.logout()
    c.logout()
    
    
if __name__ == '__main__':
    """
    Run as a stand-alone script

    """
    imap_to_campfire(IMAP_LOGIN, CAMPFIRE_LOGIN)
    