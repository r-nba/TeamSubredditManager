import praw
import prawcore
import datetime

from utils import utils

class Reddit(object):
    """Perform various operations on Reddit"""
    reddit = None
    subreddit = ''
    subredditThreads = None

    def updateSidebar(self, scheduleMD, standingsMD):
        sidebarTemplate = self.reddit.subreddit(self.subreddit).wiki['sidebar_template'].content_md
        
        sidebarMD = sidebarTemplate.replace('CLIPPER_BOT_SCHEDULE_PLACEHOLDER', scheduleMD)
        sidebarMD = sidebarMD.replace('CLIPPER_BOT_STANDINGS_PLACEHOLDER', standingsMD)
        
        settings = self.reddit.subreddit(self.subreddit).mod.settings()
        desc = settings['description']
        settings['description'] = sidebarMD

        self.reddit.subreddit(self.subreddit).mod.update(description = sidebarMD)

    def createThread(self, threadTitle, threadBody, threadType):
        self.refreshThreads()
        threadID = self.subredditThreads.findThread(threadType, utils.today())
        if threadID != None:
            return threadID

        self.unstickyGameThreads()

        threadFlair = ''
        threadSticky = False
        threadSort = ''
        
        if threadType == 'pregame':
            flairText = u'Pre-Game Thread'
            threadSticky = True
            threadSort = 'new'
        elif threadType == 'game':
            flairText = u'Game Thread'
            threadSticky = True
            threadSort = 'new'
        elif threadType =='postgame':
            flairText = u'Post-Game Thread'
            threadSticky = True
            threadSort = 'new'

        submission = self.reddit.subreddit(self.subreddit).submit(threadTitle, selftext = threadBody, send_replies = False)
        self.reddit.subreddit(self.subreddit).flair.set(submission, text = flairText, css_class = threadType)
        if threadSticky: submission.mod.sticky()
        submission.mod.suggested_sort(threadSort)

        return submission.id

    def updateThread(self, threadID, threadBody):
        submission = self.reddit.submission(id = threadID)
        submission.edit(threadBody)

    def refreshThreads(self):
        self.subredditThreads.refresh(self.reddit.subreddit(self.subreddit).new(limit=100))

    def unstickyGameThreads(self):
        topExists = True
        botExists = True

        try:
            topSticky = self.reddit.subreddit(self.subreddit).sticky(1)
        except prawcore.exceptions.NotFound:
            topExists = False
        
        try:
            botSticky = self.reddit.subreddit(self.subreddit).sticky(2)
        except prawcore.exceptions.NotFound:
            botExists = False
        
        if topExists and topSticky.link_flair_text in ('Game Thread', 'Post-Game Thread', 'Pre-Game Thread'):
            topSticky.mod.sticky(state=False)
        if botExists and botSticky.link_flair_text in ('Game Thread', 'Post-Game Thread', 'Pre-Game Thread'):
            botSticky.mod.sticky(state=False)

    def __init__(self, subreddit):
        self.reddit = praw.Reddit(user_agent='NBA Team Subreddit Manager')
        #self.reddit.refresh_access_information()
        self.subreddit = subreddit
        self.subredditThreads = SubredditThreads()

class Thread(object):
    threadType = ''
    threadDate = None
    threadID = ''

    def __init__(self, thread):
        self.threadType = str(thread.link_flair_css_class)
        self.threadDate = (datetime.datetime.fromtimestamp(thread.created) + datetime.timedelta(hours=utils.tzOffset)).replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        self.threadID = thread.id

class SubredditThreads(object):

    def refresh(self, threads):
        self.subThreads.clear()
        for thread in threads:
            self.subThreads.append(Thread(thread))

    def __init__(self):
        self.subThreads = []

    def findThread(self, threadType, threadDate):
        for thread in self.subThreads:
            if thread.threadType == threadType and thread.threadDate == threadDate:
                return thread.threadID