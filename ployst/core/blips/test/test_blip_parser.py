# -*- coding: utf-8 -*-
from unittest import TestCase
from ..blip import Blip

FULL = u"""
Something to consider.

Hey here is a link https://python.org from @orne #language:python !alex
>barrobés >read-later
""".strip()

TAGS = u"Python rules #language:python #programming #rating:5 I love it"


class TestBlipParseText(TestCase):

    def test_parse_full(self):
        blip = Blip.from_text(FULL)
        self.assertEqual(blip.mentions, [u'orne'])
        self.assertEqual(blip.privates, [u'alex'])
        self.assertEqual(blip.streams, [u'barrobés', u'read-later'])
        self.assertEqual(blip.tags, [u'language:python'])

    def test_parse_tags(self):
        blip = Blip.from_text(TAGS)
        self.assertEqual(blip.mentions, [])
        self.assertEqual(blip.privates, [])
        self.assertEqual(blip.streams, [])
        self.assertEqual(blip.tags,
                         [u'language:python', 'programming', 'rating:5'])

    def test_parse_metadata(self):
        blip = Blip.from_text(TAGS)
        self.assertEqual(blip.metadata, {'language': 'python', 'rating': '5'})
        self.assertEqual(blip['language'], 'python')
        self.assertEqual(blip['rating'], '5')


YAML_FULL = u"""
title: My blip
text: "Here is a blip about a nice programming language"
mentions:
    - orne
privates:
    - alex
tags:
    - language:python
    - rating:5
    - programming
streams:
    - barrobés
    - read-later
""".strip()


"""
class TestBlipParseYaml(TestCase):

    def test_parse_full(self):
        blip = Blip.from_yaml(YAML_FULL)
        self.assertEqual(blip['language'], 'python')
        self.assertEqual(blip['rating'], '5')
        self.assertEqual(blip.mentions, [u'orne'])
        self.assertEqual(blip.privates, [u'alex'])
        self.assertEqual(blip.streams, [u'barrobés', u'read-later'])
"""
