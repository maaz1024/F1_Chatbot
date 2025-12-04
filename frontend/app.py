import streamlit as st
import requests
import pandas as pd

API_URL = "https://f1-backend-iw5n.onrender.com"

# PAGE CONFIG
st.set_page_config(
    page_title="F1 Assistant",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)

VIP_DRIVERS = {
    "Max Verstappen": "https://media.formula1.com/content/dam/fom-website/drivers/M/MAXVER01_Max_Verstappen/maxver01.png.transform/4col/image.png",
    "Lando Norris": "https://media.formula1.com/content/dam/fom-website/drivers/L/LANNOR01_Lando_Norris/lannor01.png.transform/4col/image.png",
    "Oscar Piastri": "https://media.formula1.com/content/dam/fom-website/drivers/O/OSCPIA01_Oscar_Piastri/oscpia01.png.transform/4col/image.png",
}

st.markdown("""
<style>

.stApp {
    background-color: #0d0d0d;
}

/* PODIUM BLOCKS (1 = tallest) */
.podium-block {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-end;
    border-radius: 8px 8px 0 0;
    position: relative;
    overflow: hidden;
    color: white;
    width: 100%; /* Fill the Streamlit column */
}

/* Heights mimic a real podium */
.block-1 { 
    height: 380px; 
    /* Gold Gradient */
    background: linear-gradient(#D4AF37, #AA8C2C); 
    box-shadow: 0 0 20px rgba(212, 175, 55, 0.4);
    z-index: 2;
}

.block-2 { 
    height: 320px; 
    /* Silver Gradient */
    background: linear-gradient(#C0C0C0, #808080); 
}

.block-3 { 
    height: 280px; 
    /* Bronze Gradient */
    background: linear-gradient(#CD7F32, #8B4513); 
}

/* Full-body driver image */
.podium-img {
    width: 100%;
    height: 78%;
    object-fit: contain;
    object-position: bottom; /* Anchor image to bottom */
    margin-top: auto;
}

/* Rank Number */
.rank-number {
    position: absolute;
    top: 4px;
    left: 10px;
    font-size: 3rem; 
    font-weight: 900;
    opacity: 0.25;
    line-height: 1;
    color: #000; /* Darker number for contrast on metallics */
}

/* Footer with name + points */
.driver-footer {
    width: 100%;
    text-align: left;
    padding: 8px 10px;
    font-size: 16px;
    font-weight: 700;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.8); /* Shadow for legibility */
}

.points-footer {
    font-size: 12px;
    opacity: 0.95;
    padding-left: 10px;
    padding-bottom: 8px;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
}

/* Results list container (Left aligned) */
.results-list-container {
    width: 100%;
    margin-top: 60px; /* Increased gap to prevent overlap */
}

/* Hide Table Headers for st.table */
[data-testid="stTable"] thead {
    display: none;
}

/* Compact rows for st.table */
[data-testid="stTable"] td {
    padding-top: 0.4rem !important;
    padding-bottom: 0.4rem !important;
}

</style>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/3/33/F1.svg", width=110)
    st.markdown("## F1 Assistant")
    st.markdown("---")
    page = st.radio(
        "Navigation",
        ["🏎️ F1 QnA Chatbot", "📊 Live Standings", "🧮 WDC Title Predictor"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.info("💡 Calculate Championship permutations based on race results.")

# CHAT PAGE
if page == "🏎️ F1 QnA Chatbot":
    st.header("🏎️ F1 QnA Chatbot")
    
    msg = st.text_input(
        "Chat Input",
        placeholder="Ask me anything about Formula 1...",
        label_visibility="collapsed"
    )

    if msg:
        st.chat_message("user").write(msg)
        try:
            r = requests.post(f"{API_URL}/chat", json={"message": msg}).json()
            st.chat_message("assistant").write(r["response"])
        except Exception as e:
            st.error(f"Connection error: {e}")


# LIVE STANDINGS PAGE
elif page == "📊 Live Standings":
    st.header("World Drivers' Championship")
    try:
        data = requests.get(f"{API_URL}/standings").json()
        df = pd.DataFrame(data)

        df["Points"] = df["Points"].astype(str)

        st.dataframe(
            df[["Driver", "Points"]],
            use_container_width=False,
            hide_index=True,
            width=420
        )
    except Exception as e:
        st.error(f"Failed to fetch standings: {e}")


# SIMULATION PAGE
elif page == "🧮 WDC Title Predictor":
    st.title(" 2025 Driver's Championship Simulation")

    try:
        drivers_req = requests.get(f"{API_URL}/standings").json()

        col_input, col_results = st.columns([1, 2.1], gap="large")

        with col_input:
            st.subheader("Abu Dhabi Race Result")

            df_input = pd.DataFrame([
                {"Driver": d["Driver"], "Finish Position": "DNF"}
                for d in drivers_req
            ])

            pos_options = ["DNF"] + [str(i) for i in range(1, 21)]

            edited = st.data_editor(
                df_input,
                column_config={
                    "Finish Position": st.column_config.SelectboxColumn(
                        "POS", options=pos_options, width="small"
                    ),
                    "Driver": st.column_config.TextColumn(disabled=True),
                },
                hide_index=True,
                height=400
            )  # <--- Added closing parenthesis here

            run = st.button("🏁 Run Simulation", type="primary", use_container_width=True)

        with col_results:
            if run:
                selected_positions = edited[edited["Finish Position"] != "DNF"]["Finish Position"].tolist()
                
                if len(selected_positions) != len(set(selected_positions)):
                    st.error("🚫 **Invalid Classification:** Duplicate finishing positions detected! Each position (1–20) can only be assigned to one driver. Please fix and try again.")
                else:
                    # Proceed with simulation
                    finishing = {}
                    for _, row in edited.iterrows():
                        if row["Finish Position"] != "DNF":
                            finishing[row["Driver"]] = int(row["Finish Position"])

                    resp = requests.post(
                        f"{API_URL}/simulate",
                        json={"finishing_positions": finishing}
                    ).json()

                    res_df = pd.DataFrame(resp["standings"])

                    # Top 3 for podium
                    top3 = res_df.head(3).reset_index(drop=True)

                    st.markdown("## Projected WDC Standings")

                    # PODIUM HTML BUILDER
                    def podium_block(driver_row, rank, css_class):
                        driver = driver_row["Driver"]
                        points = driver_row["Points"]
                        img = VIP_DRIVERS.get(driver, "")

                        return f"""
                        <div class="podium-block {css_class}">
                            <div class="rank-number">{rank}</div>
                            <img src="{img}" class="podium-img">
                            <div class="driver-footer">{driver}</div>
                            <div class="points-footer">{points} pts</div>
                        </div>
                        """

                    c1, c2, c3 = st.columns([1, 1.1, 1], gap="small", vertical_alignment="bottom")

                    # 2nd Place
                    with c1:
                        st.markdown(podium_block(top3.iloc[1], 2, "block-2"), unsafe_allow_html=True)
                    # 1st Place (Winner)
                    with c2:
                        st.markdown(podium_block(top3.iloc[0], 1, "block-1"), unsafe_allow_html=True)
                    # 3rd Place
                    with c3:
                        st.markdown(podium_block(top3.iloc[2], 3, "block-3"), unsafe_allow_html=True)

                    # REMAINING POSITIONS (Positions 4-20)
                    rest = res_df.iloc[3:].reset_index(drop=True)
                    rest["POS"] = rest.index + 4
                    rest["Points"] = rest["Points"].astype(str) + " pts"
                    
                    rest_display = rest[["POS", "Driver", "Points"]]
                    rest_display.set_index("POS", inplace=True)
                    
                    list_col, _ = st.columns(2)
                    
                    with list_col:
                        st.markdown('<div class="results-list-container">', unsafe_allow_html=True)
                        st.table(rest_display)
                        st.markdown('</div>', unsafe_allow_html=True)

            else:
                st.info("👈 Set finishing positions and hit **Run Simulation**.")

    except Exception as e:
        st.error(f"Error contacting backend: {e}")