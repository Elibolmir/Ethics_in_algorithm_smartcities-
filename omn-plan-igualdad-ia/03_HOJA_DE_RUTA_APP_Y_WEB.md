# Hoja de ruta · Vender → App OMN → Web

Regla: **no se construye nada que no se haya vendido antes al menos una vez.**

---

## Fase 1 · Vender ya (semanas 1-4) · coste ≈ 0 €

- [ ] Proyecto en claude.ai con el prompt maestro (`02_PROMPT_MAESTRO.md`).
- [ ] Subir al proyecto tu *Guía Fase 1*, tu presentación y `04_PLANTILLAS_FASE1.md`.
- [ ] Lista de 10 empresas → clasificarlas (producto A, B o C) → 10 correos → 3 llamadas por semana.
- [ ] Objetivo: **1 cliente de producto C firmado** (es el de mayor importe).

---

## Fase 2 · App OMN (tu hoja de ruta, en tu mismo orden)

| N.º | Módulo | Contenido | ¿En el MVP? |
|---|---|---|---|
| 1 | Base normativa | Por artículo, con versión y vigencia | ✅ |
| 2 | Cuestionario | Solo los datos que exige cada caso | ✅ |
| 3 | Clasificador | Reglas deterministas, sin IA generativa | ✅ |
| 4 | Generador documental | Plantillas versionadas (empieza por Anexos I y II) | ✅ **aquí termina el MVP** |
| 5 | Diagnóstico y cálculos | Registro y auditoría retributiva (RD 902/2020) | — |
| 6 | Revisión y validación | Supervisión humana cualificada | — |
| 7 | Calendario y seguimiento | Alertas, indicadores, vigencia de 4 años | — |
| 8 | Panel del cliente y espacio virtual | Meta Quest, Zoom, navegador; sello de tiempo de actas | — |

**Por qué el MVP termina en el paso 4:** con eso ya identificas obligaciones y generas documentación conforme a la norma. Eso se puede vender.

**Requisitos obligatorios desde el primer día:**
- Servidores en la UE, cifrado y registro de accesos.
- Evaluación de impacto (art. 35 RGPD) antes del lanzamiento.
- Accesibilidad: Ley 11/2023 y Directiva (UE) 2019/882 (WCAG 2.1 AA).
- Ningún dato personal en la cadena de bloques: solo la huella criptográfica (*hash*).

**Condiciones previas del espacio virtual (estado según tu presentación):**
- [ ] Visto bueno de la Inspección de Trabajo: *pendiente*
- [x] Acuerdo sindical: FeTICO adherido
- [ ] Acuerdo con Meta: *en preparación*
- [x] Sin datos biométricos ni de movimiento
- [x] Alternativa obligatoria sin gafas (Zoom y navegador)

**Cómo se construye:** con Claude Code, módulo a módulo, en un repositorio propio (`omn-app`). Primer encargo: **módulos 1-3** (base normativa, cuestionario y clasificador).

---

## Fase 3 · Web nueva de OMN

**Identidad visual (extraída de tu logo):**

| Uso | Color |
|---|---|
| Principal (texto, logo) | Azul petróleo `#365661` |
| Acento (botones, puntos) | Mostaza `#E39B35` |
| Fondo | Crema `#FCF9F4` |

Logo guardado en `assets/logo-omn-hub.png`.

**Empieza por una sola página (semana 2):** `/plan-de-igualdad`
1. Titular: "¿Tu empresa está obligada? Compruébalo en 2 minutos".
2. Mini-clasificador (plantilla + convenio) → producto A, B o C.
3. Las 5 fases, en lenguaje claro.
4. Diferencial OMN: CEE + IA con supervisión humana + espacio virtual + módulo de discapacidad.
5. Botón: "Pide tu diagnóstico".

**Después:** la web completa con las **5 áreas de negocio** de OMN Hub.
Para hacerla necesito: la dirección de la web actual y las 5 áreas con el nombre exacto que quieres.
