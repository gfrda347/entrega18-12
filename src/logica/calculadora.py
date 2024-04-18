from datetime import datetime

class CalculadoraLiquidacion:
    def __init__(self, valor_uvt=39205):
        self.valor_uvt = valor_uvt

    def calcular_resultados_prueba(self, salario_basico, fecha_inicio_labores, fecha_ultimas_vacaciones, dias_acumulados_vacaciones):
        indemnizacion = self.calcular_liquidacion(salario_basico, fecha_inicio_labores, fecha_ultimas_vacaciones)
        vacaciones = self.calcular_vacaciones(salario_basico)
        cesantias = self.calcular_cesantias(salario_basico, dias_acumulados_vacaciones)
        intereses_cesantias = self.calcular_intereses_cesantias(cesantias, dias_acumulados_vacaciones)
        primas = self.calcular_prima(salario_basico)
        retencion_fuente = self.calcular_retencion(indemnizacion + vacaciones + cesantias + intereses_cesantias + primas)
        total_pagar = indemnizacion + vacaciones + cesantias + intereses_cesantias + primas - retencion_fuente
        return indemnizacion, vacaciones, cesantias, intereses_cesantias, primas, retencion_fuente, total_pagar

    def calcular_liquidacion(self, salario, fecha_inicio, fecha_fin):
        if salario < 0:
            raise ValueError("El salario básico no puede ser negativo")
    
        fecha_inicio = datetime.strptime(fecha_inicio, "%d/%m/%Y")
        fecha_fin = datetime.strptime(fecha_fin, "%d/%m/%Y")
        dias_trabajados = (fecha_fin - fecha_inicio).days + 1
        valor_diario = salario / 30
        liquidacion = valor_diario * dias_trabajados
        return round(liquidacion, 2)

    def calcular_vacaciones(self, salario_mensual):
        valor_vacaciones = salario_mensual * (1/24)  # 1/24
        return round(valor_vacaciones, 2)

    def calcular_cesantias(self, salario_mensual, dias_trabajados):
        if dias_trabajados < 0:
            raise ValueError("Los días trabajados no pueden ser negativos")
        cesantias = (salario_mensual * dias_trabajados) / 360
        return round(cesantias, 2)

    def calcular_intereses_cesantias(self, cesantias, dias_trabajados):
        if cesantias < 0:
            raise ValueError("El valor de las cesantías no puede ser negativo")
        if dias_trabajados < 0:
            raise ValueError("Los días trabajados no pueden ser negativos")
        intereses_cesantias = (cesantias * dias_trabajados * 0.12) / 360
        return round(intereses_cesantias, 2)

    def calcular_prima(self, salario_mensual):
        prima = salario_mensual * (1/12)  
        return round(prima, 2)

    def calcular_retencion(self, salario_basico):
        if not isinstance(salario_basico, (int, float)):
            raise ValueError("El salario básico debe ser un número")
        retencion = 0
        salario_basico = float(salario_basico)
        if salario_basico <= 42412:
            pass
        elif salario_basico <= 636132:
            ingreso_uvt = salario_basico / self.valor_uvt
            base_uvt = ingreso_uvt - 95
            base_pesos = base_uvt * self.valor_uvt
            retencion = (base_pesos * 0.19) + (10 * self.valor_uvt)
        return round(retencion, 2)

# Crear una instancia de la calculadora
calculadora = CalculadoraLiquidacion()

# Solicitar datos al usuario
salario_basico = float(input("Ingrese el salario básico en pesos colombianos: "))
fecha_inicio_labores = input("Ingrese la fecha de inicio de labores (dd/mm/yyyy): ")
fecha_ultimas_vacaciones = input("Ingrese la fecha de las últimas vacaciones (dd/mm/yyyy): ")
dias_acumulados_vacaciones = int(input("Ingrese los días acumulados de vacaciones: "))

try:
    indemnizacion, vacaciones, cesantias, intereses_cesantias, primas, retencion_fuente, total_pagar = calculadora.calcular_resultados_prueba(
        salario_basico=salario_basico,
        fecha_inicio_labores=fecha_inicio_labores,
        fecha_ultimas_vacaciones=fecha_ultimas_vacaciones,
        dias_acumulados_vacaciones=dias_acumulados_vacaciones
    )

    print(f"Indemnización: COP {indemnizacion:,.2f}")
    print(f"Vacaciones: COP {vacaciones:,.2f}")
    print(f"Cesantías: COP {cesantias:,.2f}")
    print(f"Intereses sobre cesantías: COP {intereses_cesantias:,.2f}")
    print(f"Prima de servicios: COP {primas:,.2f}")
    print(f"Retención en la fuente: COP {retencion_fuente:,.2f}")
    print(f"Total a pagar: COP {total_pagar:,.2f}")

except ValueError as e:
    print("Error:", e)
