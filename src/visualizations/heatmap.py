import plotly.graph_objects as go
import numpy as np

def generate_player_heatmap(player_name: str, position: str, heatmap_type: str = None):
    """
    Generates a realistic 2D tactical touch & action density heatmap
    rendered directly onto an authentic football pitch (SofaScore / WhoScored style).
    """
    # Define pitch coordinates (105m length x 68m width)
    x_dim = 105
    y_dim = 68

    # Determine distribution centers based on position and role
    pos_lower = position.lower()
    
    # Defaults
    np.random.seed(abs(hash(player_name)) % 100000)
    num_events = 220

    if "goalkeeper" in pos_lower or heatmap_type == "goalkeeper":
        # Centered in defensive 6-yard and 18-yard box
        x_pts = np.random.normal(loc=10, scale=4.5, size=num_events)
        y_pts = np.random.normal(loc=34, scale=9.0, size=num_events)
    elif "centre-back" in pos_lower or "defender" in pos_lower and "back" not in pos_lower:
        # Central defensive third & middle third build up
        x1 = np.random.normal(loc=26, scale=7.0, size=int(num_events * 0.6))
        y1 = np.random.normal(loc=34, scale=12.0, size=int(num_events * 0.6))
        x2 = np.random.normal(loc=44, scale=6.0, size=int(num_events * 0.4))
        y2 = np.random.normal(loc=34, scale=10.0, size=int(num_events * 0.4))
        x_pts = np.concatenate([x1, x2])
        y_pts = np.concatenate([y1, y2])
    elif "left-back" in pos_lower:
        # Left flank up and down, defensive 3rd into final 3rd
        x1 = np.random.normal(loc=35, scale=10.0, size=int(num_events * 0.5))
        y1 = np.random.normal(loc=58, scale=5.0, size=int(num_events * 0.5))
        x2 = np.random.normal(loc=65, scale=12.0, size=int(num_events * 0.5))
        y2 = np.random.normal(loc=60, scale=4.5, size=int(num_events * 0.5))
        x_pts = np.concatenate([x1, x2])
        y_pts = np.concatenate([y1, y2])
    elif "right-back" in pos_lower or heatmap_type == "wing_back_right":
        # Right flank up and down
        x1 = np.random.normal(loc=35, scale=10.0, size=int(num_events * 0.5))
        y1 = np.random.normal(loc=10, scale=5.0, size=int(num_events * 0.5))
        x2 = np.random.normal(loc=65, scale=12.0, size=int(num_events * 0.5))
        y2 = np.random.normal(loc=8, scale=4.5, size=int(num_events * 0.5))
        x_pts = np.concatenate([x1, x2])
        y_pts = np.concatenate([y1, y2])
    elif "defensive midfield" in pos_lower:
        # Deep central anchor
        x_pts = np.random.normal(loc=42, scale=8.0, size=num_events)
        y_pts = np.random.normal(loc=34, scale=12.0, size=num_events)
    elif "central midfield" in pos_lower:
        # Middle third box-to-box
        x_pts = np.random.normal(loc=52, scale=14.0, size=num_events)
        y_pts = np.random.normal(loc=34, scale=14.0, size=num_events)
    elif "right winger" in pos_lower or heatmap_type == "inverted_winger_right":
        # Right flank into penalty box half-space
        x1 = np.random.normal(loc=76, scale=10.0, size=int(num_events * 0.55))
        y1 = np.random.normal(loc=14, scale=5.0, size=int(num_events * 0.55))
        x2 = np.random.normal(loc=88, scale=7.0, size=int(num_events * 0.45))
        y2 = np.random.normal(loc=26, scale=6.5, size=int(num_events * 0.45))
        x_pts = np.concatenate([x1, x2])
        y_pts = np.concatenate([y1, y2])
    elif "left winger" in pos_lower or heatmap_type == "inverted_winger_left":
        # Left flank cutting inside
        x1 = np.random.normal(loc=76, scale=10.0, size=int(num_events * 0.55))
        y1 = np.random.normal(loc=54, scale=5.0, size=int(num_events * 0.55))
        x2 = np.random.normal(loc=88, scale=7.0, size=int(num_events * 0.45))
        y2 = np.random.normal(loc=42, scale=6.5, size=int(num_events * 0.45))
        x_pts = np.concatenate([x1, x2])
        y_pts = np.concatenate([y1, y2])
    else:
        # Striker / Centre-Forward: penalty box, 18-yard arc, central attacking channel
        x1 = np.random.normal(loc=88, scale=7.5, size=int(num_events * 0.7))
        y1 = np.random.normal(loc=34, scale=10.0, size=int(num_events * 0.7))
        x2 = np.random.normal(loc=72, scale=8.0, size=int(num_events * 0.3))
        y2 = np.random.normal(loc=34, scale=12.0, size=int(num_events * 0.3))
        x_pts = np.concatenate([x1, x2])
        y_pts = np.concatenate([y1, y2])

    # Clip within pitch dimensions
    x_pts = np.clip(x_pts, 3, 102)
    y_pts = np.clip(y_pts, 3, 65)

    # Calculate zone percentages
    def_third = np.sum(x_pts < 35) / len(x_pts) * 100
    mid_third = np.sum((x_pts >= 35) & (x_pts <= 70)) / len(x_pts) * 100
    att_third = np.sum(x_pts > 70) / len(x_pts) * 100

    left_flank = np.sum(y_pts > 45) / len(y_pts) * 100
    central_chan = np.sum((y_pts >= 23) & (y_pts <= 45)) / len(y_pts) * 100
    right_flank = np.sum(y_pts < 23) / len(y_pts) * 100

    # Build figure with 2D density contour
    fig = go.Figure()

    # Pitch markings
    line_col = "rgba(255, 255, 255, 0.7)"
    
    # 2D Density Contour Heatmap
    fig.add_trace(go.Histogram2dContour(
        x=x_pts,
        y=y_pts,
        colorscale=[
            [0.0, 'rgba(15, 23, 42, 0.0)'],
            [0.2, 'rgba(30, 144, 255, 0.45)'],
            [0.45, 'rgba(46, 204, 113, 0.65)'],
            [0.7, 'rgba(241, 196, 15, 0.8)'],
            [0.9, 'rgba(231, 76, 60, 0.9)'],
            [1.0, 'rgba(192, 57, 43, 0.98)']
        ],
        showscale=False,
        contours=dict(coloring='heatmap', showlines=False),
        ncontours=28,
        opacity=0.88,
        hoverinfo='none'
    ))

    # Add Scatter dots with low opacity for raw action points
    fig.add_trace(go.Scatter(
        x=x_pts,
        y=y_pts,
        mode='markers',
        marker=dict(size=4.5, color='rgba(255, 255, 255, 0.25)'),
        hoverinfo='skip',
        showlegend=False
    ))

    # Pitch Outline
    fig.add_shape(type="rect", x0=2, y0=2, x1=103, y1=66, line=dict(color=line_col, width=2))
    # Halfway Line
    fig.add_shape(type="line", x0=52.5, y0=2, x1=52.5, y1=66, line=dict(color=line_col, width=1.8))
    # Centre Circle
    fig.add_shape(type="circle", x0=52.5 - 9.15, y0=34 - 9.15, x1=52.5 + 9.15, y1=34 + 9.15, line=dict(color=line_col, width=1.8))
    fig.add_shape(type="circle", x0=52.5 - 0.5, y0=34 - 0.5, x1=52.5 + 0.5, y1=34 + 0.5, fillcolor=line_col, line=dict(color=line_col))
    
    # Left Penalty Box & 6yd box
    fig.add_shape(type="rect", x0=2, y0=13.84, x1=18.5, y1=54.16, line=dict(color=line_col, width=1.8))
    fig.add_shape(type="rect", x0=2, y0=24.84, x1=7.5, y1=43.16, line=dict(color=line_col, width=1.8))
    
    # Right Penalty Box & 6yd box
    fig.add_shape(type="rect", x0=103 - 16.5, y0=13.84, x1=103, y1=54.16, line=dict(color=line_col, width=1.8))
    fig.add_shape(type="rect", x0=103 - 5.5, y0=24.84, x1=103, y1=43.16, line=dict(color=line_col, width=1.8))

    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1, 106]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1, 69]),
        paper_bgcolor="#0b1017",
        plot_bgcolor="#0e1724",
        margin=dict(l=5, r=5, t=10, b=10),
        height=380,
        dragmode=False
    )

    zone_stats = {
        "def_third": round(def_third, 1),
        "mid_third": round(mid_third, 1),
        "att_third": round(att_third, 1),
        "left_flank": round(left_flank, 1),
        "central_chan": round(central_chan, 1),
        "right_flank": round(right_flank, 1)
    }

    return fig, zone_stats
