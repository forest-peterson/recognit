import logging

recog_log = logging.getLogger('recognit')
recog_log.setLevel(logging.INFO)  

# Add handler if one doesn't exist
if not recog_log.handlers:
    handler = logging.FileHandler('./local_temp/debug.log')
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    recog_log.addHandler(handler)
    recog_log.propagate = False

def recognit(value, header, context=None):
    recog_log.debug(" **recognit()")

    if header is None or header == {}:
        recog_log.info(" **recognit() value={value.text} for header = None")
        return False
        
    recog_log.debug(f" **recognit() value={value.text} for header type={type(header)}")

    if context is None:
        recog_log.info(" **recognit() context = {}")
        context = {}

    PASS_THRESHOLD = 0.66

    test1 = recognit_x_column(value, header)
    recog_log.debug(" **recognit() test1={test1}")
    test2 = recognit_max_value(value, header)
    recog_log.debug(" **recognit() test2={test2}")
    test3 = recognit_min_value(value, header)
    recog_log.debug(" **recognit() test3={test3}")

    #test4 = recognit_validator(value, header, context=context)

    #return ((test1 + test2 + test3 + test4) / 4) >= PASS_THRESHOLD
    test_sum = sum([test1, test2, test3])
    recog_log.critical(f" **recognit(): value.text: {value.text if hasattr(value, 'text') else value}")
    recog_log.critical(f" -- **recognit(): test1: {test1}, test2: {test2}, test3: {test3} for sum = {test_sum} of THRESHOLD {PASS_THRESHOLD}")
    recog_log.critical(f" -- **recognit(): header keys: {list(header.keys()) if isinstance(header, dict) else header}")
    recog_log.critical(f" -- **recognit(): context keys: {list(context.keys()) if isinstance(context, dict) else context}")
    
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
    if header['center_x'] is None:
        recog_log.info(" ** value = {value.text} for header['center_x'] is None")
        return True

    if header['center_x'] == 0: 
        recog_log.info(" ** value = {value.text} for header['center_x'] is 0")
        return True # Skip check if not configured
            
    if (
        (value.x < (header['center_x'] + x_tolerance))
        and 
        (value.x > (header['center_x'] - x_tolerance))
        ):
        recog_log.info(f" ** value = {value.text} x={value.x} for header x={header['center_x']} is within tolerance {x_tolerance}")
        return True
    else:
        recog_log.info(f" ** value = {value.text} x={value.x} for header x={header['center_x']} is not within tolerance {x_tolerance}")
        return False



def recognit_max_value(value, header):
    val_float = _get_float_val(value)
    
    if val_float is None:
        recog_log.info(f" ** value = {value.text} is None for max_value")
        return False

    if header['max_value'] is None:
        recog_log.info(f" ** value = {value.text} for max_value is None")
        return True

    if val_float > header['max_value']:
        recog_log.info(f" ** value = {value.text} is greater than max_value {header['max_value']}")
        return False

    return True


def recognit_min_value(value, header):
    val_float = _get_float_val(value)
    if val_float is None:
        recog_log.info(f" ** value = {value.text} is None for min_value")
        return False

    if header['min_value'] is None:
        recog_log.info(f" ** value = {value.text} for min_value is None")
        return True

    if val_float < header['min_value']:
        recog_log.info(f" ** value = {value.text} is less than min_value {header['min_value']}")
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

