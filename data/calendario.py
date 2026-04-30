SEMANAS = {
    1:  "06/04/2026",
    2:  "13/04/2026",
    3:  "20/04/2026",
    4:  "27/04/2026",
    5:  "04/05/2026",
    6:  "11/05/2026",
    7:  "18/05/2026",
    8:  "25/05/2026",
    9:  "01/06/2026",
    10: "08/06/2026",
    11: "15/06/2026",
    12: "22/06/2026",
    13: "29/06/2026",
    14: "06/07/2026",
}

DIA_OFFSET = {
    "Lunes":   0,
    "Martes":  1,
    "Jueves":  3,
    "Viernes": 4,
}

GRUPOS_DIA = {
    "Lunes":   [1, 5, 6],
    "Martes":  [7, 8, 12, 13, 14],
    "Jueves":  [2, 3, 4],
    "Viernes": [9, 10, 11],
}

ESPECIALES = {
    7:  "Parcial I",
    10: "Recuperatorio Parcial I",
    12: "Parcial II",
    14: "Recuperatorio Parcial II",
}

CONTENIDO = {
    1: (
        "Unidad 1 - Introducción a la Algoritmia y la Programación\nUnidad 2 (variables y funciones) - Tipos de Datos, Expresiones y Funciones",
        "Unidad 1 - Introducción a la Algoritmia y la Programación\nUnidad 2 (variables) - Tipos de Datos, Expresiones y Funciones",
        "Unidad 1 - Introducción a la Algoritmia y la Programación\nUnidad 2 (variables) - Tipos de Datos, Expresiones y Funciones",
        "Unidad 1 - Introducción a la Algoritmia y la Programación\nUnidad 2 (variables y funciones) - Tipos de Datos, Expresiones y Funciones",
    ),
    2: (
        "Unidad 3 (decisiones y ciclos) - Estructuras de Control",
        "Unidad 2 (funciones) - Tipos de Datos, Expresiones y Funciones\nUnidad 3 (Decisiones) - Estructuras de Control",
        "Unidad 2 (funciones) - Tipos de Datos, Expresiones y Funciones\nUnidad 3 (Decisiones) - Estructuras de Control",
        "Unidad 3 (Decisiones y ciclos) - Estructuras de Control",
    ),
    3: (
        "Unidad 4 (Rangos, Cadenas, Tuplas) - Tipos de Estructuras de Datos",
        "Unidad 3 (ciclos) - Estructuras de Control",
        "Unidad 3 (ciclos) - Estructuras de Control",
        "Unidad 4 (Rangos, Cadenas, Tuplas) - Tipos de Estructuras de Datos",
    ),
    4: (
        "Unidad 4 (Listas, Listas y Cadenas, Operaciones) - Tipos de Estructuras de Datos",
        "Unidad 4 (Rangos, Cadenas, Tuplas) - Tipos de Estructuras de Datos",
        "Unidad 4 (Rangos, Cadenas, Tuplas) - Tipos de Estructuras de Datos",
        "FERIADO",
    ),
    5: (
        "Unidad 4 (diccionarios) - Tipos de Estructuras de Datos\nUnidad 5 (archivos y errores) - Entrada y Salida de Información",
        "Unidad 4 (Listas, Listas y Cadenas, Operaciones) - Tipos de Estructuras de Datos",
        "Unidad 4 (Listas, Listas y Cadenas, Operaciones) - Tipos de Estructuras de Datos",
        "Unidad 4 (Listas, Listas y Cadenas, Operaciones) - Tipos de Estructuras de Datos",
    ),
    6: (
        "Unidad 6 (Pandas, Numpy) - Bibliotecas",
        "Unidad 4 (diccionarios) - Tipos de Estructuras de Datos\nUnidad 5 (archivos) - Entrada y Salida de Información",
        "Unidad 4 (diccionarios) - Tipos de Estructuras de Datos\nUnidad 5 (archivos) - Entrada y Salida de Información",
        "Unidad 4 (diccionarios) - Tipos de Estructuras de Datos\nUnidad 5 (archivos) - Entrada y Salida de Información",
    ),
    7: None,
    8: (
        "FERIADO",
        "Unidad 5 (Errores) - Entrada y Salida de Información\nUnidad 6 (Pandas) - Bibliotecas",
        "Unidad 5 (Errores) - Entrada y Salida de Información\nUnidad 6 (Pandas) - Bibliotecas",
        "Unidad 5 (Errores) - Entrada y Salida de Información\nUnidad 6 (Pandas) - Bibliotecas",
    ),
    9: (
        "Unidad 6 (Matplotlib) - Bibliotecas",
        "Unidad 6 (Pandas, Numpy) - Bibliotecas",
        "Unidad 6 (Pandas, Numpy) - Bibliotecas",
        "Unidad 6 (Pandas, Numpy) - Bibliotecas",
    ),
    10: None,
    11: (
        "FERIADO",
        "Unidad 6 (Matplotlib) - Bibliotecas",
        "Unidad 6 (Matplotlib) - Bibliotecas",
        "Unidad 6 (Matplotlib) - Bibliotecas",
    ),
    12: None,
    13: (
        "Repaso pre recuperatorio",
        "Repaso pre recuperatorio",
        "Repaso pre recuperatorio",
        "Repaso pre recuperatorio",
    ),
    14: None,
}

RECOMENDACIONES = {
    2:  "Repasar Unidad 1 y los apuntes de variables y funciones.",
    3:  "Repasar Unidad 2 completa (tipos de datos, expresiones y funciones).",
    4:  "Repasar Unidad 3 (decisiones y ciclos).",
    5:  "Repasar Unidad 4 — rangos, cadenas y tuplas.",
    6:  "Repasar Unidad 4 completa (listas, diccionarios) y arrancar a ver Unidad 5.",
    7:  "⚠️ Parcial I — repasar Unidades 1 a 4 completas.",
    8:  "Repasar Unidad 5 (archivos y errores).",
    9:  "Repasar Unidad 6 — Pandas y Numpy.",
    10: "⚠️ Recuperatorio Parcial I — repasar Unidades 1 a 4 completas.",
    11: "Repasar Unidad 6 — Pandas, Numpy y Matplotlib.",
    12: "⚠️ Parcial II — repasar Unidades 5 y 6 completas.",
    13: "Repaso general para el recuperatorio.",
    14: "⚠️ Recuperatorio Parcial II — repasar todo.",
}

COL_DIA = {
    "Lunes": 0,
    "Martes": 1,
    "Jueves": 2,
    "Viernes": 3,
}
