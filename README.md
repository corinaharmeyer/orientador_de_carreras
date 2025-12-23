# 🧭 Orientador de Carreras

## 📌 Descripción general

Este proyecto implementa un **orientador vocacional** cuyo objetivo es **ayudar a una persona a reflexionar sobre posibles carreras** a partir de su perfil personal.

El sistema **no toma decisiones por el usuario** ni predice éxito profesional. En cambio, propone **carreras afines**, explicando:
- por qué podrían encajar con la persona
- qué aspectos podrían requerir atención o desarrollo

De esta manera, el orientador funciona como una **herramienta de apoyo a la toma de decisiones**, fomentando el autoconocimiento y la reflexión.

---

## 🎯 Objetivo del sistema

El objetivo principal es:
- analizar **intereses**
- analizar **habilidades**
- considerar **preferencias personales** (matemática, comunicación, creatividad, trabajo con personas y en equipo)

y compararlas contra una base de datos de carreras para generar un **ranking de recomendaciones razonadas**.

---

## 🧠 Enfoque conceptual

El sistema se basa en la idea de que una carrera puede describirse mediante:
- temas que suelen interesar
- habilidades requeridas
- características del entorno de trabajo

Del mismo modo, una persona puede describirse con los mismos ejes.  
El orientador mide **qué tan similares son ambos perfiles**.

---

## 🧩 Componentes principales

### 👤 Perfil del usuario

El perfil del usuario incluye:

- **Intereses**  
  Ejemplos: tecnología, arte, salud, negocios.

- **Habilidades**  
  Ejemplos: programación, comunicación, análisis, diseño.

- **Preferencias numéricas (1 a 3)**  
  - Matemática  
  - Comunicación  
  - Creatividad  
  - Trabajo con personas (sí/no)  
  - Trabajo en equipo  

Este perfil se construye:
- mediante un **cuestionario interactivo**, o
- a través de **parámetros por línea de comandos**

---

### 🎓 Base de carreras

Cada carrera se describe con:
- nombre de la carrera
- lista de intereses asociados
- lista de habilidades asociadas
- valores esperados para cada preferencia (1 a 3)

Esto permite tratar a carreras y personas de forma **homogénea y comparable**.

---

## ⚙️ Funcionamiento del algoritmo

El sistema calcula un **puntaje total de afinidad** combinando tres tipos de similitud:

### 1️⃣ Similitud de intereses (45%)

- Se comparan los intereses del usuario con los intereses de cada carrera.
- Se utiliza una representación binaria (presencia / ausencia).
- Se calcula similitud mediante coseno.

Esto mide **motivación potencial**.

---

### 2️⃣ Similitud de habilidades (45%)

- Se comparan las habilidades del usuario con las requeridas por cada carrera.
- También se usa similitud por coseno.

Esto mide **preparación o afinidad técnica**.

---

### 3️⃣ Similitud numérica (10%)

- Se comparan los valores numéricos del usuario con los de la carrera.
- Se calcula una distancia normalizada.

Esto detecta **compatibilidad con el estilo de trabajo**.

---

### 🧮 Puntaje final

El puntaje final se obtiene combinando los tres componentes ponderados.  
Luego, las carreras se ordenan de mayor a menor afinidad.

---

## 🧾 Explicabilidad del resultado

Cada recomendación incluye:

### ✅ Razones
- intereses compartidos
- habilidades en común

### ⚠️ Advertencias
- ausencia de intereses compartidos
- ausencia de habilidades compartidas
- diferencias marcadas en preferencias (por ejemplo: matemática baja vs alta)

Esto permite que el usuario **entienda por qué apareció una carrera** y no la vea como una “caja negra”.

---

## 🖥️ Modos de uso

### 🔹 Modo interactivo

El sistema realiza un cuestionario paso a paso por consola, ideal para usuarios sin conocimientos técnicos.

### 🔹 Modo por parámetros

Permite pasar intereses, habilidades y preferencias directamente por línea de comandos, pensado para:
- pruebas
- demos
- integración futura con otras interfaces

---

## 💾 Persistencia de resultados

El sistema puede guardar cada ejecución en un archivo JSON que contiene:
- fecha y hora
- perfil del usuario
- ranking de carreras
- razones y advertencias

Esto permite:
- análisis posterior
- auditoría
- evolución del sistema

---

## 📁 Organización del proyecto

El código está dividido en módulos con responsabilidades claras:

- `questionnaire`: interacción con el usuario  
- `models`: estructuras de datos  
- `recommender`: lógica principal de recomendación  
- `utils`: funciones auxiliares de normalización  
- `persistence`: guardado de resultados  
- `cli`: interfaz de línea de comandos  

Esta separación favorece la **claridad, mantenibilidad y extensibilidad**.

---

## 🧠 Alcances y limitaciones

### ✔️ Alcances
- Orientación inicial
- Sistema explicable
- Fácil de extender
- Independiente del contexto educativo específico

### ⚠️ Limitaciones
- No reemplaza orientación profesional humana
- Depende de la calidad de la base de carreras
- No considera factores socioeconómicos o contextuales

---

## 🚀 Posibles mejoras futuras

- Ajustar pesos según el usuario
- Incorporar descripciones textuales más ricas
- Agregar interfaz gráfica o web
- Incluir trayectorias educativas sugeridas
- Evaluaciones dinámicas en lugar de valores fijos

---

## 📌 Conclusión

Este proyecto demuestra cómo técnicas simples de similitud pueden utilizarse para construir un **orientador de carreras claro, explicable y útil**, priorizando la reflexión personal por sobre la automatización de decisiones.

El sistema está pensado como una **herramienta de acompañamiento**, no como un veredicto final.
