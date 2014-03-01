from account.forms import LoginUsernameForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import FieldWithButtons


class LoginForm(LoginUsernameForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            'username',
            'password',
            'remember',
            Submit('signin', 'Sign in', css_class='col-lg-offset-3'),
        )
