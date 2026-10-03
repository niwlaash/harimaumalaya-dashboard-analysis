import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_minutes_bar_chart(df: pd.DataFrame, top_n: int = 25):
    """Horizontal stacked or grouped bar chart of player playing time in 26/27."""
    if top_n and len(df) > top_n:
        df_sorted = df.sort_values(by="minutes_26_27", ascending=False).head(top_n).sort_values(by="minutes_26_27", ascending=True)
        title_text = f"Top {top_n} Minutes Played (2026/27 Season)"
    else:
        df_sorted = df.sort_values(by="minutes_26_27", ascending=True)
        title_text = f"Minutes Played (2026/27 Season - {len(df_sorted)} Players)"

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df_sorted["name"],
        x=df_sorted["minutes_26_27"],
        orientation='h',
        marker=dict(
            color=df_sorted["minutes_26_27"],
            colorscale=[[0, '#1e293b'], [0.5, '#f59e0b'], [1.0, '#10b981']],
            line=dict(color='#111111', width=1)
        ),
        text=[f"{int(m)}' ({c})" for m, c in zip(df_sorted["minutes_26_27"].fillna(0), df_sorted.get("club", [""] * len(df_sorted)))],
        textposition="outside",
        textfont=dict(color="#ffffff", size=10)
    ))

    calc_height = max(380, min(1200, len(df_sorted) * 24 + 80))

    fig.update_layout(
        title=dict(text=title_text, font=dict(color="#f4d03f", size=14)),
        xaxis=dict(title="Minutes", gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color="#cccccc")),
        yaxis=dict(tickfont=dict(color="#ffffff", size=11)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=120, r=40, t=40, b=40),
        height=calc_height
    )
    return fig


def create_form_trend_chart(ratings: list, player_name: str):
    """Line chart showing match ratings form progression across last 5 matches."""
    matches = [f"Match -{5-i}" if i < 4 else "Latest Match" for i in range(len(ratings))]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=matches,
        y=ratings,
        mode="lines+markers+text",
        text=[f"{r:.1f}" for r in ratings],
        textposition="top center",
        textfont=dict(color="#ffffff", size=12, family="Arial"),
        line=dict(color="#f4d03f", width=3, shape="spline"),
        marker=dict(size=10, color="#e67e22", line=dict(color="#ffffff", width=2))
    ))

    fig.add_hline(y=7.0, line_dash="dash", line_color="rgba(255,255,255,0.4)", annotation_text="Benchmark 7.0")

    fig.update_layout(
        title=dict(text=f"Recent Match Rating Form (FotMob/SofaScore): {player_name}", font=dict(color="#f4d03f", size=13)),
        yaxis=dict(range=[5.5, 9.5], gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color="#ffffff")),
        xaxis=dict(gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color="#ffffff")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=20, t=40, b=30),
        height=280
    )
    return fig

def create_goal_contributions_chart(df: pd.DataFrame, top_n: int = 20):
    """Grouped bar chart for top goal contributors (Goals vs Assists)."""
    contrib_col = "goal_contributions_26_27" if "goal_contributions_26_27" in df.columns else "goals_26_27"
    attackers = df[df[contrib_col] > 0].sort_values(by=contrib_col, ascending=False).head(top_n)
    
    if attackers.empty:
        attackers = df.head(min(12, len(df)))

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=attackers["name"],
        y=attackers["goals_26_27"].fillna(0),
        name="Goals",
        marker_color="#ef4444"
    ))
    fig.add_trace(go.Bar(
        x=attackers["name"],
        y=attackers["assists_26_27"].fillna(0),
        name="Assists",
        marker_color="#f59e0b"
    ))

    fig.update_layout(
        barmode="stack",
        title=dict(text=f"Top {len(attackers)} Goal Contributions (Goals + Assists in 26/27)", font=dict(color="#f4d03f", size=14)),
        xaxis=dict(tickfont=dict(color="#ffffff", size=10)),
        yaxis=dict(title="Contributions", gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color="#cccccc")),
        legend=dict(font=dict(color="#ffffff"), orientation="h", y=1.1),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=20, t=50, b=40),
        height=380
    )
    return fig


def create_age_value_quadrant(df: pd.DataFrame):
    """Scatter plot mapping Age vs Market Value with quadrant overlays."""
    df_plot = df.copy()
    df_plot["age"] = pd.to_numeric(df_plot.get("age", 25), errors="coerce").fillna(25)
    df_plot["market_value_eur"] = pd.to_numeric(df_plot.get("market_value_eur", 100000), errors="coerce").fillna(100000)
    df_plot["plot_size"] = pd.to_numeric(df_plot.get("minutes_26_27", 100), errors="coerce").fillna(100)
    df_plot["plot_size"] = df_plot["plot_size"].apply(lambda m: max(8, min(40, float(m) / 20.0 + 8.0)))
    df_plot["position_category"] = df_plot.get("position_category", "Midfielder").fillna("Midfielder")

    fig = px.scatter(
        df_plot,
        x="age",
        y="market_value_eur",
        color="position_category",
        size="plot_size",
        hover_name="name",
        hover_data=["club", "league", "minutes_26_27"],
        text="name",
        color_discrete_map={
            "Goalkeeper": "#ffb703",
            "Defender": "#219ebc",
            "Midfielder": "#8ecae6",
            "Attacker": "#e63946"
        }
    )

    fig.update_traces(
        textposition="top right",
        textfont=dict(color="#ffffff", size=10),
        marker=dict(line=dict(width=1.5, color='#ffffff'))
    )

    fig.update_layout(
        title=dict(text="Squad Age vs Market Value Distribution (€)", font=dict(color="#f4d03f", size=14)),
        xaxis=dict(title="Age", gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color="#ffffff")),
        yaxis=dict(title="Market Value (€)", gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color="#ffffff")),
        legend=dict(font=dict(color="#ffffff")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=50, r=30, t=50, b=40),
        height=480
    )
    return fig
