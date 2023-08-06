# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import mimetypes
from functools import partial
from trytond.i18n import gettext
from trytond.model import ModelView, ModelSQL, fields
from trytond.model.exceptions import AccessError
from trytond.pyson import Eval
from trytond.pool import Pool
from trytond.wizard import Wizard, StateTransition, StateView, Button
from trytond.transaction import Transaction
from trytond.tools import grouped_slice
from trytond.config import config
from trytond.sendmail import SMTPDataManager, sendmail_transactional, sendmail
from genshi.template import TextTemplate
from jinja2 import Template as Jinja2Template
from babel.dates import format_date, format_datetime
from babel.numbers import format_currency
from emailvalid import check_email
from email import charset
from email.header import decode_header, Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64
from email.utils import formatdate, make_msgid

__all__ = ['Template', 'TemplateReport', 'SendTemplateStart', 'SendTemplate']


_ENGINES = [
    ('python', 'Python'),
    ('genshi', 'Genshi'),
    ('jinja2', 'Jinja2')
    ]
_RENDER_FIELDS = ['from_', 'sender', 'to', 'cc', 'bcc', 'subject',
    'plain', 'html']
# Determines max connections to database used for the mail send thread
MAX_DB_CONNECTION = config.getint('database', 'max_connections', default=50)


class Template(ModelSQL, ModelView):
    'Email Template'
    __name__ = 'electronic.mail.template'
    name = fields.Char('Name', required=True, translate=True)
    model = fields.Many2One('ir.model', 'Model', required=True)
    from_ = fields.Char('From', required=True)
    sender = fields.Char('Sender')
    to = fields.Char('To')
    cc = fields.Char('CC')
    bcc = fields.Char('BCC')
    subject = fields.Char('Subject', translate=True)
    language = fields.Char('Language', help=('Expression to find the ISO '
        'langauge code'))
    plain = fields.Text('Plain Text Body', translate=True)
    html = fields.Text('HTML Body', translate=True)
    reports = fields.Many2Many('electronic.mail.template.ir.action.report',
        'template', 'report', 'Reports')
    engine = fields.Selection(_ENGINES, 'Engine', required=True)
    triggers = fields.One2Many('ir.trigger', 'email_template', 'Triggers',
        context={
            'model': Eval('model'),
            'email_template': True,
            })
    signature = fields.Boolean('Use Signature',
        help='The signature from the User details will be appened to the '
        'mail.')
    create_action = fields.Boolean('Create Action', help='If set a wizard '
        'action will be created in the related model in order to send the '
        'template.')
    wizard = fields.Many2One("ir.action.wizard", 'Wizard',
        states={
            'readonly': Eval('create_action', False),
            },
        depends=['create_action'])
    activity = fields.Char('Activity',
        help='Generate a new activity record related a party:\n' \
            '${record.party.id}')
    smtp_server = fields.Many2One('smtp.server', 'SMTP Server',
        domain=[('state', '=', 'done')])
    # TODO Add styles

    @staticmethod
    def default_engine():
        return 'genshi'

    @staticmethod
    def default_create_action():
        return True

    @classmethod
    def check_xml_record(cls, records, values):
        '''It should be possible to overwrite templates'''
        return True

    @classmethod
    def eval(cls, expression, record, engine='genshi'):
        '''Evaluates the given :attr:expression

        :param expression: Expression to evaluate
        :param record: The browse record of the record
        '''
        engine_method = getattr(cls, '_engine_' + engine)
        return engine_method(expression, record)

    @staticmethod
    def template_context(record):
        """Generate the tempalte context

        This is mainly to assist in the inheritance pattern
        """
        return {'record': record}

    @classmethod
    def _engine_python(cls, expression, record):
        '''Evaluate the pythonic expression and return its value
        '''
        if expression is None:
            return ''

        assert record is not None, 'Record is undefined'
        template_context = cls.template_context(record)
        return eval(expression, template_context)

    @classmethod
    def _engine_genshi(cls, expression, record):
        '''
        :param expression: Expression to evaluate
        :param record: Browse record
        '''
        if not expression:
            return ''

        template = TextTemplate(expression)
        template_context = cls.template_context(record)
        return template.generate(**template_context).render()

    @classmethod
    def _engine_jinja2(cls, expression, record):
        '''
        :param expression: Expression to evaluate
        :param record: Browse record
        '''
        if not expression:
            return ''
        template = Jinja2Template(expression)
        template.environment.filters.update(cls.get_jinja_filters())
        template_context = cls.template_context(record)
        return template.render(template_context)

    @classmethod
    def get_jinja_filters(cls):
        '''
        Returns filters that are made available in the template context.
        * dateformat: Formats a date using babel
        * datetimeformat: Formats a datetime using babel
        * currencyformat: Formats the given number as currency
        For additional arguments that can be passed to these filters,
        refer to the Babel `Documentation
        <http://babel.edgewall.org/wiki/Documentation>`_.
        '''
        return {
            'dateformat': partial(format_date, locale=Transaction().language),
            'datetimeformat': partial(
                format_datetime, locale=Transaction().language
                ),
            'currencyformat': partial(
                format_currency, locale=Transaction().language
                ),
            }

    @classmethod
    def create(cls, vlist):
        templates = super(Template, cls).create(vlist)
        cls.create_wizards(templates)
        return templates

    @classmethod
    def write(cls, *args):
        Wizard = Pool().get('ir.action.wizard')

        super(Template, cls).write(*args)

        actions = iter(args)
        for templates, values in zip(actions, actions):
            if 'create_action' in values:
                if values['create_action']:
                    cls.create_wizards(templates)
                else:
                    cls.delete_wizards(templates)
            if values.get('name'):
                wizards = [t.wizard for t in templates if t.wizard]
                if wizards:
                    Wizard.write(wizards, {
                            'name': values.get('name'),
                            })

    @classmethod
    def delete(cls, templates):
        cls.delete_wizards(templates, ensure_create_action=False)
        super(Template, cls).delete(templates)

    @classmethod
    def create_wizards(cls, templates):
        pool = Pool()
        Keyword = pool.get('ir.action.keyword')
        Wizard = pool.get('ir.action.wizard')
        Lang = pool.get('ir.lang')

        langs = Lang.search([
            ('translatable', '=', True),
            ])
        for template in templates:
            if not template.create_action:
                continue
            wizard = Wizard()
            wizard.name = template.name
            wizard.wiz_name = 'electronic.mail.send.template'
            wizard.save()

            template.wizard = wizard
            template.save()

            if langs:
                for lang in langs:
                    with Transaction().set_context(language=lang.code,
                            fuzzy_translation=False):
                        lang_name, = cls.read([template.id], ['name'])
                        Wizard.write([wizard], lang_name)

            keyword = Keyword()
            keyword.keyword = 'form_action'
            keyword.action = wizard.action
            keyword.model = '%s,-1' % template.model.model
            keyword.save()

    @classmethod
    def delete_wizards(cls, templates, ensure_create_action=True):
        pool = Pool()
        Keyword = pool.get('ir.action.keyword')
        Wizard = pool.get('ir.action.wizard')
        wizards = [t.wizard for t in templates if t.wizard
            and (not ensure_create_action or not t.create_action)]
        if wizards:
            keywords = Keyword.search([
                    ('action', 'in', [w.action for w in wizards]),
                    ])
            if keywords:
                Keyword.delete(keywords)
            Wizard.delete(wizards)

    @staticmethod
    def validate_emails(email):
        for email in email.split(';'):
            if not check_email(email):
                return False
        return True

    @classmethod
    def mail_from_trigger(cls, records, trigger_id):
        """Send email from trigger"""
        Trigger = Pool().get('ir.trigger')

        trigger = Trigger(trigger_id)
        template = trigger.email_template
        server = template.smtp_server if template.smtp_server else None

        # TODO IMP to load first record and not browse all active ids
        data = template.pre_render(records)[0]
        values = cls.render(template, records, data, template.engine, True)
        cls.send(values, server)

    def pre_render(self, records):
        """Render a template with records"""
        Template = Pool().get('electronic.mail.template')

        engine = self.engine
        # render with language template
        if self.language:
            language = self.eval(self.language, records[0], self.engine)
            with Transaction().set_context(language=language):
                template = Template(self.id)
        else:
            template = self

        vals = []
        for record in records:
            v = {}
            for field_name in _RENDER_FIELDS:
                if len(records) > 1:
                    v[field_name] = getattr(template, field_name)
                else:
                    v[field_name] = Template.eval(
                        getattr(template, field_name), record, engine)
            vals.append(v)
        return vals

    @classmethod
    def render(cls, template, records, data, engine='genshi', render_html=True):
        """Render data with records"""
        vals = []
        for record in records:
            val = {}
            for k, v in list(data.items()):
                value = cls.eval(v, record, engine)
                if k in ['from_', 'sender', 'to', 'cc', 'bcc']:
                    value = value.replace(' ', '').replace(',', ';')
                    if value and not cls.validate_emails(value):
                        raise AccessError(
                            gettext('electronic_mail.msg_recipients_error'))
                val[k] = value

            if not render_html:
                val['html'] = None

            # Reports
            reports = []
            for report_action in template.reports:
                report = Pool().get(report_action.report_name, type='report')
                reports.append([report.execute(
                    [record.id], {
                                'id': record.id,
                                'action_id': report_action.id,
                                }),
                    cls.eval(report_action.email_filename, record, engine)])
            # The boolean for direct print in the tuple is useless for emails
            val['reports'] = [(r[0][0], r[0][1], r[0][3], r[1]) for r in reports]

            # SMTP server
            val['smtp'] = template.smtp_server

            # Signature
            val['signature'] = template.signature

            # Language
            if template.language:
                val['languages'] = [Template.eval(
                        template.language, record, engine)]

            vals.append(val)
        return vals

    @classmethod
    def send(cls, values, server=None):
        """Send values to SMTP server (send email)"""
        pool = Pool()
        SMTP = pool.get('smtp.server')
        User = pool.get('res.user')

        if not server:
            servers = SMTP.search([
                    ('state', '=', 'done'),
                    ('default', '=', True),
                    ], limit=1)
            if not servers:
                raise AccessError(
                    gettext('electronic_mail.msg_missing_default_smtp_server'))
            server, = servers

        for value in values:
            from_ = value['from_']
            recipients = value['to'].split(';')
            if not from_ or not recipients:
                continue

            if value.get('cc'):
                recipients += value['cc'].split(';')
            if value.get('bcc'):
                recipients += value['bcc'].split(';')

            message = MIMEMultipart()
            # message['Date'] = formatdate(localtime=1)
            if value.get('languages'):
                message.add_header('Content-Language', ', '.join(
                    value['languages']))
            message['Reply-to'] = from_
            message['Message-ID'] = make_msgid()
            message['From'] = from_
            if value.get('sender'):
                message['Sender'] = value['sender']
            message['To'] = value['to']
            if value.get('cc'):
                message['Cc'] = value['cc']
            if value.get('bcc'):
                message['Bcc'] = value['bcc']
            message['Subject'] = Header(value.get('subject'), 'utf-8')

            plain = value['plain']
            html = value['html']
            if value['signature']:
                user = User(Transaction().user)
                if user.signature:
                    plain = '%s\n-- \n%s' % (plain, user.signature)
                if user.signature_html:
                    html = '%s<br/>-- <br/>%s' % (html, user.signature_html)

            # TODO Add styles
            if html:
                html = "<html><head></head><body>%s</body></html>" % (html)

            if html and plain:
                body = MIMEMultipart('alternative')
                charset.add_charset('utf-8', charset.QP, charset.QP)
                body.attach(MIMEText(plain, 'plain', _charset='utf-8'))
                body.attach(MIMEText(html, 'html', _charset='utf-8'))
                message.attach(body)
            elif plain:
                charset.add_charset('utf-8', charset.QP, charset.QP)
                message.attach(MIMEText(plain, 'plain', _charset='utf-8'))
            elif html:
                charset.add_charset('utf-8', charset.QP, charset.QP)
                message.attach(MIMEText(html, 'html', _charset='utf-8'))

            if value.get('reports'):
                for report in value['reports']:
                    ext, data, filename, file_name = report[0:5]
                    filename = file_name or filename
                    filename = ext and '%s.%s' % (filename, ext) or filename
                    content_type, _ = mimetypes.guess_type(filename)
                    maintype, subtype = (
                        content_type or 'application/octet-stream'
                        ).split('/', 1)

                    attachment = MIMEBase(maintype, subtype)
                    attachment.set_payload(data)
                    encode_base64(attachment)
                    attachment.add_header(
                        'Content-Disposition', 'attachment', filename=filename)
                    message.attach(attachment)

            # TODO bool in template to sendmail or sendmail_transactional
            # sendmail_transactional get error socket getaddrinfo:
            # Name or service not known
            sendmail(from_, recipients, message, server.get_smtp_server())

            # datamanager = SMTPDataManager()
            # datamanager._server = server.get_smtp_server()
            # sendmail_transactional(from_, recipients, message,
            #     datamanager=datamanager)


class TemplateReport(ModelSQL):
    'Template - Report Action'
    __name__ = 'electronic.mail.template.ir.action.report'
    template = fields.Many2One('electronic.mail.template', 'Template')
    report = fields.Many2One('ir.action.report', 'Report')


class SendTemplateStart(ModelView):
    'Template Email Wizard Start'
    __name__ = 'electronic.mail.send.template.start'
    from_ = fields.Char('From', readonly=True)
    sender = fields.Char('Sender')
    to = fields.Char('To', required=True)
    cc = fields.Char('CC')
    bcc = fields.Char('BCC')
    subject = fields.Char('Subject', required=True)
    plain = fields.Text('Plain Text Body')
    html = fields.Text('HTML Text Body',
        states={
            'invisible': ~Eval('send_html', True),
            'required': Eval('send_html', True),
        }, depends=['send_html'])
    send_html = fields.Boolean('Send HTML',
        help='Send email with text and html')
    total = fields.Integer('Total', readonly=True,
        help='Total emails to send')
    template = fields.Many2One("electronic.mail.template", 'Template')


class SendTemplate(Wizard):
    "Send Email from template"
    __name__ = 'electronic.mail.send.template'
    start = StateView('electronic.mail.send.template.start',
        'electronic_mail.send_template_start', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Send', 'send', 'tryton-ok', default=True),
            ])
    send = StateTransition()

    def default_start(self, fields):
        default = self.render_fields(self.__name__)
        if default['html']:
            default['send_html'] = True
        return default

    def render_fields(self, name):
        pool = Pool()
        Wizard = pool.get('ir.action.wizard')

        context = Transaction().context
        active_ids = context.get('active_ids')
        action_id = context.get('action_id', None)

        wizard = Wizard(action_id)
        if wizard.template:
            template = wizard.template[0]
        else:
            raise AccessError(
                gettext('electronic_mail.msg_missing_template'))
        total = len(active_ids)

        # TODO IMP to load first record and not browse all active ids
        records = pool.get(template.model.model).browse(active_ids)

        default = {}
        default['template'] = template.id
        default['total'] = total
        for k, v in list(template.pre_render(records)[0].items()):
            default[k] = v
        return default

    def transition_send(self):
        self.render_and_send()
        return 'end'

    def render_and_send(self):
        pool = Pool()
        Template = pool.get('electronic.mail.template')

        template = self.start.template
        engine = template.engine
        records = Transaction().context.get('active_ids')

        data = {}
        for field_name in _RENDER_FIELDS:
            data[field_name] = getattr(self.start, field_name)

        for sub_records in grouped_slice(records, MAX_DB_CONNECTION):
            records = pool.get(template.model.model).browse(sub_records)
            values = Template.render(
                template, records, data, engine, self.start.send_html)
            Template.send(values, template.smtp_server)
        # TODO Add activity
