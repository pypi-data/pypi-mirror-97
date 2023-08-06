# -*- coding: utf-8 -*-
from imio.history.config import HISTORY_REVISION_NOT_VIEWABLE
from imio.history.interfaces import IImioHistory
from plone import api
from plone.app.layout.viewlets.content import ContentHistoryView
from plone.app.layout.viewlets.content import DocumentBylineViewlet
from plone.memoize.view import memoize
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getAdapter
from zope.component import getAdapters
from zope.component import getMultiAdapter
from zope.i18n import translate


class IHDocumentBylineViewlet(DocumentBylineViewlet):
    """Overrides the DocumentBylineViewlet."""

    index = ViewPageTemplateFile("templates/document_byline.pt")

    def show_history(self):
        """Rely on contenthistory.show_history."""
        contenthistory = getMultiAdapter(
            (self.context, self.request), name='contenthistory')
        res = contenthistory.show_history()
        if res:
            # do not show a link to the history if we are displaying something in
            # an overlay because history is displayed in an overlay and it does not work...
            if 'ajax_load' in self.request:
                res = False
        return res

    def highlight_history_link(self):
        """
          If a comment was added to last event of the object history,
          we highlight the link (set a css class on it) so user eye is drawn to it.
        """
        adapter = getAdapter(self.context, IImioHistory, 'workflow')
        return adapter.historyLastEventHasComments()


class IHContentHistoryView(ContentHistoryView):
    '''
      Overrides the ContentHistoryView template to use our own.
      We want to display the content_history as a table.
    '''
    histories_to_handle = (u'revision', u'workflow')
    index = ViewPageTemplateFile("templates/content_history.pt")

    def getHistory(self, checkMayViewEvent=True, checkMayViewComment=True):
        """Get the history for current object.
           Merge workflow history with content history and sort by time."""
        history = []
        history_adapters = getAdapters((self.context,), IImioHistory)
        for adapter_name, adapter in history_adapters:
            # for now, specifically limit display to u'revision' and u'workflow'
            if adapter_name in self.histories_to_handle:
                history.extend(adapter.getHistory(
                    checkMayViewEvent=checkMayViewEvent,
                    checkMayViewComment=checkMayViewComment))

        if not history:
            return []

        history.sort(key=lambda x: x["time"], reverse=True)
        return history

    def getTransitionTitle(self, transitionName):
        """
          Given a p_transitionName, return the defined title in portal_workflow
          as it is what is really displayed in the template.
        """
        currentWF = self._getCurrentContextWorkflow()
        if currentWF and transitionName in currentWF.transitions and \
           currentWF.transitions[transitionName].title:
            return currentWF.transitions[transitionName].title
        else:
            return transitionName

    def _extra_render_comments_mapping(self):
        """ """
        return {}

    def renderComments(self, event):
        """
          Render comments correctly as it is 'plain/text' and we want 'text/html'.
        """
        # prepare some data passed to translate as mappings
        mapping = event.copy()
        mapping['event_time'] = int(event['time'])
        mapping['url'] = self.context.absolute_url()
        mapping.update(self._extra_render_comments_mapping())
        # try to translate comments before it is turned into text/html
        translated = translate(
            safe_unicode(event['comments']),
            mapping=mapping,
            domain='imio.history',
            context=self.request)
        transformsTool = api.portal.get_tool('portal_transforms')
        data = transformsTool.convertTo('text/x-html-safe', translated)
        return data.getData()

    @memoize
    def _getCurrentContextWorkflow(self):
        """
          Return currently used workflow.
        """
        wfTool = getToolByName(self.context, 'portal_workflow')
        workflows = wfTool.getWorkflowsFor(self.context)
        return workflows and workflows[0] or None

    def showColors(self):
        """
          Colorize transition name?
        """
        return True

    def show_history(self):
        """
          Show the history?  This is a common method used by :
          - the view (@@historyview);
          - the viewlet (imio.history.documentbyline);
          - imio.actionspanel history action icon.
          Originally, the history is shown to people having the
          'CMFEditions: Access previous versions' permission, here
          we want everybody than can acces the object to see the history...
        """
        return True

    def showRevisionInfos(self):
        """Return True if the type of the context is versioned. """
        pr = getToolByName(self.context, 'portal_repository')
        if self.context.portal_type in pr.getVersionableContentTypes():
            return True
        else:
            return False

    def versionIsViewable(self, event):
        """
          Check if version we want to show is viewable.
        """
        return not bool(event['comments'] == HISTORY_REVISION_NOT_VIEWABLE)

    def renderCustomJS(self):
        """ """
        return '<script></script>'


class IHVersionPreviewView(BrowserView):
    """Makes it possible to display a preview of a given version."""

    def __init__(self, context, request):
        """ """
        super(IHVersionPreviewView, self).__init__(context, request)
        self.portal = getToolByName(self.context, 'portal_url').getPortalObject()
        self.portal_url = self.portal.absolute_url()

    def __call__(self, version_id):
        pr = getToolByName(self.context, 'portal_repository')
        self.versioned_object = pr.retrieve(self.context, version_id).object
        return super(IHVersionPreviewView, self).__call__()
