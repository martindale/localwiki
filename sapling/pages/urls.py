from django.conf.urls.defaults import *
from django.views.generic import ListView

from views import *
from feeds import PageChangesFeed
import models
from utils.constants import DATETIME_REGEXP
from models import Page

page_list_info = {
    'model': Page,
    'context_object_name': 'page_list',
}


def slugify(func):
    """Applies custom slugify to the slug and stashes original slug
    """
    def wrapped(*args, **kwargs):
        if 'slug' in kwargs:
            kwargs['original_slug'] = kwargs['slug']
            kwargs['slug'] = models.slugify(kwargs['slug'])
        return func(*args, **kwargs)
    return wrapped


urlpatterns = patterns('',
    url(r'^$', ListView.as_view(**page_list_info), name='title-index'),

    # TODO: break out into separate files app with own URLs
    url(r'^(?P<slug>.+)/_files/$', slugify(PageFileListView.as_view()),
        name='filelist'),
    url(r'^(?P<slug>.+)/_files/(?P<file>.+)/_revert/(?P<version>[0-9]+)$',
        slugify(PageFileRevertView.as_view()), name='file-revert'),
    url(r'^(?P<slug>.+)/_files/(?P<file>.+)/_upload$',
        slugify(upload), name='file-upload'),
    url(r'^(?P<slug>.+)/_files/(?P<file>.+)/_info/$',
        slugify(PageFileInfo.as_view()), name='file-info'),
    url(r'^(?P<slug>.+)/_files/(?P<file>.+)/_info/compare$',
        slugify(PageFileCompareView.as_view())),
    url((r'^(?P<slug>.+)/_files/(?P<file>.+)/_info/'
            r'(?P<version1>[0-9]+)\.\.\.(?P<version2>[0-9]+)?$'),
        slugify(PageFileCompareView.as_view()), name='file-compare-revisions'),
    url(r'^(?P<slug>.+)/_files/(?P<file>.+)/_info/'
        r'(?P<date1>%s)\.\.\.(?P<date2>%s)?$'
        % (DATETIME_REGEXP, DATETIME_REGEXP),
        slugify(PageFileCompareView.as_view()), name='file-compare-dates'),
    url(r'^(?P<slug>.+)/_files/(?P<file>.+)/_info/(?P<version>[0-9]+)$',
        slugify(PageFileVersionDetailView.as_view()), name='as_of_version'),
    url(r'^(?P<slug>.+)/_files/(?P<file>.+)/_info/(?P<date>%s)$'
        % DATETIME_REGEXP, slugify(PageFileVersionDetailView.as_view()),
        name='as_of_date'),
    url(r'^(?P<slug>.+)/_files/(?P<file>.+)$', slugify(PageFileView.as_view()),
        name='file'),
    url(r'^(?P<slug>.+)/_upload', slugify(upload), name='upload-image'),

    # TODO: Non-DRY here. Can break out into something like
    # ('/_history/',
    #  include(history_urls(list_view=..,compare_view=..)))?
    url(r'^(?P<slug>.+)/_history/compare$',
        slugify(PageCompareView.as_view())),
    url((r'^(?P<slug>.+)/_history/'
            r'(?P<version1>[0-9]+)\.\.\.(?P<version2>[0-9]+)?$'),
        slugify(PageCompareView.as_view()), name='compare-revisions'),
    url(r'^(?P<slug>.+)/_history/(?P<date1>%s)\.\.\.(?P<date2>%s)?$'
        % (DATETIME_REGEXP, DATETIME_REGEXP),
        slugify(PageCompareView.as_view()), name='compare-dates'),
    url(r'^(?P<slug>.+)/_history/(?P<version>[0-9]+)$',
        slugify(PageVersionDetailView.as_view()), name='as_of_version'),
    url(r'^(?P<slug>.+)/_history/(?P<date>%s)$' % DATETIME_REGEXP,
        slugify(PageVersionDetailView.as_view()), name='as_of_date'),
    url(r'^(?P<slug>.+)/_history/_feed/*$', PageChangesFeed(),
        name='changes-feed'),
    url(r'^(?P<slug>.+)/_history/$', slugify(PageHistoryList.as_view()),
        name='history'),

    url(r'^(?P<slug>.+)/_edit$', slugify(PageUpdateView.as_view()),
        name='edit'),
    url(r'^(?P<slug>.+)/_delete$', slugify(PageDeleteView.as_view()),
        name='delete'),
    url(r'^(?P<slug>.+)/_revert/(?P<version>[0-9]+)$',
        slugify(PageRevertView.as_view()), name='revert'),
    url(r'^(?P<slug>.+?)/*$', slugify(PageDetailView.as_view()), name='show'),
)
