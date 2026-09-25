"""Dataset inicial de ejemplo para la validacion experimental (Capitulo 6).

Este dataset es un PUNTO DE PARTIDA generado para poder construir y probar el
pipeline de evaluacion. Debe reemplazarse por historias reales del backlog del
equipo, anotadas de forma independiente por >=3 expertos agiles (Product
Owners / Scrum Masters) y consensuadas, antes de reportar resultados finales
en el documento.

Cada entrada tiene:
- id: identificador de la historia.
- story_text: texto completo Como/Quiero/Para.
- project_context: contexto de proyecto opcional (backlog, dependencias).
- ground_truth: dict con 1 (cumple) / 0 (incumple) para cada uno de los 6
  criterios INVEST, segun el consenso de expertos.

NOTA: las anotaciones de ground_truth en este dataset de ejemplo son
ilustrativas (generadas para poder probar el pipeline), NO provienen de
expertos reales. No se deben citar como resultado del experimento en el
documento final.
"""

INVEST_CRITERIA = ("independent", "negotiable", "valuable", "estimable", "small", "testable")


DATASET = [
    {
        "id": "HU-EJ-01",
        "story_text": "Como usuario registrado quiero restablecer mi contraseña para recuperar el acceso a mi cuenta.",
        "project_context": "Módulo de autenticación, base de datos Postgres, envío de correos vía SendGrid.",
        "ground_truth": {"independent": 1, "negotiable": 1, "valuable": 1, "estimable": 1, "small": 1, "testable": 1},
    },
    {
        "id": "HU-EJ-02",
        "story_text": "Como cliente frecuente quiero recibir una notificación por correo cuando un producto de mi lista de deseos baje de precio para decidir si lo compro.",
        "project_context": "Módulo de catálogo y lista de deseos existente; motor de precios publica eventos en una cola interna.",
        "ground_truth": {"independent": 1, "negotiable": 1, "valuable": 1, "estimable": 1, "small": 1, "testable": 1},
    },
    {
        "id": "HU-EJ-03",
        "story_text": "Como usuario quiero una interfaz rápida y amigable para tener una experiencia óptima.",
        "project_context": None,
        "ground_truth": {"independent": 0, "negotiable": 0, "valuable": 0, "estimable": 0, "small": 1, "testable": 0},
    },
    {
        "id": "HU-EJ-04",
        "story_text": "Quiero un botón para exportar el reporte.",
        "project_context": None,
        "ground_truth": {"independent": 0, "negotiable": 0, "valuable": 0, "estimable": 0, "small": 1, "testable": 0},
    },
    {
        "id": "HU-EJ-05",
        "story_text": "Como administrador del sistema quiero gestionar usuarios, roles, permisos, reportes y configuración global para tener control total de la plataforma.",
        "project_context": "Sistema con módulos separados de usuarios, reportes y configuración.",
        "ground_truth": {"independent": 0, "negotiable": 1, "valuable": 1, "estimable": 0, "small": 0, "testable": 0},
    },
    {
        "id": "HU-EJ-06",
        "story_text": "Como analista de datos quiero descargar un reporte mensual de ventas en formato CSV para compartirlo con el equipo directivo.",
        "project_context": "Módulo de reportes ya expone datos agregados por mes en la base de datos.",
        "ground_truth": {"independent": 1, "negotiable": 1, "valuable": 1, "estimable": 1, "small": 1, "testable": 1},
    },
    {
        "id": "HU-EJ-07",
        "story_text": "Como PO quiero que el sistema sea escalable y flexible para soportar el crecimiento futuro del negocio.",
        "project_context": None,
        "ground_truth": {"independent": 0, "negotiable": 0, "valuable": 0, "estimable": 0, "small": 0, "testable": 0},
    },
    {
        "id": "HU-EJ-08",
        "story_text": "Como usuario de la app móvil quiero recibir una notificación push cuando mi pedido cambie de estado para hacer seguimiento sin abrir la app.",
        "project_context": "Sistema de pedidos con estados definidos (confirmado, enviado, entregado); servicio de push ya integrado (Firebase).",
        "ground_truth": {"independent": 1, "negotiable": 1, "valuable": 1, "estimable": 1, "small": 1, "testable": 1},
    },
    {
        "id": "HU-EJ-09",
        "story_text": "Como desarrollador quiero refactorizar el módulo de pagos para mejorar la calidad del código.",
        "project_context": "Cambio técnico interno sin impacto visible para el usuario final.",
        "ground_truth": {"independent": 1, "negotiable": 1, "valuable": 0, "estimable": 0, "small": 1, "testable": 0},
    },
    {
        "id": "HU-EJ-10",
        "story_text": "Como cliente quiero aplicar un cupón de descuento en el checkout para pagar un precio menor por mi compra.",
        "project_context": "Módulo de checkout existente; tabla de cupones con reglas de validez ya definida.",
        "ground_truth": {"independent": 1, "negotiable": 1, "valuable": 1, "estimable": 1, "small": 1, "testable": 1},
    },
    {
        "id": "HU-EJ-11",
        "story_text": "Como PO quiero mejorar el rendimiento general del sistema para que todo funcione mejor.",
        "project_context": None,
        "ground_truth": {"independent": 0, "negotiable": 0, "valuable": 0, "estimable": 0, "small": 0, "testable": 0},
    },
    {
        "id": "HU-EJ-12",
        "story_text": "Como usuario quiero filtrar la lista de productos por categoría y rango de precio para encontrar lo que busco más rápido.",
        "project_context": "Catálogo ya indexado por categoría y precio en la base de datos.",
        "ground_truth": {"independent": 1, "negotiable": 1, "valuable": 1, "estimable": 1, "small": 1, "testable": 1},
    },
    {
        "id": "HU-EJ-13",
        "story_text": "Como PO quiero rediseñar todo el flujo de compra, el catálogo, el carrito y el checkout para modernizar la plataforma completa.",
        "project_context": "Involucra múltiples módulos del sistema simultáneamente.",
        "ground_truth": {"independent": 0, "negotiable": 1, "valuable": 1, "estimable": 0, "small": 0, "testable": 0},
    },
    {
        "id": "HU-EJ-14",
        "story_text": "Como usuario quiero cerrar sesión desde cualquier pantalla para proteger mi cuenta cuando uso un dispositivo compartido.",
        "project_context": "Sistema de sesiones ya implementado con tokens JWT.",
        "ground_truth": {"independent": 1, "negotiable": 1, "valuable": 1, "estimable": 1, "small": 1, "testable": 1},
    },
    {
        "id": "HU-EJ-15",
        "story_text": "Como usuario quiero un sistema robusto y eficiente para que la aplicación funcione de forma confiable.",
        "project_context": None,
        "ground_truth": {"independent": 0, "negotiable": 0, "valuable": 0, "estimable": 0, "small": 1, "testable": 0},
    },
    {
        "id": "HU-EJ-16",
        "story_text": "Como PO quiero registrar una historia de usuario en una interfaz web para iniciar su análisis.",
        "project_context": "MVP del asistente INVEST, módulo de captura ya definido.",
        "ground_truth": {"independent": 1, "negotiable": 1, "valuable": 1, "estimable": 1, "small": 1, "testable": 1},
    },
    {
        "id": "HU-EJ-17",
        "story_text": "Como PO quiero validar el contenido de la historia con los criterios INVEST de IA para detectar fallos de negocio.",
        "project_context": "Depende del módulo lingüístico (spaCy) y del motor semántico LLM ya construidos.",
        "ground_truth": {"independent": 0, "negotiable": 1, "valuable": 1, "estimable": 1, "small": 1, "testable": 1},
    },
    {
        "id": "HU-EJ-18",
        "story_text": "Como usuario quiero que la app sea intuitiva y sencilla de usar para no perder tiempo aprendiendo a usarla.",
        "project_context": None,
        "ground_truth": {"independent": 0, "negotiable": 0, "valuable": 0, "estimable": 0, "small": 1, "testable": 0},
    },
    {
        "id": "HU-EJ-19",
        "story_text": "Como gerente de ventas quiero ver un dashboard con las métricas clave del mes (ventas totales, ticket promedio, top 5 productos) para tomar decisiones informadas.",
        "project_context": "Datos ya disponibles en el data warehouse; se requiere solo la capa de visualización.",
        "ground_truth": {"independent": 1, "negotiable": 1, "valuable": 1, "estimable": 1, "small": 1, "testable": 1},
    },
    {
        "id": "HU-EJ-20",
        "story_text": "Como PO quiero exportar la evaluación final a CSV para documentar la calidad de los requerimientos en mi equipo.",
        "project_context": "Resultado de validación ya generado por el orquestador backend.",
        "ground_truth": {"independent": 1, "negotiable": 1, "valuable": 1, "estimable": 1, "small": 1, "testable": 1},
    },
    {
        "id": "HU-EJ-21",
        "story_text": "Como usuario quiero una plataforma segura para confiar en el sistema.",
        "project_context": None,
        "ground_truth": {"independent": 0, "negotiable": 0, "valuable": 0, "estimable": 0, "small": 1, "testable": 0},
    },
    {
        "id": "HU-EJ-22",
        "story_text": "Como comprador quiero guardar varias direcciones de envío en mi perfil para elegir una rápidamente al finalizar la compra.",
        "project_context": "Perfil de usuario ya existente con campos editables.",
        "ground_truth": {"independent": 1, "negotiable": 1, "valuable": 1, "estimable": 1, "small": 1, "testable": 1},
    },
    {
        "id": "HU-EJ-23",
        "story_text": "Como PO quiero visualizar recomendaciones explicables y una propuesta de historia optimizada para corregirla de inmediato.",
        "project_context": "Depende de la respuesta JSON del motor LLM ya construido.",
        "ground_truth": {"independent": 0, "negotiable": 1, "valuable": 1, "estimable": 1, "small": 1, "testable": 1},
    },
    {
        "id": "HU-EJ-24",
        "story_text": "Como usuario nuevo quiero completar un tutorial guiado la primera vez que uso la app para entender cómo funciona.",
        "project_context": "Pantallas principales de la app ya existen; se requiere una capa de overlay/guía.",
        "ground_truth": {"independent": 1, "negotiable": 1, "valuable": 1, "estimable": 1, "small": 1, "testable": 1},
    },
    {
        "id": "HU-EJ-25",
        "story_text": "Como PO quiero un producto de alta calidad para satisfacer a los usuarios.",
        "project_context": None,
        "ground_truth": {"independent": 0, "negotiable": 0, "valuable": 0, "estimable": 0, "small": 0, "testable": 0},
    },
    {
        "id": "HU-EJ-26",
        "story_text": "Como usuario quiero recuperar mi carrito de compras si cierro la app sin finalizar la compra para no perder los productos seleccionados.",
        "project_context": "Carrito ya se persiste en backend asociado a la sesión del usuario.",
        "ground_truth": {"independent": 1, "negotiable": 1, "valuable": 1, "estimable": 1, "small": 1, "testable": 1},
    },
    {
        "id": "HU-EJ-27",
        "story_text": "Como PO quiero rediseñar la arquitectura completa del sistema, migrar la base de datos y actualizar todos los módulos para modernizar la infraestructura.",
        "project_context": "Impacta todos los módulos existentes simultáneamente.",
        "ground_truth": {"independent": 0, "negotiable": 1, "valuable": 1, "estimable": 0, "small": 0, "testable": 0},
    },
    {
        "id": "HU-EJ-28",
        "story_text": "Como soporte técnico quiero buscar un ticket por número de folio para responder más rápido a los clientes.",
        "project_context": "Sistema de tickets con folio único ya implementado.",
        "ground_truth": {"independent": 1, "negotiable": 1, "valuable": 1, "estimable": 1, "small": 1, "testable": 1},
    },
    {
        "id": "HU-EJ-29",
        "story_text": "Como usuario quiero una experiencia fluida y agradable en toda la aplicación.",
        "project_context": None,
        "ground_truth": {"independent": 0, "negotiable": 0, "valuable": 0, "estimable": 0, "small": 0, "testable": 0},
    },
    {
        "id": "HU-EJ-30",
        "story_text": "Como usuario quiero calificar un producto con estrellas y un comentario después de recibir mi pedido para compartir mi experiencia con otros compradores.",
        "project_context": "Módulo de pedidos ya marca cuándo un pedido fue entregado.",
        "ground_truth": {"independent": 1, "negotiable": 1, "valuable": 1, "estimable": 1, "small": 1, "testable": 1},
    },
]
