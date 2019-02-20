from telethon import TelegramClient, events, sync, utils
from time import sleep
import unittest
import logging
import os
from bot import messages, keyboard


logging.basicConfig(level=logging.ERROR)
logging.getLogger('telethon').setLevel(logging.CRITICAL)


class TestBot(unittest.TestCase):
    def setUp(self):
        self.api_id = os.environ.get('TELETHON_API_ID')
        self.api_hash = os.environ.get('TELETHON_API_HASH')
        self.client = TelegramClient('data', self.api_id, self.api_hash)
        self.messages = messages
        self.keyboard = keyboard


    def test_start_command(self):
        with self.client:
            self.client.send_message('koya_bar_bot', '/start')
            sleep(1)
            answer = self.client.get_messages('koya_bar_bot', limit=1)[0]
            self.assertEqual(self.messages['start'], answer.message)
            self.assertIsNotNone(answer.reply_markup)
            self.assertEqual(len(self.keyboard), len(answer.reply_markup.rows))


    def test_joke_command(self):
        with self.client:
            self.client.send_message('koya_bar_bot', '/joke')
            sleep(1)
            answer = self.client.get_messages('koya_bar_bot', limit=1)[0]
            self.assertTrue(len(answer.message) > 10)


    def test_article_command(self):
        with self.client:
            self.client.send_message('koya_bar_bot', '/article')
            sleep(5)
            answer = self.client.get_messages('koya_bar_bot', limit=1)[0]
            self.assertIsNotNone(answer.media)
            self.assertTrue(len(answer.entities) == 3)
            self.assertTrue(answer.entities[0].length > 4)
            self.assertTrue(answer.entities[1].length > 4)
            self.assertTrue(answer.entities[2].length > 4)


    def test_article_command_with_tag(self):
        with self.client:
            self.client.send_message('koya_bar_bot', '/article snoop dogg')
            sleep(5)
            answer = self.client.get_messages('koya_bar_bot', limit=1)[0]
            self.assertIsNotNone(answer.media)
            self.assertTrue(len(answer.entities) == 3)
            self.assertTrue(answer.entities[0].length > 4)
            self.assertTrue(answer.entities[1].length > 4)
            self.assertTrue(answer.entities[2].length > 4)


    def test_article_command_with_wrong_tag(self):
        with self.client:
            self.client.send_message('koya_bar_bot', '/article asdfasd')
            sleep(4)
            answer = self.client.get_messages('koya_bar_bot', limit=1)[0]
            self.assertIsNone(answer.media)
            self.assertIsNone(answer.entities)
            self.assertEqual(answer.message, self.messages['no_article'])


    def test_unknown_command(self):
        with self.client:
            self.client.send_message('koya_bar_bot', '/random')
            sleep(1)
            answer = self.client.get_messages('koya_bar_bot', limit=1)[0]
            self.assertEqual(self.messages['unknown_command'], answer.message)


    def test_text_messages(self):
        with self.client:
            self.client.send_message('koya_bar_bot', 'text')
            sleep(1)
            answer = self.client.get_messages('koya_bar_bot', limit=1)[0]
            self.assertEqual(self.messages['text'], answer.message)


if __name__ == '__main__':
    unittest.main()
