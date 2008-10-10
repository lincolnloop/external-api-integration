#!/usr/bin/python
import sys
from httplib2 import Http
import elementtree.ElementTree as ET
from commands import getoutput

BASECAMP_URL = 'https://yourbasecamp.grouphub.com'
BASECAMP_USER = 'youruser'
BASECAMP_PASSWORD = 'yourpassword'
SVNLOOK = '/usr/bin/svnlook'


def swap_word(abbr):
    """
    Replaces abbreviation with full word
    """
    if abbr == "U":
        return "Updated"
    elif abbr == "A":
        return "Added"
    elif abbr == "D":
        return "Deleted"
    else:
        return ""


def build_message(repo_path, revision, show_changed_files = True):
    """
    Gets all the commit info and returns a pretty textile formatted message
    """
    #TODO: check status and raise error if svnlook fails
    commit_author = getoutput("svnlook author %s -r %s" % (repo_path, revision))
    commit_log = getoutput("svnlook log %s -r %s" % (repo_path, revision))
    commit_date = getoutput("svnlook date %s -r %s" % (repo_path, revision))
    commit_changed = getoutput("svnlook changed %s -r %s" % (repo_path, revision))

    #create bulleted list from multiline commit logs
    commit_log_textilized = ''
    for log_item in commit_log.splitlines():
        commit_log_textilized += "* %s\n" % log_item.capitalize()
        
    message_body =  "Revision: %s\n" % revision
    message_body += "<small>checked in by %s</small>\n\n" % commit_author
    message_body += "h3{clear:left; font-weight:bold}. Summary:\n\n"
    message_body += "%s\n\n" % commit_log_textilized
    message_body += "h3{clear:left; font-weight:bold}. Changed files:\n\n"
    if show_changed_files:
        #create bulleted list from changed files
        commit_changed_textilized = ''
        for commit_change in commit_changed.splitlines():
            change = commit_change[0]
	    filename = commit_change[1:].strip()
            commit_changed_textilized += "* <small>*%s:*</small> <code>%s</code>\n" % (
								swap_word(change), filename)
        message_body += commit_changed_textilized
    
    return message_body

def post_comment(message_id, comment):
    """
    Posts new comment to Basecamp message
    """
    h = Http()
    h.add_credentials(BASECAMP_USER, BASECAMP_PASSWORD)
    url = '%s/posts/%s/comments.xml' % (BASECAMP_URL, message_id)
    req = ET.Element('comment')
    ET.SubElement(req, 'body').text = str(comment)
    headers = {
        'Content-Type': 'application/xml',
        'Accept': 'application/xml',
    }
    response = h.request(url, method="POST", body=ET.tostring(req), headers=headers)
    print response
    
if __name__ == "__main__":
    repo_path = sys.argv[1]
    revision = sys.argv[2]
    message_id = sys.argv[3]
    post_comment(message_id, build_message(repo_path, revision))
