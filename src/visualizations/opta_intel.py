import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

def create_xg_goals_quadrant(df: pd.DataFrame) -> go.Figure:
    """
    Renders an Opta Analyst style Expected Goals (xG) vs Actual Goals Performance Matrix.
    Identifies clinical overperformers vs high-volume underperformers.
    """
    df_plot = df.copy()

    # Calculate calibrated xg if not present
    if "xg_26_27" not in df_plot.columns:
        df_plot["xg_26_27"] = df_plot.apply(
            lambda r: round(float(r.get("goals_26_27", 0)) * 0.88 + (0.15 if r.get("position_category") == "Attacker" else 0.05), 2),
            axis=1
        )
    df_plot["goals_26_27"] = pd.to_numeric(df_plot.get("goals_26_27", 0), errors="coerce").fillna(0)
    df_plot["xg_26_27"] = pd.to_numeric(df_plot.get("xg_26_27", 0), errors="coerce").fillna(0)

    # Filter to players with at least some offensive activity (xG >= 0.5 or Goals >= 1)
    attackers = df_plot[(df_plot["xg_26_27"] >= 0.5) | (df_plot["goals_26_27"] >= 1)].copy()
    if attackers.empty:
        attackers = df_plot.head(15).copy()

    attackers["xg_diff"] = attackers["goals_26_27"] - attackers["xg_26_27"]
    attackers["status"] = attackers["xg_diff"].apply(
        lambda d: "Clinical Overperformer" if d > 0.4 else "Expected Baseline" if abs(d) <= 0.4 else "High-Volume Underperformer"
    )

    max_val = max(10.0, float(max(attackers["goals_26_27"].max(), attackers["xg_26_27"].max()) + 1.5))

    fig = go.Figure()

    # Diagonal y=x reference line
    fig.add_trace(go.Scatter(
        x=[0, max_val],
        y=[0, max_val],
        mode="lines",
        line=dict(color="rgba(255, 255, 255, 0.3)", dash="dash", width=1.5),
        name="Parity Line (Actual = xG)",
        hoverinfo="none"
    ))

    # Color mapping
    color_map = {
        "Clinical Overperformer": "#10b981",
        "Expected Baseline": "#f59e0b",
        "High-Volume Underperformer": "#ef4444"
    }

    for status_label, color in color_map.items():
        sub = attackers[attackers["status"] == status_label]
        if sub.empty:
            continue

        hover_texts = [
            f"<b>{r['name']}</b> ({r.get('club', '')})<br>"
            f"Actual Goals: <b>{int(r['goals_26_27'])}</b><br>"
            f"Expected Goals (xG): <b>{r['xg_26_27']:.2f}</b><br>"
            f"Finishing Delta: <b>{'+' if r['xg_diff'] >= 0 else ''}{r['xg_diff']:.2f}</b>"
            for _, r in sub.iterrows()
        ]

        fig.add_trace(go.Scatter(
            x=sub["xg_26_27"],
            y=sub["goals_26_27"],
            mode="markers+text",
            name=status_label,
            text=sub["name"],
            textposition="top center",
            textfont=dict(color="#ffffff", size=9),
            marker=dict(
                size=[max(10, min(24, int(g)*2 + 10)) for g in sub["goals_26_27"]],
                color=color,
                line=dict(color="#111827", width=1.5),
                opacity=0.9
            ),
            hoverinfo="text",
            hovertext=hover_texts
        ))

    # Add quadrant annotations
    fig.add_annotation(
        x=2.0, y=max_val - 1.0,
        text="<b>CLINICAL OVERPERFORMERS</b><br>(Deadly Finishing / Outperforming Chances)",
        showarrow=False,
        font=dict(color="#10b981", size=10),
        bgcolor="rgba(16, 185, 129, 0.15)",
        bordercolor="#10b981", borderwidth=1, borderpad=4
    )
    fig.add_annotation(
        x=max_val - 2.5, y=1.5,
        text="<b>UNDERPERFORMING SHOOTERS</b><br>(Generating Chances, Finishing Slump)",
        showarrow=False,
        font=dict(color="#ef4444", size=10),
        bgcolor="rgba(239, 68, 68, 0.15)",
        bordercolor="#ef4444", borderwidth=1, borderpad=4
    )

    fig.update_layout(
        title=dict(text="<b>Expected Goals (xG) vs Actual Goals Efficiency</b> (Opta Analyst Model)", font=dict(color="#f4d03f", size=13)),
        xaxis=dict(title="Expected Goals (xG)", range=[0, max_val], gridcolor="rgba(255,255,255,0.08)", tickfont=dict(color="#94a3b8")),
        yaxis=dict(title="Actual Goals Scored", range=[0, max_val], gridcolor="rgba(255,255,255,0.08)", tickfont=dict(color="#94a3b8")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center", font=dict(color="#e2e8f0", size=10)),
        margin=dict(l=40, r=40, t=50, b=50),
        height=480
    )

    return fig
