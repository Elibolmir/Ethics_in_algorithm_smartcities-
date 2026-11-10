# Plantillas Fase 1 · listas para que la IA las rellene

Basadas en los Anexos I y II de tu *Guía Fase 1*. Los campos `{{así}}` los rellena la plataforma (o Claude) con los datos del cuestionario.

---

## Anexo I · Promoción de la negociación del Plan de Igualdad

Mediante el presente escrito, y en virtud del artículo 5 del Real Decreto 901/2020, de 13 de octubre, la empresa **{{razon_social}}**, NIF {{nif}}, domicilio social {{domicilio}}, CNAE {{cnae}}, convenio colectivo aplicable {{convenio}}, promueve la negociación de su Plan de Igualdad y diagnóstico previo y expone:

1. Que la persona abajo firmante ostenta legitimación por parte de {{razon_social}} para negociar el Plan de Igualdad y su diagnóstico previo.
2. Que el ámbito de negociación es la empresa, con {{n_centros}} centro(s) de trabajo en {{provincias_ccaa}}, con {{n_personas}} personas trabajadoras, y {{tiene_rlt_por_centro}} representación legal o sindical en cada centro.
3. Que las materias objeto de negociación, conforme al artículo 46.2 de la LO 3/2007 y al RD 901/2020, serán al menos:
   - Proceso de selección y contratación
   - Clasificación profesional
   - Formación
   - Promoción profesional
   - Condiciones de trabajo, incluida la auditoría salarial entre mujeres y hombres
   - Ejercicio corresponsable de los derechos de la vida personal, familiar y laboral
   - Infrarrepresentación femenina
   - Retribuciones
   - Prevención del acoso sexual y por razón de sexo
   - {{materias_adicionales}} *(violencia de género, lenguaje no sexista u otras del convenio)*
4. Que la empresa señala como domicilio a efectos de comunicaciones {{domicilio_comunicaciones}} y como persona de contacto a {{contacto_nombre}}, {{contacto_email}}, {{contacto_telefono}}.

Y para que conste, firma la presente {{representante_nombre}} ({{representante_dni}}), representante legal de la empresa a efectos de negociación.

En {{lugar}}, a {{fecha}}.

---

## Anexo II · Acta de constitución de la Comisión Negociadora

En {{lugar}}, a {{fecha}}, reunidas:

- Por la **representación de la empresa**: {{lista_empresa}} *(nombre, apellidos y cargo)*
- Por la **representación de las personas trabajadoras**: {{lista_plantilla}} *(nombre, apellidos y cargo)*

con motivo de la constitución de la Comisión Negociadora del Plan de Igualdad de {{razon_social}}, en cumplimiento de los artículos 45 y 46 de la LO 3/2007, ambas partes se reconocen capacidad y legitimación suficiente y **ACUERDAN** constituir la Comisión y establecer sus competencias y normas de funcionamiento.

**1. Composición.** Paritaria; se promueve la composición equilibrada entre mujeres y hombres; la parte social, proporcional a su representatividad. Máximo 13 personas por parte (6 si no hay representación legal).

**2. Funciones.**
- Negociar y elaborar el diagnóstico y las medidas del Plan.
- Elaborar el informe de resultados del diagnóstico.
- Identificar medidas prioritarias, ámbito, medios, responsables y cronograma.
- Impulsar la implantación del Plan.
- Definir indicadores e instrumentos de seguimiento y evaluación.
- Remitir el Plan aprobado a la autoridad laboral para su registro, depósito y publicación.
- Impulsar las primeras acciones de información y sensibilización.
- {{otras_funciones}}

**3. Funcionamiento.**
- Presidencia: {{presidencia}} · Secretaría: {{secretaria}} *(alternas entre las partes)*.
- **3.1 Reuniones:** periodicidad {{periodicidad}}. Acta de cada reunión con materias tratadas, acuerdos, puntos sin acuerdo y firma (con manifestaciones de parte si procede).
- **3.2 Acuerdos:** buena fe; mayoría de cada parte; conformidad de la mayoría de la representación de la plantilla. Asesoría externa de **OMN Hub CEE** ({{asesora}}), con voz y sin voto. En caso de desacuerdo, solución autónoma de conflictos si así se acuerda.
- **3.3 Confidencialidad:** deber de sigilo; ningún documento se usará fuera de la Comisión.
- **3.4 Sustitución:** por vacancia, ausencia, dimisión, fin de mandato o causa justificada ({{causas}}), por escrito y anexado a esta acta.
- **3.5 Otras disposiciones:** {{otras_disposiciones}}

Se levanta la sesión a las {{hora}} del {{fecha}}.

| Firma (empresa) | Firma (plantilla) |
|---|---|
| {{firmante_empresa}} | {{firmante_plantilla}} |

---

## Campos que el cuestionario debe pedir (resumen para la app)

`razon_social · nif · domicilio · cnae · convenio · n_centros · provincias_ccaa · n_personas · tiene_rlt_por_centro · contacto · representante · lista_empresa · lista_plantilla · periodicidad · asesora`

> Los datos personales (nombre, DNI) solo van en el documento final firmado, **nunca** en el texto que se envía a la IA. La IA trabaja con los campos vacíos y la plataforma los rellena al final.
