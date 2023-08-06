# This file is part electronic_mail module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import activity
from . import template
from . import action
from . import user
from . import trigger

__all__ = ['register']


def register():
    Pool.register(
        template.Template,
        template.TemplateReport,
        template.SendTemplateStart,
        action.ActionReport,
        action.ActionWizard,
        user.User,
        trigger.Trigger,
        module='electronic_mail', type_='model')
    Pool.register(
        activity.Activity,
        depends=['activity'],
        module='electronic_mail', type_='model')
    Pool.register(
        template.SendTemplate,
        module='electronic_mail', type_='wizard')
