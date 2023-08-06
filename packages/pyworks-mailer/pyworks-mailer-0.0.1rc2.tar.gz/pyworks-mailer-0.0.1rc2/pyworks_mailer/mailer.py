import os
import codecs
import io
import yagmail
import htmlmin
from jinja2 import Template, Environment, FileSystemLoader

from pyworks_mailer.config import config
from pyworks_mailer import minifier


class Mailer:

    PREFIX='[Pyworks Mailer]'
    TEMPLATES_ROOT_DIR = config.MAIL_TEMPLATES_ROOT
    TEMPLATE_USER_REGISTERED = 'user_registered.minify.html'
    TEMPLATE_ORDER_CREATED = 'order_created.minify.html'
    TEMPLATE_NEWSLETTER = 'newsletter.minify.html'
    TEMPLATE_FORGOT_PASSWORD = 'forgot_password.minify.html'

    def __init__(self, provider):
        self._set_provider(provider)

    def send(self, subject, body, attachments: list = [], has_prefix: bool = False):
        if has_prefix:
            subject = self._get_subject(subject)

        if attachments and len(attachments):
            pass

        try:
            yag = yagmail.SMTP(config.MAIL_USERNAME, config.MAIL_PASSWORD)
            yag.send(
                to=config.MAIL_RECEIVERS,
                subject=subject,
                contents=body, 
            )
            return True
        except Exception as e:
            # raise e
            return False

    def _set_provider(self, provider):
        if provider in config.MAIL_PROVIDER_SUPPORTED:
            self.provider = provider
        else:
            raise Exception(f"Only support these mail providers: {''.join(config.MAIL_PROVIDER_SUPPORTED)}")

    # def send_user_registered(self, data):
    #     try:
    #         subject = self._get_subject('Thank you for register awesome website')
    #         body=self.render_body(data, self.TEMPLATE_USER_REGISTERED)
    #         self.send(subject=subject, body=body)
    #     except Exception as e:
    #         raise e

    # def send_newsletter(self, data):
    #     try:
    #         subject = self._get_subject('New Content Publishing API, PyWorks Community Blog, and more')
    #         self.send(subject=subject, body=self.render_body(data, self.TEMPLATE_NEWSLETTER))
    #     except Exception as e:
    #         raise e

    # def send_order_created(self, data):
    #     try:
    #         subject = self._get_subject('Order Successfully')
    #         self.send(subject=subject, body=self.render_body(data, self.TEMPLATE_ORDER_CREATED))
    #     except Exception as e:
    #         raise e

    def _get_subject(self, subject):
        return '{prefix} {subject}'.format(prefix=self.PREFIX, subject=subject)

    def render_body(self, data, template):                    
        return self.render_from_template(data, template_file=template)

    def render_from_template(self, data, template_name, overwrite_minify:bool = False):
        # Minify template file 
        template_file = f'{self.TEMPLATES_ROOT_DIR}/{template_name}.html'
        template_file_minified = f'{self.TEMPLATES_ROOT_DIR}/{template_name}.min.html'

        if not os.path.isfile(template_file_minified) or overwrite_minify:
            minifier.minify(input_file=template_file, output_file=template_file_minified)

        # Parse template data from minified template
        file_loader = FileSystemLoader(self.TEMPLATES_ROOT_DIR)
        env = Environment(loader=file_loader)
        template_min = f'{template_name}.min.html'
        template = env.get_template(template_min)
        output = template.render(data)
        return output

        # t = Template(template_file_minified)
        # return t.render(data)

if __name__ == '__main__':
    mail = Mailer(provider='gmail')
    
    subject = "Reset your password"
    data = {
        "user": {
            "fullname": "Brian Lee"
        }
    }
    body = mail.render_from_template(data=data, template_name='forgot_password')
    # print(body)
    mail.send(subject=subject, body=body)
    