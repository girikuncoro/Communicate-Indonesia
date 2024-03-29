import logging
from app.api.sms.base_action import OneArgCommand
from app.command.base import Action
from app.model.farm import Farm

from app.i18n import _
from google.appengine.ext import ndb
from app.model.permission import RECORD_PLANT


class PlantAction(Action):
    """
    Execute a plant operation
    """
    CMD = 'plant'

    def __init__(self, command):
        super(PlantAction, self).__init__(command)

    def execute(self):
        """
        Update plant totals
        """
        cmd = self.command
        user = cmd.sms.user

        if RECORD_PLANT not in user.permissions:
            logging.info('{} - User {} does not have permission {}'.format(
                cmd.sms.id, user.id, RECORD_PLANT))
            return _('Command not allowed')

        plant = Farm.query(ndb.AND(Farm.district_id == user.district_id,
                                   Farm.crop_name == cmd.plant,
                                   Farm.action == 'plant')).get()
        if not plant:
            plant = Farm(id=Farm.id(),
                         district_id=user.district_id,
                         action=self.CMD,
                         crop_name=cmd.plant,
                         quantity=0)

        plant.quantity += cmd.amount
        plant.put()

        return _('Plant command succeeded')


class PlantCommand(OneArgCommand):
    """
    Represents a plant command

    A plant command can take the form of:
        <command> <value> <plant>
        <command> <plant> <value>

    eg.
        plant 20 potato
        plant potato 20
    """
    VALID_CMDS = [
        'plant',  # en
        'tanam',  # in
    ]

    def __init__(self, sms):
        super(PlantCommand, self).__init__(sms)
        self.plant = None
        self.amount = None

        words = self.message.split()

        for word in words:
            if word.isdigit():
                self.amount = int(word)
                words.remove(word)
                break

        if words:
            self.plant = ' '.join(words)

    def valid(self):
        return super(PlantCommand, self).valid() \
            and self.amount and self.plant
