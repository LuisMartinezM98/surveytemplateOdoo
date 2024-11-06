class SurveyQuestion(models.Model):
    _name = 'survey.question'
    _description = 'Survey Question'

    template_id = fields.Many2one('survey.template', string="Template")
    question_text = fields.Char(string="Question Text", required=True)
    question_type = fields.Char(string="Question Type", required=True)
