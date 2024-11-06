from odoo import models, fields, api
import requests
from odoo.exceptions import UserError

class SurveyTemplate(models.Model):
    _name = 'survey.template'
    _description = 'Survey Template'

    name = fields.Char(string="Template Title", required=True)
    description = fields.Text(string="Description")
    user_id = fields.Many2one('res.users', string="User")
    question_ids = fields.One2many('survey.question', 'template_id', string="Questions")

    def import_forms_from_api(self, api_token, user_id):
        headers = {'Authorization': f'Bearer {api_token}'}
        url = f'https://your-api-url/api/forms/{user_id}'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            self._process_imported_forms(data)
        else:
            raise UserError("Failed to import forms from the API.")

    def _process_imported_forms(self, data):
        for form in data:
            template = self.create({
                'name': form['title'],
                'description': form['description'],
                'user_id': form['user_id'],
            })

            for question in form['questions']:
                self.env['survey.question'].create({
                    'template_id': template.id,
                    'question_text': question['question'],
                    'question_type': question['type_question']['type_question'],
                })

