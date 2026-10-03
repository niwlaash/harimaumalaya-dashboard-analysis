import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_minutes_bar_chart(df: pd.DataFrame):
    """Horizontal stacked or grouped bar chart of player playing time in 26/27."""
    df_sorted = df.sort_values(by="minutes_26_27", ascending=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df_sorted["name"],
        x=df_sorted["minutes_26_27"],
        orientation='h',
        marker=dict(
            color=df_sorted["minutes_26_27"],
            colorscale=[[0, '#2c3e50'], [0.5, '#f39c12'], [1.0, '#f1c40f']],
            line=dict(color='#111111', width=1)
        ),
        text=[f"{m}' ({c})" for m, c in zip(df_sorted["minutes_26_27"], df_sorted["club"])],
        textposition="outside",
        textfont=dict(color="#ffffff", size=10)
    ))

    fig.update_layout(
        title=dict(text="Total Minutes Played (2026/27 Season)", font=dict(color="#f4d03f", size=14)),
        xaxis=dict(title="Minutes", gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color="#cccccc")),
        yaxis=dict(tickfont=dict(color="#ffffff", size=11)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=120, r=40, t=40, b=40),
        height=620
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

def create_goal_contributions_chart(df: pd.DataFrame):
    """Grouped bar chart for top goal contributors (Goals vs Assists)."""
    attackers = df[df["goal_contributions_26_27"] > 0].sort_values(by="goal_contributions_26_27", ascending=False)
    
    if attackers.empty:
        attackers = df.head(8)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=attackers["name"],
        y=attackers["goals_26_27"],
        name="Goals",
        marker_color="#e74c3c"
    ))
    fig.add_trace(go.Bar(
        x=attackers["name"],
        y=attackers["assists_26_27"],
        name="Assists",
        marker_color="#f1c40f"
    ))

    fig.update_layout(
        barmode="stack",
        title=dict(text="Goal Contributions (Goals + Assists in 26/27)", font=dict(color="#f4d03f", size=14)),
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
    fig = px.scatter(
        df,
        x="age",
        y="market_value_eur",
        color="position_category",
        size="minutes_26_27",
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
