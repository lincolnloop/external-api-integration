subversion_basecamp_notifier.py
===============================

Requires ``elementtree`` and ``httplib2``

#. Drop your Basecamp info into the script
#. Create a message in Basecamp (make sure your user entered above has access to the message)
#. Note the message ID from the URL (it's the second number)
#. Create a post-commit hook on your subversion repo that calls this script

::

    #! /bin/sh
    BASECAMP_MESSAGE=11111111
    # $1 is the repository path
    # $2 is the revision
    python /path/to/subversion_basecamp_notifier.py $1 $2 $BASECAMP_MESSAGE


imap_to_campfire.py
===================

Requires pinder_

Built to run as a cron job that will periodically check an IMAP mailbox and post the email headers (from, to, subject) to a Campfire_ chat room.

.. _pinder: http://dev.oluyede.org/pinder/
.. _Campfire: http://www.campfirenow.com