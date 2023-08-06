import datetime
import logging
import unittest

from graphene.utils.str_converters import to_camel_case
import factories
from ..constants import (
    LOOKUP_FILTER_TERM,
    LOOKUP_FILTER_TERMS,
    LOOKUP_FILTER_RANGE,
    LOOKUP_FILTER_EXISTS,
    LOOKUP_FILTER_PREFIX,
    LOOKUP_FILTER_WILDCARD,
    # LOOKUP_FILTER_REGEXP,
    # LOOKUP_FILTER_FUZZY,
    # LOOKUP_FILTER_TYPE,
    LOOKUP_FILTER_GEO_DISTANCE,
    LOOKUP_FILTER_GEO_POLYGON,
    LOOKUP_FILTER_GEO_BOUNDING_BOX,
    LOOKUP_QUERY_CONTAINS,
    LOOKUP_FILTER_PREFIX,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
    LOOKUP_QUERY_STARTSWITH,
    LOOKUP_QUERY_ENDSWITH,
    LOOKUP_QUERY_ISNULL,
    LOOKUP_QUERY_EXCLUDE,
    VALUE,
    LOWER,
    UPPER,
)
from .base import BaseGrapheneElasticTestCase

__all__ = (
    'FilterBackendElasticTestCase',
)

logger = logging.getLogger(__name__)


class FilterBackendElasticTestCase(BaseGrapheneElasticTestCase):

    endpoint = 'allPostDocuments'

    def setUp(self):
        super(FilterBackendElasticTestCase, self).setUp()

        # Important thing to know about the factories.
        # The `PostFactory` factory has `num_views` between 0 and 1_000.
        # The `ManyViewsPostFactory` factory has `num_views` between
        # 2_000 and 10_000.
        self.num_elastic_posts = 4
        self.elastic_posts = factories.PostFactory.create_batch(
            self.num_elastic_posts,
            category='Elastic',
            tags=None,
            created_at=self.faker.date_between(
                start_date="+1d", end_date="+30d"
            )
        )
        for _post in self.elastic_posts:
            _post.save()

        self.num_django_posts = 3
        self.django_posts = factories.PostFactory.create_batch(
            self.num_django_posts,
            category='Django',
            created_at=self.faker.date_between(
                start_date="+1d", end_date="+30d"
            )
        )
        for _post in self.django_posts:
            _post.save()

        self.num_python_posts = 2
        self.python_posts = factories.ManyViewsPostFactory.create_batch(
            self.num_python_posts,
            category='Python',
            created_at=self.faker.date_between(
                start_date="-30d", end_date="-1d"
            )
        )
        for _post in self.python_posts:
            _post.save()

        self.num_all_posts = (
            self.num_elastic_posts +
            self.num_django_posts +
            self.num_python_posts
        )
        self.all_posts = (
            self.elastic_posts + self.django_posts + self.python_posts
        )

        self.num_future_posts = (
            self.num_elastic_posts + self.num_django_posts
        )
        self.num_past_posts = self.num_python_posts
        self.today = datetime.datetime.now().strftime('%Y-%m-%d')

        self.sleep()

    def __test_filter_text_lookups(self,
                                   query,
                                   num_posts,
                                   lookup=VALUE,
                                   field='category'):
        """Test filter text lookups (on field `category`).

        :param query:
        :param num_posts:
        :param field:
        :return:
        """
        _query = """
        query {
          %s(filter:{%s:{%s:%s}}) {
            edges {
              node {
                category
                title
                content
                numViews
                comments{
                    author
                    content
                    createdAt
                }
              }
            }
          }
        }
        """ % (self.endpoint, field, lookup, query)
        logger.debug(_query)
        executed = self.client.execute(_query)
        self.assertEqual(
            len(executed['data']['allPostDocuments']['edges']),
            num_posts
        )

    def __test_nested_filter_lookups(
        self,
        *fields,
        lookup,
        value,
        num_posts
    ):
        """Test nested filter lookups and check num of results.

        :param fields: fields hierarchy
        :param lookup:
        :param value:
        :param num_posts: num of results
        :return:
        """
        def _query_params():
            s = ""
            for field in fields:
                s += "{}:{{".format(field)
            s += "{}: {}".format(lookup, value)
            s += "}" * len(fields)
            return s

        _query = """
        query {
            %s(filter:{%s}) {
                edges {
                    node {
                        category
                        title
                        content
                        numViews
                        comments{
                            author
                            tag
                            content
                            createdAt
                        }
                    }
                }
            }
        }
        """ % (self.endpoint, _query_params())
        logger.info(_query)
        executed = self.client.execute(_query)
        self.assertEqual(
            len(executed["data"][self.endpoint]["edges"]),
            num_posts,
            _query
        )

    def __test_filter_number_lookups(self,
                                     field,
                                     value,
                                     num_posts,
                                     lookup=LOOKUP_QUERY_GT):
        """Test filter number lookups (on field `num_views`).

        :param field:
        :param value:
        :param num_posts:
        :param lookup:
        :return:
        """
        _query = """
        query {
          %s(filter:{%s:{%s:%s}}) {
            edges {
              node {
                category
                title
                content
                numViews
                comments{
                    author
                    content
                    createdAt
                }
              }
            }
          }
        }
        """ % (self.endpoint, field, lookup, value)
        logger.debug(_query)
        executed = self.client.execute(_query)
        self.assertEqual(
            len(executed['data']['allPostDocuments']['edges']),
            num_posts,
            _query
        )

    def _test_filter_term_terms_lookup(self):
        """"Test filter `term` and `terms` lookups (on field `category`).

        :return:
        """
        with self.subTest('Test filter on field `category` "Django" '
                          'using default lookup (`term`)'):
            self.__test_filter_text_lookups(
                '"Django"',
                self.num_django_posts
            )

        with self.subTest('Test filter on field `category` "Django" '
                          'using `term` lookup'):
            self.__test_filter_text_lookups(
                '"Django"',
                self.num_django_posts,
                lookup=LOOKUP_FILTER_TERM
            )

        with self.subTest('Test filter on field `category` "Elastic" '
                          'using default lookup (`term`)'):
            self.__test_filter_text_lookups(
                '"Elastic"',
                self.num_elastic_posts
            )

        with self.subTest('Test filter on field `category` "Elastic" '
                          'using `term` lookup'):
            self.__test_filter_text_lookups(
                '"Elastic"',
                self.num_elastic_posts,
                LOOKUP_FILTER_TERM
            )

        with self.subTest('Test filter on field `category` '
                          '["Elastic", "Django"] using `terms` lookup'):
            self.__test_filter_text_lookups(
                '["Elastic", "Django"]',
                self.num_elastic_posts + self.num_django_posts,
                LOOKUP_FILTER_TERMS
            )

        with self.subTest('Test filter on field `category` '
                          '["Elastic", "Django"] using `in` lookup'):
            self.__test_filter_text_lookups(
                '["Elastic", "Django"]',
                self.num_elastic_posts + self.num_django_posts,
                LOOKUP_QUERY_IN
            )

    def _test_filter_prefix_starts_ends_with_contains_wildcard_lookups(self):
        """"Test filters `prefix`, `starts_with` and `ends_with` lookups (on
        field `category`).

        :return:
        """
        with self.subTest('Test filter on field `category` "Elastic" '
                          'using `contains` lookup'):
            self.__test_filter_text_lookups(
                '"ytho"',
                self.num_python_posts,
                LOOKUP_QUERY_CONTAINS
            )

        with self.subTest('Test filter on field `category` "Elastic" '
                          'using `wildcard` lookup'):
            self.__test_filter_text_lookups(
                '"*ytho*"',
                self.num_python_posts,
                LOOKUP_FILTER_WILDCARD
            )

        with self.subTest('Test filter on field `category` "Elastic" '
                          'using `prefix` lookup'):
            self.__test_filter_text_lookups(
                '"Pyth"',
                self.num_python_posts,
                to_camel_case(LOOKUP_FILTER_PREFIX)
            )

        with self.subTest('Test filter on field `category` "Elastic" '
                          'using `starts_with` lookup'):
            self.__test_filter_text_lookups(
                '"Pyth"',
                self.num_python_posts,
                to_camel_case(LOOKUP_QUERY_STARTSWITH)
            )

        with self.subTest('Test filter on field `category` "Elastic" '
                          'using `ends_with` lookup'):
            self.__test_filter_text_lookups(
                '"ython"',
                self.num_python_posts,
                to_camel_case(LOOKUP_QUERY_ENDSWITH)
            )

    def _test_filter_exclude_lookup(self):
        """"Test filter `exclude` lookup (on field `category`).

        :return:
        """
        with self.subTest('Test filter on field `category` "Elastic" '
                          'using `exclude` lookup'):
            self.__test_filter_text_lookups(
                '"Python"',
                self.num_all_posts - self.num_python_posts,
                LOOKUP_QUERY_EXCLUDE
            )

    def _test_filter_exists_is_null_lookups(self):
        """"Test filter `exists` lookup (on fields `category`
        and `i_do_not_exist`).

        :return:
        """
        with self.subTest('Test filter on field `category`'
                          'using `exists` lookup'):
            self.__test_filter_text_lookups(
                'true',
                self.num_all_posts,
                LOOKUP_FILTER_EXISTS
            )

        with self.subTest('Test filter on field `category`'
                          'using `is_null` lookup'):
            self.__test_filter_text_lookups(
                'false',
                self.num_all_posts,
                to_camel_case(LOOKUP_QUERY_ISNULL)
            )

        # TODO: See if we can test this case
        # with self.subTest('Test filter on field `i_do_not_exist`'
        #                   'using `exists` lookup'):
        #     self._test_filter_text_lookups(
        #         'true',
        #         0,
        #         LOOKUP_FILTER_EXISTS,
        #         field='i_do_not_exist'
        #     )

    def _test_filter_gt_gte_lt_lte_range_lookups(self):
        """"Test filter `gt`, `gte`, `lt`, `lte`, `range` lookups (on
        field `num_views`).

        :return:
        """
        # This should be all posts, since minimum value for posts is 0.
        with self.subTest('Test filter on field `num_views` '
                          'using `gt` lookup'):
            self.__test_filter_number_lookups(
                'numViews',
                '{decimal:"0.1"}',
                self.num_all_posts
            )

        # This should be Python posts only, since they may start at 2_000.
        with self.subTest('Test filter on field `num_views` '
                          'using `gt` lookup'):
            self.__test_filter_number_lookups(
                'numViews',
                '{decimal:"1999"}',
                self.num_python_posts
            )

        # This should be Elastic and Django posts only, since they have
        # dates in future.
        with self.subTest('Test filter on field `created_at` '
                          'using `gt` lookup'):
            self.__test_filter_number_lookups(
                'createdAt',
                '{date:"%s"}' % self.today,
                self.num_future_posts,
                lookup=LOOKUP_QUERY_GT
            )

        # This shall be all posts (including 0).
        with self.subTest('Test filter on field `num_views` '
                          'using `gte` lookup'):
            self.__test_filter_number_lookups(
                'numViews',
                '{decimal:"0"}',
                self.num_all_posts,
                lookup=LOOKUP_QUERY_GTE
            )

        # This should be Elastic and Django posts only, since they have
        # dates in future.
        with self.subTest('Test filter on field `created_at` '
                          'using `gt` lookup'):
            self.__test_filter_number_lookups(
                'createdAt',
                '{date:"%s"}' % self.today,
                self.num_future_posts,
                lookup=LOOKUP_QUERY_GTE
            )

        # This shall be Python posts only, since they may start at 2_000.
        with self.subTest('Test filter on field `num_views` '
                          'using `gte` lookup'):
            self.__test_filter_number_lookups(
                'numViews',
                '{decimal:"2000"}',
                self.num_python_posts,
                lookup=LOOKUP_QUERY_GTE
            )

        # This shall be all posts, since maximum is 10_000.
        with self.subTest('Test filter on field `num_views` '
                          'using `lt` lookup'):
            self.__test_filter_number_lookups(
                'numViews',
                '{decimal:"10001"}',
                self.num_all_posts,
                lookup=LOOKUP_QUERY_LT
            )

        # This should be Python posts only, since they have
        # dates in past.
        with self.subTest('Test filter on field `created_at` '
                          'using `lt` lookup'):
            self.__test_filter_number_lookups(
                'createdAt',
                '{date:"%s"}' % self.today,
                self.num_past_posts,
                lookup=LOOKUP_QUERY_LT
            )

        # This shall exclude Python posts, since they start at 2_000.
        with self.subTest('Test filter on field `num_views` '
                          'using `lt` lookup'):
            self.__test_filter_number_lookups(
                'numViews',
                '{decimal:"2000"}',
                self.num_all_posts - self.num_python_posts,
                lookup=LOOKUP_QUERY_LT
            )

        # This shall be all posts, since maximum is 10_000.
        with self.subTest('Test filter on field `num_views` '
                          'using `lte` lookup'):
            self.__test_filter_number_lookups(
                'numViews',
                '{decimal:"10000"}',
                self.num_all_posts,
                lookup=LOOKUP_QUERY_LTE
            )

        # This should be Python posts only, since they have
        # dates in past.
        with self.subTest('Test filter on field `created_at` '
                          'using `lte` lookup'):
            self.__test_filter_number_lookups(
                'createdAt',
                '{date:"%s"}' % self.today,
                self.num_past_posts,
                lookup=LOOKUP_QUERY_LTE
            )

        # This shall exclude all Python posts, since they start at 2_000
        with self.subTest('Test filter on field `num_views` '
                          'using `lte` lookup'):
            self.__test_filter_number_lookups(
                'numViews',
                '{decimal:"1999"}',
                self.num_all_posts - self.num_python_posts,
                lookup=LOOKUP_QUERY_LTE
            )

        # To test range successfully, since we do not make specific range
        # factories in between, we simply count the number of posts
        # between 100 and 300 and test.
        with self.subTest('Test filter on field `num_views` '
                          'using `range` lookup'):
            _count = 0
            for _p in self.all_posts:
                if 100 <= _p.num_views <= 300:
                    _count += 1
            self.__test_filter_number_lookups(
                'numViews',
                '{%s: {decimal:"%s"}, %s: {decimal:"%s"}}' % (
                    LOWER,
                    '100',
                    UPPER,
                    '300'
                ),
                _count,
                lookup=LOOKUP_FILTER_RANGE
            )

    def _test_filter_nested_lookup(self):

        with self.subTest('Test filter on field `comments.tag`'
                          'using `term` lookup'):
            _count = 0
            for _post in self.all_posts:
                for _post_comment in _post.comments:
                    if _post_comment.tag == "Python":
                        _count += 1
                        break

            self.__test_nested_filter_lookups(
                "comments",
                "tag",
                lookup="term",
                value='"Python"',
                num_posts=_count
            )

        with self.subTest('Test filter on field `comments.tag`'
                          'using `terms` lookup'):
            _count = 0
            for _post in self.all_posts:
                for _post_comment in _post.comments:
                    if _post_comment.tag in ["Python", "MongoDB"]:
                        _count += 1
                        break

            self.__test_nested_filter_lookups(
                "comments",
                "tag",
                lookup="terms",
                value='["Python", "MongoDB"]',
                num_posts=_count
            )

    # TODO: Test range dates

    def test_all(self):
        """Test all.

        Since we don't write in specific tests, it's more efficient to run
        them all from a single method in order to save on speed ups between
        tests.
        """
        self._test_filter_term_terms_lookup()
        self._test_filter_prefix_starts_ends_with_contains_wildcard_lookups()
        self._test_filter_exclude_lookup()
        self._test_filter_exists_is_null_lookups()
        self._test_filter_gt_gte_lt_lte_range_lookups()
        self._test_filter_nested_lookup()


if __name__ == '__main__':
    unittest.main()
