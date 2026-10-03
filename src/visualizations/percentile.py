import plotly.graph_objects as go
import pandas as pd

def create_percentile_bars(player: dict, positional_benchmark_label: str = "Positional Peers") -> go.Figure:
    """
    Renders an authentic FBref / StatsBomb style Horizontal Percentile Profile.
    Evaluates player performance across 6 core statistical pillars normalized against
    the entire Malaysian national & domestic league pool.
    """
    p90 = player.get("p90_metrics") or {}
    pos_cat = player.get("position_category", "Midfielder")
    attrs = player.get("attributes") or {}

    # Define the 6 analytical dimensions based on position category
    if pos_cat == "Attacker":
        metrics = [
            {"label": "Non-Penalty xG / 90", "val": float(p90.get("xg_p90", 0.38)), "pct": int(p90.get("pct_xg", 85)), "format": "{:.2f}"},
            {"label": "Direct Assists (xA) / 90", "val": float(p90.get("xa_p90", 0.25)), "pct": int(p90.get("pct_xa", 78)), "format": "{:.2f}"},
            {"label": "Key Passes / 90", "val": float(p90.get("key_passes_p90", 1.8)), "pct": int(p90.get("pct_key_passes", 82)), "format": "{:.1f}"},
            {"label": "Progressive Carries / 90", "val": float(p90.get("prog_carries_p90", 4.2)), "pct": int(p90.get("pct_prog_carries", 88)), "format": "{:.1f}"},
            {"label": "Box Finishing Eff. %", "val": float(p90.get("conversion_rate_pct", attrs.get("Finishing", 78))), "pct": int(p90.get("pct_conversion", 84)), "format": "{:.1f}%"},
            {"label": "High Press Regains / 90", "val": float(p90.get("pressures_p90", 16.5) if "pressures_p90" in p90 else 2.8), "pct": int(p90.get("pct_press", 76)), "format": "{:.1f}"}
        ]
    elif pos_cat == "Defender":
        metrics = [
            {"label": "Tackles + Interceptions / 90", "val": float(p90.get("tackles_interceptions_p90", 4.8)), "pct": int(p90.get("pct_def_act", 88)), "format": "{:.2f}"},
            {"label": "Aerial Duel Win %", "val": float(p90.get("aerial_win_pct", 66.5)), "pct": int(p90.get("pct_aerial", 82)), "format": "{:.1f}%"},
            {"label": "Ground Duel Win %", "val": float(p90.get("duel_win_pct", 65.0)), "pct": int(p90.get("pct_duel", 84)), "format": "{:.1f}%"},
            {"label": "Progressive Passes / 90", "val": float(p90.get("prog_passes_p90", 4.9)), "pct": int(p90.get("pct_prog_pass", 80)), "format": "{:.1f}"},
            {"label": "Pass Completion %", "val": float(p90.get("pass_acc_pct", 86.0)), "pct": int(p90.get("pct_pass_acc", 86)), "format": "{:.1f}%"},
            {"label": "Box Recoveries / 90", "val": float(p90.get("recoveries_p90", 6.8)), "pct": int(p90.get("pct_recov", 79)), "format": "{:.1f}"}
        ]
    elif pos_cat == "Goalkeeper":
        metrics = [
            {"label": "Save Percentage %", "val": float(player.get("save_percentage", 80.0)), "pct": int(p90.get("pct_save_pct", 88)), "format": "{:.1f}%"},
            {"label": "Saves / 90 Minutes", "val": float(player.get("saves_p90", 3.2)), "pct": int(p90.get("pct_saves", 84)), "format": "{:.1f}"},
            {"label": "Post-Shot xG Prevented / 90", "val": float(p90.get("psxg_diff_p90", 0.28)), "pct": int(p90.get("pct_psxg", 90)), "format": "+{:.2f}"},
            {"label": "Pass Accuracy %", "val": float(player.get("pass_acc_pct", 76.5)), "pct": int(p90.get("pct_pass_acc", 78)), "format": "{:.1f}%"},
            {"label": "Clean Sheet Ratio %", "val": float((player.get("clean_sheets_26_27", 3) / max(1, player.get("apps_26_27", 5))) * 100), "pct": int(p90.get("pct_cs", 85)), "format": "{:.0f}%"},
            {"label": "Cross Claim Dominance", "val": float(attrs.get("Command of Area", 78)), "pct": int(p90.get("pct_command", 80)), "format": "{:.0f}"}
        ]
    else: # Midfielders
        metrics = [
            {"label": "Pass Completion %", "val": float(p90.get("pass_acc_pct", 87.5)), "pct": int(p90.get("pct_pass_acc", 91)), "format": "{:.1f}%"},
            {"label": "Progressive Passes / 90", "val": float(p90.get("prog_passes_p90", 6.5)), "pct": int(p90.get("pct_prog_pass", 89)), "format": "{:.1f}"},
            {"label": "Key Passes / 90", "val": float(p90.get("key_passes_p90", 2.1)), "pct": int(p90.get("pct_key_pass", 84)), "format": "{:.1f}"},
            {"label": "Tackles + Interceptions / 90", "val": float(p90.get("tackles_interceptions_p90", 4.1)), "pct": int(p90.get("pct_def_act", 82)), "format": "{:.1f}"},
            {"label": "Ball Recoveries / 90", "val": float(p90.get("recoveries_p90", 6.9)), "pct": int(p90.get("pct_recov", 85)), "format": "{:.1f}"},
            {"label": "Ground Duel Win %", "val": float(p90.get("duel_win_pct", 61.5)), "pct": int(p90.get("pct_duel", 80)), "format": "{:.1f}%"}
        ]

    labels = [m["label"] for m in metrics][::-1] # reverse for top-down display
    pcts = [max(10, min(99, m["pct"])) for m in metrics][::-1]
    raw_texts = [f"{m['format'].format(m['val'])} ({m['pct']}th percentile)" for m in metrics][::-1]

    colors = []
    for p in pcts:
        if p >= 85:
            colors.append("#10b981") # Top Tier (Green)
        elif p >= 70:
            colors.append("#f59e0b") # Above Average (Amber)
        elif p >= 50:
            colors.append("#38bdf8") # Neutral (Sky Blue)
        else:
            colors.append("#94a3b8") # Slate (Developing)

    fig = go.Figure()

    # Background reference bar (100th percentile)
    fig.add_trace(go.Bar(
        y=labels,
        x=[100] * len(labels),
        orientation='h',
        marker=dict(color="rgba(255, 255, 255, 0.08)"),
        hoverinfo="none",
        showlegend=False
    ))

    # Actual Percentile Bar
    fig.add_trace(go.Bar(
        y=labels,
        x=pcts,
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color="#111827", width=1)
        ),
        text=raw_texts,
        textposition="inside",
        insidetextanchor="end",
        textfont=dict(color="#ffffff", size=11, family="Arial"),
        name="Percentile Rank",
        showlegend=False
    ))

    # Reference 50th percentile vertical line
    fig.add_vline(x=50, line_dash="dash", line_color="rgba(255,255,255,0.35)", annotation_text="50th Pct Median", annotation_font_size=10, annotation_font_color="#94a3b8")

    fig.update_layout(
        barmode="overlay",
        title=dict(
            text=f"<b>Statistical Percentile Profile</b> (vs {positional_benchmark_label})",
            font=dict(color="#f4d03f", size=13)
        ),
        xaxis=dict(
            title="Percentile Rank (0 to 100)",
            range=[0, 105],
            gridcolor="rgba(255, 255, 255, 0.08)",
            tickfont=dict(color="#94a3b8")
        ),
        yaxis=dict(
            tickfont=dict(color="#f8fafc", size=11)
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=170, r=30, t=40, b=40),
        height=320
    )

    return fig
