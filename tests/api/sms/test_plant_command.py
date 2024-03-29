import unittest

from app.api.sms.plant_action import PlantCommand
from app.model.sms_request import SmsRequest


class PlantCommandTest(unittest.TestCase):

    def setUp(self):

        self.sms = SmsRequest()

    def test_plant_command(self):
        valid_messages = [
            'plant 20 potato',
            'plant potato 20',
            'tanam 20 potato',
            'tanam potato 20'
        ]

        for body in valid_messages:
            self.sms.body = body
            cmd = PlantCommand(self.sms)
            self.assertTrue(cmd.valid())
            self.assertEqual(20, cmd.amount)
            self.assertEqual('potato', cmd.plant)

    def test_plant_command_without_plant(self):
        invalid_messages = [
            'plant 20',
            'tanam 20'
        ]

        for body in invalid_messages:
            self.sms.body = body
            cmd = PlantCommand(self.sms)
            self.assertFalse(cmd.valid())

    def test_plant_command_without_amount(self):
        invalid_messages = [
            'plant potato',
            'tanam potato'
        ]

        for body in invalid_messages:
            self.sms.body = body
            cmd = PlantCommand(self.sms)
            self.assertFalse(cmd.valid())

    def test_plant_command_with_invalid_command(self):
        invalid_messages = [
            'sell 20 potato',
            'sell potato 20',
            'jual 20 potato',
            'jual potato 20'
        ]

        for body in invalid_messages:
            self.sms.body = body
            cmd = PlantCommand(self.sms)
            self.assertFalse(cmd.valid())

    def test_multi_word_plant(self):
        invalid_messages = {
            'plant 20 chinese broccoli': ('chinese broccoli', 20),
            'plant chinese broccoli 20': ('chinese broccoli', 20),
            'tanam 20 sweet potato': ('sweet potato', 20),
            'tanam sweet potato 20': ('sweet potato', 20),
        }

        for body, v in invalid_messages.items():
            self.sms.body = body
            cmd = PlantCommand(self.sms)

            self.assertTrue(cmd.valid())
            self.assertEqual(v[0], cmd.plant)
            self.assertEqual(v[1], cmd.amount)
