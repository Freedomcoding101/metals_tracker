from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label="Name")
    email = forms.EmailField(required=True, label="Email")
    subject = forms.CharField(max_length=200, required=True, label="Subject")
    message = forms.CharField(widget=forms.Textarea, required=True, label="Message")

    def __init__(self,*args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})