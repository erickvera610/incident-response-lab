# Tutorial en español: Incident Workflow Lab

## 1. Qué problema resuelve

Un incidente debe tener un estado coherente y una historia que no se pierda. Dos intentos de cambiarlo pueden entrar en conflicto; por eso usamos versiones y transacciones.

## 2. Pruébalo primero

Abre https://erickvera610.github.io/incident-response-lab/ . La demo funciona en tu navegador. Cambia un control y compara la salida. Los datos ficticios no son usuarios reales; los ejemplos tampoco representan trabajo realizado para una empresa.

## 3. Instálalo paso a paso

1. Instala Python desde python.org y Git desde git-scm.com.
2. Abre PowerShell y escribe `python --version` y `git --version`.
3. Escribe `git clone https://github.com/erickvera610/incident-response-lab.git`.
4. Escribe `cd incident-response-lab`.
5. Escribe `python app.py` y mantén abierta la terminal.
6. Abre http://127.0.0.1:8000 y prueba los controles.
7. Detén el servidor con Ctrl+C.

## 4. La secuencia de trabajo

`Create incident → check version → validate transition → append durable event`

**SQLite** guarda tablas en un archivo. **Transacción** significa que el estado y su evento se guardan juntos, o ninguno se guarda. **Versión** cuenta cambios: si viste versión 1 y alguien ya creó versión 2, tu escritura debe rechazarse. **Idempotencia** significa que repetir la misma petición no duplica su efecto. Aquí una clave identifica un cambio de estado; una repetición idéntica devuelve el registro sin crear otro evento.

Crea un incidente y avanza Open → Investigating → Resolved → Closed. No puedes saltar de Open a Closed. Reinicia Python para comprobar que el registro sigue en SQLite. En la demo pública, los datos permanecen en ese navegador mediante localStorage, no en un servidor compartido.

## 5. Leer el código con calma

Empieza por `core.py` y busca `run`. Después abre el archivo especializado indicado en README. Sigue una sola entrada hasta su salida. Lee las pruebas: cada una describe un comportamiento concreto. Por último, revisa `enhanced.js` para comparar la versión del navegador.

## 6. Reproducir los resultados

```bash
python -m unittest discover -v
node test_enhanced.cjs
python benchmark.py
```

Abre `benchmark-results.json` y compara su resumen con `CASE_STUDY.md`. El reporte incluye una hora real de ejecución. Los experimentos con semillas repetidas muestran varios resultados; no escogemos solo el mejor. Las métricas sintéticas de JavaScript pueden diferir de Python.

## 7. Tu siguiente mejora personal

Añade idempotencia también a la creación y una prueba de dos escritores concurrentes. Para alojarlo en un servidor, diseña autenticación y permisos antes de exponer datos.

```bash
git switch -c feature/my-improvement
# Edita código y ejecuta las pruebas
git add .
git commit -m "Describe the actual behavior change"
git push -u origin feature/my-improvement
```

Abre un pull request y explica problema, solución, resultado y límite. Se usó asistencia de IA para construir esta base. En una entrevista distingue lo que recibiste, lo que estudiaste y lo que realmente cambiaste.

## 8. Practicar la entrevista

- What problem does this application solve?
- Which data are available when the prediction is made?
- What is the simplest baseline?
- How did you avoid data leakage or inconsistent state?
- Which result surprised you?
- What failure case remains?
- What did you personally improve?

Primero responde en español. Después prepara cuatro frases cortas en inglés: problema, método, resultado y limitación. Usa solo resultados documentados.
