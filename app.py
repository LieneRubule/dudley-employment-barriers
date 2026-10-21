"""Explore Dudley employment barriers with careful interpretation."""

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Dudley | Employment Barriers",
    layout="wide",
)

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "cleaned_datasets" / "dudley_combined_prepared.csv"
RESULTS_PATH = (
    ROOT / "outputs" / "hypothesis_testing" / "spearman_hypothesis_results.csv"
)

PLUM = "#57384F"
MAUVE = "#A57790"
TEAL = "#397C7A"
IVORY = "#FAF7F3"
INK = "#302832"

OUTCOME = "Selected_Inactive_Pct"

COMPONENTS = [
    "Inactive_Home_Or_Family",
    "Inactive_Long_Term_Sick_Or_Disabled",
    "Inactive_Other",
]

COMPONENT_NAMES = [
    "Home or family responsibilities",
    "Long-term sickness or disability",
    "Other inactivity",
]

BARRIERS = {
    "Health limitations": "Limited_A_Lot_16_Plus_Pct",
    "No formal qualifications": "No_Qualifications_Pct",
    "No car or van": "No_Car_Van_Households_Pct",
}

LABELS = {
    OUTCOME: "Selected inactivity (%)",
    "Limited_A_Lot_16_Plus_Pct": "Activities limited a lot (%)",
    "No_Qualifications_Pct": "No formal qualifications (%)",
    "No_Car_Van_Households_Pct": "Households without a vehicle (%)",
    "LSOA_Name": "Neighbourhood",
    "LSOA_Code": "Area code",
}

MEASURES = [OUTCOME] + list(BARRIERS.values())

HYPOTHESES = [
    {
        "id": "H1",
        "title": "Health limitations",
        "column": BARRIERS["Health limitations"],
        "colour": PLUM,
        "question": (
            "Do areas with more residents whose activities are "
            "limited a lot have higher selected inactivity?"
        ),
        "limitation": (
            "Health limitations overlap conceptually with the "
            "long-term sickness component of selected inactivity. "
            "The relationship is not an independent causal effect."
        ),
    },
    {
        "id": "H2",
        "title": "No formal qualifications",
        "column": BARRIERS["No formal qualifications"],
        "colour": MAUVE,
        "question": (
            "Do areas with more residents without formal "
            "qualifications have higher selected inactivity?"
        ),
        "limitation": (
            "No formal qualifications does not mean no skills. "
            "Age structure and other unmeasured characteristics "
            "may contribute to this relationship."
        ),
    },
    {
        "id": "H3",
        "title": "No car or van",
        "column": BARRIERS["No car or van"],
        "colour": TEAL,
        "question": (
            "Do areas with more households without a car or van "
            "have higher selected inactivity?"
        ),
        "limitation": (
            "Vehicle availability is measured for households. "
            "It does not directly measure public transport access, "
            "travel costs or whether transport prevents employment."
        ),
    },
]


# Apply a consistent theme without adding decorative icons.
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FAF7F3;
        color: #302832;
    }
    .block-container {
        max-width: 1420px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    h1, h2, h3 {
        color: #57384F;
    }
    .hero {
        background: #57384F;
        padding: 28px 32px;
        border-radius: 16px;
        margin-bottom: 24px;
    }
    .hero h1 {
        color: white;
        margin: 8px 0 12px;
        font-size: 2.4rem;
    }
    .hero p {
        color: #F3EAF0;
        margin-bottom: 0;
    }
    .eyebrow {
        color: #EADCE5;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 0.8rem;
    }
    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #E5DCE2;
        border-top: 4px solid #A57790;
        border-radius: 10px;
        padding: 16px;
    }
    [data-testid="stMetricValue"] {
        color: #57384F;
        font-size: 2rem;
    }
    button[data-baseweb="tab"] {
        color: #57384F;
        font-size: 1rem;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background: #EEE3EA;
        border-radius: 6px 6px 0 0;
    }
    [data-baseweb="tab-highlight"] {
        background-color: #57384F;
    }
    [data-testid="stCaptionContainer"] {
        color: #665C65;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def load_data():
    """Validate inputs and calculate selected inactivity."""
    data = pd.read_csv(DATA_PATH)
    required = (
        [
            "LSOA_Code",
            "LSOA_Name",
            "Economic_Total_16_Plus",
        ]
        + COMPONENTS
        + list(BARRIERS.values())
    )

    missing = sorted(set(required) - set(data.columns))
    if missing:
        raise ValueError("Missing columns: " + ", ".join(missing))

    if data.empty:
        raise ValueError("The prepared dataset is empty.")

    if data[required].isna().any().any():
        raise ValueError("Required dashboard fields contain missing data.")

    if data["LSOA_Code"].duplicated().any():
        raise ValueError("The dataset contains duplicate area codes.")

    numeric = required[2:]
    data[numeric] = data[numeric].apply(
        pd.to_numeric,
        errors="raise",
    )

    if not np.isfinite(data[numeric].to_numpy()).all():
        raise ValueError("Numeric fields contain invalid values.")

    if (data["Economic_Total_16_Plus"] <= 0).any():
        raise ValueError("Economic population totals must be positive.")

    if (data[COMPONENTS] < 0).any().any():
        raise ValueError("Inactivity counts cannot be negative.")

    # Match notebook 08: three selected categories over the TS066 total.
    # This is not a measure of all economically inactive residents.
    data["Selected_Inactive_Count"] = data[COMPONENTS].sum(axis=1)
    data[OUTCOME] = (
        data["Selected_Inactive_Count"] / data["Economic_Total_16_Plus"] * 100
    )

    invalid = (data[MEASURES] < 0) | (data[MEASURES] > 100)
    if invalid.any().any():
        raise ValueError("Dashboard percentages must fall within 0–100.")

    return data.sort_values("LSOA_Name").reset_index(drop=True)


def show_chart(figure, height=400):
    """Use the same formatting for every interactive chart."""
    # Reference: Streamlit chart display and configuration.
    # https://docs.streamlit.io/develop/api-reference/charts
    figure.update_layout(
        template="plotly_white",
        paper_bgcolor=IVORY,
        plot_bgcolor=IVORY,
        font={"family": "Arial", "size": 14, "color": INK},
        height=height,
        margin={"l": 20, "r": 25, "t": 35, "b": 35},
        legend_title_text="",
    )
    figure.update_xaxes(
        gridcolor="#E8E0E5",
        zeroline=False,
        automargin=True,
    )
    figure.update_yaxes(
        gridcolor="#E8E0E5",
        zeroline=False,
        automargin=True,
    )
    st.plotly_chart(
        figure,
        use_container_width=True,
        theme=None,
        config={"displaylogo": False},
    )


def add_area_trace(figure, data, predictor, name, colour, size=8):
    """Add one group directly without Plotly Express grouping."""
    # Direct traces avoid the previous "Chosen areas" grouping error.
    # Reference: constructing figures from individual graph objects.
    # https://plotly.com/python/graph-objects/
    if data.empty:
        return

    figure.add_trace(
        go.Scatter(
            x=data[predictor].tolist(),
            y=data[OUTCOME].tolist(),
            customdata=data[["LSOA_Name", "LSOA_Code"]].to_numpy().tolist(),
            mode="markers",
            name=name,
            marker={
                "color": colour,
                "size": size,
                "opacity": 0.8,
                "line": {"color": IVORY, "width": 1},
            },
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "%{customdata[1]}<br>"
                + LABELS[predictor]
                + ": %{x:.2f}<br>"
                + LABELS[OUTCOME]
                + ": %{y:.2f}<extra></extra>"
            ),
        )
    )


def read_results(data):
    """Validate and align saved results using hypothesis identifiers."""
    if not RESULTS_PATH.exists():
        raise ValueError(
            "Missing results export: outputs/hypothesis_testing/"
            "spearman_hypothesis_results.csv"
        )

    results = pd.read_csv(RESULTS_PATH)
    required = [
        "Hypothesis",
        "Number_of_Areas",
        "Spearman_Rho",
        "Unadjusted_P_Value",
        "Holm_Adjusted_P_Value",
        "Reject_H0_At_0_05",
    ]

    missing = sorted(set(required) - set(results.columns))
    if missing:
        raise ValueError("Missing results columns: " + ", ".join(missing))

    if len(results) != 3:
        raise ValueError("The results export must contain three tests.")

    numeric = required[1:5]
    results[numeric] = results[numeric].apply(
        pd.to_numeric,
        errors="raise",
    )

    if not np.isfinite(results[numeric].to_numpy()).all():
        raise ValueError("The saved results contain invalid numbers.")

    if not results["Number_of_Areas"].eq(len(data)).all():
        raise ValueError("Saved tests and dashboard area counts differ.")

    if not results["Spearman_Rho"].between(-1, 1).all():
        raise ValueError("Saved correlations must fall within -1 and 1.")

    for column in ["Unadjusted_P_Value", "Holm_Adjusted_P_Value"]:
        if not results[column].between(0, 1).all():
            raise ValueError("Saved p-values must fall within 0 and 1.")

    # Match H1–H3 explicitly rather than relying on CSV row order.
    results["Test_ID"] = (
        results["Hypothesis"].astype(str).str.extract(r"^(H[123])\b")[0]
    )
    if set(results["Test_ID"]) != {"H1", "H2", "H3"}:
        raise ValueError("Results must identify H1, H2 and H3 once each.")

    results = results.set_index("Test_ID").loc[["H1", "H2", "H3"]]

    # Compare coefficients with the loaded data to catch stale exports.
    # Correlating average ranks reproduces Spearman coefficients.
    # Reference: pandas correlation methods.
    # https://pandas.pydata.org/docs/reference/frame.html
    for hypothesis in HYPOTHESES:
        columns = [hypothesis["column"], OUTCOME]
        current_rho = data[columns].rank().corr().iloc[0, 1]
        saved_rho = results.loc[hypothesis["id"], "Spearman_Rho"]
        if not np.isclose(current_rho, saved_rho, atol=0.0005):
            raise ValueError(
                "Saved coefficients do not match the loaded data. "
                "Review the notebook export before displaying results."
            )

    return results


def show_hypotheses(data):
    """Display saved evidence with charts and plain-language findings."""
    try:
        results = read_results(data)
    except (OSError, ValueError, TypeError) as error:
        st.error(f"Hypothesis results could not be displayed: {error}")
        return

    st.markdown("#### Comparing the three relationships")
    st.write(
        "Each dot shows a saved Spearman correlation with selected "
        "inactivity. Values nearer +1 indicate a stronger positive "
        "rank association."
    )

    comparison = go.Figure()
    for hypothesis in HYPOTHESES:
        row = results.loc[hypothesis["id"]]
        title = hypothesis["title"]
        rho = float(row["Spearman_Rho"])

        comparison.add_trace(
            go.Scatter(
                x=[0, rho],
                y=[title, title],
                mode="lines",
                line={"color": "#DFD2DC", "width": 5},
                hoverinfo="skip",
                showlegend=False,
            )
        )
        comparison.add_trace(
            go.Scatter(
                x=[rho],
                y=[title],
                mode="markers+text",
                marker={"color": hypothesis["colour"], "size": 18},
                text=[f"{rho:.3f}"],
                textposition="top center",
                customdata=[[float(row["Holm_Adjusted_P_Value"])]],
                hovertemplate=(
                    "%{y}<br>Spearman rho: %{x:.3f}<br>"
                    "Holm-adjusted p: %{customdata[0]:.3e}"
                    "<extra></extra>"
                ),
                showlegend=False,
            )
        )

    comparison.update_layout(
        xaxis_title="Spearman correlation with selected inactivity",
        xaxis_range=[-1, 1],
        yaxis_title=None,
    )
    comparison.update_yaxes(autorange="reversed")
    comparison.add_vline(x=0, line_color="#988793", line_dash="dot")
    show_chart(comparison, height=320)

    st.caption(
        "Correlation strength is not causal importance. Differences "
        "between these correlations have not been formally tested."
    )

    for hypothesis in HYPOTHESES:
        row = results.loc[hypothesis["id"]]
        rho = float(row["Spearman_Rho"])
        adjusted_p = float(row["Holm_Adjusted_P_Value"])
        predictor = hypothesis["column"]

        st.divider()
        st.markdown(f"#### {hypothesis['id']} · {hypothesis['title']}")
        st.write(hypothesis["question"])

        chart_column, finding_column = st.columns([1.8, 1])

        with chart_column:
            figure = go.Figure()
            add_area_trace(
                figure,
                data,
                predictor,
                hypothesis["title"],
                hypothesis["colour"],
            )
            figure.update_layout(
                xaxis_title=LABELS[predictor],
                yaxis_title=LABELS[OUTCOME],
                showlegend=False,
            )
            show_chart(figure, height=390)
            st.caption(
                "One point per neighbourhood. Hover to see its " "name and percentages."
            )

        with finding_column:
            st.metric("Spearman correlation", f"{rho:.3f}")
            st.caption(
                f"Holm-adjusted p: {adjusted_p:.3e} | "
                f"Areas: {int(row['Number_of_Areas'])}"
            )

            if rho > 0:
                st.write(
                    "Areas with higher values on this measure "
                    "tend to have higher selected inactivity."
                )
            elif rho < 0:
                st.write(
                    "Areas with higher values on this measure "
                    "tend to have lower selected inactivity."
                )
            else:
                st.write("The saved rank correlation is zero.")

            if adjusted_p < 0.05:
                st.write(
                    "The association meets the 5% significance "
                    "threshold after adjustment for three tests."
                )
            else:
                st.write(
                    "The association does not meet the 5% "
                    "threshold after adjustment for three tests."
                )

            st.markdown("**Interpret with care**")
            st.write(hypothesis["limitation"])

    with st.expander("View the detailed results and download"):
        displayed = results.copy()
        displayed["Spearman_Rho"] = displayed["Spearman_Rho"].round(3)
        for column in ["Unadjusted_P_Value", "Holm_Adjusted_P_Value"]:
            displayed[column] = displayed[column].map(lambda value: f"{value:.3e}")
        displayed = displayed.rename(
            columns={
                "Number_of_Areas": "Areas",
                "Spearman_Rho": "Spearman rho",
                "Unadjusted_P_Value": "Unadjusted p",
                "Holm_Adjusted_P_Value": "Holm-adjusted p",
                "Reject_H0_At_0_05": "Reject H0 at 0.05",
            }
        )
        st.dataframe(
            displayed,
            hide_index=True,
            use_container_width=True,
        )
        st.download_button(
            "Download hypothesis results",
            data=results.to_csv(index=False).encode("utf-8"),
            file_name="spearman_hypothesis_results.csv",
            mime="text/csv",
        )

    st.markdown("#### What these findings tell us")
    st.write(
        "These are area-level associations, not evidence that any "
        "factor causes inactivity. The tests do not isolate independent "
        "effects or control for age structure and other confounders."
    )
    st.write(
        "The p-values are approximate and exploratory. Neighbouring "
        "areas may share characteristics, affecting independence. "
        "Holm adjustment addresses multiple testing, but does not "
        "resolve spatial dependence or confounding."
    )


try:
    df = load_data()
except (OSError, ValueError, TypeError) as error:
    st.error(f"The dashboard data could not be loaded: {error}")
    st.stop()


st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Dudley / Neighbourhood evidence</div>
        <h1>Employment Barriers</h1>
        <p>
            Explore health, qualifications and vehicle availability
            alongside selected economic inactivity.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(
    f"{len(df)} included neighbourhoods | Census 2021 | "
    "Area-level associations, not evidence of causation"
)

if len(df) != 199:
    st.warning("The project analysis used 199 areas. Review this dataset.")

cards = st.columns(4)
cards[0].metric("Neighbourhoods included", len(df))
cards[1].metric(
    "Mean selected inactivity",
    f"{df[OUTCOME].mean():.1f}%",
)
cards[2].metric("Lowest area percentage", f"{df[OUTCOME].min():.1f}%")
cards[3].metric("Highest area percentage", f"{df[OUTCOME].max():.1f}%")

st.caption(
    "The mean gives each neighbourhood equal weight. "
    "It is not a pooled borough percentage."
)

with st.expander("What does selected inactivity include?"):
    st.write(
        "Residents looking after home or family, those inactive "
        "because of long-term sickness or disability, and those "
        "in the 'Other' inactivity category."
    )
    st.write(
        "Their combined count is divided by all usual residents "
        "aged 16 and over in the economic activity dataset. "
        "Students and retired residents are excluded from this "
        "selected numerator. This is not total inactivity or "
        "an unemployment rate."
    )

overview, explore, results_tab, ethics = st.tabs(
    [
        "Overview",
        "Explore Areas",
        "Hypothesis Results",
        "Sources & Ethics",
    ]
)


with overview:
    st.subheader("How does selected inactivity vary?")
    st.write(
        "Explore the spread across neighbourhoods and the categories "
        "that make up the selected measure."
    )

    left, right = st.columns([1.15, 1])

    with left:
        st.markdown("#### Distribution across areas")
        histogram = go.Figure(
            go.Histogram(
                x=df[OUTCOME].tolist(),
                nbinsx=16,
                marker_color=MAUVE,
                hovertemplate=(
                    "Selected inactivity: %{x}<br>"
                    "Neighbourhoods: %{y}<extra></extra>"
                ),
            )
        )
        histogram.add_vline(
            x=float(df[OUTCOME].median()),
            line_dash="dot",
            line_color=PLUM,
        )
        histogram.update_layout(
            xaxis_title=LABELS[OUTCOME],
            yaxis_title="Number of neighbourhoods",
            bargap=0.04,
        )
        show_chart(histogram)
        st.caption("The dotted line marks the median area percentage.")

    with right:
        st.markdown("#### Composition of selected inactivity")
        composition = go.Figure(
            go.Pie(
                labels=COMPONENT_NAMES,
                values=df[COMPONENTS].sum().tolist(),
                hole=0.68,
                sort=False,
                marker={"colors": [PLUM, MAUVE, TEAL]},
                textinfo="percent",
                textposition="inside",
                hovertemplate=(
                    "%{label}<br>%{value:,.0f} residents<br>"
                    "%{percent}<extra></extra>"
                ),
            )
        )
        composition.update_layout(
            legend={
                "orientation": "h",
                "y": -0.15,
                "x": 0,
                "font": {"size": 11},
            }
        )
        show_chart(composition)
        st.caption(
            "Shares of selected inactive residents across included "
            "areas, rather than shares of the entire population."
        )

    st.markdown("#### Relationships between the selected measures")
    st.caption(
        "Spearman rank correlations across included areas. "
        "Different measures use different source populations."
    )

    correlation = df[MEASURES].rank().corr()
    short_names = [
        "Selected inactivity",
        "Health limitations",
        "No qualifications",
        "No vehicle",
    ]
    heatmap = go.Figure(
        go.Heatmap(
            z=correlation.to_numpy().tolist(),
            x=short_names,
            y=short_names,
            zmin=-1,
            zmax=1,
            colorscale=[[0, TEAL], [0.5, IVORY], [1, PLUM]],
            text=correlation.round(2).to_numpy().tolist(),
            texttemplate="%{text:.2f}",
            colorbar={"title": "Spearman rho"},
            hovertemplate=("%{x}<br>%{y}<br>rho: %{z:.3f}<extra></extra>"),
        )
    )
    heatmap.update_yaxes(autorange="reversed")
    show_chart(heatmap, height=450)
    st.caption(
        "Health limitations overlap conceptually with the sickness "
        "component of the outcome. Vehicle availability does not "
        "directly measure access to public transport."
    )


with explore:
    st.subheader("Explore neighbourhood patterns")
    st.write(
        "Choose a measure and highlight up to six neighbourhoods. "
        "Each point represents one included area."
    )

    controls, choices = st.columns([1, 2])
    with controls:
        barrier_name = st.selectbox(
            "Choose a measure",
            options=list(BARRIERS),
        )
    with choices:
        selected_areas = st.multiselect(
            "Choose neighbourhoods to highlight",
            options=df["LSOA_Name"].tolist(),
            default=df["LSOA_Name"].head(3).tolist(),
            max_selections=6,
        )

    predictor = BARRIERS[barrier_name]
    chosen_mask = df["LSOA_Name"].isin(selected_areas)
    scatter = go.Figure()

    add_area_trace(
        scatter,
        df.loc[~chosen_mask],
        predictor,
        "Other areas",
        "#BAA7B4",
    )
    add_area_trace(
        scatter,
        df.loc[chosen_mask],
        predictor,
        "Chosen areas",
        PLUM,
        size=12,
    )
    scatter.update_layout(
        xaxis_title=LABELS[predictor],
        yaxis_title=LABELS[OUTCOME],
        legend={"orientation": "h", "y": 1.1},
    )
    show_chart(scatter, height=470)
    st.caption(
        "Highlighting changes the emphasis, not the data used "
        "in the saved hypothesis tests."
    )

    st.markdown("#### Compare your chosen neighbourhoods")
    comparison_measure = st.selectbox(
        "Measure for comparison",
        options=MEASURES,
        format_func=lambda column: LABELS[column],
    )
    selected = df.loc[chosen_mask].copy()

    if selected.empty:
        st.info("Choose at least one neighbourhood to see its comparison.")
    else:
        ordered = selected.sort_values(comparison_measure)
        comparison = go.Figure(
            go.Bar(
                x=ordered[comparison_measure].tolist(),
                y=ordered["LSOA_Name"].tolist(),
                orientation="h",
                marker_color=MAUVE,
                text=ordered[comparison_measure].round(1).tolist(),
                texttemplate="%{text:.1f}%",
                textposition="outside",
                cliponaxis=False,
                hovertemplate="%{y}<br>%{x:.2f}%<extra></extra>",
            )
        )
        area_mean = float(df[comparison_measure].mean())
        comparison.add_vline(
            x=area_mean,
            line_dash="dot",
            line_color=TEAL,
        )
        upper = max(
            float(ordered[comparison_measure].max()),
            area_mean,
        )
        comparison.update_layout(
            xaxis_title=LABELS[comparison_measure],
            yaxis_title=None,
            xaxis_range=[0, upper * 1.2 + 1],
        )
        show_chart(comparison, height=350)
        st.caption(
            f"The dotted line is the included-area mean: "
            f"{area_mean:.1f}%. Each area has equal weight."
        )

        table = selected[["LSOA_Name", "LSOA_Code"] + MEASURES]
        st.dataframe(
            table.rename(columns=LABELS).round(2),
            hide_index=True,
            use_container_width=True,
        )
        st.download_button(
            "Download chosen neighbourhoods",
            data=table.to_csv(index=False).encode("utf-8"),
            file_name="chosen_neighbourhoods.csv",
            mime="text/csv",
        )


with results_tab:
    st.subheader("What did the hypothesis tests find?")
    st.write(
        "Compare the three relationships, then explore the evidence "
        "and interpretation for each hypothesis."
    )
    show_hypotheses(df)


with ethics:
    st.subheader("Sources, methods and ethical considerations")

    st.markdown("#### Project question")
    st.write(
        "To what extent do localized structural barriers—specifically "
        "health limitations, qualification deficits, and transport "
        "poverty—drive economic inactivity across Dudley's "
        "199 neighbourhoods?"
    )
    st.write(
        "The analysis examines associations relevant to this question. "
        "It cannot establish that the measured factors cause inactivity."
    )

    st.markdown("#### Measures and denominators")
    definitions = pd.DataFrame(
        {
            "Measure": [
                "Selected inactivity",
                "Activities limited a lot",
                "No formal qualifications",
                "No car or van",
            ],
            "Numerator": [
                "Home/family + long-term sick/disabled + other",
                "Residents whose activities are limited a lot",
                "Residents with no formal qualifications",
                "Households with no car or van",
            ],
            "Denominator": [
                "TS066 usual residents aged 16+",
                "RM019 usual residents aged 16+",
                "TS067 usual residents aged 16+",
                "TS045 households",
            ],
        }
    )
    st.dataframe(
        definitions,
        hide_index=True,
        use_container_width=True,
    )
    st.write(
        "Each percentage uses its own source denominator. "
        "Totals from separate Census tables are not interchangeable."
    )

    st.markdown("#### Data sources")
    nomis_url = "https://www.nomisweb.co.uk/sources/census_2021"
    iod_url = (
        "https://www.gov.uk/government/statistics/"
        "english-indices-of-deprivation-2019"
    )
    st.markdown(
        f"[ONS Census 2021 via Nomis]({nomis_url}): "
        "TS066 economic activity, TS067 qualifications, "
        "RM019 disability and TS045 car or van availability."
    )
    st.markdown(
        f"[English Indices of Deprivation 2019]({iod_url}): "
        "historical context retained in the prepared dataset. "
        "Published deprivation measures are not recalculated "
        "using Census 2021 populations."
    )

    st.markdown("#### Coverage and limitations")
    st.write(
        "The prepared dataset includes 199 shared LSOAs. "
        "The ONS lookup confirmed unchanged boundaries between "
        "2011 and 2021 for these included areas."
    )
    st.write(
        "Four Census areas and two deprivation-only areas were "
        "excluded from the combined dataset. Findings describe "
        "the included areas, not complete borough coverage."
    )
    st.write(
        "Census measures refer to 2021. Deprivation measures use "
        "the 2019 release, with varying underlying observation dates. "
        "These data do not describe current conditions."
    )

    st.markdown("#### Responsible interpretation")
    st.markdown("""
        - Neighbourhood patterns must not be attributed to individuals.
          The dashboard does not identify who needs employment support.
        - Disability does not imply unwillingness to work. Health
          limitations overlap with part of the selected outcome.
        - No formal qualifications does not mean a person lacks
          skills, experience or ability.
        - No household vehicle does not establish transport poverty.
          Public transport, affordability and journey times are not
          directly measured.
        - Caring responsibilities are not personal failings.
          Selected inactivity includes different circumstances.
        - Age structure and other unmeasured factors may influence
          the observed relationships.
        - Findings can support further investigation and inclusive
          planning, not individual eligibility decisions or labels
          attached to neighbourhoods.
        """)

    st.markdown("#### Understand the data")
    st.write(
        "The data dictionaries explain variable meanings, sources, "
        "reference years, units, population coverage, denominators "
        "and calculations."
    )

    dictionary_items = [
        (
            "Prepared dataset",
            "Explains the 105 columns in the prepared dataset.",
            "prepared_data_dictionary.csv",
        ),
        (
            "Selected inactivity measures",
            "Explains the selected inactivity count and percentage.",
            "supplementary_data_dictionary.csv",
        ),
    ]

    for title, description, filename in dictionary_items:
        st.markdown(f"**{title}**")
        st.write(description)
        path = ROOT / "outputs" / "data_dictionary" / filename
        if path.exists():
            st.download_button(
                f"Download: {title}",
                data=path.read_bytes(),
                file_name=filename,
                mime="text/csv",
            )
        else:
            st.caption("This dictionary file is not currently available.")

    with st.expander("How the dashboard uses the project files"):
        st.write(
            "The dashboard reads the prepared CSV and derives selected "
            "inactivity using the same categories and denominator "
            "as notebook 08. Source and prepared files are unchanged."
        )
        st.write(
            "Hypothesis results come from the saved notebook export. "
            "The app checks the area count and correlations against "
            "the loaded dataset before presenting those results."
        )
        st.write(
            "No machine-learning model or individual prediction "
            "is used in this dashboard."
        )

    st.caption(
        "Sources: ONS Census 2021 via Nomis and MHCLG English "
        "Indices of Deprivation 2019. Contains public sector "
        "information licensed under the Open Government Licence v3.0."
    )
    st.caption(
        "ChatGPT assisted with code development and documentation. "
        "The project author is responsible for checking the analysis, "
        "interpretation and dashboard."
    )
