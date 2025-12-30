def recognit(value, validator, context=None):

    if context is None:
        context = {}

    PASS_THRESHOLD = 0.75

    test1 = recognit_x_column(value, validator)
    test2 = recognit_max_value(value, validator)
    test3 = recognit_min_value(value, validator)
    test4 = recognit_validator(value, validator, context=context)

    return ((test1 + test2 + test3 + test4) / 4) >= PASS_THRESHOLD
    

#helper

def _get_float_val(value):
    try:
        # Clean common currency/formatting chars
        text = value.text.replace('$', '').replace(',', '').strip()
        return float(text)
    except (ValueError, AttributeError):
        return None

#speific tests

def recognit_x_column(value, validator):
    x_tolerance = 12.0
    if validator['x_center'] is None:
        return True

    if validator['x_center'] == 0: 
        return True # Skip check if not configured
            
    if (
        (value.x < (validator['x_center'] + x_tolerance))
        and 
        (value.x > (validator['x_center'] - x_tolerance))
        ):
        return True
    else:
        return False



def recognit_max_value(value, validator):
    val_float = _get_float_val(value)
    if val_float is None:
        return False

    if validator['max_value'] is None:
        return True

    if val_float > validator['max_value']:
        return False

    return True


def recognit_min_value(value, validator):
    val_float = _get_float_val(value)
    if val_float is None:
        return False

    if validator['min_value'] is None:
        return True

    if val_float < validator['min_value']:
        return False
    
    return True


def recognit_validator(value, validator, context):
    val_float = _get_float_val(value)

    if val_float is None:
        return False

    if validator['validator'] is None:
        return True


    if validator['validator'](val_float, **context):
        return True

    return False

#unified test with score
