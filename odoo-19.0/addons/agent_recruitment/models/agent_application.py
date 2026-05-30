from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from markupsafe import Markup

class AgentApplication(models.Model):
    _name = 'agent.application'
    _description = 'Agent Application'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Ism', required=True, tracking=True)
    last_name = fields.Char(string='Familiya', required=True, tracking=True)
    phone = fields.Char(string='Telefon raqam', required=True, tracking=True)
    email = fields.Char(string='Email', required=True, tracking=True)
    age = fields.Integer(string='Yoshi', required=True, tracking=True)
    gender = fields.Selection([
        ('male', 'Erkak'),
        ('female', 'Ayol')
    ], string='Jinsi', required=True, tracking=True)
    has_experience = fields.Selection([
        ('yes', 'Ha'),
        ('no', 'Yo\'q')
    ], string='Tajribasi bormi?', required=True, default='no', tracking=True)
    experience_details = fields.Text(string='Tajribasi haqida', tracking=True)
    resume = fields.Binary(string='Resume (CV)', attachment=True)
    resume_name = fields.Char(string='Resume File Name')
    bio = fields.Text(string='O\'zi haqida qisqacha ma\'lumot', tracking=True)
    location = fields.Selection([
        ('toshkent_sh', 'Toshkent shahri'),
        ('toshkent_v', 'Toshkent viloyati'),
        ('andijon', 'Andijon viloyati'),
        ('buxoro', 'Buxoro viloyati'),
        ('fargona', 'Farg\'ona viloyati'),
        ('jizzax', 'Jizzax viloyati'),
        ('xorazm', 'Xorazm viloyati'),
        ('namangan', 'Namangan viloyati'),
        ('navoiy', 'Navoiy viloyati'),
        ('qashqadaryo', 'Qashqadaryo viloyati'),
        ('samarqand', 'Samarqand viloyati'),
        ('sirdaryo', 'Sirdaryo viloyati'),
        ('surxondaryo', 'Surxondaryo viloyati'),
        ('qoraqalpogiston', 'Qoraqalpog\'iston Respublikasi'),
    ], string='Qaysi hududda ishlamoqchi', required=True, tracking=True)
    working_time = fields.Selection([
        ('full', 'To\'liq stavka'),
        ('half', 'Yarim stavka')
    ], string='Ishlash vaqti', required=True, tracking=True)
    state = fields.Selection([
        ('new', 'Yangi'),
        ('reviewed', 'Ko\'rib chiqildi'),
        ('accepted', 'Qabul qilindi'),
        ('rejected', 'Rad etildi')
    ], string='Holati', default='new', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        records = super(AgentApplication, self).create(vals_list)
        for record in records:
            # Administratorlar kanalini qidirish
            channel = self.env['discuss.channel'].sudo().search([('name', '=', 'Administratorlar')], limit=1)
            if not channel:
                # Agar kanal bo'lmasa, uni yaratish
                channel = self.env['discuss.channel'].sudo().create({
                    'name': 'Administratorlar',
                    'channel_type': 'channel',
                })
            
            # Xabar matni
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            menu_id = self.env.ref('agent_recruitment.menu_agent_application').id
            action_id = self.env.ref('agent_recruitment.action_agent_application').id
            url = f"{base_url}/web#id={record.id}&menu_id={menu_id}&action={action_id}&model=agent.application&view_type=form"
            
            message_body = f"""
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #007bff;">
                    <h3 style="color: #007bff; margin-top: 0;">🚀 Yangi agent arizasi!</h3>
                    <p><b>Ism:</b> {record.name} {record.last_name}</p>
                    <p><b>Telefon:</b> {record.phone}</p>
                    <p><b>Hudud:</b> {record.location}</p>
                    <p><b>Ish vaqti:</b> {dict(self._fields['working_time'].selection).get(record.working_time)}</p>
                    <div style="margin-top: 15px;">
                        <a href="{url}" style="background-color: #007bff; color: white; padding: 8px 15px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                            Arizani ko'rish
                        </a>
                    </div>
                </div>
            """
            
            channel.message_post(
                body=Markup(message_body),
                message_type='comment',
                subtype_xmlid='mail.mt_comment'
            )
        return records

    @api.constrains('bio')
    def _check_bio_length(self):
        for record in self:
            if record.bio and len(record.bio) < 100:
                raise ValidationError(_("O'zingiz haqidagi ma'lumot kamida 100 ta harfdan iborat bo'lishi shart!"))

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.name} {record.last_name}"
            result.append((record.id, name))
        return result
