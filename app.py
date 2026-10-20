
import streamlit as st
import pandas as pd

from main import (
    calculate_hitting_percentage,
    calculate_assists_per_set,
    calculate_season_assists_per_set,
    calculate_season_hitting_percentage
)

from db import initialize_database, save_match, load_matches, delete_match

initialize_database()

st.title("🏐 VolleyTrack")
st.write("Record and analyze volleyball matches.")

# Initialize session state
if "pending_delete" not in st.session_state:
    st.session_state["pending_delete"] = None


# RECORD A MATCH
st.subheader("Record a Match")

with st.form("match_form"):
    opponent = st.text_input("Opponent")
    sets_played = st.number_input("Sets Played", min_value=0, step=1)
    kills = st.number_input("Kills", min_value=0, step=1)
    attack_errors = st.number_input("Attack Errors", min_value=0, step=1)
    attack_attempts = st.number_input("Attack Attempts", min_value=0, step=1)
    assists = st.number_input("Assists", min_value=0, step=1)
    digs = st.number_input("Digs", min_value=0, step=1)
    aces = st.number_input("Aces", min_value=0, step=1)
    blocks = st.number_input("Blocks", min_value=0, step=1)

    submitted = st.form_submit_button("Save Match")

if submitted:
    match = {
        "sets_played": sets_played,
        "kills": kills,
        "attack_errors": attack_errors,
        "attack_attempts": attack_attempts,
        "assists": assists,
        "digs": digs,
        "aces": aces,
        "blocks": blocks,
        "opponent": opponent
    }

    errors = []

    if not opponent.strip():
        errors.append("Please enter an opponent name.")

    if sets_played == 0:
        errors.append("Sets played must be at least 1.")

    if kills + attack_errors > attack_attempts:
        errors.append("Kills and attack errors cannot exceed attack attempts.")

    if errors:
        for error in errors:
            st.error(error)
    else:
        save_match(match)
        st.success("Match saved successfully!")

        hitting_percentage = calculate_hitting_percentage(match)
        assists_per_set = calculate_assists_per_set(match)

        st.subheader("Match Statistics")

        if hitting_percentage is None:
            st.write("Hitting Percentage: N/A")
        else:
            st.write(f"Hitting Percentage: {hitting_percentage:.3f}")

        if assists_per_set is None:
            st.write("Assists Per Set: N/A")
        else:
            st.write(f"Assists Per Set: {assists_per_set:.2f}")


# MATCH HISTORY
st.subheader("Match History")

saved_matches = load_matches()

for match in saved_matches:
    col1, col2 = st.columns([4, 1])

    with col1:
        with st.expander(match["opponent"]):
            hitting_percentage = calculate_hitting_percentage(match)
            assists_per_set = calculate_assists_per_set(match)

            # Row 1: Kills, Assists, Digs
            row1 = st.columns(3)

            with row1[0]:
                st.metric("Kills", match["kills"])

            with row1[1]:
                st.metric("Assists", match["assists"])

            with row1[2]:
                st.metric("Digs", match["digs"])

            # Row 2: Aces, Blocks, Sets
            row2 = st.columns(3)

            with row2[0]:
                st.metric("Aces", match["aces"])

            with row2[1]:
                st.metric("Blocks", match["blocks"])

            with row2[2]:
                st.metric("Sets Played", match["sets_played"])

            # Row 3: Attack Statistics
            row3 = st.columns(3)

            with row3[0]:
                st.metric("Attack Attempts", match["attack_attempts"])

            with row3[1]:
                st.metric("Attack Errors", match["attack_errors"])

            with row3[2]:
                st.metric(
                    "Hitting Percentage",
                    f"{hitting_percentage:.3f}" if hitting_percentage is not None else "N/A"
                )

            # Row 4: Assists Per Set
            row4 = st.columns(3)

            with row4[0]:
                st.metric(
                    "Assists Per Set",
                    f"{assists_per_set:.2f}" if assists_per_set is not None else "N/A"
                )

    # Delete button
    with col2:
        if st.button("Delete", key=f"delete_{match['id']}"):
            st.session_state["pending_delete"] = match["id"]

    # Delete confirmation
    if st.session_state["pending_delete"] == match["id"]:
        st.warning(
            f"Are you sure you want to delete the match against {match['opponent']}?"
        )

        confirm_col, cancel_col = st.columns(2)

        with confirm_col:
            if st.button("Confirm Delete", key=f"confirm_{match['id']}"):
                delete_match(match["id"])
                st.session_state["pending_delete"] = None
                st.rerun()

        with cancel_col:
            if st.button("Cancel", key=f"cancel_{match['id']}"):
                st.session_state["pending_delete"] = None
                st.rerun()


# SEASON OVERVIEW
st.subheader("Season Overview")

if len(saved_matches) > 0:
    season_hitting_percentage = calculate_season_hitting_percentage(saved_matches)
    season_assists_per_set = calculate_season_assists_per_set(saved_matches)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Matches", len(saved_matches))

    with col2:
        if season_assists_per_set is None:
            st.metric("Season Assists Per Set", "N/A")
        else:
            st.metric("Season Assists Per Set", f"{season_assists_per_set:.2f}")

    with col3:
        if season_hitting_percentage is None:
            st.metric("Season Hitting Percentage", "N/A")
        else:
            st.metric("Season Hitting Percentage", f"{season_hitting_percentage:.3f}")
else:
    st.info("No matches recorded yet. Save a match to see season statistics.")


# PERFORMANCE TRENDS
st.subheader("Performance Trends")

statistic = st.selectbox(
    "Statistic",
    ["Hitting Percentage", "Assists Per Set", "Kills", "Digs", "Aces"]
)

chart_data = []

for i, match in enumerate(saved_matches, start=1):
    if statistic == "Hitting Percentage":
        value = calculate_hitting_percentage(match)
    elif statistic == "Assists Per Set":
        value = calculate_assists_per_set(match)
    elif statistic == "Kills":
        value = match["kills"]
    elif statistic == "Digs":
        value = match["digs"]
    elif statistic == "Aces":
        value = match["aces"]

    if value is not None:
        chart_data.append({
            "Match Number": i,
            statistic: value
        })

if len(chart_data) >= 2:
    chart_df = pd.DataFrame(chart_data)

    st.line_chart(
        chart_df,
        x="Match Number",
        y=statistic
    )
else:
    st.info("At least two matches with valid data are needed to display this chart.")
