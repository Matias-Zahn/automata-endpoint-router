# DFA REST Router

Este proyecto es un enrutador de endpoints para una API REST de backend, diseñado y modelado mediante un Autómata Finito Determinista (AFD). La implementación está realizada en Python y busca proporcionar una validación de rutas técnica, estricta y eficiente.

## Arquitectura del Proyecto

El sistema se divide en dos componentes fundamentales que transforman una cadena de texto (URI) en un estado de aceptación o rechazo dentro de la lógica del servidor.

### Lexer (Preprocesamiento léxico)
El Lexer actúa como la primera capa de procesamiento. Se encarga de limpiar la URI de entrada, eliminando caracteres innecesarios y dividiéndola en segmentos individuales. Su función principal es la abstracción de parámetros:
- Utiliza expresiones regulares (como `^[0-9]+$`) para identificar si un segmento corresponde a un valor dinámico.
- Convierte estos valores en tokens genéricos que el autómata puede entender (por ejemplo, transforma el número `123` en el token `ID_VALIDO`).

### Autómata Finito Determinista (AFD)
Una vez que el Lexer ha generado la secuencia de tokens, el AFD los utiliza como su alfabeto de entrada. El autómata transita entre estados siguiendo reglas estrictas de definición de rutas.
- Si la secuencia de tokens no coincide con ninguna ruta válida, el autómata transita hacia un **estado de pozo** (`qpozo`).
- El estado de pozo se utiliza para simular y disparar errores **HTTP 404 Not Found**, garantizando que solo las rutas definidas lleguen a la lógica de negocio.

## Modelo Matemático (Quíntupla)

El comportamiento del enrutador se define formalmente mediante la siguiente quíntupla simplificada:
- **Estados (Q):** `{q0, q1, q2, q3, q4, q5, q6, qpozo}`
- **Alfabeto (Σ):** `{health, api, users, ID_VALIDO, auth, login}`
- **Estado Inicial (q0):** `q0`
- **Estados de Aceptación (F):** `{q2, q3, q4, q6}`

## Requisitos

Para ejecutar este proyecto, asegúrese de contar con los siguientes elementos instalados en su sistema:
- Python 3.x
- Librería `automata-lib`

## Instalación y Uso

Siga estos pasos para configurar el entorno de ejecución y probar el enrutador:

1. **Crear un entorno virtual:**
```bash
python3 -m venv env
source env/bin/activate
pip install automata-lib
python enrutador.py
```

## Ejemplos de Rutas Soportadas

El autómata está configurado para reconocer y validar con éxito las siguientes estructuras de endpoints:

- `/health` (Estado de salud del sistema)
- `/api/users` (Listado de usuarios)
- `/api/users/{id}` (Detalle de un usuario específico, donde `{id}` debe cumplir el patrón numérico)
- `/api/auth/login` (Autenticación de usuarios)