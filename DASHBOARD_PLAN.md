# Dashboard Plan: Dudley Employment Barriers

## Purpose and Research Question

The dashboard explores how health limitations, formal qualifications and household vehicle availability relate to selected economic inactivity across 199 included Dudley neighbourhoods.

The project asks:

> To what extent do localized structural barriers—specifically health limitations, qualification deficits, and transport poverty—drive economic inactivity across Dudley’s 199 neighbourhoods?

The dashboard examines associations relevant to this question. The available data cannot establish whether these factors cause economic inactivity or determine an individual resident’s circumstances.

Ethical considerations shape both the presentation and interpretation of the evidence. The dashboard encourages readers to consider the circumstances surrounding economic inactivity without treating disability, caring responsibilities, qualifications or vehicle ownership as measures of personal effort or worth.

## Intended Audience

The dashboard is intended for readers interested in Dudley’s employment context, including residents, community organisations and people exploring local support needs.

Readers without a statistical background can use the summary cards, chart labels and explanatory notes to understand the main patterns. Readers seeking more detail can inspect correlation results, adjusted p-values, measure definitions and downloadable supporting information.

The dashboard supports further investigation and discussion. It does not identify which individuals need support or provide sufficient evidence to allocate services between neighbourhoods.

## Reader Journey

The four tabs guide readers through four questions:

1. **Overview:** How does selected economic inactivity vary across the included neighbourhoods?
2. **Explore Areas:** How do particular neighbourhoods compare within the wider pattern?
3. **Hypothesis Results:** What did the three statistical tests find, and how should those findings be interpreted?
4. **Sources & Ethics:** Where does the evidence come from, how were the measures constructed, and what are their limitations?

Definitions and interpretation notes also appear alongside the relevant charts. Responsible interpretation should not depend on readers visiting the final tab.

## Shared Dashboard Information

The dashboard introduces the three investigated measures and identifies the coverage as 199 neighbourhoods using Census 2021 data.

Summary cards display:

- Number of included neighbourhoods.
- Mean selected inactivity percentage.
- Lowest included area percentage.
- Highest included area percentage.

These cards provide a quick sense of coverage and variation. The mean gives each neighbourhood equal weight; it is not a pooled percentage for Dudley’s population. The accompanying note makes that distinction explicit.

An expandable definition explains that selected inactivity combines home or family responsibilities, long-term sickness or disability, and other inactivity. Retirement and inactive students are excluded from the numerator, while the denominator includes all residents aged 16 and over.

This definition prevents readers from mistaking the measure for total economic inactivity or working-age inactivity.

## Tab 1: Overview

### What this tab aims to show

The Overview introduces the spread of selected inactivity, the categories contributing to it, and the relationships between the four main measures.

### Visuals and their purpose

**Distribution histogram**

The histogram shows how many neighbourhoods fall within different selected inactivity percentage ranges. A median reference line helps readers locate the centre of the distribution.

This chart shows whether values are concentrated within a narrow range or spread across different levels. It also provides context for unusually high or low observations without immediately labelling particular neighbourhoods.

**Composition doughnut chart**

The doughnut chart shows the contributions of home or family responsibilities, long-term sickness or disability, and other inactivity to the selected inactive population across the included areas.

The accompanying explanation distinguishes these shares from percentages of the whole population.

**Spearman correlation heatmap**

The heatmap summarises the direction and strength of relationships between selected inactivity, health limitations, no formal qualifications and household vehicle absence.

It provides an initial view of the relationships explored in more detail in the Hypothesis Results tab.

### Ethical considerations shaping the design

The Overview presents variation without dividing neighbourhoods into “good” and “bad” categories. The composition chart also makes clear that selected inactivity includes different circumstances rather than one uniform experience.

The heatmap is accompanied by interpretation notes because correlation strength can easily be mistaken for causal importance. Health limitations overlap conceptually with the sickness component of selected inactivity, while household vehicle availability does not directly measure public transport access.

## Tab 2: Explore Areas

### What this tab aims to show

Explore Areas lets readers examine individual neighbourhoods while keeping the wider pattern across all included areas visible.

### Visuals and interactions

**Measure selector and scatter plot**

Readers choose a measure to compare with selected inactivity. Each point represents one included neighbourhood.

The scatter plot shows the spread of observations, including variation between areas with similar values. This helps readers see that a strong overall association does not mean every neighbourhood follows the same pattern.

**Neighbourhood highlighting**

Readers can highlight up to six neighbourhoods. The remaining areas stay visible to preserve context.

Highlighting changes visual emphasis only. It does not change the dataset used for the saved hypothesis tests.

**Comparison bar chart**

A separate measure selector allows readers to compare the chosen neighbourhoods using horizontal bars. A reference line shows the mean across the included areas.

The mean is a descriptive reference point, not a target or a threshold for deciding whether an area needs intervention.

**Table and download**

A table provides the selected neighbourhoods’ values and area codes. Readers can download the chosen neighbourhood data for closer inspection.

### Ethical considerations shaping the design

Neighbourhood selection is controlled by the reader rather than presented as a predetermined list of places requiring attention. Keeping all areas visible reduces the risk of interpreting a small selection without context.

The comparison features describe area-level statistics. They do not identify individual residents, explain why a particular person is economically inactive, or rank communities by their value or potential.

Vehicle availability is labelled at household level so readers do not mistake it for a personal measure of transport access.

## Tab 3: Hypothesis Results

### What this tab aims to show

This tab presents the three completed tests and explains how they contribute to the project question.

The hypotheses ask:

1. **Health limitations:** Do areas with more residents whose activities are limited a lot have higher selected inactivity?
2. **No formal qualifications:** Do areas with more residents without formal qualifications have higher selected inactivity?
3. **No car or van:** Do areas with more households without a car or van have higher selected inactivity?

### Visuals and supporting information

**Correlation comparison chart**

A dot-and-line chart places the three Spearman correlation coefficients on the same scale from −1 to +1.

Using a shared scale allows readers to compare the reported associations. The accompanying note explains that differences between the correlations have not been formally tested and do not establish which factor has the greatest causal influence.

**Individual hypothesis panels**

Each hypothesis has:

- A scatter plot showing the neighbourhood observations.
- The Spearman correlation coefficient.
- The Holm-adjusted p-value and number of included areas.
- A plain-language interpretation.
- A measure-specific explanation of limitations.

Readers can inspect the scatter plots alongside the numerical results rather than relying on statistical significance alone.

**Detailed results and download**

An expandable section provides access to the detailed saved results and a download for readers who want to examine the statistical output.

### Ethical considerations shaping the design

Each result is paired with a caution relevant to that measure:

- **Health limitations:** The predictor overlaps conceptually with long-term sickness or disability within the outcome. The association is not an independent estimate of a health effect.
- **No formal qualifications:** Absence of formal qualifications does not mean absence of skills, experience or ability.
- **No car or van:** Vehicle absence does not directly establish poor public transport, unaffordable travel or a transport barrier to employment.

The results describe neighbourhood associations, not individual employability. The tests do not control for age structure or other possible confounders.

P-values are presented as approximate and exploratory. Neighbouring areas may share characteristics, and Holm adjustment addresses multiple testing without resolving spatial dependence or confounding.

## Tab 4: Sources & Ethics

### What this tab aims to show

Sources & Ethics gives readers the information needed to assess where the evidence came from, what the measures mean and how responsibly they can be used.

### Content and supporting features

**Project question and analytical scope**

The research question is displayed alongside an explanation that the analysis examines associations and cannot establish causation.

**Measures and denominators**

A table identifies the numerator and denominator for each main measure.

This makes differences between resident-based and household-based percentages visible. It also explains why totals from separate Census tables should not be assumed to be interchangeable.

**Data sources**

The tab identifies the Census 2021 sources accessed through Nomis and the English Indices of Deprivation 2019 used in the project.

Source attribution allows readers to trace the evidence and distinguishes the project’s analysis from the original data providers’ work.

**Coverage and limitations**

The coverage notes explain why the combined dataset contains 199 matched neighbourhoods and identify the excluded areas.

The reference years are stated so historical statistics are not presented as a description of current conditions.

**Responsible interpretation**

The guidance explains that:

- Area-level patterns must not be attributed to individual residents.
- Disability does not imply unwillingness to work.
- Caring responsibilities should not be described as personal failure.
- No formal qualifications does not mean no skills.
- Household vehicle absence is an incomplete indicator of transport circumstances.
- Findings support further investigation and inclusive planning.

**Data dictionaries and project information**

Downloads explain the prepared dataset and the selected inactivity measures. An expandable section explains how the dashboard uses the project files.

### Ethical, legal and social considerations shaping the design

The dashboard presents aggregated neighbourhood statistics and avoids identifying individual residents. Source and licence acknowledgements make the origin of the material visible without implying endorsement by the data providers.

Definitions, exclusions and limitations are accessible within the dashboard so readers can assess the evidence before reusing it.

The wording recognises that neighbourhoods contain people with different experiences. Findings should support informed discussion with communities rather than labels attached to them.

## Visual Style and Communication

The dashboard uses a consistent plum, mauve and teal palette with a light background. Colour distinguishes measures and highlighted observations without using a red–green scale to judge neighbourhoods.

Chart titles explain the question being explored, and axis labels identify the measures and percentage units. Supporting text explains statistical terms and the meaning of reference lines.

Tables, numerical results and explanatory text complement the charts. This gives readers additional ways to inspect the evidence rather than relying entirely on colour or visual position.

Accessibility remains an area for further checking. Colour contrast, keyboard navigation, screen-reader behaviour and readability on smaller screens should be assessed before claiming that the dashboard is fully accessible.

## Future Development

Further development should improve both usability and the quality of interpretation:

- Gather feedback from readers with different levels of statistical knowledge to check whether definitions and limitations are understood.
- Review accessibility and mobile layouts, including whether chart labels and interpretation notes remain readable.
- Explore additional transport evidence before drawing stronger conclusions about transport barriers.
- Consider methods that account for spatial dependence and relevant confounding factors.
- Assess updated data for compatibility before incorporating it, documenting any changes in boundaries, definitions or coverage.

Any expansion should preserve the distinction between neighbourhood evidence and individual circumstances. Additional features should help readers understand the data without creating unsupported rankings, predictions or claims about residents.
