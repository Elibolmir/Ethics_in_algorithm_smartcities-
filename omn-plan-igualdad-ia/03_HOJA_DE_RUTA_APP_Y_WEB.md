# Hoja de ruta · Vender → Automatizar → App OMN → Web

Regla: **no se construye nada que no haya sido vendido antes al menos una vez.**

---

## Fase 1 · Vender ya (semanas 1-4) · coste ≈ 0 €

- [ ] Proyecto en claude.ai con el prompt maestro (ver `02_PROMPT_MAESTRO.md`).
- [ ] Plantillas base: propuesta, contrato, encargo de tratamiento RGPD, Excel de datos.
- [ ] Lista de 10 empresas con 50+ personas → 10 correos → 3 llamadas por semana.
- [ ] Objetivo: **1 cliente firmado**.

**Siguiente paso tras firmar:** ejecutar los pasos 2-9 de la guía con Claude.

---

## Fase 2 · Automatizar con herramientas sencillas (semanas 5-10)

| Necesidad | Herramienta sin programar |
|---|---|
| Formulario de alta del cliente | Google Forms o Tally |
| Datos de plantilla | Plantilla Google Sheets protegida |
| Cálculos de brecha | Fórmulas en Sheets (media, mediana, % brecha) generadas con Claude |
| Redacción de informes | Proyecto Claude + plantillas Docs |
| Cobro | Enlace de pago (Stripe o transferencia) |
| Seguimiento de clientes | Notion (ya tienes el Dashboard OMN Hub CEE) |

Objetivo: reducir el tiempo de un plan completo a la mitad. **Medirlo** en horas reales.

---

## Fase 3 · App OMN (cuando haya 3-5 clientes)

**Producto mínimo (MVP) · módulo "Igualdad":**
1. Acceso de empresa cliente (usuario y contraseña).
2. Subida del Excel de plantilla seudonimizado.
3. Cálculo automático: 9 materias + registro retributivo + alertas ≥ 25 %.
4. Generación de borradores (diagnóstico, plan, actas) con la API de Claude.
5. Panel de revisión de la consultora → aprobación → PDF final.
6. Calendario de seguimiento con avisos (vigencia máxima 4 años).

**Requisitos obligatorios:**
- Servidores en la UE; cifrado; registro de accesos.
- Contrato de encargo de tratamiento con cada cliente.
- Revisión humana antes de cualquier documento final.
- Accesibilidad WCAG 2.1 AA (coherente con la identidad de un CEE).

**Cómo se construye:** con Claude Code, paso a paso, en un repositorio propio `omn-app`.
Te pediré decisiones solo cuando sean tuyas (nombre, precio, colores).

---

## Fase 4 · Web nueva de OMN

**Empieza por una sola página (semana 2):** `omnhub.com/plan-de-igualdad`
1. Titular: problema legal + solución en 3 meses.
2. ¿Estás obligada? (calculadora: n.º personas → sí/no y plazos).
3. Qué incluye (los 10 pasos, en lenguaje claro).
4. Diferencial OMN: CEE + IA + experta firmante + módulo discapacidad.
5. Botón: "Pide tu diagnóstico".

**Después:** la web completa con las **5 áreas de negocio** de OMN Hub.
Para hacerlo necesito que me pases: dirección actual de la web, logotipo y las 5 áreas tal como quieres nombrarlas.
