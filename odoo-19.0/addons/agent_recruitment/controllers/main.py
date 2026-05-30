from odoo import http
from odoo.http import request
import base64

class AgentRecruitmentController(http.Controller):

    @http.route(['/agent/apply'], type='http', auth="public", website=True)
    def agent_apply(self, **post):
        return request.render("agent_recruitment.agent_application_form_template", {})

    @http.route(['/agent/apply/submit'], type='http', auth="public", methods=['POST'], website=True, csrf=True)
    def agent_apply_submit(self, **post):
        # File handling
        resume = post.get('resume')
        resume_data = False
        resume_name = False
        if resume:
            resume_data = base64.b64encode(resume.read())
            resume_name = resume.filename

        # Create record
        vals = {
            'name': post.get('name'),
            'last_name': post.get('last_name'),
            'phone': post.get('phone'),
            'email': post.get('email'),
            'age': int(post.get('age')) if post.get('age') else 0,
            'gender': post.get('gender'),
            'has_experience': post.get('has_experience'),
            'experience_details': post.get('experience_details'),
            'resume': resume_data,
            'resume_name': resume_name,
            'bio': post.get('bio'),
            'location': post.get('location'),
            'working_time': post.get('working_time'),
        }
        
        application = request.env['agent.application'].sudo().create(vals)
        
        return request.render("agent_recruitment.agent_application_thanks_template", {
            'application': application
        })
