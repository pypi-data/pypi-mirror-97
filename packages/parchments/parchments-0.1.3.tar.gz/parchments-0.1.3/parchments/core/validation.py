from datetime import date, datetime


def is_valid_date_or_datetime(date):
    if type(date) is date or type(date) is datetime:
        return True
    else:
        raise ValueError('Invalid. Must be a date or datetime')


def is_valid_list_choice(variable, choice_list):
    if variable in choice_list:
        return True
    else:
        raise SyntaxError('Invalid option. Choices are %s' % choice_list)