import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="YouTube Learning Quality Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)






# --------------------------------------------------
# GLOBAL BLACK THEME (CRITICAL)
# --------------------------------------------------
st.markdown("""
<style>

/* GLOBAL */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #000000;
    color: #FFFFFF;
    font-family: "Inter", "Segoe UI", sans-serif;
}

/* HEADER */
[data-testid="stHeader"] {
    background: #000000;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background-color: #000000;
    border-right: 1px solid #111827;
}
[data-testid="stSidebar"] * {
    color: #E5E7EB;
}


.kpi-card {
    background: linear-gradient(120deg, #008080, #006666);
    border-radius: 16px;
    padding: 24px;
    
    text-align: center;
    border: 1px solid #66b2b2;
}

.kpi-title {
    font-size: 12px;
    font-weight: 600;
    color: #E0F2F1;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.kpi-value {
    font-size: 30px;
    font-weight: 600;
    color: #FFFFFF;
    margin-top: 8px;
}




/* TABS */
/* Container for all tabs - targets the parent to center everything */
div[role="tablist"] {
    justify-content: center;
    column-gap: 20px; /* Adjust this value for more or less space between buttons */
}

/* Individual TAB buttons */
button[data-baseweb="tab"] {
    background-color: #020617;
    color: #FFFFFF;
    /* Optional: ensures buttons have consistent padding */
    padding-left: 20px;
    padding-right: 20px;
}

/* Active TAB state */
button[data-baseweb="tab"][aria-selected="true"] {
    color: #2DD4BF;
    border-bottom: 2px solid #2DD4BF;
}

/* SELECTS */
div[data-baseweb="select"] > div {
    background-color: #020617;
    border: 1px solid #111827;
}

/* REMOVE PLOT BACKGROUND */
.js-plotly-plot .plotly {
    background: transparent !important;
}

/* Target the radio group container */
div[role="radiogroup"] {
    justify-content: center;
    gap: 30px; /* Creates the space between the two options */
    margin-top: 5px;
    color: #FFFFFF;
}

/* Optional: Make the radio labels bold and cleaner */
div[data-testid="stWidgetLabel"] p {
    font-weight: bold;
    color: #FFFFFF;
}

/* Optional: Styling the radio buttons to match your dark theme */
div[data-testid="stMarkdownContainer"] p {
    font-size: 16px;
    color: #FFFFFF;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# COLORS
# --------------------------------------------------
ACCENT = "#2DD4BF"
NEG = "#F87171"
NEUTRAL = "#FBBF24"
TEXT = "#FFFFFF" 

# --------------------------------------------------
# DATA
# --------------------------------------------------
df = pd.read_csv("Clean_Data/final_dataset.csv")


df_quality = pd.read_csv("Clean_Data/video_quality_with_channel_info.csv",encoding='latin-1')
df_channel_cluster = pd.read_csv("Clean_Data/channel_cluster_analysis_file.csv")
df_channel_cluster_1 = pd.read_csv("Clean_Data/channel_cluster_analysis_file_1.csv")
# Loading researcher based in team
# Generating the final dataset

research_dff = pd.read_csv("Clean_Data/Educator_metadata.csv")

# Keep only scientific channels
research_df = research_dff[research_dff["role"] == "scientist"].copy()
cluster_df = pd.read_csv("Clean_Data/cluster_distribution_by_educator_role.csv")
index_df = pd.read_csv("Clean_Data/hindex_by_cluster.csv")


# Counts
total_researchers = research_df["channel_id"].nunique()
individual_count = research_df[
    research_df["Individual/Affiliated"] == "Individual"
]["channel_id"].nunique()

affiliated_count = research_df[
    research_df["Individual/Affiliated"] == "Company Affiliated"
]["channel_id"].nunique()

ind_pct = individual_count / total_researchers
aff_pct = affiliated_count / total_researchers

# Counts for transcript analysis
Total_channel = df['channel_id'].nunique()
number_of_channels_with_good_score= df_quality['channel_id'].loc[df_quality['overall_score'] > 70].nunique()
number_of_channels_with_medium_score= df_quality['channel_id'].loc[(df_quality['overall_score'] > 50)&(df_quality['overall_score'] < 70)].nunique()
number_of_channels_with_low_score = df_quality['channel_id'].loc[df_quality['overall_score'] < 50].nunique()
good_df = df_quality[['channel_title','overall_score']].loc[df_quality['overall_score'] > 70]
good_df = good_df.groupby('channel_title').mean().reset_index().round(0)
bad_df = df_quality[['channel_title','overall_score']].loc[df_quality['overall_score'] < 50 ]
bad_df = bad_df.groupby('channel_title').mean().reset_index().round(0)


good_score = number_of_channels_with_good_score/Total_channel
median_score = number_of_channels_with_medium_score/Total_channel
low_score = number_of_channels_with_low_score/Total_channel

with open("Clean_Data/sentiments_results.json", "r") as f:
    sentiment_df = pd.DataFrame(json.load(f))


channel_sentiment = (
    sentiment_df
    .groupby("channel_title")
    .mean(numeric_only=True)
    .reset_index()
)

# --------------------------------------------------
# PLOT THEME FUNCTION
# --------------------------------------------------
def black_plot(fig):
    fig.update_layout(
        paper_bgcolor="#000000",
        plot_bgcolor="#000000",
       
        font=dict(color="#FFFFFF"),
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(bgcolor="rgba(0,0,0,0)")
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    return fig

# --------------------------------------------------
# TITLE
# --------------------------------------------------
st.title("YouTube Learning Quality Intelligence")




st.markdown("<br>", unsafe_allow_html=True)


# --------------------------------------------------
# TABS
# --------------------------------------------------
tab1, tab2 = st.tabs(["Channel Analysis", "Content Intelligence"])
st.markdown("<br>", unsafe_allow_html=True)

# ==================================================
# TAB 1 — CHANNEL ANALYSIS
# ==================================================
# SIDEBAR FILTER


with tab1:
    st.markdown("""
##### Welcome to our website!
Explore the quality, structure, and impact of educational YouTube channels through a data-driven lens.

This platform goes beyond views and subscribers to analyze content clarity, description quality, audience sentiment, transcript intelligence, and research orientation—helping you understand **how well creators teach**, not just **how many they reach**.
""")

    

    # KPI VALUES
    
    
    
    total_channels = df["channel_id"].nunique()
    avg_views = round(df["total_views"].mean(),0)
    pct_individual = round((df["Individual_company_brand"] == "Individual").mean() * 100,0)
    pct_data_science = round((df["Category"] == "Data Science").mean() * 100,0)
    
    st.markdown("""
    <style>
    .sophisticated-header {
        font-family: 'Inter', sans-serif;
        font-size: 28px;
        font-weight: 700;
        letter-spacing: -0.5px;
        background: linear-gradient(90deg, #2DD4BF 0%, #0077be 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(45, 212, 191, 0.3);
        margin-top: 20px;
        margin-bottom: 15px;
    }
    </style>
    <div class="sophisticated-header">Channel Overview</div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    st.markdown("<br>", unsafe_allow_html=True)
    
    
    
    
    
    with c1:
        st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">TOTAL CHANNELS</div>
        <div class="kpi-value">{total_channels}</div>
    </div>
    """, unsafe_allow_html=True)
        
    with c2:
        st.markdown(f"""
                    <div class="kpi-card">
                    <div class="kpi-title">AVERAGE VIEWS</div>
                    <div class="kpi-value">{avg_views/1e6:.2f}M</div>
                    </div>
                    """, unsafe_allow_html=True)
        
    with c3:
        st.markdown(f"""
                    <div class="kpi-card">
                    <div class="kpi-title">INDIVIDUAL CREATORS</div>
                    <div class="kpi-value">{pct_individual:.1f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
    
    with c4:
        st.markdown(f"""
                    <div class="kpi-card">
                    <div class="kpi-title">DATA SCIENCE CREATORS</div>
                    <div class="kpi-value">{pct_data_science:.1f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
        

    
    col_left, col_right = st.columns([1, 1.2])
    
    with col_left:
        
        
        st.markdown(
        f"""
        <div>
            <h2 style="margin:0;color:white;">{total_researchers}</h2>
            <p style="margin:0;color:#9adede;">Total Researchers</p>
        </div>
        """,
        unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown(f"**Individual Researchers — {individual_count}**")
        st.progress(ind_pct)
        
        st.markdown(f"**Affiliated Researchers — {affiliated_count}**")
        st.progress(aff_pct)

    
    with col_right:
        
        
        researcher_type = st.radio(
        "Select researcher type",
        ["Company Affiliated","Individual"],
        horizontal=True)
        
        filtered_researchers = research_df[
        research_df["Individual/Affiliated"] == researcher_type][[
        "channel_title",
        "citations",
        "h-index",
        "i10-index"]].sort_values("citations", ascending=False)
        
        st.dataframe(
        filtered_researchers.rename(columns={
            "channel_title": "Channel Name",
            "citations": "Citations",
            "h-index": "H-Index",
            "i10-index": "i10-Index"
        }),
        use_container_width=True,
        hide_index=True)
        
        st.caption(
        f"Showing {len(filtered_researchers)} {researcher_type.lower()} researchers")
        
    st.markdown("""
    <style>
    .sophisticated-header {
        font-family: 'Inter', sans-serif;
        font-size: 28px;
        font-weight: 700;
        letter-spacing: -0.5px;
        background: linear-gradient(90deg, #2DD4BF 0%, #0077be 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(45, 212, 191, 0.3);
        margin-top: 20px;
        margin-bottom: 15px;
    }
    </style>
    <div class="sophisticated-header"></div>
    """, unsafe_allow_html=True)
        
    
    scope = st.radio(
    label="", # This label will be hidden by CSS but is needed for accessibility
    options=["All Channels", "Data Science Only"],
    horizontal=True,       # Displays them inline natively
    label_visibility="collapsed")
    st.caption("*The buttons are valid for all charts in channel analysis except the KPI cards")
    
    filtered_df = df if scope == "All Channels" else df[df["Category"] == "Data Science"]




    
    

    # TOP CHANNELS
    
    
    st.markdown("""
    <style>
    .sophisticated-header {
        font-family: 'Inter', sans-serif;
        font-size: 28px;
        font-weight: 700;
        letter-spacing: -0.5px;
        background: linear-gradient(90deg, #2DD4BF 0%, #0077be 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(45, 212, 191, 0.3);
        margin-top: 20px;
        margin-bottom: 15px;
    }
    </style>
    <div class="sophisticated-header">Channel Performance</div>
    """, unsafe_allow_html=True)
    
    st.markdown("##### What are the top 10 channels by views and subscribers?")
 

    l, r = st.columns(2)
   

    fig_views = px.bar(
        filtered_df.sort_values("total_views", ascending=False).head(11),
        y="channel_title",
        x="total_views",
        orientation="h",
        color_discrete_sequence=[ACCENT],
        title="Top Channels by Views",
        
    )
    l.plotly_chart(black_plot(fig_views), use_container_width=True)

    fig_subs = px.bar(
        filtered_df.sort_values("subscribers", ascending=False).head(11),
        y="channel_title",
        x="subscribers",
        orientation="h",
        color_discrete_sequence=[ACCENT],
        title="Top Channels by Subscribers"
    )
    r.plotly_chart(black_plot(fig_subs), use_container_width=True)

    # SCATTER
    
    st.markdown("""
    <style>
    .sophisticated-header {
        font-family: 'Inter', sans-serif;
        font-size: 28px;
        font-weight: 700;
        letter-spacing: -0.5px;
        background: linear-gradient(90deg, #2DD4BF 0%, #0077be 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(45, 212, 191, 0.3);
        margin-top: 20px;
        margin-bottom: 15px;
    }
    </style>
    <div class="sophisticated-header">Content Volumn Impact</div>
    """, unsafe_allow_html=True)
    
    st.markdown("##### Does increase in no.of videos means more views/subscriber?")
 
    l, r = st.columns(2)

    fig1 = px.scatter(
        filtered_df,
        x="total_videos",
        y="subscribers",
        size="total_views",
        color="Individual_company_brand",
        hover_name="channel_title",
        trendline="ols",
        title="Videos vs Subscribers",
        color_discrete_sequence=[ACCENT, NEG]
    )
    fig1.update_layout(
        legend=dict(
        bgcolor = "white")
    )
    fig1.update_xaxes(type="log")
    fig1.update_yaxes(type="log")
    l.plotly_chart(black_plot(fig1), use_container_width=True)

    fig2 = px.scatter(
        filtered_df,
        x="total_videos",
        y="total_views",
        size="subscribers",
        color="Individual_company_brand",
        hover_name="channel_title",
        trendline="ols",
        title="Videos vs Views",
        color_discrete_sequence=[ACCENT, NEG]
    )
    fig2.update_xaxes(type="log")
    fig2.update_yaxes(type="log")
    r.plotly_chart(black_plot(fig2), use_container_width=True)

    # DESCRIPTION ANALYSIS
    
    st.markdown("""
    <style>
    .sophisticated-header {
        font-family: 'Inter', sans-serif;
        font-size: 28px;
        font-weight: 700;
        letter-spacing: -0.5px;
        background: linear-gradient(90deg, #2DD4BF 0%, #0077be 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(45, 212, 191, 0.3);
        margin-top: 20px;
        margin-bottom: 15px;
    }
    </style>
    <div class="sophisticated-header">Description Quality Intelligence</div>
    """, unsafe_allow_html=True)
    
    st.markdown("##### How well the channel owner have managed their channel description in terms of clarity, explanation, length ?")
 

    l1, r1 = st.columns(2)
    factors = ["length", "explainability", "clarity", "links"]
    plot_df = filtered_df.copy()
    plot_df["channel_title"] = plot_df["channel_title"].apply(lambda x: x[:20] + '...' if len(x) > 20 else x)
    
    heat = px.imshow(
    plot_df.set_index("channel_title")[factors],
    aspect="auto",
    color_continuous_scale="teal",
    title="Channel with their factors coverability")
    # 2. Update layout to reclaim space
    # 
    heat.update_layout(
    # Reduce outer margins
    yaxis=dict(
        automargin=True, # Automatically adjust for label size
        tickfont=dict(size=10) # Smaller font gives more room for the map
    ),
    xaxis=dict(side="top") )
    l1.plotly_chart(black_plot(heat), use_container_width=True)
    l1.caption("We used the TinyLLama LLM model to evaluate and rank the channel description based on 4 different factors such as clarity, explainabilty, length and links. The score ranges from 1 to 5, 1 being the least and 5 being the most")

    # RADAR
    channel = r1.selectbox("Inspect Channel", filtered_df["channel_title"].unique())
    row = filtered_df[filtered_df["channel_title"] == channel].iloc[0]

    radar = go.Figure(go.Scatterpolar(
        r=[row[f] for f in factors],
        theta=[f.title() for f in factors],
        fill="toself",
        line_color=ACCENT,
        
    ))

    radar.update_layout(
        polar=dict(radialaxis=dict(range=[0, 1], visible=True)),
        paper_bgcolor="#000000",
        showlegend=False,
        
        title="Individual channel description factor analysis"
    )

    r1.plotly_chart(radar, use_container_width=True)
    
    




   
 
    st.markdown("""
    <style>
    .sophisticated-header {
        font-family: 'Inter', sans-serif;
        font-size: 28px;
        font-weight: 700;
        letter-spacing: -0.5px;
        background: linear-gradient(90deg, #2DD4BF 0%, #0077be 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(45, 212, 191, 0.3);
        margin-top: 20px;
        margin-bottom: 15px;
    }
    </style>
    <div class="sophisticated-header">Final Dataset</div>
    """, unsafe_allow_html=True)



    Dataset_type = st.radio(
        "Select the dataset you want to download"
        ,["Channel Level Data","Video_transcript Analysis","Final clustering data"],
        horizontal= True
    )
    
    if Dataset_type == "Channel Level Data":
        st.dataframe(
        df[['channel_id', 'channel_title', 'Category',
       'subscribers', 'total_views', 'total_videos', 
       'Individual_company_brand','channel_description', 'rating']].rename(columns={
            "channel_title": "Channel Name",
            "rating" : "Description Ratings",
            "channel_id": "Channel ID",
            'subscribers':'Subscribers',
            'total_views':'Total Views',
            'total_videos': 'Total Videos',
            'Individual_company_brand': 'Individual/Company_brand'
                    
        }),
        use_container_width=True,
        hide_index=True)
        st.caption("Description:This is a pure channel level data, that was initially extracted using YouTube API. Features like category, Individual_company_brand,ratings are feature engineered using different LLMs.")
    
    elif Dataset_type == "Video_transcript Analysis":
        st.dataframe(df_quality.rename(columns = {
            "channel_title": "Channel Name",
            "video_id": "Video ID",
            "channel_id": "Channel ID",
            
            "overall_score":"Overall Score",
            "Technical_depth":"Technical Depth",
            "clarity": "Clarity",
            "practical_value":"Practical Value",
            "structure": "Structure",
            "engagement":"Engagement",
            "word_count": "Word Count"
            
        }))
        st.caption("Description: The video transcripts from different channels were evaluted on 6 different factors to see the effectiveness of the transcripts. ")
        
    else:
        st.dataframe(df_channel_cluster)
        
    

    
    
    




# TAB 2 — CONTENT INTELLIGENCE

with tab2:
    st.markdown("""
The content intelligence tab has two sections one section solely dedicated towards the comment distribution of different youTube channel and another section analyzes the transcript for different videos in those YouTube channel..
""")
    st.markdown("""
    <style>
    .sophisticated-header {
        font-family: 'Inter', sans-serif;
        font-size: 28px;
        font-weight: 700;
        letter-spacing: -0.5px;
        background: linear-gradient(90deg, #2DD4BF 0%, #0077be 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(45, 212, 191, 0.3);
        margin-top: 20px;
        margin-bottom: 15px;
    }
    </style>
    <div class="sophisticated-header">Channelwise Sentiment Analysis</div>
    """, unsafe_allow_html=True)
    col_left, col_right = st.columns(2)
    col_left.markdown("##### What are the top 5 channels with the most positive comments in their videos and Top 5 channels with the most negative comments? ")
    
    top = channel_sentiment.sort_values("positive_percent", ascending=False).head(10)
    bottom = channel_sentiment.sort_values("negative_percent", ascending=False).head(10)
    top = top.copy()
    bottom = bottom.copy()
    fig_div = go.Figure()
    
    fig_div.add_trace(go.Bar(
    y=top["channel_title"],
    x=top["positive_percent"],
    orientation="h",
    name="Positive",
    marker_color="#87CEEB" # Your watery teal
    ))
    
    fig_div.add_trace(go.Bar(
    y=bottom["channel_title"],
    x=-bottom["negative_percent"],
    orientation="h",
    name="Negative",
    marker_color="#FF4B4B" 
    ))
    
    fig_div.update_layout(
    barmode="relative",
    height=600,                # Increases vertical elongation
     # Tight margins to use full container width
    
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    
    col_left.plotly_chart(black_plot(fig_div), use_container_width=True)

    

    selected_channels = col_right.multiselect(
    "Select channels to compare sentiment composition",
    channel_sentiment["channel_title"],
    default=channel_sentiment.sort_values(
        "positive_percent", ascending=False
    ).head(3)["channel_title"])
    
    filtered_sentiment = channel_sentiment[
    channel_sentiment["channel_title"].isin(selected_channels)]
    
    fig_stack = px.bar(
    filtered_sentiment,
    x=["positive_percent", "neutral_percent", "negative_percent"],
    y="channel_title",
    title="Sentiment Composition by Channel",
    color_discrete_sequence=["#87CEEB", "#F4A261", "#E63946"])
    
    fig_stack.update_layout(
    yaxis_title="Percentage of Comments",
    xaxis_title="Channel")
    

    col_right.plotly_chart(black_plot(fig_stack), use_container_width=True)

    
    st.markdown("""
    <style>
    .sophisticated-header {
        font-family: 'Inter', sans-serif;
        font-size: 28px;
        font-weight: 700;
        letter-spacing: -0.5px;
        background: linear-gradient(90deg, #2DD4BF 0%, #0077be 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(45, 212, 191, 0.3);
        margin-top: 20px;
        margin-bottom: 15px;
    }
    </style>
    <div class="sophisticated-header">Video transcript analysis for different channels</div>
    """, unsafe_allow_html=True)
    st.markdown(
        """Video transcript are evaluated across five quality dimensions: 
* Technical Depth
* Clarity
* Practical Value
* Structure
* Engagement

The weighted average of scores is computed to calculate the overall video quality score 
"""
    )
    c , l = st.columns(2)
    c.markdown(
        f"""
        <div>
            <h2 style="margin:0;color:white;">{Total_channel}</h2>
            <p style="margin:0;color:#9adede;">Total channels</p>
        </div>
        """,
        unsafe_allow_html=True)
        
    c.markdown("<br>", unsafe_allow_html=True)
        
    c.markdown(f"**Good Transcript Score (Above 70) — {number_of_channels_with_good_score}**")
    c.progress(good_score)
        
    c.markdown(f"**Medium level transcript score (In between 50 to 70) — {number_of_channels_with_medium_score}**")
    c.progress(median_score)
    
    c.markdown(f"**Low Transcript Score (Less than 50) — {number_of_channels_with_low_score}**")
    c.progress(low_score)
    
    # We are interested in looking at channels with Good transcript and the low quality transcript channel
    
    st.markdown("""
    <style>
    .sophisticated-header {
        font-family: 'Inter', sans-serif;
        font-size: 28px;
        font-weight: 700;
        letter-spacing: -0.5px;
        background: linear-gradient(90deg, #2DD4BF 0%, #0077be 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(45, 212, 191, 0.3);
        margin-top: 20px;
        margin-bottom: 15px;
    }
    </style>
    <div class="sophisticated-header">Deep Dive </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="large")
    
   

    fig_views = px.bar(
        good_df.sort_values("overall_score", ascending=False).head(11),
        y="channel_title",
        x="overall_score",
        orientation="h",
        color_discrete_sequence=[ACCENT],
        title="Channels with best quality transcript",
        
    )
    col1.plotly_chart(black_plot(fig_views), use_container_width=True)

    fig_subs = px.bar(
        bad_df.sort_values("overall_score", ascending=False).head(21),
        y="channel_title",
        x="overall_score",
        orientation="h",
        color_discrete_sequence=[ACCENT],
        title="Channels with low quality transcript"
    )
    col2.plotly_chart(black_plot(fig_subs), use_container_width=True)
   
    


    
    def factor_distribution_chart(df, column, title):
        fig = px.histogram(
        df,
        x=column,
        nbins=20,
        histnorm="probability density",
        opacity=0.8,
        color_discrete_sequence=["#87CEEB"])
        
        
        fig.update_layout(
        title=title,
        xaxis_title=column.capitalize(),
        yaxis_title="Density",
        paper_bgcolor="#000000",
        plot_bgcolor="#000000",
        font=dict(color="white"),
        margin=dict(t=50, l=30, r=30, b=30))
        
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        return fig

    factors = [
    "technical_depth",	"clarity",	"practical_value",	"structure",	"engagement"]
    
    st.plotly_chart(factor_distribution_chart(df_quality,"overall_score","overall_score"),use_container_width= True)
    
    

    c1, c2, c3 = st.columns(3)
    
    c1.plotly_chart(
    factor_distribution_chart(df_quality,factors[0], "Technical depth"),
    use_container_width=True)
    
    c2.plotly_chart(
    factor_distribution_chart(df_quality, factors[1], "Clarity"),
    use_container_width=True)
    
    c3.plotly_chart(
    factor_distribution_chart(df_quality,factors[2],  "Practical value"),
    use_container_width=True)
    
    
    c4, c5 = st.columns(2)
    
    c4.plotly_chart(
    factor_distribution_chart(df_quality,factors[3], "Structure"),
    use_container_width=True)
    
    c5.plotly_chart(
    factor_distribution_chart(df_quality, factors[4],  "Engagement"),
    use_container_width=True)
    
    st.markdown("""
    <style>
    .sophisticated-header {
        font-family: 'Inter', sans-serif;
        font-size: 28px;
        font-weight: 700;
        letter-spacing: -0.5px;
        background: linear-gradient(90deg, #2DD4BF 0%, #0077be 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(45, 212, 191, 0.3);
        margin-top: 20px;
        margin-bottom: 15px;
    }
    </style>
    <div class="sophisticated-header">Channel Level Clustering</div>
    """, unsafe_allow_html=True)
    
    st.markdown("##### What is the overall status of the channels, In which cluster they belong ?")
    l2, r2 = st.columns(2)
    # Convert cluster labels to strings so Plotly treats them as discrete categories
    df_channel_cluster["Labels"] = df_channel_cluster["Labels"].astype(str)
    
    fig_cluster = px.scatter(
    df_channel_cluster,
    x="pca_1",
    y="pca_2",
    color="Labels",
    hover_name="channel_title",
    color_discrete_sequence=px.colors.qualitative.Vivid )
    
    fig_cluster.update_layout(
    paper_bgcolor="black",
    plot_bgcolor="black",
    font=dict(color="white"),
    margin=dict(l=5, r=5, t=40, b=80), # Extra bottom margin for the legend
    legend=dict(
        orientation="h",      
        y=-0.5, # Moves legend below the axis
        xanchor="center",        
        x=0.3,
        bgcolor = "white",
        
        entrywidth=180,
        entrywidthmode="pixels",
        title_text="" # Remove the "cluster_label" title for a cleaner look
    ))
    # Hide gridlines for a "sophisticated" dark look
    fig_cluster.update_xaxes(showgrid=False, zeroline=False)
    fig_cluster.update_yaxes(showgrid=False, zeroline=False)
    
    l2.plotly_chart(fig_cluster, use_container_width=True)
    l2.caption("*The channels are clustered into four different clusters based on the transcript and comments features such as the Sentiment Score and the transcript Score. The clustering is based on K-means clustering.")
    
    
    
    cluster_options = sorted(df_channel_cluster_1["cluster_label"].unique())
    
    selected_cluster = r2.selectbox(
    "Select Cluster Label",
    cluster_options)
    

    cluster_filtered = df_channel_cluster_1[
    df_channel_cluster_1["cluster_label"] == selected_cluster
    ]
    
    channel_freq = (
    cluster_filtered["channel_title"]
    .value_counts()
    .to_dict()
    )
    
    # Create the WordCloud with higher resolution
    wordcloud = WordCloud(
    width=1000,
    height=600,
    background_color="black",
    colormap="GnBu", # Modern Teal/Blue gradient
    max_words=50,    # Reduced to keep it readable
    font_path=None,  # Use default or point to a .ttf file for more style
    prefer_horizontal=1.0, # All text horizontal looks more sophisticated
    collocations=False).generate_from_frequencies(channel_freq)
    fig_wc, ax_wc = plt.subplots(figsize=(10, 6))
    ax_wc.imshow(wordcloud, interpolation="lanczos") # Lanczos is sharper than bilinear
    ax_wc.axis("off")
    # Ensure the figure itself has no border or background
    fig_wc.patch.set_facecolor("black")
    plt.tight_layout(pad=0)
    r2.pyplot(fig_wc)
    r2.caption("Description : On selecting each of the cluster options you will see different channel names which falls into the cluster.")
    
    l, r = st.columns(2)
   
    fig = go.Figure()
    
    fig.add_bar(
    y=cluster_df["cluster_label"],
    x=cluster_df["scientist"],
    name="Scientist",
    orientation="h",
    marker_color="#66b2b2")
    
    fig.add_bar(
    y=cluster_df["cluster_label"],
    x=cluster_df["employee"],
    name="Employee",
    orientation="h",
    marker_color="#008080")
    
    fig.add_bar(
    y=cluster_df["cluster_label"],
    x=cluster_df["freelancer"],
    name="Freelancer",
    orientation="h",
    marker_color="#004c4c")
    fig.update_layout(
    barmode="stack",
    height=450,
    paper_bgcolor="black",
    plot_bgcolor="black",

   

    font=dict(
        color="white",
        size=13
    ),

    xaxis=dict(
        title="Proportion of Educator Roles",
        showgrid=True,
        gridcolor="#1f3f3f",
        tickformat=".0%"
    ),

    yaxis=dict(
        title="Content Clusters",
        autorange="reversed"
    ),

    legend=dict(
        orientation="h",      
        y=-0.5, # Moves legend below the axis
        xanchor="center",        
        x=0.3,
        bgcolor = "white",
        
        entrywidth=180,
        entrywidthmode="pixels",
        title_text="" 
    ),

    margin=dict(l=20, r=20, t=30, b=20))
    l.plotly_chart(fig, use_container_width=True)
    
  
   

    fig_views = px.bar(
        index_df.sort_values("h-index", ascending=False),
        y="h-index",
        x="cluster_label",
        color_discrete_sequence=[ACCENT],
        title="Cluster Based H-index Analysis",
        
    )
    r.plotly_chart(black_plot(fig_views), use_container_width=True)
    
   




    
        
    
