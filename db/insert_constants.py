from models import *

"""
example of data insertion in measurements:
INSERT INTO measurements(id, user_id, variable_id, value, time)
VALUES (4, 1, 0, 36.78, '2030-12-12 00:00:00');
"""

def insert_constants():
    """Insert constants into the database."""

    variables = {0: {'name': 'Ambient temperature', 'units': '°C',      'desc': 'Temperature in celsius degrees.'},
                 1: {'name': 'Ambient temperature', 'units': '°F',      'desc': 'Temperature in fahrenheit degrees.'},
                 2: {'name': 'Water temperature',   'units': '°C',      'desc': 'Temperature in celsius degrees.'},
                 3: {'name': 'Water temperature',   'units': '°F',      'desc': 'Temperature in fahrenheit degrees.'},
                 4: {'name': 'Relative humidity',   'units': '%',       'desc': 'Relative humidity in %.'},
                 5: {'name': 'Pressure',            'units': 'hPa',     'desc': 'Pressure in hectopascal.'},
                 6: {'name': 'Pressure',            'units': 'mmHg',    'desc': 'Pressure in millimeters of mercury.'},
                 7: {'name': 'Electroconductivity', 'units': 'mS/cm',   'desc': 'Quantity of dissolved nutrient in water.'},
                 8: {'name': 'Electroconductivity', 'units': 'ppm',     'desc': 'Quantity of dissolved nutrient in water.'},
                 9: {'name': 'pH',                  'units': 'numeric', 'desc': 'pH value of the water.'},
                 10: {'name': 'Light',              'units': 'lux',     'desc': 'Light intensity in lux.'},
                 11: {'name': 'Light',              'units': 'W/m²',    'desc': 'Photosynthetically active radiation (PAR) in W/m².'}}

    for key, value in variables.items():
        variable = Variable(id=int(key), name=value['name'], units=value['units'], desc=value['desc'])
        db_session.add(variable)

    db_session.commit()

if __name__ == '__main__':
    insert_constants()



