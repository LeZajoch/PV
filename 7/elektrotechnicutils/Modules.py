# Creation of module

def current_calculator(voltage, resistance):
    """
    Calculates the current given voltage and resistance.

    Args: 
    voltage (float): Voltage in volts
    resistance (float): Resistance in ohms

    Raises:
    ValueError: If the voltage or resistance is not a numeric value.

    """
    if not isinstance(voltage, (int, float)) or not isinstance(resistance, (int, float)):
        raise ValueError("Voltage and resistance must be numeric values.")
    calc = {'Current': voltage / resistance}
    return calc

def resistance_calculator(current, voltage):
    """
    Calculates the resistance given current and voltage.

    Args: 
    current (float): Current in amperes
    voltage (float): Resistance in ohms

    Raises:
    ValueError: If the current or voltage is not a numeric value.
    """
    if not isinstance(current, (int, float)) or not isinstance(voltage, (int, float)):
        raise ValueError("Current and voltage must be numeric values.")
    calc = {'Resistance': voltage / current}
    return calc

def voltage_calculator(resistance, current):
    """
    Calculates the voltage given resistance and current.

    Args: 
    resistance (float): Resistance in ohms
    current (float): Current in amperes

    Raises:
    ValueError: If the resistance or current is not a numeric value.
    """
    if not isinstance(resistance, (int, float)) or not isinstance(current, (int, float)):
        raise ValueError("Current and voltage must be numeric values.")
    calc = {'Voltage': resistance * current}
    return calc



def coulomb_force(Q1, Q2, r):

    # Coulomb's constant
    k = 8.99e9  # N m^2/C^2
    
    if not isinstance(Q1, (int, float)) or not isinstance(Q2, (int, float)) or not isinstance(r, (int, float)):
        raise ValueError("All values must be numeric values.")
    calc = k * abs(Q1 * Q2) / (r ** 2)
    return calc
