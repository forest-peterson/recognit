import logging
logging.basicConfig(
    filename='./local_temp/debug.log', 
    level=logging.DEBUG, 
    format='%(asctime)s - %(message)s')

def recognit(value, header, context=None):

    if header is None:
        return False

    if context is None:
        context = {}

    PASS_THRESHOLD = 0.66

    test1 = recognit_x_column(value, header)
    test2 = recognit_max_value(value, header)
    test3 = recognit_min_value(value, header)

    #test4 = recognit_validator(value, header, context=context)

    #return ((test1 + test2 + test3 + test4) / 4) >= PASS_THRESHOLD
    logging.info(f"test1: {test1}, test2: {test2}, test3: {test3}")
    logging.info(f"PASS_THRESHOLD: {PASS_THRESHOLD}")
    logging.info(f"value.text: {value.text if hasattr(value, 'text') else value}")
    logging.info(f"header keys: {list(header.keys()) if isinstance(header, dict) else header}")
    logging.info(f"context keys: {list(context.keys()) if isinstance(context, dict) else context}")
    return ((test1 + test2 + test3) / 3) >= PASS_THRESHOLD
    

#helper

def _get_float_val(value):
    try:
        # Clean common currency/formatting chars
        text = value.text.replace('$', '').replace(',', '').strip()
        return float(text)
    except (ValueError, AttributeError):
        return None

#speific tests

def recognit_x_column(value, header):
    x_tolerance = 12.0
    if header['x_center'] is None:
        return True

    if header['x_center'] == 0: 
        return True # Skip check if not configured
            
    if (
        (value.x < (header['x_center'] + x_tolerance))
        and 
        (value.x > (header['x_center'] - x_tolerance))
        ):
        return True
    else:
        return False



def recognit_max_value(value, header):
    val_float = _get_float_val(value)
    if val_float is None:
        return False

    if header['max_value'] is None:
        return True

    if val_float > header['max_value']:
        return False

    return True


def recognit_min_value(value, header):
    val_float = _get_float_val(value)
    if val_float is None:
        return False

    if header['min_value'] is None:
        return True

    if val_float < header['min_value']:
        return False
    
    return True


def recognit_validator(value, header, context):
    val_float = _get_float_val(value)

    if val_float is None:
        return False

    if header['validator'] is None:
        return True


    if header['validator'](val_float, **context):
        return True

    return False

