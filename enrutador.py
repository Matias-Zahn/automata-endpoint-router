import re
from automata.fa.dfa import DFA
from automata.base.exceptions import RejectionException

# 1. Definición del alfabeto y estados base según el documento
alfabeto = {'health', 'api', 'users', 'ID_VALIDO', 'auth', 'login'}
estados = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'qpozo'}

# 2. Construcción de la tabla de transiciones estricta
# Se define qpozo como un sumidero para capturar errores de sintaxis o rutas inexistentes
transiciones = {
    'q0': {'health': 'q2', 'api': 'q1'},
    'q1': {'users': 'q3', 'auth': 'q5'},
    'q2': {}, 
    'q3': {'ID_VALIDO': 'q4'},
    'q4': {},
    'q5': {'login': 'q6'},
    'q6': {},
    'qpozo': {simbolo: 'qpozo' for simbolo in alfabeto}
}

# Completar las transiciones faltantes hacia el estado pozo para garantizar el determinismo
for estado in estados:
    if estado != 'qpozo':
        for simbolo in alfabeto:
            if simbolo not in transiciones[estado]:
                transiciones[estado][simbolo] = 'qpozo'

# 3. Instanciación del AFD
enrutador_dfa = DFA(
    states=estados,
    input_symbols=alfabeto,
    transitions=transiciones,
    initial_state='q0',
    final_states={'q2', 'q3', 'q4', 'q6'}
)

# 4. Lexer y procesamiento de la URI
def procesar_ruta(uri):
    """
    Toma la URI cruda, la fragmenta y la evalúa en el AFD.
    """
    # Saneamiento: Eliminar barras iniciales/finales y fragmentar
    uri_limpia = uri.strip('/')
    if not uri_limpia:
        return "404 Not Found (Ruta raíz vacía)"
        
    segmentos = uri_limpia.split('/')
    
    tokens = []
    # Validación léxica restringida a formato exclusivamente numérico
    regex_id = re.compile(r'^[0-9]+$')
    
    for segmento in segmentos:
        if regex_id.match(segmento):
            tokens.append('ID_VALIDO')
        else:
            # Se respeta la sensibilidad de caracteres (Case-Sensitive)
            tokens.append(segmento)
            
    # 5. Evaluación en el autómata
    try:
        # Intenta consumir la secuencia de tokens
        estado_final = enrutador_dfa.read_input(tokens)
        return f"200 OK - Enrutado con éxito (Estado: {estado_final})"
    except RejectionException:
        # Se rechaza si el token no pertenece al alfabeto o el camino termina en qpozo
        return "404 Not Found - Ruta rechazada"

# ==========================================
# Pruebas de Integración (Para el Anexo)
# ==========================================
if __name__ == '__main__':
    rutas_prueba = [
        # Rutas válidas
        "/health",                 # Debe llegar a q2
        "/api/users",              # Debe llegar a q3
        "/api/users/123",          # Debe llegar a q4 (ID validado)
        "/api/auth/login",         # Debe llegar a q6
        
        # Rutas inválidas (Errores controlados)
        "/api/users/abc",          # Falla Regex, cadena alfanumérica
        "/API/users",              # Falla Case-Sensitive
        "/api/inventado/login",    # Token no perteneciente al alfabeto
        "/api/users/123/extra"     # Segmentos excedentes
    ]

    print("--- Resultados del Enrutador REST ---")
    for ruta in rutas_prueba:
        resultado = procesar_ruta(ruta)
        print(f"Ruta: {ruta:<25} | {resultado}")