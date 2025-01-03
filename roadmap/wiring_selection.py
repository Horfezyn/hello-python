import math

def seleccionar_calibre(): #Aqui realizaremos todos los calculos necesarios para calcular el calibre, solo para 120V.
    """
    Programa para la selección de cableado eléctrico conforme a la NOM-001-SEDE-2022
    para circuitos monofásicos de 120V.
    """
    # Datos de entrada que necesitamos ingresar para hacer el calculo correcto.
    print("\n=== Selección de Cableado ===")
    potencia = float(input("Ingrese la potencia de la carga (W): "))
    factor_potencia = float(input("Ingrese el factor de potencia (0-1): "))
    longitud = float(input("Ingrese la longitud del circuito (m): "))
    temperatura = float(input("Ingrese la temperatura ambiente (°C): "))
    num_conductores = int(input("Ingrese el número de conductores en el ducto: "))

    # Paso 1: Cálculo de la corriente nominal
    voltaje = 120  # Voltaje fijo para circuito monofásico
    corriente = potencia / (voltaje * factor_potencia)
    print(f"\nCorriente nominal calculada: {corriente:.2f} A")

    # Paso 2: Selección inicial del calibre
    tabla_capacidad_corriente = { # Creamos un diccionario que contiene la ampacidad para 30grados 
        "14": 15,
        "12": 20,
        "10": 30,
        "8": 40,
        "6": 55,
        "4": 70,
        "2": 95
    }  # Tabla simplificada (en amperios)

    calibre_inicial = None
    for calibre, capacidad in tabla_capacidad_corriente.items(): #calibre toma cada valor del diccionario y capacidad el valor a la clave
        if corriente <= capacidad:
            calibre_inicial = calibre
            break

    if not calibre_inicial:
        print("No se encontró un calibre adecuado para la corriente calculada.")
        return

    print(f"Calibre inicial seleccionado: {calibre_inicial} AWG")

    # Paso 3: Factores de corrección
    # Corrección por temperatura
    if temperatura > 30:
        if 31 <= temperatura <= 40:
            factor_temp = 0.91
        elif 41 <= temperatura <= 50:
            factor_temp = 0.82
        elif 51 <= temperatura <= 60:
            factor_temp = 0.71
        else:
            print("Temperatura fuera del rango soportado.")
            return
    else:
        factor_temp = 1.0

    # Corrección por número de conductores
    if num_conductores > 3:
        if 4 <= num_conductores <= 6:
            factor_agrupamiento = 0.8
        elif 7 <= num_conductores <= 9:
            factor_agrupamiento = 0.7
        else:
            factor_agrupamiento = 0.5
    else:
        factor_agrupamiento = 1.0

    factor_total = factor_temp * factor_agrupamiento
    capacidad_corregida = tabla_capacidad_corriente[calibre_inicial] * factor_total

    print(f"\nFactor de corrección por temperatura: {factor_temp}")
    print(f"Factor de corrección por agrupamiento: {factor_agrupamiento}")
    print(f"Capacidad corregida del calibre inicial: {capacidad_corregida:.2f} A")

    # Verificar si el calibre inicial sigue siendo adecuado
    if corriente > capacidad_corregida:
        print("El calibre inicial no es suficiente después de aplicar los factores de corrección.")
        return

    # Paso 4: Verificar caída de tensión
    resistencia_por_km = {
        "14": 8.286,
        "12": 5.211,
        "10": 3.277,
        "8": 2.061,
        "6": 1.296,
        "4": 0.815,
        "2": 0.512
    }  # En ohm/km

    resistencia_calibre = resistencia_por_km[calibre_inicial] / 1000  # Convertir a ohm/m
    caida_tension = 2 * longitud * corriente * resistencia_calibre

    print(f"\nCaída de tensión calculada: {caida_tension:.2f} V")
    if caida_tension > (voltaje * 0.03):  # 3% de caída de tensión
        print("La caída de tensión excede el 3%. Considera un calibre mayor.")
        return

    print("\n=== Resultado Final ===")
    print(f"Calibre recomendado: {calibre_inicial} AWG")
    print(f"Caída de tensión: {caida_tension:.2f} V (cumple con el 3% máximo permitido)")

# Ejecutar el programa
if __name__ == "__main__":
    seleccionar_calibre()