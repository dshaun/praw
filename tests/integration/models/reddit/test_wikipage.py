from praw.models import Redditor, WikiPage
from prawcore import NotFound
import pytest

from ... import IntegrationTest


class TestWikiPage(IntegrationTest):
    def test_content_md(self):
        subreddit = self.reddit.subreddit(
            pytest.placeholders.test_subreddit)
        page = WikiPage(self.reddit, subreddit, 'test')

        with self.recorder.use_cassette('TestWikiPage.test_content_md'):
            assert page.content_md

    def test_edit(self):
        subreddit = self.reddit.subreddit(
            pytest.placeholders.test_subreddit)
        page = WikiPage(self.reddit, subreddit, 'test')

        self.reddit.read_only = False
        with self.recorder.use_cassette('TestWikiPage.test_edit'):
            page.edit('PRAW updated')

    def test_edit__with_reason(self):
        subreddit = self.reddit.subreddit(
            pytest.placeholders.test_subreddit)
        page = WikiPage(self.reddit, subreddit, 'test')

        self.reddit.read_only = False
        with self.recorder.use_cassette('TestWikiPage.test_edit__with_reason'):
            page.edit('PRAW updated with reason', reason='PRAW testing')

    def test_invalid_page(self):
        subreddit = self.reddit.subreddit(
            pytest.placeholders.test_subreddit)
        page = WikiPage(self.reddit, subreddit, 'invalid')

        with self.recorder.use_cassette('TestWikiPage.test_invalid_page'):
            with pytest.raises(NotFound):
                page.content_md

    def test_revision_by(self):
        subreddit = self.reddit.subreddit(
            pytest.placeholders.test_subreddit)
        page = WikiPage(self.reddit, subreddit, 'test')

        with self.recorder.use_cassette('TestWikiPage.test_revision_by'):
            assert isinstance(page.revision_by, Redditor)


class TestWikiPageModeration(IntegrationTest):
    def test_add(self):
        subreddit = self.reddit.subreddit(
            pytest.placeholders.test_subreddit)
        page = WikiPage(self.reddit, subreddit, 'test')

        self.reddit.read_only = False
        with self.recorder.use_cassette('TestWikiPageModeration.test_add'):
            page.mod.add('bboe')

    def test_remove(self):
        subreddit = self.reddit.subreddit(
            pytest.placeholders.test_subreddit)
        page = WikiPage(self.reddit, subreddit, 'test')

        self.reddit.read_only = False
        with self.recorder.use_cassette('TestWikiPageModeration.test_remove'):
            page.mod.remove('bboe')

    def test_settings(self):
        subreddit = self.reddit.subreddit(
            pytest.placeholders.test_subreddit)
        page = WikiPage(self.reddit, subreddit, 'test')

        self.reddit.read_only = False
        with self.recorder.use_cassette(
                'TestWikiPageModeration.test_settings'):
            settings = page.mod.settings()
        assert {'editors': [], 'listed': True, 'permlevel': 0} == settings

    def test_update(self):
        subreddit = self.reddit.subreddit(
            pytest.placeholders.test_subreddit)
        page = WikiPage(self.reddit, subreddit, 'test')

        self.reddit.read_only = False
        with self.recorder.use_cassette(
                'TestWikiPageModeration.test_update'):
            updated = page.mod.update(listed=False, permlevel=1)
        assert {'editors': [], 'listed': False, 'permlevel': 1} == updated
