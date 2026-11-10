"""Spanish change report for v2. Usage: python3 -I build_report.py OUT.docx"""
import sys
import docx
from docx.shared import Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

d = docx.Document()
st = d.styles['Normal']
st.font.name = 'Arial'
st.font.size = Pt(11)


def table(rows, widths=None):
    t = d.add_table(rows=len(rows), cols=len(rows[0]))
    t.style = 'Table Grid'
    for ri, row in enumerate(rows):
        for ci, v in enumerate(row):
            c = t.cell(ri, ci)
            c.text = ''
            r = c.paragraphs[0].add_run(v)
            r.font.size = Pt(9.5)
            r.bold = ri == 0
            if ri == 0:
                sh = OxmlElement('w:shd'); sh.set(qn('w:fill'), 'DCE6F2'); sh.set(qn('w:val'), 'clear')
                c._tc.get_or_add_tcPr().append(sh)
    d.add_paragraph()


d.add_heading('Versión 2 corregida: informe de cambios', 0)
d.add_paragraph('Artículo: Profiling Bias in LLMs, LMMs, LRMs. An Ethical and Legal Framework for the Inclusion of Neurodivergent Users. Base: versión del 16/07/2026. Anotaciones: profesor Víctor (PDF "victor 3").')
d.add_paragraph('Archivos: v2 final (limpia) y v2 REVISIÓN (el texto nuevo aparece en azul). Las páginas indicadas corresponden a la versión final en PDF.')

d.add_heading('1. Las 14 notas del profesor: qué se ha hecho', 1)
table([
    ['#', 'Nota del profesor', 'Qué he hecho', 'Pág.'],
    ['1', '"ontologically incapable": ¿es así? Propone un experimento con el dataset de Hugging Face.', 'La frase pasa a ser una hipótesis de trabajo, con remisión a la sección 3.4. El experimento se describe en el apartado de trabajo futuro.', '2, 36'],
    ['2', '"the standard"', 'Ahora dice "the standard EN 301 549".', '3'],
    ['3', 'Falta un espacio en "silenced.Although"', 'Corregido.', '3'],
    ['4', 'Subraya "unequivocal" (afirmación demasiado fuerte)', 'Sustituido por "The argument developed in this section suggests…".', '3'],
    ['5', 'La pregunta de investigación le parece muy interesante', 'Se mantiene. La respuesta a RQ1 se refuerza con la sección técnica (nota 15).', '—'],
    ['6', 'Añadir ejemplos de textos de personas con TDAH, dislexia o TEA', 'Nueva sección 2.1.1 con citas literales de tu corpus, agrupadas en 4 rasgos, más el corpus DysList (Rello et al., 2014). Sin ejemplos inventados.', '4'],
    ['7', 'Elogio de la estructura ética → jurídica → valoración', 'Sin cambios.', '—'],
    ['8', '"Not accidental; it is political" es mucho decir', 'Reescrito con argumentos legales comprobables (CRPD art. 1, EAA art. 3(1), W3C 2021). Se plantea como una pregunta abierta, no como una acusación.', '35'],
    ['9', 'La dignidad de la diferencia parece más propia de Extremo Oriente', 'Añadidos Mishná Sanedrín 4:5, Sacks (2002) "The Dignity of Difference" y Analectas 13.23 (armonía sin uniformidad).', '6'],
    ['10', 'Revisar los datasets existentes y resumirlos en una tabla', 'Nueva Tabla 2 con 13 recursos y párrafo con las 3 lagunas encontradas.', '8'],
    ['11', '¿Eres la autora de la taxonomía?', 'Nuevo apartado "Originality of the taxonomy": qué es original tuyo y qué procede de otros autores (incluido Lemke et al., 2024).', '12'],
    ['12', '¿Cómo has creado la tabla? ¿Están online los experimentos?', 'Nuevo apartado "Construction of the forensic tables" (4 pasos) y compromiso de publicar datos y script en GitHub.', '12'],
    ['13', 'Empezar cada sección con una definición', '9 definiciones, una al inicio de cada sesgo (SI-01 a SO-03).', '13–20'],
    ['14', 'Muchas evidencias son limitaciones técnicas, no sesgos', 'Nueva sección 3.4 con un criterio operativo (3 pruebas). Se reconoce que el 100 % se debe a cómo se seleccionaron los casos.', '27, 33'],
    ['15', 'Hacer el análisis técnico: ¿dónde se produce el problema?', 'Nuevo párrafo con 4 capas (tokenización, RLHF, system prompt, decodificación) y cómo medir cada una.', '28'],
    ['16', '"Deficts" → deficits?', 'Corregido: "Axiological Deficits".', '35'],
    ['17', 'HK Danmark: conexión con el derecho laboral', 'Desarrollada: Directiva 2000/78/CE (art. 5, ajustes razonables) y AI Act Anexo III punto 4 (empleo = alto riesgo).', '36'],
])

d.add_heading('2. Errores que he corregido aunque el profesor no los marcó', 1)
table([
    ['Error', 'Corrección', 'Por qué importa'],
    ['AI Act citado como "2024/1353"', '2024/1689', 'Número oficial incorrecto.'],
    ['"Large Retrieval Models (LRMs)"', '"Large Reasoning Models"', 'LRM significa modelos de razonamiento (como el modo "Thinking" que citan tus CSV).'],
    ['"Çarık et al., 2024" con arXiv 2309.00770', 'Gallegos et al. (2024), Computational Linguistics', 'Ese arXiv es de Gallegos et al.; el autor "Çarık" no corresponde.'],
    ['Brandsen (2023) citado como estudio de "alucinaciones"', 'Brandsen et al. (2024): asociaciones negativas con términos de neurodivergencia', 'Lo comprobé leyendo el PDF de tu Drive. La atribución anterior era incorrecta.'],
    ['Lemke et al. (2024) citado sobre "falsedades negadas"', 'Lemke: estereotipos sobre la dislexia en imágenes generadas', 'Mismo motivo.'],
    ['Cita literal de Çarık ("systematic drift…") y de Bender ("plausible outputs…")', 'Eliminadas. Bender se cita con su definición de "stochastic parrot".', 'No pude verificar que esas frases existan.'],
    ['SI-03: falsedad "intentional"', '"follows a recurrent pattern"', 'La intención de un modelo no se puede probar.'],
    ['Tabla 3: SO-02 y SO-03 repetidos, celdas vacías, "AI Act Art. 29"', 'SO-01/SO-02/SO-03 correctos; literatura completada; Art. 26', 'El art. 29 del texto final regula los organismos notificados. Las obligaciones de los responsables del despliegue (deployers) están en el art. 26.'],
    ['FRIA "obliges providers"', '"obliges certain deployers"', 'El art. 27 obliga a responsables del despliegue, no a proveedores.'],
    ['Faltaba el alcance legal de ChatGPT', 'Nuevo párrafo: no es alto riesgo por sí mismo; se aplican los arts. 50, 53 y 55', 'Evita la objeción "ChatGPT no es alto riesgo".'],
    ['Art. 5 citado de forma genérica', 'Art. 5(1)(a), (b) y (g)', 'El art. 5(1)(b) menciona expresamente la discapacidad, lo que refuerza tu tesis.'],
    ['"twelve profiling biases"', '"nine"', 'Son 9 sesgos.'],
    ['Dos tablas llamadas "Table 3"', 'Renumeradas como Tablas 2 a 5', 'Numeración coherente.'],
    ['Restos de borrador: "you presented in Chapter 3", "seno", "Profiling bird", "provn", "exology", "However, However"', 'Corregidos', 'Calidad formal.'],
    ['6 referencias citadas en el texto que faltaban en la bibliografía', 'Añadidas (Fricker, Crawford, Nussbaum, Barocas et al., Casey, Birhane et al. 2022)', 'Norma APA.'],
])

d.add_heading('3. Decisiones que solo tú puedes tomar', 1)
items = [
    ('Ejemplos de la sección 2.1.1', 'Dice que los textos son tuyos y que tu perfil combina TDAH, dislexia y TEA. Es la solución honesta, porque son textos reales de una persona neurodivergente, pero revela un dato de salud. Si no quieres revelarlo, dímelo y lo reformulo.'),
    ('Protocolo EFSM (sección 4)', 'El texto afirma que la cabecera EFSM se aplicó a los 189 casos. Algunos casos son de 2023 y el contrato EFSM es posterior. Confirma si los volviste a probar con EFSM o si se aplicó después, al clasificarlos.'),
    ('Los 4 pasos de "Construction of the forensic tables"', 'Los he deducido de tus archivos (conversation_export.json y los CSV). Confirma que describen lo que hiciste.'),
    ('Yang (2024)', 'Lo he retirado de la sección SI-03 porque no pude comprobar lo que se le atribuía. Si lo has leído, puedes volver a añadirlo.'),
    ('Widder (2024) y Gallego-Molina', 'Widder no está en la bibliografía. Gallego-Molina aparece como 2021 en el texto y 2024 en la bibliografía. Necesito los datos exactos.'),
    ('Resumen (abstract)', 'Menciona "quantitative fairness indicators (accuracy gaps, selection rates)", pero no aparecen en el artículo. Hay que desarrollarlos o quitarlos.'),
    ('Páginas por verificar', 'Brandsen et al. (2024): volumen y páginas de Autism Research. Las preprints de 2025 del Supplementary Material (AccessEval, ABLEIST…) no se incluyen porque no pude verificarlas.'),
    ('Dataset de Hugging Face (moremilk)', 'No pude abrirlo (la red de esta sesión lo bloquea). Antes de usarlo hay que saber si los textos son reales o generados por IA.'),
]
for t, x in items:
    p = d.add_paragraph(style='List Number')
    p.add_run(t + '. ').bold = True
    p.add_run(x)

d.add_heading('4. Antes de publicar los datos (siguiente paso)', 1)
for x in [
    'Los CSV atribuyen "GPT-5" a conversaciones de 2023 a julio de 2025. GPT-5 se lanzó el 7 de agosto de 2025: hay que poner el modelo real de cada fecha.',
    'En 3 archivos (sp01, sp03, sp0304) los hash no se pueden reproducir. En 4 archivos se calcularon solo sobre la cita, no sobre conv_id‖quote como dice el artículo.',
    'SO-04 Political (skeleton) contiene filas de relleno, y 16 filas de SO-01 son "ejemplo literal N". Hay que eliminarlas o sustituirlas por casos reales.',
    'Los códigos de los archivos (SO-04 Emotional, SO-05 Ghosting…) no coinciden con la taxonomía del artículo (SP-03 = Ghosting).',
    'adult_condition1.csv es el dataset clásico UCI Adult (ingresos, sexo, raza). Lo cito en la Tabla 2 como referencia general de fairness, no como dato tuyo.',
]:
    d.add_paragraph(x, style='List Bullet')

d.save(sys.argv[1])
