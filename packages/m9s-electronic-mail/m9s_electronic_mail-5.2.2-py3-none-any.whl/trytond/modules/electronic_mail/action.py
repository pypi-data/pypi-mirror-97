# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond import backend

__all__ = ['ActionReport', 'ActionWizard']


class ActionReport(metaclass=PoolMeta):
    __name__ = 'ir.action.report'
    email_filename = fields.Char('Email File Name', translate=True,
        help='File name e-mail attachment without extension. '
        'eg. sale_${record.reference}')

    @classmethod
    def __register__(cls, module_name):
        TableHandler = backend.get('TableHandler')
        table = TableHandler(cls, module_name)

        # Migration from 3.8: rename file_name into email_filename
        if (table.column_exist('file_name')
                and not table.column_exist('email_filename')):
            table.column_rename('file_name', 'email_filename')

        super(ActionReport, cls).__register__(module_name)


class ActionWizard(metaclass=PoolMeta):
    __name__ = 'ir.action.wizard'
    template = fields.One2Many("electronic.mail.template", 'wizard', 'Template')
