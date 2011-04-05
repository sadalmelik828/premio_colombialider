'''
Created on 28/02/2011

@author: roque
'''
import os 
from django import forms
from django.utils.translation import gettext as _

class DocumentValidationError(forms.ValidationError):
    def __init__(self):
        super(DocumentValidationError, self).__init__(_(u'El tipo de documento no es valido. Solo se acepta: ') + ', '.join(DocumentField.valid_file_extensions))

class DocumentField(forms.FileField):
    """A validating document upload field"""
    valid_content_types = ('application/pdf')
    valid_file_extensions = ('pdf')

    def __init__(self, *args, **kwargs):
        super(DocumentField, self).__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        f = super(DocumentField, self).clean(data, initial)
        ext = os.path.splitext(data['name'])[1][1:].lower()
        if ext in DocumentField.valid_file_extensions and data['content-type'] in DocumentField.valid_content_types:
            return f
        raise DocumentValidationError()
