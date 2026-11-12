# Uso de IA

## IA dentro del pipeline

| | |
| --- | --- |
| **Proveedor** | Microsoft Foundry |
| **Modelo** | GPT-4o, desplegado como agente |
| **Tarea** | Generación de texto (chat) para extraer datos estructurados |
| **Para qué** | Convierte una descripción del tiempo en lenguaje natural en el JSON con las siete variables meteorológicas que recibe el modelo de regresión |

Con el modo `mock` el pipeline no consulta a ninguna IA.

## IA durante el desarrollo

Asistente utilizado: Claude (Anthropic), en formato de chat.

- **Generado con IA:** la documentación del proyecto (`README.md` y este fichero), posteriormente revisada y corregida.
- **Consulta a la IA:** Base del archivo de configuración `logging.conf`, el cual ha sido posteriormente modificado para adaptarse a las necesidades del proyecto.
- La IA **no** ha sido utilizada para generar ningún fragmento del código.