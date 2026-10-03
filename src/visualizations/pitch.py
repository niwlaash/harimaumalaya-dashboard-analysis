import plotly.graph_objects as go
import pandas as pd

def draw_tactical_pitch(formation: str = "4-3-3", starting_xi_players: list = None):
    """
    Renders an editorial-grade, professional 2D tactical football pitch
    (inspired by Opta Analyst and StatsBomb) for starting XI and positional depth analysis.
    """
    fig = go.Figure()

    pitch_length = 105
    pitch_width = 68

    # Professional dark pitch canvas
    fig.add_shape(
        type="rect",
        x0=0, y0=0, x1=pitch_length, y1=pitch_width,
        fillcolor="#0e131b",
        line=dict(color="#1a2332", width=2),
        layer="below"
    )

    # Subtle pitch mowing cuts
    for stripe in range(0, 105, 15):
        fig.add_shape(
            type="rect",
            x0=stripe, y0=0, x1=min(105, stripe + 7.5), y1=pitch_width,
            fillcolor="#111722",
            line=dict(color="rgba(0,0,0,0)"),
            layer="below"
        )

    # Crisp pitch markings
    line_color = "rgba(255, 255, 255, 0.45)"
    
    # Outer touchlines & goal lines
    fig.add_shape(type="rect", x0=2, y0=2, x1=103, y1=66, line=dict(color=line_color, width=1.5))
    
    # Halfway line
    fig.add_shape(type="line", x0=52.5, y0=2, x1=52.5, y1=66, line=dict(color=line_color, width=1.5))
    
    # Centre circle & spot
    fig.add_shape(type="circle", x0=52.5 - 9.15, y0=34 - 9.15, x1=52.5 + 9.15, y1=34 + 9.15, line=dict(color=line_color, width=1.5))
    fig.add_shape(type="circle", x0=52.5 - 0.5, y0=34 - 0.5, x1=52.5 + 0.5, y1=34 + 0.5, fillcolor=line_color, line=dict(color=line_color))

    # Left Penalty box & 6-yard box
    fig.add_shape(type="rect", x0=2, y0=13.84, x1=18.5, y1=54.16, line=dict(color=line_color, width=1.5))
    fig.add_shape(type="rect", x0=2, y0=24.84, x1=7.5, y1=43.16, line=dict(color=line_color, width=1.5))
    fig.add_shape(type="circle", x0=13 - 0.5, y0=34 - 0.5, x1=13 + 0.5, y1=34 + 0.5, fillcolor=line_color, line=dict(color=line_color))

    # Right Penalty box & 6-yard box
    fig.add_shape(type="rect", x0=103 - 16.5, y0=13.84, x1=103, y1=54.16, line=dict(color=line_color, width=1.5))
    fig.add_shape(type="rect", x0=103 - 5.5, y0=24.84, x1=103, y1=43.16, line=dict(color=line_color, width=1.5))
    fig.add_shape(type="circle", x0=92 - 0.5, y0=34 - 0.5, x1=92 + 0.5, y1=34 + 0.5, fillcolor=line_color, line=dict(color=line_color))

    # Coordinate mapping
    coords_dict = {
        "4-3-3": [
            {"slot": 0, "role": "GK", "x": 8, "y": 34},
            {"slot": 1, "role": "LB", "x": 28, "y": 56},
            {"slot": 2, "role": "LCB", "x": 23, "y": 42},
            {"slot": 3, "role": "RCB", "x": 23, "y": 26},
            {"slot": 4, "role": "RB", "x": 28, "y": 12},
            {"slot": 5, "role": "DM", "x": 42, "y": 34},
            {"slot": 6, "role": "LCM", "x": 56, "y": 48},
            {"slot": 7, "role": "RCM", "x": 56, "y": 20},
            {"slot": 8, "role": "LW", "x": 80, "y": 55},
            {"slot": 9, "role": "CF", "x": 88, "y": 34},
            {"slot": 10, "role": "RW", "x": 80, "y": 13},
        ],
        "3-4-3": [
            {"slot": 0, "role": "GK", "x": 8, "y": 34},
            {"slot": 1, "role": "LCB", "x": 23, "y": 49},
            {"slot": 2, "role": "CB", "x": 21, "y": 34},
            {"slot": 3, "role": "RCB", "x": 23, "y": 19},
            {"slot": 4, "role": "LWB", "x": 46, "y": 58},
            {"slot": 5, "role": "LCM", "x": 46, "y": 40},
            {"slot": 6, "role": "RCM", "x": 46, "y": 28},
            {"slot": 7, "role": "RWB", "x": 46, "y": 10},
            {"slot": 8, "role": "LW", "x": 80, "y": 54},
            {"slot": 9, "role": "CF", "x": 88, "y": 34},
            {"slot": 10, "role": "RW", "x": 80, "y": 14},
        ],
        "4-2-3-1": [
            {"slot": 0, "role": "GK", "x": 8, "y": 34},
            {"slot": 1, "role": "LB", "x": 28, "y": 56},
            {"slot": 2, "role": "LCB", "x": 23, "y": 42},
            {"slot": 3, "role": "RCB", "x": 23, "y": 26},
            {"slot": 4, "role": "RB", "x": 28, "y": 12},
            {"slot": 5, "role": "LDM", "x": 44, "y": 42},
            {"slot": 6, "role": "RDM", "x": 44, "y": 26},
            {"slot": 7, "role": "AM", "x": 66, "y": 34},
            {"slot": 8, "role": "LW", "x": 80, "y": 54},
            {"slot": 9, "role": "CF", "x": 88, "y": 34},
            {"slot": 10, "role": "RW", "x": 80, "y": 14},
        ]
    }

    positions = coords_dict.get(formation, coords_dict["4-3-3"])
    x_coords, y_coords, hover_texts, labels, colors = [], [], [], [], []

    for i, pos in enumerate(positions):
        x_coords.append(pos["x"])
        y_coords.append(pos["y"])
        role = pos["role"]
        
        p_name = f"Player {i+1}"
        club = "Club"
        rating = "7.0"
        mins = "0"
        
        if starting_xi_players and i < len(starting_xi_players):
            p = starting_xi_players[i]
            p_name = p.get("name", p_name)
            club = p.get("club", club)
            rating = p.get("fotmob_rating", p.get("sofascore_rating", "7.0"))
            mins = p.get("minutes_26_27", "0")

        hover_text = (
            f"<b>{p_name}</b> ({role})<br>"
            f"Club: {club}<br>"
            f"26/27 Mins: {mins}'<br>"
            f"Avg Rating: {rating}"
        )
        hover_texts.append(hover_text)
        labels.append(f"<b>{role}</b><br>{p_name.split()[-1] if ' ' in p_name else p_name}")

        # Position colors (Editorial Opta style palette)
        if "GK" in role:
            colors.append("#eab308") # Gold
        elif any(r in role for r in ["CB", "LB", "RB", "WB"]):
            colors.append("#0284c7") # Deep Sky
        elif any(r in role for r in ["DM", "CM", "AM"]):
            colors.append("#0d9488") # Teal
        else:
            colors.append("#e11d48") # Crimson

    fig.add_trace(
        go.Scatter(
            x=x_coords,
            y=y_coords,
            mode="markers+text",
            marker=dict(
                size=32,
                color=colors,
                line=dict(color="#ffffff", width=1.8),
                symbol="circle"
            ),
            text=labels,
            textposition="bottom center",
            textfont=dict(color="#f8fafc", size=10, family="Segoe UI, sans-serif"),
            hoverinfo="text",
            hovertext=hover_texts,
            showlegend=False
        )
    )

    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-2, 107]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-6, 74]),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=5, r=5, t=10, b=10),
        height=470,
        dragmode=False
    )

    return fig
