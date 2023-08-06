"""
Validation bounds

Defines a custom dictionary specifying each property of an ECG analysis
and their expected values in the way of bounds (minimum and maximum values),
they also include a reason of failure in case any validation fails.
"""

validation_bounds = {
    'sex': {
        'min': 0,
        'max': 1,
        'reason': 'sex should be an integer between 0 (M) and 1 (F)'
    },
    'age': {
        'min': 0,
        'max': 150,
        'reason': 'age not suitable for EGC analysis'
    },
    'height': {
        'min': 0,
        'max': 300,
        'reason': 'weight should be a semi-normal positive value in centimeters (cm)'
    },
    'weight': {
        'min': 0,
        'max': 500,
        'reason': 'weight should be a semi-normal positive value in kilograms (kg)'
    },
    'HR': {
        'min': 30,
        'max': 150,
        'reason': 'HR not suitable for EGC analysis'
    },
    'Pd': {
        'min': 40,
        'max': 270,
        'reason': 'Pd not suitable for EGC analysis'
    },
    'PQ': {
        'min': 50,
        'max': 350,
        'reason': 'PQ not suitable for EGC analysis'
    },
    'QRS': {
        'min': 20,
        'max': 190,
        'reason': 'QRS not suitable for EGC analysis'
    },
    'QT': {
        'min': 110,
        'max': 640,
        'reason': 'QT not suitable for EGC analysis'
    },
    'QTcFra': {
        'min': 150,
        'max': 650,
        'reason': 'QTcFra not suitable for EGC analysis'
    }
}
