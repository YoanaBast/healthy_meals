class ErrorMessagesMixin:
    default_error_messages = {
        'name': {
            'required': 'Please enter a name.',
            'unique': 'This name already exists.',
            'max_length': 'Name is too long — maximum 100 characters.',  # ← this was missing
        },
        'quantity': {
            'required': 'Please enter a quantity.',
            'invalid': 'Enter a valid number.',
        },
        'unit': {
            'required': 'Please select a unit.',
        },
    }

    def apply_error_messages(self, fields=None):
        fields = fields or self.default_error_messages.keys()
        for field_name in fields:
            if field_name in self.fields and field_name in self.default_error_messages:
                self.fields[field_name].error_messages.update(
                    self.default_error_messages[field_name]
                )