#format python
'''
    Simple Vote macro for MoinMoin.
    Author: Martin Stone <martins@evos.net>
    Hacked by: John Cocula (john@cocula.com)

    Usage:
        [[Vote(pageName, voteTitle, candidate1, ...)]]

    E.g:
        [[Vote(MyBlog, Do polls work?, yes)]]
    
    Just like Martin's Vote macro, except you must specify the name of the
    page on which to vote "appears."  Without this information, when a user
    votes from an included page, after pressing the Vote button they are
    returned to the included page, not the main page.  Also different is
    that the current number of votes is hidden until the user has voted.
    Lastly, it is possible to have a poll that only has one choice, which
    is kind of funny.  The remainder of the description is Martin's:

    You can have multiple votes on one page (so long as the titles are unique).
    You can add candidates after a vote has started, but note that renaming 
    candidates will lose the votes (and not allow users to recast their votes).
    Changing the vote title creates a new vote.

    Vote data is stored in data_dir/pages/pagename/votes 
    (i.e. alongside the attachments directory for a page).

    You can customise the appearance by defining the following CSS styles:
        table.vote 
        td.votelogin (for "must login" message)
'''

from MoinMoin import user, webapi, wikiutil, config
import os
import pickle
import string

def getVotesDir(macro):
    """ Get directory where votes on this page are stored.
    """
    pagename = macro.formatter.page.page_name
    return os.path.join(macro.request.cfg.data_dir, "pages", pagename, "votes")

def makeFilename(voteName):
    voteName = voteName.encode('ascii', 'replace')
    voteName = voteName.translate(string.maketrans(u'\\/:*?"<>| ', u'xxxxxxxxx_')) # any I've missed?
    return voteName + ".pik"


def loadVotes(macro,voteName):
    try:
        f = open(os.path.join(getVotesDir(macro), makeFilename(voteName)), 'r')
        return pickle.load(f)
    except:
        return {}


def saveVotes(macro,voteName, votes):
    votesDir = getVotesDir(macro)
    if not os.path.isdir(votesDir): 
        os.makedirs(votesDir) #need mode?

    f = open(os.path.join(votesDir, makeFilename(voteName)), 'w')
    pickle.dump(votes, f)


def countVotes(votes):
    results = {}
    for v in votes.values():
        results.setdefault(v, 0)
        results[v] = results[v] + 1

    return results


def execute(macro, args):
    args = string.split(args, ",")
    args = map(string.strip, args)

    if len(args) < 3: return macro.formatter.rawHTML('<pre>[[Vote: Insufficient macro arguments]]</pre>')

    pageName = args[0]
    voteName = args[1]
    candidates = args[2:]

    form = macro.form
    votes = loadVotes(macro,voteName)
    voter = macro.request.user.name

    # votes are stored in a dictionary as {user: candidate} to avoid duplicate votes
    # (a voter could switch their vote but this UI doesn't expose that facility)
    if form.has_key('vote') and form.has_key('voteName') and voter:
        if form['voteName'][0] == voteName:
            votes[voter] = form['vote'][0]
            try:
               saveVotes(macro, voteName, votes)
            except Exception, e:
               return macro.formatter.rawHTML('<a id="voteform"><pre>[[Failed to store vote: %s ]]</pre></a>' % e)

    # generate dictionary {candidate: numvotes}
    results = countVotes(votes)

    hasVoted = voter in votes

    # spit out votes table (as part of a form if the user hasn't voted yet)
    html = ''
    if not hasVoted:
        voteButton = '<td><INPUT type="radio" name="vote" value="%s">vote</td>'
        html += '''
            <form method="get" action="%(scriptname)s/%(pageName)s#voteform">\n
            <input type="hidden" name="voteName" value="%(voteName)s">
            ''' % {'scriptname': r'/moin.cgi', 'pageName': pageName, 'voteName': voteName}
    else:
        voteButton = ''

    html += '<a id="voteform"><table class="vote"><tr><th colspan="2">%s</th></tr>' % voteName

    for candidate in candidates:
        button = voteButton and (voteButton % candidate)
        if not hasVoted:
            button = '<INPUT type="radio" name="vote" value="%s">' % (candidate)
            count = candidate
        else:
            button = candidate
            count = results.setdefault(candidate, 0)
        html += '<tr><td>%s</td><td>%s</td></tr>\n' % (button, count)

    if not voter and not hasVoted:
        html += '<tr><td colspan="2" class="votelogin">You need to login to vote</td></tr>'

    if not hasVoted:
        html += '<tr><td colspan="2" class="votesubmit"><input type="submit" value="Vote"></td></tr>'

    html += '</table>\n'
    html += '</form>\n'
       
    return macro.formatter.rawHTML(html)

