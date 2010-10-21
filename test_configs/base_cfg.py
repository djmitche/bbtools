# -*- python -*-
# ex: set syntax=python:

# This is a sample buildmaster config file. It must be installed as
# 'master.cfg' in your buildmaster's base directory (although the filename
# can be changed with the --basedir option to 'mktap buildbot master').

# It has one job: define a dictionary named BuildmasterConfig. This
# dictionary has a variety of keys to control different aspects of the
# buildmaster. They are documented in docs/config.xhtml .

# This is the dictionary that the buildmaster pays attention to. We also use
# a shorter alias to save typing.
c = BuildmasterConfig = {}

####### BUILDSLAVES

# the 'slaves' list defines the set of allowable buildslaves. Each element is
# a tuple of bot-name and bot-password. These correspond to values given to
# the buildslave's mktap invocation.
from buildbot.buildslave import BuildSlave
c['slaves'] = [ BuildSlave("bot", "pass", properties = { 'slprop' : 'val'})]

# to limit to two concurrent builds on a slave, use
#  c['slaves'] = [BuildSlave("bot1name", "bot1passwd", max_builds=2)]


# 'slavePortnum' defines the TCP port to listen on. This must match the value
# configured into the buildslaves (with their --master option)

c['slavePortnum'] = 9989

####### CHANGESOURCES

# the 'change_source' setting tells the buildmaster how it should find out
# about source code changes. Any class which implements IChangeSource can be
# put here: there are several in buildbot/changes/*.py to choose from.

from buildbot.changes.svnpoller import SVNPoller, split_file_branches
from buildbot.changes.pb import PBChangeSource
c['changeHorizon'] = 2
c['change_source'] = [
        SVNPoller(svnurl='http://svn.r.igoro.us/projects/toys/Processor/',
                                pollinterval=120, # two minutes
                                split_file=split_file_branches),
        PBChangeSource(),
]

####### SCHEDULERS

## configure the Schedulers

from buildbot.schedulers import basic, filter, triggerable, timed, trysched
c['schedulers'] = []
c['schedulers'].append(basic.AnyBranchScheduler(name="all",
    branches=['foo', 'bar'],
                                 treeStableTimer=1200,
                                 builderNames=["builder"]))
c['schedulers'].append(triggerable.Triggerable(name="a",
                                 builderNames=["builder"]))
if 0:
    c['schedulers'].append(timed.Periodic(name="n", periodicBuildTimer=1,
                                     builderNames=["builder"]))
c['schedulers'].append(trysched.Try_Userpass(name="goaheadtryme",
                                builderNames=[ 'builder', ],
                                port=9999,
                                userpass=[('testy', 'test')]))


####### BUILDERS

from buildbot.process import factory
from buildbot.steps.source import SVN, P4, Mercurial
from buildbot.steps.shell import ShellCommand, PerlModuleTest
from buildbot.steps.master import MasterShellCommand
from buildbot.steps.transfer import FileDownload, DirectoryUpload, FileUpload
from buildbot.steps.trigger import Trigger
from buildbot.steps.python_twisted import Trial
from buildbot.process.properties import WithProperties
f1 = factory.BuildFactory()
#f1.addStep(P4(p4base="//depot/proj"))
f1.addStep(SVN(baseURL='http://svn.r.igoro.us/projects/toys/Processor/', defaultBranch='trunk'))
#f1.addStep(Mercurial(baseURL='http://bitbucket.org/nicolas17/pyboinc', mode='copy'))
#f1.addStep(ShellCommand(command=WithProperties("echo %(scheduler)s"), logEnviron=False))
#f1.addStep(ShellCommand(command="sleep 15", logEnviron=False))
#f1.addStep(MasterShellCommand(command="sleep 5"))
#f1.addStep(Trigger(schedulerNames=['a'], waitForFinish=True))
f1.addStep(ShellCommand(command="cat main.cp", description='catting', descriptionDone='catted', usePTY=True))
#f1.addStep(FileUpload(slavesrc="main.cp", masterdest="/tmp/main.cp"))
#f1.addStep(ShellCommand(command="false", flunkOnFailure=True))

from buildbot.config import BuilderConfig
c['builders'] = [
          BuilderConfig(
            name = "builder",
            slavenames = "bot",
            factory = f1,
          ) ]


####### STATUS TARGETS

# 'status' is a list of Status Targets. The results of each build will be
# pushed to these targets. buildbot/status/*.py has a variety to choose from,
# including web pages, email senders, and IRC bots.

c['status'] = []

from buildbot.status import html
c['status'].append(html.WebStatus(http_port=8010, allowForce=True))

# from buildbot.status import mail
# c['status'].append(mail.MailNotifier(fromaddr="buildbot@localhost",
#                                      extraRecipients=["builds@example.com"],
#                                      sendToInterestedUsers=False))
#
# from buildbot.status import words
# c['status'].append(words.IRC(host="irc.example.com", nick="bb",
#                              channels=["#example"]))
#
# from buildbot.status import client
# c['status'].append(client.PBListener(9988))


####### DEBUGGING OPTIONS

# if you set 'debugPassword', then you can connect to the buildmaster with
# the diagnostic tool in contrib/debugclient.py . From this tool, you can
# manually force builds and inject changes, which may be useful for testing
# your buildmaster without actually commiting changes to your repository (or
# before you have a functioning 'sources' set up). The debug tool uses the
# same port number as the slaves do: 'slavePortnum'.

#c['debugPassword'] = "debugpassword"

# if you set 'manhole', you can ssh into the buildmaster and get an
# interactive python shell, which may be useful for debugging buildbot
# internals. It is probably only useful for buildbot developers. You can also
# use an authorized_keys file, or plain telnet.
#from buildbot import manhole
#c['manhole'] = manhole.PasswordManhole("tcp:9999:interface=127.0.0.1",
#                                       "admin", "password")


####### PROJECT IDENTITY

# the 'projectName' string will be used to describe the project that this
# buildbot is working on. For example, it is used as the title of the
# waterfall HTML page. The 'projectURL' string will be used to provide a link
# from buildbot HTML pages to your project's home page.

# for testing
#c['buildHorizon'] = 88888

c['projectName'] = "Buildbot"
c['projectURL'] = "http://svn.r.igoro.us/"

# the 'buildbotURL' string should point to the location where the buildbot's
# internal web server (usually the html.Waterfall page) is visible. This
# typically uses the port number set in the Waterfall 'status' entry, but
# with an externally-visible host name which the buildbot cannot figure out
# without some help.

c['buildbotURL'] = "http://localhost:8010/"
