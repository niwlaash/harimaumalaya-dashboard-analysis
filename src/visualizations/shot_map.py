import plotly.graph_objects as go
import pandas as pd

def create_shot_map(shots_df: pd.DataFrame, player_name: str) -> go.Figure:
    """
    Renders an authentic, editorial StatsBomb / Opta Analyst style 2D Half-Pitch Shot Map.
    Visualizes shot locations, outcome states, and expected goal (xG) volume.
    Attacking direction is left-to-right toward the goal at x=105.
    """
    fig = go.Figure()

    # Half pitch boundaries (x from 52.5 to 105, y from 0 to 68)
    line_color = "rgba(255, 255, 255, 0.45)"
    pitch_bg = "#111827"

    # Pitch Outline & Halfway Line
    fig.add_shape(type="rect", x0=52.5, y0=0, x1=105, y1=68, line=dict(color=line_color, width=2))
    fig.add_shape(type="line", x0=52.5, y0=0, x1=52.5, y1=68, line=dict(color=line_color, width=2))

    # 18-yard Penalty Box
    fig.add_shape(type="rect", x0=88.5, y0=13.84, x1=105, y1=54.16, line=dict(color=line_color, width=1.8))

    # 6-yard Goal Box
    fig.add_shape(type="rect", x0=99.5, y0=24.84, x1=105, y1=43.16, line=dict(color=line_color, width=1.5))

    # Penalty Spot (x=94, y=34)
    fig.add_shape(type="circle", x0=93.7, y0=33.7, x1=94.3, y1=34.3, fillcolor=line_color, line_color=line_color)

    # Goal Posts (x=105, y=30.34 to 37.66)
    fig.add_shape(type="line", x0=105, y0=30.34, x1=105, y1=37.66, line=dict(color="#f59e0b", width=5))

    # Penalty Arc (radius 9.15m from penalty spot x=94, y=34)
    fig.add_shape(
        type="circle",
        x0=94 - 9.15, y0=34 - 9.15, x1=94 + 9.15, y1=34 + 9.15,
        line=dict(color=line_color, width=1.5, dash="dot")
    )

    if shots_df.empty:
        fig.add_annotation(
            text="No competitive shots recorded in 2026/27 season sample.",
            x=78.75, y=34, showarrow=False,
            font=dict(color="#94a3b8", size=13)
        )
        fig.update_layout(
            xaxis=dict(range=[50, 107], visible=False),
            yaxis=dict(range=[-2, 70], visible=False),
            paper_bgcolor=pitch_bg,
            plot_bgcolor=pitch_bg,
            height=380,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        return fig

    # Separate shots by outcome for clear legend and layer styling
    outcome_styles = {
        "Goal": {"color": "#f59e0b", "symbol": "star", "name": "Goal (Clinical Strike)"},
        "Saved": {"color": "#06b6d4", "symbol": "circle", "name": "Saved on Target"},
        "Blocked": {"color": "#94a3b8", "symbol": "square", "name": "Blocked in Box"},
        "Missed": {"color": "#ef4444", "symbol": "x", "name": "Off Target"}
    }

    tot_xg = shots_df["xg"].sum()
    goals_num = len(shots_df[shots_df["outcome"] == "Goal"])
    xg_diff = goals_num - tot_xg

    for outcome, style in outcome_styles.items():
        sub_df = shots_df[shots_df["outcome"] == outcome]
        if sub_df.empty:
            continue

        # Scale marker size dynamically by xG (minimum 9px, maximum 26px)
        marker_sizes = [max(9, min(26, float(val) * 32.0 + 7.0)) for val in sub_df["xg"]]

        hover_texts = [
            f"<b>{outcome.upper()}</b><br>"
            f"Distance: {row['distance_m']}m<br>"
            f"Expected Goal (xG): <b>{row['xg']:.2f}</b><br>"
            f"Type: {row['body_part']}<br>"
            f"Period: {row['period']}"
            for _, row in sub_df.iterrows()
        ]

        fig.add_trace(go.Scatter(
            x=sub_df["x"],
            y=sub_df["y"],
            mode="markers",
            name=f"{style['name']} ({len(sub_df)})",
            marker=dict(
                size=marker_sizes,
                color=style["color"],
                symbol=style["symbol"],
                line=dict(color="#ffffff", width=1.2 if outcome != "Goal" else 2.0),
                opacity=0.92
            ),
            hoverinfo="text",
            hovertext=hover_texts
        ))

    diff_str = f"+{xg_diff:.2f}" if xg_diff >= 0 else f"{xg_diff:.2f}"
    title_text = (
        f"<b>{player_name}</b> | 2026/27 xG Shot Map "
        f"({goals_num} Goals / {len(shots_df)} Shots | Cumulative xG: {tot_xg:.2f} | Finishing Delta: {diff_str})"
    )

    fig.update_layout(
        title=dict(text=title_text, font=dict(color="#f4d03f", size=13)),
        xaxis=dict(range=[51, 107], visible=False),
        yaxis=dict(range=[-2, 70], visible=False, scaleanchor="x", scaleratio=1),
        paper_bgcolor=pitch_bg,
        plot_bgcolor=pitch_bg,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.12,
            xanchor="center",
            x=0.5,
            font=dict(color="#e2e8f0", size=10)
        ),
        margin=dict(l=10, r=10, t=40, b=40),
        height=400
    )

    return fig
