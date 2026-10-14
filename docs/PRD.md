# Cursada: documento de requisitos (PRD)

Versión 0.2 · 11 de octubre de 2026 · Autor: Lauti

## 1. Objetivo

Cursada es el lugar único donde un estudiante ve todas sus fechas de la facultad y accede a todo lo de cada materia, sin importar dónde se publicó cada cosa. Además, ofrece un espacio de estudio asistido con IA sobre sus propios apuntes.

## 2. Problema

- Las fechas de entrega y evaluación están dispersas en tres fuentes: el aula virtual (Moodle), PDFs de cada cátedra y, sobre todo, lo que se dice en clase.
- Ninguna herramienta actual reúne todas esas fechas en una sola vista. Moodle solo muestra las que el docente carga.
- Sin una vista única de los deadlines, es difícil organizar el tiempo entre materias.
- Los recursos de cada materia (carpeta de Drive, aula de Moodle) están en lugares distintos y hay que buscarlos cada vez.

## 3. Usuarios

- Estudiantes universitarios que cursan varias materias en simultáneo.
- Cada usuario tiene su cuenta y sus propios datos. Nada se comparte entre usuarios.
- Usuario de referencia: estudiante de Ingeniería en Sistemas de la UCC que usa Google Drive para sus archivos y Moodle como aula virtual.

## 4. Espacios de la app

| Espacio | Para qué sirve | Qué contiene |
| --- | --- | --- |
| Materias | Llegar rápido a todo lo de una materia | Ficha por materia con links a Drive y Moodle, sus fechas y sus apuntes |
| Fechas | Ver todos los deadlines juntos | Calendario y línea de tiempo con las fechas de todas las materias |
| Estudio | Estudiar con IA sobre los apuntes propios | Apuntes subidos y sesiones de estudio |

## 5. Funcionalidades

Prioridades: **P0** es imprescindible para que la app sirva, **P1** es importante y **P2** es deseable.

### Cuenta

| ID | Funcionalidad | Prioridad |
| --- | --- | --- |
| C1 | Registro e inicio de sesión con email y contraseña | P0 |
| C2 | Cada usuario ve y edita solo sus propios datos | P0 |
| C3 | Recuperar la contraseña con un link enviado por mail | P1 |
| C4 | Iniciar sesión con una cuenta de Google | P2 |

### Materias

| ID | Funcionalidad | Prioridad |
| --- | --- | --- |
| M1 | Crear, editar y eliminar materias (nombre, año, cuatrimestre, docente) | P0 |
| M2 | Guardar en cada materia el link a su carpeta de Drive y a su aula de Moodle | P0 |
| M3 | Ficha de la materia con sus próximas fechas y sus apuntes | P1 |
| M4 | Archivar materias terminadas sin borrarlas | P2 |

### Fechas

| ID | Funcionalidad | Prioridad |
| --- | --- | --- |
| F1 | Crear, editar y eliminar fechas: título, materia, tipo (TP, parcial, proyecto, otro), fecha y estado (pendiente, entregado) | P0 |
| F2 | Vista "esta semana" con las fechas de los próximos 7 días, ordenadas | P0 |
| F3 | Vista de calendario mensual | P1 |
| F4 | Vista de línea de tiempo del cuatrimestre | P1 |
| F5 | Carga rápida en lenguaje natural ("el TP2 de Redes es para el viernes 20"), que el usuario confirma antes de guardar | P1 |
| F6 | Extracción de fechas desde el PDF del cronograma de la cátedra, con confirmación del usuario | P1 |

### Estudio

| ID | Funcionalidad | Prioridad |
| --- | --- | --- |
| E1 | Subir apuntes en PDF a una materia, desde su ficha o dentro de una sesión. Todo apunte queda en la biblioteca de la materia y puede reutilizarse en otras sesiones | P1 |
| E2 | Generar preguntas de repaso a partir de los apuntes elegidos (pregunta, respuesta y dificultad). El alumno elige la cantidad, dentro de un máximo que depende del tamaño de los apuntes | P1 |
| E3 | Preguntarle a los apuntes de la sesión, con respuestas que citan de qué apunte sale cada parte | P1 |
| E4 | Sesión de estudio: pertenece a una materia, usa los apuntes que el alumno elige o sube en ese momento y permite consultar y practicar con preguntas | P1 |
| E6 | Guardar las sesiones con su historial completo para retomarlas más tarde | P1 |
| E5 | Soporte para apuntes en .docx y fotos | P2 |

### Integraciones

| ID | Funcionalidad | Prioridad |
| --- | --- | --- |
| I1 | Consultar fechas y apuntes desde Claude mediante un servidor MCP propio ("¿qué entregas tengo esta semana?") | P2 |

## 6. Fuera del alcance

- **Reemplazar a Drive:** los apuntes se suben solo como material de estudio. La organización general de archivos sigue en Drive, y Cursada guarda un link a cada carpeta.
- **Integración automática con Drive o Moodle:** en esta versión solo se guardan links. Leer carpetas o fechas directamente requiere autenticación con cada servicio.
- **Fechas compartidas entre compañeros:** cada estudiante carga las suyas.
- **Planificar el tiempo del usuario:** la app muestra las fechas ordenadas y el usuario decide cómo organizarse.
- **Notificaciones** por mail o push.
- **App móvil nativa:** es una app web.

## 7. Criterios de éxito

- Cargar una fecha manualmente toma menos de 30 segundos.
- La vista "esta semana" muestra correctamente las fechas de todas las materias.
- La carga en lenguaje natural interpreta bien materia y fecha en al menos 9 de cada 10 casos de prueba.
- Las respuestas sobre apuntes citan su fuente, y la cita corresponde al contenido.
- Un usuario no puede ver ni modificar datos de otro.

## 8. Relación con el plan de aprendizaje

| Funcionalidades | Fase | Qué se aprende |
| --- | --- | --- |
| C1 a C3, M1, M2 | 1 | Primer agente de código y tests |
| F1, F2 | 2 | Tests primero con el agente |
| F3, F4 | 3 | Verificar la UI con un navegador por MCP |
| F5, F6, E2 | 4 | API, salidas estructuradas y tool use |
| E1, E3, E4, E6 | 5 | RAG, embeddings y citas |
| I1 | 6 | Servidor MCP propio |

## 9. Decisiones tomadas

- El login es con email y contraseña, con recuperación por mail. El acceso con Google queda como mejora.
- El alumno elige cuántas preguntas de repaso generar, con un máximo según el tamaño de los apuntes.
- Cada sesión de estudio pertenece a una sola materia y se guarda con su historial.

## 10. Preguntas abiertas

- ¿Qué tamaño máximo de PDF y cuántos apuntes por sesión se permiten? Se define en `DISENO.md` según costo y ventana de contexto.
