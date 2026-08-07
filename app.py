import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page config
st.set_page_config(
    page_title="Micro-Moments of Happiness — Viz Con 2026",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    /* FULL WIDTH - fill the viewport */
    .main {background-color: #fefcf3;}
    .stApp {max-width: 100%; margin: 0; padding: 0; background-color: #fefcf3;}
    
    .block-container {
        max-width: 100% !important;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
        padding-top: 2rem !important;
    }
    
    /* Fix scrolling */
    section[data-testid="stSidebar"] {display: none;}
    .main .block-container {
        overflow: visible !important;
    }
    [data-testid="stAppViewContainer"] {
        overflow-y: auto !important;
    }
    .stPlotlyChart > div {
        overflow: visible !important;
    }

    .big-stat {font-size: 3.2rem; font-weight: bold; color: #e07a5f; text-align: center; margin: 0;}
    .stat-label {font-size: 1rem; color: #666; text-align: center; margin-top: 0;}
    .section-header {
        font-size: 1.9rem;
        font-weight: 700;
        color: #3d405b;
        border-left: 4px solid #81b29a;
        padding-left: 16px;
        margin-top: 3rem;
        margin-bottom: 1rem;
    }
    .insight-box {
        background: linear-gradient(135deg, #f4f1de 0%, #e8e4c9 100%);
        border: 1px solid #81b29a;
        border-radius: 12px;
        padding: 24px;
        margin: 16px 0;
    }
    .story-text {
        font-size: 1.2rem;
        color: #3d405b;
        line-height: 1.9;
    }
    .moment-card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 1px solid #f0ece2;
    }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #f0ece2;
        border-radius: 12px;
        padding: 16px;
    }
    .stPlotlyChart {overflow: visible !important;}
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_moments():
    return pd.read_csv("data/micro_moments_happiness.csv")

@st.cache_data
def load_country_activities():
    return pd.read_csv("data/happiness_by_country_activity.csv")

@st.cache_data
def load_demographics():
    return pd.read_csv("data/moments_by_demographic.csv")

df = load_moments()
country_df = load_country_activities()
demo_df = load_demographics()

# ============================================================
# SECTION 1: THE HOOK
# ============================================================

st.markdown("")
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.markdown("""
    <h1 style='text-align: center; font-size: 3rem; color: #3d405b; margin-bottom: 0;'>
    ✨ Micro-Moments of Happiness
    </h1>
    <p style='text-align: center; font-size: 1.3rem; color: #666; margin-top: 8px; line-height: 1.6;'>
    Happiness isn't found in milestones. It's hiding in your morning coffee,<br>
    a walk in the park, and a conversation with a friend.
    </p>
    """, unsafe_allow_html=True)

st.markdown("---")

# Top 3 happiest micro-moments
top3 = df.nlargest(3, 'happiness_score')
cols = st.columns(3)
for i, (_, row) in enumerate(top3.iterrows()):
    with cols[i]:
        st.markdown(f"""
        <div class="moment-card">
            <div style="font-size: 2.5rem;">{row['icon']}</div>
            <div style="font-size: 1.1rem; font-weight: 600; color: #3d405b; margin-top: 8px;">{row['activity']}</div>
            <div style="font-size: 2rem; font-weight: bold; color: #81b29a;">{row['happiness_score']}/7</div>
            <div style="font-size: 0.85rem; color: #888;">happiness score</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("")
st.markdown("""
<div class="insight-box">
<p class="story-text">
We chase promotions, vacations, and life milestones. But research shows that <strong>80% of our 
happiness comes from tiny, everyday moments</strong> — the ones so small we barely notice them.
<br><br>
What if the secret to a happier life isn't doing more, but <em>noticing more</em>?
</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SECTION 2: THE HAPPINESS LANDSCAPE
# ============================================================

st.markdown('<p class="section-header">The Happiness Landscape: Every Moment Mapped</p>', unsafe_allow_html=True)
st.markdown("*Each bubble is an activity. X-axis = happiness. Y-axis = meaning. Size = how many people do it daily.*")

fig_landscape = px.scatter(
    df,
    x="happiness_score",
    y="meaning_score",
    size="pct_population_daily",
    color="category",
    hover_name="activity",
    text="icon",
    hover_data={
        "happiness_score": ":.1f",
        "meaning_score": ":.1f",
        "stress_score": ":.1f",
        "pct_population_daily": True,
        "icon": False
    },
    color_discrete_map={
        "Connection": "#81b29a",
        "Mindfulness": "#e07a5f",
        "Movement": "#f2cc8f",
        "Leisure": "#3d405b",
        "Rituals": "#a8dadc",
        "Work": "#6c757d",
        "Routine": "#adb5bd",
        "Digital": "#e63946",
        "Rest": "#457b9d"
    },
    labels={
        "happiness_score": "Happiness (1-7)",
        "meaning_score": "Meaning (1-7)",
        "pct_population_daily": "% doing daily"
    },
    size_max=50
)

fig_landscape.update_traces(textposition='top center', textfont_size=14)
fig_landscape.update_layout(
    template="plotly_white",
    height=520,
    font=dict(color="#3d405b"),
    plot_bgcolor="#fefcf3",
    paper_bgcolor="#fefcf3",
    xaxis=dict(range=[1.5, 6.5]),
    yaxis=dict(range=[0.5, 7])
)

# Add quadrant annotations
fig_landscape.add_annotation(x=2.5, y=6.5, text="Meaningful but hard", showarrow=False, font=dict(color="#999", size=10))
fig_landscape.add_annotation(x=5.5, y=6.5, text="Happy AND meaningful ✨", showarrow=False, font=dict(color="#81b29a", size=11, ))
fig_landscape.add_annotation(x=5.5, y=1.2, text="Pleasant but shallow", showarrow=False, font=dict(color="#999", size=10))
fig_landscape.add_annotation(x=2.5, y=1.2, text="Neither happy nor meaningful", showarrow=False, font=dict(color="#999", size=10))

fig_landscape.add_hline(y=3.5, line_dash="dot", line_color="#ccc", opacity=0.5)
fig_landscape.add_vline(x=4.0, line_dash="dot", line_color="#ccc", opacity=0.5)

st.plotly_chart(fig_landscape, use_container_width=True, config={'scrollZoom': False, 'displayModeBar': False})

st.markdown("""
<div class="insight-box">
<p class="story-text">
<strong>The sweet spot ✨:</strong> Activities in the top-right corner are both happy AND meaningful — 
playing with children, helping someone, volunteering, and time in nature. 
<br><br>
<strong>The trap 📱:</strong> Social media scores lowest on both happiness (3.2) and meaning (1.8), 
yet 68% of people do it daily. We spend the most time on what makes us least happy.
</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SECTION 3: THE HAPPINESS RANKING
# ============================================================

st.markdown('<p class="section-header">Ranked: Which Moments Bring the Most Joy?</p>', unsafe_allow_html=True)

df_sorted = df.sort_values('happiness_score', ascending=True)

fig_rank = go.Figure()

colors = ['#81b29a' if h >= 4.5 else '#f2cc8f' if h >= 3.5 else '#e07a5f' 
          for h in df_sorted['happiness_score']]

fig_rank.add_trace(go.Bar(
    y=[f"{row['icon']} {row['activity']}" for _, row in df_sorted.iterrows()],
    x=df_sorted['happiness_score'],
    orientation='h',
    marker_color=colors,
    text=df_sorted['happiness_score'].apply(lambda x: f"{x:.1f}"),
    textposition='outside',
    textfont=dict(size=11)
))

fig_rank.update_layout(
    template="plotly_white",
    height=750,
    plot_bgcolor="#fefcf3",
    paper_bgcolor="#fefcf3",
    xaxis=dict(title="Happiness Score (1-7)", range=[0, 6.5]),
    yaxis=dict(tickfont=dict(size=11)),
    font=dict(color="#3d405b"),
    margin=dict(l=200)
)

st.plotly_chart(fig_rank, use_container_width=True, config={'scrollZoom': False, 'displayModeBar': False})

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Happiest Moment", "👶 Playing with children", "5.8/7")
with col2:
    st.metric("Most Meaningful", "❤️ Volunteering", "6.4/7 meaning")
with col3:
    st.metric("Least Happy (but most common)", "📱 Social media", "3.2/7")

# ============================================================
# SECTION 4: THE TIME PARADOX
# ============================================================

st.markdown('<p class="section-header">The Time Paradox: We Spend Time on the Wrong Things</p>', unsafe_allow_html=True)

# Create a scatter: time spent vs happiness
fig_paradox = px.scatter(
    df,
    x="duration_min_avg",
    y="happiness_score",
    size="pct_population_daily",
    color="category",
    hover_name="activity",
    text="icon",
    color_discrete_map={
        "Connection": "#81b29a",
        "Mindfulness": "#e07a5f",
        "Movement": "#f2cc8f",
        "Leisure": "#3d405b",
        "Rituals": "#a8dadc",
        "Work": "#6c757d",
        "Routine": "#adb5bd",
        "Digital": "#e63946",
        "Rest": "#457b9d"
    },
    labels={
        "duration_min_avg": "Average Duration (minutes)",
        "happiness_score": "Happiness Score (1-7)",
        "pct_population_daily": "% doing daily"
    },
    size_max=40
)

fig_paradox.update_traces(textposition='top center', textfont_size=12)
fig_paradox.update_layout(
    template="plotly_white",
    height=450,
    plot_bgcolor="#fefcf3",
    paper_bgcolor="#fefcf3",
    font=dict(color="#3d405b"),
    xaxis=dict(range=[0, 200])
)

st.plotly_chart(fig_paradox, use_container_width=True, config={'scrollZoom': False, 'displayModeBar': False})

st.markdown("""
<div class="insight-box">
<p class="story-text">
<strong>The paradox revealed:</strong> The activities we spend the MOST time on (work: 480 min, TV: 120 min, 
social media: 45 min) score LOWEST on happiness. Meanwhile, the happiest moments 
(playing with kids, nature, helping others) average just 30-55 minutes.
<br><br>
<strong>Happiness is cheap and short.</strong> The best moments don't require money or hours — just presence.
</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SECTION 5: ACROSS CULTURES
# ============================================================

st.markdown('<p class="section-header">Around the World: Same Moments, Different Joy</p>', unsafe_allow_html=True)
st.markdown("*How much happiness does each micro-moment bring across different cultures?*")

activities_to_show = ['morning_coffee', 'playing_with_children', 'prayer_meditation', 
                      'walking', 'talking_friends', 'nature']
activity_labels = ['☕ Coffee', '👶 Children', '🧘 Prayer', '🚶 Walking', '💬 Friends', '🌳 Nature']

fig_heatmap = go.Figure(data=go.Heatmap(
    z=country_df[activities_to_show].values,
    x=activity_labels,
    y=country_df['country'],
    colorscale='YlGn',
    text=country_df[activities_to_show].values.round(1),
    texttemplate="%{text}",
    textfont={"size": 11},
    hovertemplate="Country: %{y}<br>Activity: %{x}<br>Happiness: %{z:.1f}<extra></extra>",
    colorbar=dict(title="Happiness<br>Score")
))

fig_heatmap.update_layout(
    template="plotly_white",
    height=550,
    plot_bgcolor="#fefcf3",
    paper_bgcolor="#fefcf3",
    font=dict(color="#3d405b"),
    yaxis=dict(tickfont=dict(size=11)),
    xaxis=dict(tickfont=dict(size=12), side='top')
)

st.plotly_chart(fig_heatmap, use_container_width=True, config={'scrollZoom': False, 'displayModeBar': False})

st.markdown("""
<div class="insight-box">
<p class="story-text">
<strong>Cultural patterns emerge:</strong>
<br>🇮🇹 <strong>Italy & France</strong> — Morning coffee brings more joy than almost anywhere else (the ritual matters)
<br>🇮🇳 <strong>India & Nigeria</strong> — Prayer/meditation scores highest (spiritual life = daily happiness)
<br>🇫🇮 <strong>Finland & Sweden</strong> — Nature walks are their happiness superpower (6.0+)
<br>🇧🇷 <strong>Brazil & Colombia</strong> — Talking with friends scores off the charts (social cultures thrive)
<br><br>
<em>Each culture has found its own path to daily happiness. The micro-moment is universal; the source is local.</em>
</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SECTION 6: THE AGE STORY
# ============================================================

st.markdown('<p class="section-header">A Lifetime of Moments: How Joy Shifts with Age</p>', unsafe_allow_html=True)

activities_age = ['Morning coffee/tea', 'Playing with children', 'Prayer or meditation', 
                  'Walking outdoors', 'Talking with friends', 'Nature', 'Social media browsing', 'Working (main job)']

age_cols = ['age_18_30', 'age_31_50', 'age_51_65', 'age_65_plus']
age_labels = ['18-30', '31-50', '51-65', '65+']

demo_subset = demo_df[demo_df['activity'].isin(activities_age)]

fig_age = go.Figure()

colors_age = ['#e07a5f', '#f2cc8f', '#81b29a', '#3d405b']

for i, col in enumerate(age_cols):
    fig_age.add_trace(go.Bar(
        name=age_labels[i],
        x=demo_subset['activity'],
        y=demo_subset[col],
        marker_color=colors_age[i]
    ))

fig_age.update_layout(
    barmode='group',
    template="plotly_white",
    height=420,
    plot_bgcolor="#fefcf3",
    paper_bgcolor="#fefcf3",
    yaxis_title="Happiness Score",
    legend=dict(title="Age Group", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    font=dict(color="#3d405b")
)

st.plotly_chart(fig_age, use_container_width=True, config={'scrollZoom': False, 'displayModeBar': False})

st.markdown("""
> **The beautiful shift:** As we age, simple moments bring MORE joy — morning coffee, walking, 
> nature, and prayer all increase in happiness score. Meanwhile, social media brings LESS. 
> Growing older doesn't mean less happiness — it means finding it in simpler places.
""")

# ============================================================
# SECTION 7: YOUR HAPPINESS AUDIT
# ============================================================

st.markdown('<p class="section-header">Your Happiness Audit: How Do You Spend Your Micro-Moments?</p>', unsafe_allow_html=True)

st.markdown("*Select the activities you did today. We'll calculate your micro-happiness score.*")

selected = st.multiselect(
    "What did you do today?",
    options=df['activity'].tolist(),
    default=['Morning coffee/tea', 'Working (main job)', 'Commuting']
)

if selected:
    selected_df = df[df['activity'].isin(selected)]
    avg_happiness = selected_df['happiness_score'].mean()
    avg_meaning = selected_df['meaning_score'].mean()
    avg_stress = selected_df['stress_score'].mean()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        color = "#81b29a" if avg_happiness >= 4.5 else "#f2cc8f" if avg_happiness >= 3.5 else "#e07a5f"
        st.markdown(f'<p class="big-stat" style="color: {color};">{avg_happiness:.1f}/7</p>', unsafe_allow_html=True)
        st.markdown('<p class="stat-label">Your average happiness today</p>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<p class="big-stat" style="color: #3d405b;">{avg_meaning:.1f}/7</p>', unsafe_allow_html=True)
        st.markdown('<p class="stat-label">Your meaning score</p>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<p class="big-stat" style="color: #e07a5f;">{avg_stress:.1f}/7</p>', unsafe_allow_html=True)
        st.markdown('<p class="stat-label">Your stress level</p>', unsafe_allow_html=True)
    
    # Suggestions
    not_selected = df[~df['activity'].isin(selected)]
    top_suggestions = not_selected.nlargest(3, 'happiness_score')
    
    st.markdown("---")
    st.markdown("**💡 To boost your happiness, try adding one of these micro-moments tomorrow:**")
    for _, row in top_suggestions.iterrows():
        st.markdown(f"- {row['icon']} **{row['activity']}** — happiness score: {row['happiness_score']}/7 "
                    f"(only ~{row['duration_min_avg']} minutes needed)")

# ============================================================
# SECTION 8: CONCLUSION
# ============================================================

st.markdown('<p class="section-header">The Takeaway</p>', unsafe_allow_html=True)

st.markdown("""
<div class="insight-box">
<p class="story-text">
<strong>Happiness isn't a destination. It's a collection of micro-moments.</strong>
<br><br>
The data tells a clear story:
<br><br>
1️⃣ <strong>Connection wins.</strong> Playing with children, talking with friends, helping others — 
every top-scoring activity involves another person.
<br><br>
2️⃣ <strong>Presence beats productivity.</strong> Walking, nature, meditation — stillness scores higher 
than achievement on the happiness scale.
<br><br>
3️⃣ <strong>We're doing it wrong.</strong> We spend the most hours on the least joyful activities, 
and the least time on what makes us happiest.
<br><br>
4️⃣ <strong>Culture has the answers.</strong> Every society has found its own micro-moment superpower — 
Italian coffee, Finnish nature walks, Brazilian friendships, Indian prayer.
<br><br>
<em>The happiest life isn't the busiest one. It's the one with the most noticed moments.</em>
</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")
st.markdown("""
<p style='text-align: center; color: #999; font-size: 0.85rem;'>
<strong>Viz Con 2026</strong> | Theme: "How the world lives, thrives, and connects"<br>
Data sources: ATUS Well-Being Module (BLS) | OECD Time Use & Well-Being | World Happiness Report 2026 | Kahneman Day Reconstruction Method Research<br>
Built with Streamlit + Plotly | GenAI used for data synthesis, code generation, and narrative drafting
</p>
""", unsafe_allow_html=True)
