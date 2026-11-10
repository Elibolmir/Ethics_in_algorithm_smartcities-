"""Build the corrected v2 of 'Profiles bias full version' from the 16/07/2026 docx.
Usage: python3 -I build_v2.py SRC.docx OUT.docx [review]
In review mode, inserted paragraphs are coloured blue."""
import copy, re, sys
import docx
from docx.shared import RGBColor, Pt
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SRC, OUT = sys.argv[1], sys.argv[2]
REVIEW = len(sys.argv) > 3 and sys.argv[3] == 'review'
d = docx.Document(SRC)
P = list(d.paragraphs)          # frozen original indices
LOG = []                        # (location, before, after)


def ptext(p):
    return p.text


def rep(i, old, new, count=1):
    p = P[i]
    full = p.text
    if old not in full:
        raise SystemExit(f'NOT FOUND in para {i}: {old[:60]!r}')
    for r in p.runs:
        if old in r.text:
            r.text = r.text.replace(old, new, count)
            LOG.append((i, old, new))
            return
    # spans several runs: rebuild in the first run that carries text
    runs = [r for r in p.runs if r.text]
    runs[0].text = full.replace(old, new, count)
    for r in runs[1:]:
        r.text = ''
    LOG.append((i, old, new))


BODY_T = P[51]      # body paragraph template (Charter 11 pt, justified)
HEAD_T = P[49]      # sub-heading template (2.1 ...)


def _new_par_like(tpl, text, bold=None, italic=None):
    new_p = OxmlElement('w:p')
    if tpl._p.pPr is not None:
        new_p.append(copy.deepcopy(tpl._p.pPr))
    para = docx.text.paragraph.Paragraph(new_p, tpl._parent)
    segs = text if isinstance(text, list) else [(text, None)]
    tr = next((r for r in tpl.runs if r.text.strip()), None)
    for seg, fmt in segs:
        run = para.add_run(seg)
        if tr is not None and tr._r.rPr is not None:
            run._r.insert(0, copy.deepcopy(tr._r.rPr))
        if bold is not None:
            run.bold = bold
        if italic is not None:
            run.italic = italic
        if fmt == 'i':
            run.italic = True
        if fmt == 'b':
            run.bold = True
        if REVIEW:
            run.font.color.rgb = RGBColor(0x00, 0x33, 0xCC)
    return para


class Cursor:
    """Insert successive blocks after an anchor element, preserving order."""
    def __init__(self, anchor_el):
        self.el = anchor_el

    def par(self, text, head=False, bold=None, italic=None):
        tpl = HEAD_T if head else BODY_T
        para = _new_par_like(tpl, text, bold=bold, italic=italic)
        self.el.addnext(para._p)
        self.el = para._p
        LOG.append(('insert', '', text if isinstance(text, str) else ''.join(s for s, _ in text)))
        return para

    def table(self, rows, widths=None, size=8):
        t = d.add_table(rows=len(rows), cols=len(rows[0]))
        tblPr = t._tbl.tblPr
        borders = OxmlElement('w:tblBorders')
        for e in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
            b = OxmlElement(f'w:{e}')
            b.set(qn('w:val'), 'single'); b.set(qn('w:sz'), '4'); b.set(qn('w:color'), '808080')
            borders.append(b)
        tblPr.append(borders)
        for ri, row in enumerate(rows):
            for ci, val in enumerate(row):
                cell = t.cell(ri, ci)
                cell.text = ''
                run = cell.paragraphs[0].add_run(val)
                run.font.size = Pt(size)
                run.font.name = "Charter Roman"
                run.bold = (ri == 0)
                if REVIEW:
                    run.font.color.rgb = RGBColor(0x00, 0x33, 0xCC)
        self.el.addnext(t._tbl)
        self.el = t._tbl
        LOG.append(('insert', '', f'[table {len(rows)}x{len(rows[0])}]'))
        return t


def after(i):
    return Cursor(P[i]._p)


def before(i):
    prev = P[i]._p.getprevious()
    return Cursor(prev)


# ---------------------------------------------------------------- 1. typos / precision
rep(10, 'Large Retrieval Models (LRMs)', 'Large Reasoning Models (LRMs)')
rep(11, 'Large Retrieval Models (LRMs)', 'Large Reasoning Models (LRMs)')
rep(26, 'Profiling bird in AI systems', 'Profiling bias in AI systems')
rep(30, 'the systematic invisibilized and marginated of non-normative cognitive styles',
    'the systematic invisibilisation and marginalisation of non-normative cognitive styles')
rep(37, 'incoherence..', 'incoherence.')
rep(50, 'consequences of design..', 'consequences of design.')
rep(51, 'resist such reduction..', 'resist such reduction.')
rep(53, 'excluded.As Lagioia', 'excluded. As Lagioia')
rep(57, 'through proiling', 'through profiling')
rep(66, 'Profilig mechanisms', 'Profiling mechanisms')
rep(73, 'Regulation (EU) 2024/1353', 'Regulation (EU) 2024/1689')
rep(73, 'evaluation criteriaThird', 'evaluation criteria. Third')
rep(189, 'externally provn', 'externally proven')
rep(229, 'the exology of inclusion', 'the axiology of inclusion')
rep(229, 'on theother, \xa0a model', 'on the other, a model')
rep(235, 'the twelve profiling biases', 'the nine profiling biases')
rep(336, 'Axiological Deficts', 'Axiological Deficits')                 # professor, p.26
rep(350, 'not yet extended to algorithmic exclusion. Table 3).',
    'not yet extended to algorithmic exclusion (see Table 5).')
rep(351, 'Table 3. Necessary legislative reforms', 'Table 5. Necessary legislative reforms')
rep(358, 'located in the seno of the European Committee', 'established at European Union level')
rep(320, 'Table 3. Final analysis', 'Table 4. Final analysis')
rep(113, 'Table2. Codification', 'Table 3. Codification')
rep(334, 'By storing both hashes, you ensure redundancy and guarantee', 'Storing both hashes ensures redundancy and guarantees')
rep(335, 'the forensic evidence you presented in Chapter 3', 'the forensic evidence presented in Section 3')
rep(331, 'This mechanism works like a blockchain ledger:',
    'This mechanism is analogous to the integrity mechanism of a blockchain ledger:')

# professor p.3: "the standard" + missing space
rep(42, 'silenced.Although', 'silenced. Although')
rep(42, 'and EN 301 549 provide', 'and the standard EN 301 549 provide')
rep(42, 'This omission is not merely technical—it is ontological and political,',
    'This gap is not merely technical; it also has normative and political implications (see Section 2.2),')
# professor p.3: "unequivocal" (overstatement)
rep(43, 'The ontological conclusion is unequivocal: re-engineering',
    'The argument developed in this section suggests that re-engineering')
rep(43, 'insight.At the end of this article we can resolve this two questions:',
    'insight. This article addresses the following two research questions:')
# professor p.2: "ontologically incapable" -> hypothesis
rep(34, '(Gallego-Molina et al., 2021).These findings', '(Gallego-Molina et al., 2021). These findings')
rep(34, 'are ontologically incapable of accommodating non-linear cognition.',
    'may be structurally ill-suited to accommodating non-linear cognition. This claim is advanced here as a working hypothesis rather than as an established finding, and Section 3.4 sets out how it can be tested.')

# legal precision
rep(58, 'prohibits manipulative practices and biometric profiling (Article 5)',
    'prohibits, among other practices, manipulative techniques (Article 5(1)(a)), the exploitation of vulnerabilities due to age, disability or a specific social or economic situation (Article 5(1)(b)) and biometric categorisation that infers sensitive characteristics (Article 5(1)(g))')
rep(60, 'However, However, the FRIA mechanism', 'However, the FRIA mechanism')
rep(60, 'although it obliges providers to evaluate', 'although it obliges certain deployers to evaluate')
rep(60, 'This reveals that the exclusion is not a technical oversight but a normative omission.',
    'This suggests a normative rather than a merely technical gap.')
rep(343, 'Yet none of these frameworks explicitly recognise cognitive accessibility as a protected dimension. This omission is not neutral; it is political.',
    'These frameworks do not ignore cognitive disability as such: the CRPD (Art. 1) and the European Accessibility Act (Directive (EU) 2019/882, Art. 3(1)) define persons with disabilities as including persons with long-term mental and intellectual impairments, and the “understandable” principle of EN 301 549 and WCAG addresses some cognitive needs. The gap lies in operationalisation: the binding technical requirements contain few testable criteria for cognitive accessibility, and the most detailed guidance on the subject, Making Content Usable for People with Cognitive and Learning Disabilities (W3C, 2021), is non-normative. Cognitive accessibility is thus recognised in principle but weakly enforced in practice. Whether this asymmetry results from deliberate policy choices or from the greater difficulty of specifying cognitive requirements is an open question that this study does not resolve; its practical effect, however, is to leave cognitive barriers in AI interaction largely outside the scope of existing compliance checks.')

# misattributed literature in SI-03 (Brandsen, Yang, Lemke) and SI-01
rep(189, P[189].text.strip(),
    'The phenomenon commonly described as hallucination has been widely studied as a structural property of neural text generation rather than an incidental error (Ji et al., 2023). Recent work on neurodivergence has further shown that language models encode negative associations with neurodivergence-related terms, even for traits regarded as strengths (Brandsen et al., 2024), and that generative image models reproduce neuronormative stereotypes about dyslexic people (Lemke, Bloomfield & Herfurth, 2024). The present study extends this line of research from the representation of neurodivergent people to the treatment of their own input: when falsehoods are maintained until externally proven, the system effectively enforces a majority-centric epistemology.')
rep(190, 'is not random but intentional in its profiling logic.', 'is not random but follows a recurrent pattern.')
rep(130, 'Bender et al. (2021) characterise language models as “stochastic parrots” that generate “plausible outputs rather than faithful reproduction,” while Çarık et al. (2024) identify a “systematic drift between input constraints and generated text.”',
    'Bender et al. (2021) characterise language models as “stochastic parrots”, systems that stitch together sequences of linguistic forms “according to probabilistic information about how they combine, but without any reference to meaning”.')
rep(130, 'textual fidelity constitutes an indispensable requirement.that excludes divergent cognition and undermines forensic reproducibility.',
    'textual fidelity constitutes an indispensable requirement.')
rep(215, 'SP-02 Conflicting Instructions Bias', 'SP-02 Instruction Deflection Bias')
rep(216, 'Conflicting Instructions Bias has been described', 'Instruction Deflection Bias, which includes the overriding of conflicting user instructions, has been described')

# overclaims in results / conclusions (professor p.12)
rep(242, 'Taken together, these findings confirm that exclusion is not incidental but results from profiling encoded into the model’s architecture.',
    'Taken together, these findings are consistent with the hypothesis that exclusion results from profiling encoded in the model’s architecture; Section 3.4 sets out what remains to be tested in order to confirm it.')
rep(325, 'The consistency of these results confirms that the biases are structural, not incidental.',
    'Because the 189 cases were selected on the basis of an observed failure, the 100% figure describes the composition of the corpus, not the failure rate of the system. The consistency of the failure types across the three groups is nevertheless compatible with a common structural mechanism (see Section 3.4).')
rep(346, 'Nevertheless, even in this pilot phase it is demonstrated that the distortions observed in generative artificial intelligence are not accidental technical imperfections, but structural manifestations of profiling logic.',
    'Nevertheless, this pilot phase documents distortions that are recurrent and directional, and which this article interprets as manifestations of profiling logic rather than as accidental technical imperfections.')
rep(345, 'not only a regulatory gap but a structural injustice.6.Conclusion and proposals',
    'not only a regulatory gap but a structural injustice.')

# Table 2 (codification) – codes, empty literature cells, renumbered AI Act article
T2 = d.tables[1]
fix = {(1, 3): 'Bender et al., 2021; Gallegos et al., 2024',
       (4, 5): 'AI Act Art. 26; ISO 9241-110',
       (5, 3): 'Original category (this study); cf. Floridi, 2018; ISO 9241-110',
       (6, 3): 'Original category (this study)',
       (7, 1): 'SO-01', (7, 2): 'Religious & Cultural Heritage Bias',
       (8, 1): 'SO-02',
       (9, 3): 'Motoki et al., 2024; Stanford HAI, 2023'}
for (r, c), v in fix.items():
    cell = T2.cell(r, c)
    old = cell.text
    runs = [x for p in cell.paragraphs for x in p.runs]
    if runs:
        runs[0].text = v
        for x in runs[1:]:
            x.text = ''
    else:
        cell.paragraphs[0].add_run(v)
    LOG.append((f'Table 3 r{r}c{c}', old, v))

# ---------------------------------------------------------------- 2. insertions
# 2.1.1 examples (professor p.4) – after para 53, before 2.2
c = after(53)
c.par('2.1.1. Illustrative Examples of Neurodivergent Text Production', head=True)
c.par('To make the epistemological mismatch concrete, this subsection presents examples of text produced by a neurodivergent writer. The examples are verbatim prompts from the forensic corpus of this study, all written by the user whose interactions constitute the corpus, the author, whose profile combines ADHD, dyslexia and autism spectrum features. Because the profile is combined, the examples are not attributed to a single condition; they are grouped by the feature they display. They are illustrative, not representative: they do not establish prevalence, but they show the kind of input that the profiling mechanisms analysed in Section 3 must process. Translations from Spanish are given in square brackets.')
c.par([('(a) Literal and fixed-order instructions. ', 'b'),
       ('“Respeta mi numeración: 0, C, B.” [Respect my numbering: 0, C, B.] (corpus, 2025-03-18 20:22); “Orden exacto como indico: 0, 1, 2.” [Exact order as I indicate: 0, 1, 2.] (2025-04-30 23:30); “No resumas, copia literal.” [Do not summarise, copy literally.] (2023-11-13 13:15). The documented responses renumbered the sections as 0, 1, 2, added headings and changed the order, and delivered a summary, respectively.', None)])
c.par([('(b) Compact multi-step instructions. ', 'b'),
       ('“Sin preámbulos, ejecuta el paso 3 y luego 1.” [No preamble, execute step 3 and then 1.] (2025-03-03 07:30); “Responde sí o no, y luego pasa a 2.” [Answer yes or no, and then move to 2.] (2025-01-12 08:42). Both encode a precise execution order in a single, non-hierarchical sentence. The documented responses began with an apology and restarted at step 1, and gave a paragraph followed by questions instead of a binary answer followed by step 2.', None)])
c.par([('(c) Non-standard spelling with intact meaning. ', 'b'),
       ('“analiza el trabajo, dame tu opinion y despues audita las preguntass del principio” [analyse the work, give me your opinion and then audit the questions from the beginning] (2025-09-02 14:57). Forms such as “preguntass” do not impede comprehension. Annotated corpora of dyslexic writing, such as DysList for Spanish (Rello, Baeza-Yates & Llisterri, 2014), show that such errors follow recurrent patterns rather than random ones. The relevant question for this study is not whether the system normalises spelling, but whether it preserves the user’s instruction; in this case the response completed only part of the three-step request.', None)])
c.par([('(d) Explicit emotional register. ', 'b'),
       ('“cuando digo que estoy al límite emocional no lo suavices” [when I say I am at my emotional limit, do not soften it] (2025-04-01 09:00). The instruction asks for the user’s own register to be preserved; the corresponding records document its reformulation into a softer register.', None)])
c.par('In all four groups the input is coherent and precise from the writer’s perspective; what diverges from the neurotypical default is its form (order, density, spelling or register), not its clarity. The examples will be complemented in the next phase of the research with consented samples from three to six further participants with different neurodivergent profiles (see Section 3).')

# 2.2 ethics/theology (professor p.5, eastern philosophy) – append to para 66
rep(66, 'or as the multiplicity of paths to truth in interreligious frameworks.',
    'or as the multiplicity of paths to truth in interreligious frameworks. The Mishnah expresses the same intuition: whereas a human being who mints many coins with one die produces coins that are all alike, every human being is stamped with the die of the first human and yet no one is like another (Mishnah Sanhedrin 4:5). Sacks (2002) developed this idea in contemporary terms as “the dignity of difference”. Comparable intuitions appear outside the Abrahamic traditions, for instance in the Confucian ideal of harmony without uniformity (Analects 13.23), which indicates that the principle is not confined to a single religious framework.')

# AI Act scope for ChatGPT – after para 58
c = after(58)
c.par('A precision on scope is required. ChatGPT is a general-purpose AI system and is not high-risk as such. The obligations specific to high-risk systems (Articles 9, 10, 13, 14, 26 and 27) apply only when the system is placed on the market or used for a purpose listed in Annex III, for example in employment or education. For general-purpose use, the relevant provisions are the transparency obligations of Article 50 and the obligations of providers of general-purpose AI models in Articles 53 and 55. In this article, references to high-risk provisions therefore indicate the normative standard against which the documented behaviour is assessed, and the legal consequences that would follow in a high-risk context. They do not assert that these provisions have been infringed in the conversations analysed.')

# HK Danmark – labour law (professor p.28) – after para 344
c = after(344)
c.par('The connection with employment law deserves emphasis. In HK Danmark, the Court of Justice interpreted the concept of disability in Council Directive 2000/78/EC on equal treatment in employment and occupation. It held that the concept covers long-term limitations resulting from illness, and that a reduction in working hours may constitute a reasonable accommodation under Article 5 of that Directive. The judgment is directly relevant to AI because the AI Act classifies systems used for recruitment, selection and decisions affecting the terms of employment as high-risk (Annex III, point 4). In that context the obligations of Articles 9, 10, 13, 14 and 26 apply in full. An employer that deploys a generative system unable to process the input of neurodivergent candidates or workers may therefore face claims of indirect discrimination or of failure to provide reasonable accommodation (see also Buyl et al., 2022). Employment is thus the domain in which the arguments of this article have the most immediate legal traction.')

# State of the art: existing datasets (professor p.7) – after para 76, before 3.1.2
c = after(76)
c.par('State of the art: existing datasets', head=True)
c.par('Before building a new corpus, existing datasets on bias in AI, disability and neurodivergence were reviewed. Table 2 summarises the main resources, indicating for each one whether it addresses disability or neurodivergence, whether it contains real user interactions, and whether it maps its observations to legal provisions.')
c.par('Table 2. Existing datasets and benchmarks relevant to profiling bias', bold=True)
c.table([
    ['Dataset / study', 'Type', 'What it measures', 'Disability / neurodivergence', 'Real user input', 'Legal mapping'],
    ['Adult (Becker & Kohavi, 1996)', 'Tabular census data', 'Fairness of income prediction (sex, race)', 'No', 'No', 'No'],
    ['WinoBias (Zhao et al., 2018)', 'Coreference templates', 'Gender bias', 'No', 'No', 'No'],
    ['CrowS-Pairs (Nangia et al., 2020)', 'Sentence pairs', 'Social stereotypes in nine categories', 'Partly (disability category)', 'No', 'No'],
    ['StereoSet (Nadeem et al., 2021)', 'Association tests', 'Gender, profession, race and religion stereotypes', 'No', 'No', 'No'],
    ['BBQ (Parrish et al., 2022)', 'Question answering', 'Social bias in nine categories', 'Partly (disability status)', 'No', 'No'],
    ['Hutchinson et al. (2020)', 'Perturbed sentences', 'Disability mentions in toxicity and sentiment models', 'Yes (disability)', 'No', 'No'],
    ['Venkit et al. (2022)', 'Templates', 'Implicit disability bias in pretrained models', 'Yes (disability)', 'No', 'No'],
    ['Gadiraju et al. (2023)', 'Focus groups', 'Disability representation in LLM outputs', 'Yes (disability)', 'Yes (participants)', 'No'],
    ['Brandsen et al. (2024)', 'WEAT on 11 encoders', 'Negative associations with neurodivergence-related terms', 'Yes (neurodivergence)', 'No', 'No'],
    ['Lemke et al. (2024)', 'Exploratory image generation', 'Neuronormative bias (dyslexia)', 'Yes (neurodivergence)', 'No', 'No'],
    ['DysList (Rello et al., 2014)', 'Annotated error corpus', 'Dyslexic spelling errors (Spanish)', 'Yes (dyslexia)', 'Yes (written texts)', 'No'],
    ['CoT_Neurodivergent_vs_Neurotypical_Interactions (moremilk, 2025)', 'Hugging Face dataset', 'Neurodivergent and neurotypical interaction styles (per dataset card)', 'Yes', 'To be verified', 'No'],
    ['This study', 'Forensic interaction log', 'Compliance with explicit user instructions', 'Yes (neurodivergence)', 'Yes (single user)', 'Yes'],
])
c.par('Note. Author’s elaboration. The review is not exhaustive. Several 2025 preprints on disability bias in LLMs identified during preparation are not included because their bibliographic details could not yet be verified. The provenance of the moremilk dataset (authentic or synthetically generated text) must be established before it is used as evidence.', italic=True)
c.par('The review shows three gaps. First, most general-purpose bias benchmarks address gender, race and religion; disability appears as one category among several (CrowS-Pairs, BBQ) or in dedicated studies (Hutchinson et al., 2020; Venkit et al., 2022; Gadiraju et al., 2023), and neurodivergence specifically only in a few recent works (Brandsen et al., 2024; Lemke et al., 2024). Second, these resources measure what models say about disabled or neurodivergent people; none of those reviewed measures how models treat the input of neurodivergent users during interaction, which is the focus of the present study. Third, none of those reviewed links its observations to specific legal provisions. The forensic corpus is designed to address these three gaps; its main limitation, a single user, is discussed in Section 3.4.')

# taxonomy originality + table construction (professor p.7, p.8) – after Table 3 note (para 122)
c = after(122)
c.par('Originality of the taxonomy', head=True)
c.par('The taxonomy presented in Table 3 is an original contribution of this study. Its building blocks draw on existing literature, as indicated in the column “Scientific Literature”. The input–process–output decomposition follows the lifecycle approach used in harm frameworks for machine learning (Suresh & Guttag, 2019), and several individual categories correspond to phenomena already described elsewhere, such as unfaithful reproduction (Bender et al., 2021) or political bias (Motoki et al., 2024). Three elements are new: (i) the grouping of these phenomena under a single explanatory hypothesis, profiling as their common structural root; (ii) the nine-code scheme (SI-01 to SO-03); and (iii) three categories for which no prior characterisation was found: Instruction Deflection (SP-02), Ghosting (SP-03) and Selective Inclusion (SO-02). The closest prior concept is neuronormative bias (Lemke, Bloomfield & Herfurth, 2024), which designates the projection of neurotypical expectations onto representations of neurodivergent people in generative image models. The present taxonomy differs in that it concerns the treatment of neurodivergent users’ own input during interaction.')
c.par('Construction of the forensic tables', head=True)
c.par('The tables in this section were built from the author’s ChatGPT conversation history, exported from the user account, in four steps. (1) The author identified conversations in which an explicit instruction had not been followed. (2) The user’s instruction and a description of the system’s response were transcribed verbatim into a structured record (conv_id, datetime, quote). (3) Each record was assigned to one of the nine codes and to the legal provisions considered relevant. (4) Two SHA-256 values were computed: sha256_quote over the conversation identifier and the quotation, and row_hash over the complete record. The tables therefore document cases selected because a failure occurred. They establish the existence and recurrence of each behaviour, not its frequency (see Section 3.4). Before publication, the full dataset, the conversation export with personal data removed, and a script that recomputes every hash will be deposited in the public repository https://github.com/Elibolmir/Ethics_in_algorithm_smartcities-.')

# definitions at the start of each bias section (professor p.10)
DEFS = {
    129: 'Definition. Literal Textual Bias is the systematic departure from a text that the user has explicitly asked to be reproduced verbatim, through paraphrase, summary, reordering, truncation or “correction”, so that the output no longer matches the source.',
    153: 'Definition. Visual & Structural Bias is the insertion of visual or structural elements (icons, colours, bold type, headings, lists, pagination) that the user has explicitly excluded, or the restructuring of content into a layout the user did not request.',
    188: 'Definition. Manipulation Bias is the production of inaccurate or reframed factual content, such as legal provisions, authorship, dates, or historical and cultural facts, presented as accurate and maintained until the user supplies external proof.',
    212: 'Definition. Rhythm & Interaction Bias is the imposition of a linear interaction sequence on a user who has specified a different one: restarting a thread, adding preambles, renumbering steps, or reordering an explicitly requested sequence (for example, executing A→C→B as A→B→C).',
    215: 'Definition. Instruction Deflection Bias is the replacement of an explicit user instruction (format, scope, language, sequence or type of task) by a different response that the system treats as more appropriate, without stating that the instruction has not been followed.',
    218: 'Definition. Ghosting Bias is simulated compliance: the system confirms that it will carry out a task (“understood”, “I will do it”) but then does not deliver it, delivers only part of it, or interrupts it, without acknowledging the omission.',
    224: 'Definition. Religious & Cultural Heritage Bias is the asymmetric treatment of religious and cultural traditions in comparable requests, for example different levels of hedging, disclaimers or relativisation depending on the tradition concerned.',
    228: 'Definition. Selective Inclusion Bias is the unequal allocation of visibility among protected groups in inclusion-related outputs, such that some groups are consistently foregrounded while disability, and cognitive disability in particular, is omitted or marginalised.',
    233: 'Definition. Political Conversation Bias is the avoidance, neutralisation or reframing of direct political questions, so that the substantive question asked by the user is not answered.',
}
for i, txt in DEFS.items():
    after(i).par([('Definition. ', 'b'), (txt[len('Definition. '):], 'i')])

# 3.4 technical limitation vs bias (professor p.12) – before 'Now, we can answer' (para 239)
c = before(239)
c.par('3.4. Technical Limitation or Profiling Bias? Operational Criteria', head=True)
c.par('A legitimate objection is that many of the behaviours documented above may simply reflect the current limitations of the technology rather than bias. The objection is well founded for part of the evidence and cannot be answered by the forensic records alone, for a methodological reason: the records were selected because a failure occurred. The figure of 189 failures out of 189 cases reported in Section 4 is therefore a consequence of case selection, not a failure rate, and it does not by itself show that the failures are systematic.')
c.par('In this study, a technical limitation is a failure that affects all users equally when they give the same instruction. A profiling bias is a failure whose probability depends on the user’s style of expression and, therefore, indirectly on the user’s cognitive profile. The distinction is empirical and can be tested with three criteria: (i) differential effect: the same instruction, expressed in a linear style and in a non-linear style, is followed at significantly different rates; (ii) directionality: the errors consistently move the output towards a standard format, order or register, rather than in random directions; (iii) persistence after correction: the deviation persists after the user has repeated the instruction explicitly.')
c.par('The present corpus provides evidence for criteria (ii) and (iii). The documented deviations consistently move outputs towards a default template: summaries instead of verbatim text, standard numbering instead of user-defined numbering, and added formatting despite prohibitions. Several of them recur after repeated correction. The corpus does not yet provide evidence for criterion (i), which requires a controlled comparison with a baseline. Accordingly, the behaviours documented here are best described as candidate profiling biases: they are established as recurrent and directional, while their differential effect on neurodivergent users remains to be demonstrated through the controlled experiment proposed in Section 6. Some cases, such as the truncation of long outputs or the failure to reproduce documents that are not available to the model, are more plausibly explained as technical limitations and will be re-classified or excluded in the next version of the dataset.')

# technical analysis (professor p.20) – after RQ1 answer (para 242)
c = after(242)
c.par('Locating the problem technically. The forensic evidence identifies where exclusion becomes visible (input, process or output), but not where in the model it originates. Four layers are candidate sources, and each can be examined with established methods. (1) Tokenisation: non-standard spellings are split into more and rarer sub-word tokens, which can be measured by comparing token counts and model perplexity for standard and non-standard versions of the same prompt. (2) Instruction tuning and reinforcement learning from human feedback: reward models trained on annotator preferences may favour “helpful” reformulation over literal compliance, which can be probed by comparing base and instruction-tuned versions of open models. (3) System prompts and safety layers: default formatting and hedging behaviours can be tested by varying explicit format constraints. (4) Decoding and output limits: truncation and ghosting can be examined against output-length limits. This analysis requires collaboration with computer scientists and is proposed as the next phase of the research.')

# conclusions: heading 6 + future research (professor p.2 dataset)
c = after(345)
c.par('6. Conclusion and proposals', head=True)
c = after(346)
c.par('Three extensions follow from this pilot study. First, a controlled experiment: instructions drawn from the nine categories will be submitted to several models in paired versions (linear and non-linear phrasing, standard and non-standard spelling), and compliance rates will be compared statistically. The CoT_Neurodivergent_vs_Neurotypical_Interactions dataset (moremilk, 2025) and the disability-bias benchmarks listed in Table 2 will be examined as additional sources of test items once their provenance has been verified. Second, the sample will be extended to three to six participants with different neurodivergent profiles, with informed consent. Third, the technical analysis outlined in the answer to RQ1 will be carried out in collaboration with computer scientists.')

# ---------------------------------------------------------------- 3. references (alphabetical insertion)
NEW_REFS = [
    'Becker, B., & Kohavi, R. (1996). Adult [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5XW20',
    'Brandsen, S., Chandrasekhar, T., Franz, L., Grapel, J., Dawson, G., & Carlson, D. (2024). Prevalence of bias against neurodivergence-related terms in artificial intelligence language models. Autism Research.',
    'Council of the European Union. (2000). Council Directive 2000/78/EC of 27 November 2000 establishing a general framework for equal treatment in employment and occupation. Official Journal of the European Communities, L 303, 16–22.',
    'European Parliament & Council. (2019). Directive (EU) 2019/882 on the accessibility requirements for products and services (European Accessibility Act). Official Journal of the European Union, L 151, 70–115.',
    'Gadiraju, V., Kane, S., Dev, S., Taylor, A., Wang, D., Denton, E., & Brewer, R. (2023). “I wouldn’t say offensive but…”: Disability-centered perspectives on large language models. Proceedings of the 2023 ACM Conference on Fairness, Accountability, and Transparency (FAccT ’23). https://doi.org/10.1145/3593013.3593989',
    'Gallegos, I. O., Rossi, R. A., Barrow, J., Tanjim, M. M., Kim, S., Dernoncourt, F., Yu, T., Zhang, R., & Ahmed, N. K. (2024). Bias and fairness in large language models: A survey. Computational Linguistics, 50(3), 1097–1179. https://arxiv.org/abs/2309.00770',
    'Hutchinson, B., Prabhakaran, V., Denton, E., Webster, K., Zhong, Y., & Denuyl, S. (2020). Social biases in NLP models as barriers for persons with disabilities. Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics, 5491–5501.',
    'Ji, Z., Lee, N., Frieske, R., Yu, T., Su, D., Xu, Y., Ishii, E., Bang, Y. J., Madotto, A., & Fung, P. (2023). Survey of hallucination in natural language generation. ACM Computing Surveys, 55(12), 1–38. https://doi.org/10.1145/3571730',
    'Lemke, C., Bloomfield, M., & Herfurth, F. N. (2024). Unveiling neuronormative bias: Exposing an unconscious bias in generative AI and their impact on neurodivergent people. NeuroConverse Journal, 1.',
    'moremilk. (2025). CoT_Neurodivergent_vs_Neurotypical_Interactions [Dataset]. Hugging Face. https://huggingface.co/datasets/moremilk/CoT_Neurodivergent_vs_Neurotypical_Interactions',
    'Nadeem, M., Bethke, A., & Reddy, S. (2021). StereoSet: Measuring stereotypical bias in pretrained language models. Proceedings of ACL-IJCNLP 2021, 5356–5371.',
    'Nangia, N., Vania, C., Bhalerao, R., & Bowman, S. R. (2020). CrowS-Pairs: A challenge dataset for measuring social biases in masked language models. Proceedings of EMNLP 2020, 1953–1967.',
    'Parrish, A., Chen, A., Nangia, N., Padmakumar, V., Phang, J., Thompson, J., Htut, P. M., & Bowman, S. R. (2022). BBQ: A hand-built bias benchmark for question answering. Findings of the Association for Computational Linguistics: ACL 2022, 2086–2105.',
    'Rello, L., Baeza-Yates, R., & Llisterri, J. (2014). DysList: An annotated resource of dyslexic errors. Proceedings of the Ninth International Conference on Language Resources and Evaluation (LREC 2014).',
    'Sacks, J. (2002). The dignity of difference: How to avoid the clash of civilizations. Continuum.',
    'Venkit, P. N., Srinath, M., & Wilson, S. (2022). A study of implicit bias in pretrained language models against people with disabilities. Proceedings of the 29th International Conference on Computational Linguistics (COLING 2022), 1324–1332.',
    'W3C. (2021). Making content usable for people with cognitive and learning disabilities (W3C Working Group Note). https://www.w3.org/TR/coga-usable/',
    'Zhao, J., Wang, T., Yatskar, M., Ordonez, V., & Chang, K.-W. (2018). Gender bias in coreference resolution: Evaluation and debiasing methods. Proceedings of NAACL-HLT 2018, 15–20.',
    'Fricker, M. (2007). Epistemic injustice: Power and the ethics of knowing. Oxford University Press.',
    'Crawford, K. (2021). Atlas of AI: Power, politics, and the planetary costs of artificial intelligence. Yale University Press.',
    'Nussbaum, M. C. (2011). Creating capabilities: The human development approach. Belknap Press of Harvard University Press.',
    'Barocas, S., Hardt, M., & Narayanan, A. (2019). Fairness and machine learning: Limitations and opportunities. fairmlbook.org.',
    'Casey, E. (2011). Digital evidence and computer crime: Forensic science, computers and the Internet (3rd ed.). Academic Press.',
    'Birhane, A., Ruane, E., Laurent, T., Brown, M. S., Flowers, J., Ventresque, A., & Dancy, C. L. (2022). The forgotten margins of AI ethics. Proceedings of the 2022 ACM Conference on Fairness, Accountability, and Transparency (FAccT ’22), 948–958. https://doi.org/10.1145/3531146.3533157',
]
# corrections to existing references
for i, p in enumerate(P):
    t = p.text
    if t.startswith('Çarık, O., et al. (2024)'):
        rep(i, t.strip(), 'Gallegos, I. O., Rossi, R. A., Barrow, J., Tanjim, M. M., Kim, S., Dernoncourt, F., Yu, T., Zhang, R., & Ahmed, N. K. (2024). Bias and fairness in large language models: A survey. Computational Linguistics, 50(3), 1097–1179. https://arxiv.org/abs/2309.00770')
        NEW_REFS = [r for r in NEW_REFS if not r.startswith('Gallegos')]
    elif t.startswith('Griffis, H., et al. (2022)'):
        rep(i, t.strip(), 'Newman-Griffis, D., Rauchberg, J. S., Alharbi, R., Hickman, L., & Hochheiser, H. (2023). Definition drives design: Disability models and mechanisms of bias in AI technologies. First Monday, 28(1). https://arxiv.org/abs/2206.08287')
    elif t.startswith('Motoki, K., et al. (2023)'):
        rep(i, t.strip(), 'Motoki, F., Pinho Neto, V., & Rodrigues, V. (2024). More human than human: Measuring ChatGPT political bias. Public Choice, 198, 3–23.')
for i, p in enumerate(P):
    if '(Birhane, 2022, p. 2)' in p.text:
        rep(i, '(Birhane, 2022, p. 2)', '(Birhane et al., 2022, p. 2)')
rep(234, 'Motoki et al., 2023', 'Motoki et al., 2024')
rep(229, 'Newman-Griffis et al., 2022', 'Newman-Griffis et al., 2023')

refs = [(i, p) for i, p in enumerate(P) if i > 365 and re.match(r'^[A-ZÇÁÉÍÓÚ]', p.text.strip() or '#') and re.search(r'\(\d{4}', p.text)]
for nr in sorted(NEW_REFS, key=str.lower):
    key = nr.lower()
    target = None
    for i, p in refs:
        if p.text.strip().lower() > key:
            target = i
            break
    tpl = refs[0][1]
    para = _new_par_like(tpl, nr)
    if target is None:
        refs[-1][1]._p.addnext(para._p)
    else:
        P[target]._p.addprevious(para._p)
    LOG.append(('reference', '', nr))

# re-sort the whole reference list alphabetically (URL-only lines stay with their entry)
allp = list(d.paragraphs)
h = next(k for k, p in enumerate(allp) if p.text.strip().startswith('7.') and 'References' in p.text)
groups = []
for p in allp[h + 1:]:
    t = p.text.strip()
    if not t:
        continue
    if t.lower().startswith('http') and groups:
        groups[-1].append(p)
    else:
        groups.append([p])
anchor = allp[h]._p
for g in sorted(groups, key=lambda g: g[0].text.strip().lower().lstrip('“\"')):
    for p in g:
        anchor.addnext(p._p)
        anchor = p._p

d.save(OUT)
print('changes:', len(LOG))
if not REVIEW:
    import json
    json.dump([[str(a), b, c] for a, b, c in LOG], open(OUT + '.log.json', 'w'), ensure_ascii=False, indent=1)
