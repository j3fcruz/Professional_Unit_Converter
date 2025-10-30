#core/unit_conversion.py

class UnitConverterCore:
    """Core unit conversion logic"""
    
    def __init__(self):
        self.unit_mappings = {
            "Distance": {
                "units": ["mm", "cm", "m", "km", "miles", "yards", "feet", "inch"],
                "to_base": {
                    "mm": 0.001, "cm": 0.01, "m": 1, "km": 1000,
                    "miles": 1609.344, "yards": 0.9144, "feet": 0.3048, "inch": 0.0254
                }
            },
            "Time": {
                "units": ["seconds", "minutes", "hours", "days", "years", "decades", "centuries"],
                "to_base": {
                    "seconds": 1, "minutes": 60, "hours": 3600,
                    "days": 86400, "years": 31536000,
                    "decades": 315360000, "centuries": 3153600000
                }
            },
            "Temperature": {
                "units": ["Celsius", "Fahrenheit", "Kelvin"],
                "to_base": {}  # Special handling
            },
            "Mass": {
                "units": ["grams", "kilograms", "milligrams", "pounds", "ounces", "ton"],
                "to_base": {
                    "grams": 1, "kilograms": 1000, "milligrams": 0.001,
                    "pounds": 453.592, "ounces": 28.3495, "ton": 1_000_000
                }
            },
            "Volume": {
                "units": ["milliliters", "centiliters", "deciliters", "liters", "gallons", "cups", "quarts", "pints"],
                "to_base": {
                    "milliliters": 1, "centiliters": 10, "deciliters": 100,
                    "liters": 1000, "gallons": 3785.41, "cups": 236.588,
                    "quarts": 946.353, "pints": 473.176
                }
            },
            "Computer Storage": {
                "units": ["bytes", "kilobytes", "megabytes", "gigabytes", "terabytes"],
                "to_base": {
                    "bytes": 1, "kilobytes": 1024, "megabytes": 1024**2,
                    "gigabytes": 1024**3, "terabytes": 1024**4
                }
            },
            "Power": {
                "units": ["watts", "kilowatts", "horsepower", "megawatts"],
                "to_base": {
                    "watts": 1, "kilowatts": 1000, "horsepower": 745.7, "megawatts": 1_000_000
                }
            },
            "Pressure": {
                "units": ["pascals", "bar", "atm", "psi", "torr"],
                "to_base": {
                    "pascals": 1, "bar": 100000, "atm": 101325,
                    "psi": 6894.76, "torr": 133.322
                }
            },
            "Energy": {
                "units": ["joules", "kilojoules", "calories", "kilocalories", "watt-hours", "kilowatt-hours"],
                "to_base": {
                    "joules": 1, "kilojoules": 1000, "calories": 4.184,
                    "kilocalories": 4184, "watt-hours": 3600, "kilowatt-hours": 3.6e6
                }
            }
        }

    def convert_temperature(self, value, from_unit, to_unit):
        """Special temperature conversion handling"""
        if from_unit == to_unit:
            return value
        
        if from_unit == "Celsius":
            if to_unit == "Fahrenheit":
                return (value * 9/5) + 32
            elif to_unit == "Kelvin":
                return value + 273.15
        elif from_unit == "Fahrenheit":
            if to_unit == "Celsius":
                return (value - 32) * 5/9
            elif to_unit == "Kelvin":
                return ((value - 32) * 5/9) + 273.15
        elif from_unit == "Kelvin":
            if to_unit == "Celsius":
                return value - 273.15
            elif to_unit == "Fahrenheit":
                return ((value - 273.15) * 9/5) + 32
        
        return value

    def convert_units(self, value, from_unit, to_unit, conversion_type):
        """Convert units based on the conversion type"""
        try:
            value = float(value)
        except (ValueError, TypeError):
            return {"error": "Invalid input value"}

        if conversion_type not in self.unit_mappings:
            return {"error": "Unsupported conversion type"}

        # Special handling for temperature
        if conversion_type == "Temperature":
            result = self.convert_temperature(value, from_unit, to_unit)
            return {
                "result": result,
                "formatted": f"{value} {from_unit} = {result:.4f} {to_unit}"
            }

        # Standard conversion using base units
        unit_data = self.unit_mappings[conversion_type]
        
        if from_unit not in unit_data["to_base"] or to_unit not in unit_data["to_base"]:
            return {"error": "Invalid units for conversion"}

        # Convert to base unit, then to target unit
        base_value = value * unit_data["to_base"][from_unit]
        result = base_value / unit_data["to_base"][to_unit]

        return {
            "result": result,
            "formatted": f"{value} {from_unit} = {result:,.4f} {to_unit}"
        }

    #New
    def convert_units_bug(self, value, from_unit, to_unit, conversion_type):
        """General unit conversion method"""
        try:
            # Convert input to float
            value = float(value)

            # Define conversion factors
            if conversion_type == "Distance":
                factor = {"m":1, "km":1000, "mile":1609.34}
            elif conversion_type == "Weight":
                factor = {"g":1, "kg":1000, "lb":453.592}
            else:
                return {"error": "unknown type", "result": 0, "formatted": "0"}

            if from_unit not in factor or to_unit not in factor:
                return {"error": "unknown unit", "result": 0, "formatted": "0"}

            # Perform conversion
            result_value = value * factor[from_unit] / factor[to_unit]
            formatted = f"{result_value:,.4f} {to_unit}"

            return {"result": result_value, "formatted": formatted}

        except Exception as e:
            # Handle any errors gracefully
            return {"error": str(e), "result": 0, "formatted": "0"}

    def get_units_for_type(self, conversion_type):
        """Get available units for a conversion type"""
        if conversion_type in self.unit_mappings:
            return self.unit_mappings[conversion_type]["units"]
        return []
