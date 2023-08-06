from xchk_core import contentviews as basecv
from xchk_core.courses import Course
from .contentviews import *

course = Course('git',
                'Git',
                [(GitBasicsSelfTestView,[GitPullBasicsView,GitRmView,GitAddRemoteView,GitLogView,GitStatusAndGitIgnoreView]),
                 (GitRmView,[GitStageChangesView]),
                 (GitIgnoreConceptView,[GitStageChangesView]),
                 (GitStatusView,[GitStageChangesView]),
                 (GitPushView,[GitStageChangesView,GitRemotesConceptView]),
                 (GitAddRemoteView,[GitRemotesConceptView]),
                 (GitStatusAndGitIgnoreView,[GitStatusView,GitIgnoreConceptView]),
                 (GitPullBasicsView,[GitPushView]),
                 (GitLogView,[GitStageChangesView]),
                 (GitStageChangesView,[GitStagesView]),
                 (GitRemotesConceptView,[GitStagesView]),
                 (GitStagesView,[GitInitView]),
                 (GitInitView,[WhatIsGitView]),
                 (WhatIsGitView,[])])
