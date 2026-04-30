# Botardito

Botardito es un bot de Discord pensado para acompañar la cursada de **Pensamiento Computacional del CBC**.

El objetivo del bot es ayudar a los estudiantes a organizarse, consultar información importante de la materia y practicar con preguntas tipo parcial.

## Funciones principales

Botardito incluye comandos para:

- Consultar fechas importantes de la cursada;
- Ver el temario semanal;
- Saber qué conviene repasar según el cronograma;
- Acceder a recursos y preguntas frecuentes;
- Practicar con preguntas rápidas;
- Simular parciales de práctica;
- Hacer consultas al bot sobre temas de la materia.

## Comandos disponibles

| Comando | Descripción |
|---|---|
| `/ayuda` | Muestra todos los comandos disponibles. |
| `/fechas` | Muestra fechas importantes del curso. |
| `/calendario` | Muestra el cronograma semanal de la cursada. |
| `/repasar` | Recomienda qué estudiar según la semana actual. |
| `/recursos` | Muestra recursos útiles de la materia. |
| `/faq` | Muestra preguntas frecuentes. |
| `/quiz` | Envía una pregunta rápida de práctica. |
| `/parcial` | Inicia un parcial de práctica con preguntas aleatorias. |
| `/preguntarle` | Permite hacerle una consulta al bot. |

## Parciales de práctica

El comando `/parcial` permite elegir entre:

- **Primer parcial**
  - Unidad 1
  - Unidad 2
  - Unidad 3
  - Unidad 4: rangos, cadenas, tuplas y listas

- **Segundo parcial**
  - Unidad 4: diccionarios
  - Unidad 5
  - Unidad 6

Cada parcial toma preguntas aleatorias desde el archivo:

```text
data/preguntas_parciales.json
```

Al finalizar, el bot muestra:

- cantidad de respuestas correctas;
- nota estimada;
- detalle de respuestas;
- temas a repasar;
- explicación de los errores.

## Estructura del proyecto

```text
botardito/
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
│
├── cogs/
│   ├── academico.py
│   ├── botardito.py
│   ├── parcial.py
│   ├── preguntas.py
│   └── quiz.py
│
└── data/
    ├── calendario.py
    ├── preguntas.json
    └── preguntas_parciales.json
```

## Requisitos

Para usar el bot necesitás tener instalado:

- Python 3.10 o superior;
- una aplicación creada en Discord Developer Portal;
- el token del bot;
- el bot invitado a tu servidor con permisos para usar comandos slash.
- y una API key para interactuar con el comando /preguntarle

## Estado del proyecto

Este bot está pensado como herramienta de apoyo para estudiantes de Pensamiento Computacional.

No reemplaza a los docentes ni a los materiales oficiales de la materia, pero ayuda a practicar, organizarse y resolver dudas frecuentes.
