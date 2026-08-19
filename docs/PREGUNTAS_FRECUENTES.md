# Preguntas frecuentes

## Sobre el programa

**¿Esto reemplaza una carrera de pedagogía?**
No. No otorga título, grado ni habilitación legal para ejercer. Es un programa de formación
profesional y autoformación: entrega criterios, evidencia y práctica documentada. Quien quiera
ejercer como docente en un sistema formal necesita el título que su país exige.

**¿Sirve si nunca he hecho clases?**
Sí, y es una de sus rutas previstas. Empieza por el tronco común (partes 00 a 02) y usa los casos
de `cases/` y la escuela simulada de `virtual-school-lab/` como contexto de práctica.

**¿Cuánto tiempo toma?**
El supuesto declarado es de 2,5 horas por clase: 1 hora de material y 1,5 de práctica. El programa
completo son unas 540 horas. Con cinco horas semanales sostenidas, algo más de dos años. Las
rutas de [RUTAS_DE_APRENDIZAJE.md](RUTAS_DE_APRENDIZAJE.md) permiten recorridos mucho más cortos
según el objetivo.

**¿Puedo estudiar solo la parte que me interesa?**
Sí, después del tronco común. Las partes 00 a 02 fijan el vocabulario y los mecanismos que el
resto usa; saltarlas produce aplicación de técnicas sin criterio para decidir cuándo no usarlas.

**¿Por qué 12 clases por parte y no las que cada tema necesite?**
Porque la regularidad permite planificar, comparar avance y sostener el hábito. Es una decisión de
diseño discutible y declarada: la profundidad se ajusta dentro de la clase, no en su número.

## Sobre el contenido

**¿De dónde sale lo que afirma cada clase?**
De la bibliografía de [BIBLIOGRAFIA.md](BIBLIOGRAFIA.md) y de las fuentes oficiales de
[FUENTES.md](FUENTES.md). Cada clase cita dos o tres obras con la razón de esa lectura y declara
el estado de la evidencia que la sostiene.

**¿Qué significan `ROBUSTA`, `EN-DEBATE` y los demás estados?**
Son los seis niveles de respaldo que el programa distingue. Su definición y su uso están en
[ESTANDARES_DE_EVIDENCIA.md](ESTANDARES_DE_EVIDENCIA.md), y su distribución real en
[STATUS.md](../STATUS.md).

**¿Por qué el programa rechaza los estilos de aprendizaje?**
Porque la hipótesis de emparejar la enseñanza con la modalidad preferida ha sido puesta a prueba
repetidamente y no mejora el aprendizaje. Sigue siendo la creencia más extendida entre docentes;
su costo es desviar tiempo y atención de diferencias que sí importan, empezando por el
conocimiento previo.

**El programa dice que algo está «en debate». ¿No debería darme la respuesta?**
No cuando no la hay. Presentar consenso donde hay desacuerdo publicado entre especialistas
competentes sería más cómodo y menos honesto. En esas clases el objetivo es que sepas qué
evidencia te haría cambiar de posición.

**¿Es contenido chileno o internacional?**
La capa de evidencia es internacional; la capa normativa es Chile-first y está marcada como
`MARCO-NORMATIVO`. Para adaptarlo a otro país, se sustituyen las fuentes normativas y se conserva
el resto. Ver [GUIA_DEL_FORMADOR.md](GUIA_DEL_FORMADOR.md), sección 8.

## Sobre el uso

**¿Puedo usarlo para capacitar en mi institución?**
Sí, bajo licencia CC BY-NC-SA 4.0: con atribución, compartiendo igual y **sin fines comerciales**.
Para uso comercial, se necesita autorización previa del autor. El paquete exportable y las
instrucciones están en [MIGRACION_A_CAPACITACION.md](MIGRACION_A_CAPACITACION.md).

**¿Puedo aplicar las actividades con mis estudiantes reales?**
Sí, respetando el [protocolo de práctica responsable](ETICA_Y_PRACTICA_RESPONSABLE.md). La regla
de fondo: un estudiante no es material de práctica, y toda decisión debe justificarse por su
beneficio.

**¿Cómo demuestro que completé el programa?**
Con tu portafolio de evidencias: 300 productos con contexto, decisión, fundamento y criterio
aplicado, más los 18 proyectos integradores. No hay certificado; hay evidencia, que es lo que se
puede revisar.

**¿Puedo contribuir?**
Sí. Las condiciones están en [CONTRIBUTING.md](../CONTRIBUTING.md). En resumen: se edita el
manifiesto, no la clase publicada; se cita la fuente; y se distingue evidencia de opinión.

## Sobre el repositorio

**¿Por qué el contenido se genera en vez de escribirse a mano?**
Para garantizar que ninguna de las 300 clases quede sin criterios de logro, sin estado de
evidencia o sin lecturas, y para que una mejora del contrato pedagógico se aplique a todas a la
vez. El detalle está en [ARQUITECTURA.md](ARQUITECTURA.md).

**Edité una clase y el CI falla. ¿Por qué?**
Porque `curriculum/` es contenido generado. Edita el manifiesto correspondiente en `manifests/` y
ejecuta `python scripts/generar_clases.py`.

**¿Dónde está el sitio publicado?**
En GitHub Pages, generado con `python scripts/generar_sitio.py` y desplegado automáticamente
desde `main`. El enlace está en el README.

**¿Necesito instalar algo para usar el repositorio?**
Para leerlo, no. Para regenerarlo, Python 3.11 o superior y nada más: los generadores usan solo
la biblioteca estándar.

---

| Anterior | Índice | Siguiente |
|---|---|---|
| [Arquitectura](ARQUITECTURA.md) | [Programa](../README.md) · [Documentos](../FILE_INDEX.md) | [Metodología](METODOLOGIA.md) |
