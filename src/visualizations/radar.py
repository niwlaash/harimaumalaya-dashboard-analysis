import plotly.graph_objects as go

def create_attribute_radar(player: dict, title: str = None):
    """
    Creates a single player multi-attribute radar chart (FIFA/SofaScore style).
    """
    attributes = player.get("attributes", {})
    if not attributes:
        attributes = {"Pace": 70, "Shooting": 70, "Passing": 70, "Dribbling": 70, "Defending": 70, "Physical": 70}

    categories = list(attributes.keys())
    values = list(attributes.values())
    
    # Close polygon loop
    categories.append(categories[0])
    values.append(values[0])

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(244, 208, 63, 0.35)',
        line=dict(color='#f4d03f', width=2.5),
        name=player.get("name", "Player")
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showticklabels=True,
                ticks="outside",
                tickfont=dict(size=10, color="#cccccc"),
                gridcolor="rgba(255,255,255,0.2)"
            ),
            angularaxis=dict(
                gridcolor="rgba(255,255,255,0.2)",
                tickfont=dict(size=12, color="#ffffff")
            ),
            bgcolor="rgba(20, 24, 33, 0.8)"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        title=dict(
            text=title or f"Attribute Profile: {player.get('name', 'Player')}",
            font=dict(color="#f4d03f", size=14)
        ),
        margin=dict(l=40, r=40, t=50, b=40),
        height=400
    )
    return fig

def create_comparison_radar(p1: dict, p2: dict, p3: dict = None):
    """
    Creates a multi-player radar comparison chart.
    """
    # Unify categories
    attr1 = p1.get("attributes", {})
    attr2 = p2.get("attributes", {})
    
    # Use common keys or standard fallback
    all_keys = list(dict.fromkeys(list(attr1.keys()) + list(attr2.keys())))
    if len(all_keys) < 4:
        all_keys = ["Pace", "Shooting", "Passing", "Dribbling", "Defending", "Physical"]

    v1 = [attr1.get(k, 70) for k in all_keys]
    v2 = [attr2.get(k, 70) for k in all_keys]

    # Close loops
    keys_closed = all_keys + [all_keys[0]]
    v1_closed = v1 + [v1[0]]
    v2_closed = v2 + [v2[0]]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=v1_closed,
        theta=keys_closed,
        fill='toself',
        fillcolor='rgba(244, 208, 63, 0.3)',
        line=dict(color='#f4d03f', width=2.5),
        name=p1.get("name", "Player 1")
    ))

    fig.add_trace(go.Scatterpolar(
        r=v2_closed,
        theta=keys_closed,
        fill='toself',
        fillcolor='rgba(52, 152, 219, 0.3)',
        line=dict(color='#3498db', width=2.5),
        name=p2.get("name", "Player 2")
    ))

    if p3:
        attr3 = p3.get("attributes", {})
        v3 = [attr3.get(k, 70) for k in all_keys]
        v3_closed = v3 + [v3[0]]
        fig.add_trace(go.Scatterpolar(
            r=v3_closed,
            theta=keys_closed,
            fill='toself',
            fillcolor='rgba(231, 76, 60, 0.3)',
            line=dict(color='#e74c3c', width=2.5),
            name=p3.get("name", "Player 3")
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.2)"),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.2)", tickfont=dict(color="#ffffff")),
            bgcolor="rgba(20, 24, 33, 0.8)"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(font=dict(color="#ffffff"), orientation="h", y=-0.15),
        margin=dict(l=40, r=40, t=40, b=50),
        height=450
    )
    return fig

# Alias for consistent naming
create_player_attribute_radar = create_attribute_radar

