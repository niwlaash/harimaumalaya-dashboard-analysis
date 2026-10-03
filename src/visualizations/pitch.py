import plotly.graph_objects as go
import pandas as pd

def draw_tactical_pitch(formation: str = "4-3-3", squad_df: pd.DataFrame = None):
    """
    Renders an interactive 2D football pitch with starting XI and positional nodes
    using Plotly for Streamlit.
    """
    fig = go.Figure()

    # Pitch boundary & grass styling
    pitch_length = 105
    pitch_width = 68

    # Grass background
    fig.add_shape(
        type="rect",
        x0=0, y0=0, x1=pitch_length, y1=pitch_width,
        fillcolor="#143820",
        line=dict(color="#2e6930", width=2),
        layer="below"
    )

    # Pitch markings (Lines)
    line_color = "rgba(255, 255, 255, 0.65)"
    
    # Outer lines
    fig.add_shape(type="rect", x0=2, y0=2, x1=103, y1=66, line=dict(color=line_color, width=2))
    
    # Halfway line
    fig.add_shape(type="line", x0=52.5, y0=2, x1=52.5, y1=66, line=dict(color=line_color, width=2))
    
    # Centre circle
    fig.add_shape(type="circle", x0=52.5 - 9.15, y0=34 - 9.15, x1=52.5 + 9.15, y1=34 + 9.15, line=dict(color=line_color, width=2))
    fig.add_shape(type="circle", x0=52.5 - 0.6, y0=34 - 0.6, x1=52.5 + 0.6, y1=34 + 0.6, fillcolor=line_color, line=dict(color=line_color))

    # Left Penalty box & 6-yard box
    fig.add_shape(type="rect", x0=2, y0=13.84, x1=18.5, y1=54.16, line=dict(color=line_color, width=2))
    fig.add_shape(type="rect", x0=2, y0=24.84, x1=7.5, y1=43.16, line=dict(color=line_color, width=2))
    fig.add_shape(type="circle", x0=13 - 0.5, y0=34 - 0.5, x1=13 + 0.5, y1=34 + 0.5, fillcolor=line_color, line=dict(color=line_color))

    # Right Penalty box & 6-yard box
    fig.add_shape(type="rect", x0=103 - 16.5, y0=13.84, x1=103, y1=54.16, line=dict(color=line_color, width=2))
    fig.add_shape(type="rect", x0=103 - 5.5, y0=24.84, x1=103, y1=43.16, line=dict(color=line_color, width=2))
    fig.add_shape(type="circle", x0=92 - 0.5, y0=34 - 0.5, x1=92 + 0.5, y1=34 + 0.5, fillcolor=line_color, line=dict(color=line_color))

    # Formations coordinates mapping (Left to Right: GK on left, Attack on right)
    coords_dict = {
        "4-3-3": [
            {"role": "GK", "name": "Syihan Hazmi", "x": 8, "y": 34},
            {"role": "LB", "name": "Corbin-Ong", "x": 28, "y": 56},
            {"role": "LCB", "name": "Brad Tapp", "x": 24, "y": 42},
            {"role": "RCB", "name": "Ubaidullah Shamsul", "x": 24, "y": 26},
            {"role": "RB", "name": "Dion Cools", "x": 28, "y": 12},
            {"role": "DM", "name": "Hong Wan", "x": 45, "y": 34},
            {"role": "LCM", "name": "Nooa Laine", "x": 58, "y": 48},
            {"role": "RCM", "name": "Stuart Wilkin", "x": 58, "y": 20},
            {"role": "LW", "name": "Faisal Halim", "x": 82, "y": 55},
            {"role": "ST", "name": "Bérgson", "x": 88, "y": 34},
            {"role": "RW", "name": "Arif Aiman", "x": 82, "y": 13},
        ],
        "3-4-3": [
            {"role": "GK", "name": "Syihan Hazmi", "x": 8, "y": 34},
            {"role": "LCB", "name": "Harith Haiqal", "x": 24, "y": 48},
            {"role": "CB", "name": "Brad Tapp", "x": 22, "y": 34},
            {"role": "RCB", "name": "Dion Cools", "x": 24, "y": 20},
            {"role": "LWB", "name": "Corbin-Ong", "x": 48, "y": 58},
            {"role": "LCM", "name": "Nooa Laine", "x": 46, "y": 40},
            {"role": "RCM", "name": "Stuart Wilkin", "x": 46, "y": 28},
            {"role": "RWB", "name": "Quentin Cheng", "x": 48, "y": 10},
            {"role": "LW", "name": "Faisal Halim", "x": 80, "y": 54},
            {"role": "ST", "name": "Paulo Josué", "x": 86, "y": 34},
            {"role": "RW", "name": "Arif Aiman", "x": 80, "y": 14},
        ],
        "4-2-3-1": [
            {"role": "GK", "name": "Syihan Hazmi", "x": 8, "y": 34},
            {"role": "LB", "name": "Daniel Ting", "x": 28, "y": 56},
            {"role": "LCB", "name": "Brad Tapp", "x": 24, "y": 42},
            {"role": "RCB", "name": "Harith Haiqal", "x": 24, "y": 26},
            {"role": "RB", "name": "Dion Cools", "x": 28, "y": 12},
            {"role": "LDM", "name": "Hong Wan", "x": 44, "y": 42},
            {"role": "RDM", "name": "Nooa Laine", "x": 44, "y": 26},
            {"role": "AM", "name": "Paulo Josué", "x": 65, "y": 34},
            {"role": "LW", "name": "Faisal Halim", "x": 78, "y": 54},
            {"role": "RW", "name": "Manuel Hidalgo", "x": 78, "y": 14},
            {"role": "ST", "name": "Bérgson", "x": 88, "y": 34},
        ]
    }

    positions = coords_dict.get(formation, coords_dict["4-3-3"])

    # Match player stats if squad_df is provided
    x_coords, y_coords, hover_texts, labels, colors = [], [], [], [], []

    for pos in positions:
        x_coords.append(pos["x"])
        y_coords.append(pos["y"])
        role = pos["role"]
        p_name = pos["name"]
        
        info_text = f"<b>{p_name}</b> ({role})<br>"
        if squad_df is not None:
            matches = squad_df[squad_df["name"].str.contains(p_name.split()[0], case=False, na=False)]
            if not matches.empty:
                row = matches.iloc[0]
                info_text += (
                    f"Club: {row['club']}<br>"
                    f"26/27 Mins: {row['minutes_26_27']}'<br>"
                    f"FotMob Rating: {row.get('fotmob_rating', 'N/A')}<br>"
                    f"Market Value: €{row.get('market_value_eur', 0):,}"
                )
        hover_texts.append(info_text)
        labels.append(f"<b>{role}</b><br>{p_name}")
        
        if "GK" in role:
            colors.append("#ffb703") # Gold/Yellow for GK
        elif any(r in role for r in ["CB", "LB", "RB", "WB"]):
            colors.append("#219ebc") # Blue for DEF
        elif any(r in role for r in ["DM", "CM", "AM"]):
            colors.append("#023047") # Dark navy for MID
        else:
            colors.append("#e63946") # Crimson Red for ATT

    fig.add_trace(
        go.Scatter(
            x=x_coords,
            y=y_coords,
            mode="markers+text",
            marker=dict(
                size=36,
                color=colors,
                line=dict(color="#f4d03f", width=2.5),
                symbol="circle"
            ),
            text=labels,
            textposition="bottom center",
            textfont=dict(color="#ffffff", size=11, family="Arial, sans-serif"),
            hoverinfo="text",
            hovertext=hover_texts,
            showlegend=False
        )
    )

    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-2, 107]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-5, 75]),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=5, r=5, t=10, b=10),
        height=520,
        dragmode=False
    )

    return fig
