"""
StudySync -- Find a Study Spot (Ticket 3, Tinker 3B).

TICKET: none of the ranking logic is implemented yet -- every function
below is a stub.
"""

import csv

NOISE_ORDER = {"quiet": 0, "moderate": 1, "loud": 2}


def load_study_spots(csv_path: str) -> list:
    """
    Load study spots from a CSV into a list of dicts, converting
    "distance_miles" to float and "seats_available" to int.
    """
    spots = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["distance_miles"] = float(row["distance_miles"])
            row["seats_available"] = int(row["seats_available"])
            spots.append(row)
    return spots


def score_study_spot(profile: dict, spot: dict) -> tuple:
    """
    Score one study spot against a student profile.

    profile example: {"max_noise": "moderate", "max_distance": 1.0, "min_seats": 4}

    Return (score, reasons) where reasons is a list of short strings
    explaining what contributed to the score, e.g. ["quiet enough", "close enough"].
    """
    score = 0.0
    reasons = []

    if NOISE_ORDER[spot["noise_level"]] <= NOISE_ORDER[profile["max_noise"]]:
        score += 2.5
        reasons.append("quiet enough")
    else:
        score -= 1.0
        reasons.append("too noisy")

    if spot["distance_miles"] <= profile["max_distance"]:
        score += 1.5
        reasons.append("close enough")
    else:
        score -= 1.0
        reasons.append("too far")

    if spot["seats_available"] >= profile["min_seats"]:
        score += 1.0
        reasons.append("enough seats")
    else:
        score -= 1.0
        reasons.append("not enough seats")

    return score, reasons


def rank_study_spots(profile: dict, spots: list, k: int = 3) -> list:
    """
    Score every study spot, then return the top k as (spot, score, reasons)
    tuples, sorted by score descending.
    """
    # TODO: score every spot with score_study_spot(), then use
    # sorted(..., key=..., reverse=True)[:k] to keep only the top k.
    raise NotImplementedError


def format_results(ranked: list) -> None:
    """Print each ranked study spot with its score and reasons, one line each."""
    # TODO: for each (spot, score, reasons) tuple, print a readable line, e.g.:
    # "1. Innovation Commons -- Score: 5.0 -- Because: quiet enough, close enough"
    raise NotImplementedError


def render_study_spot_tab():
    import streamlit as st

    st.subheader("Find a Study Spot")
    max_noise = st.selectbox("Max noise level", ["quiet", "moderate", "loud"], index=1)
    max_distance = st.slider("Max distance (miles)", 0.0, 3.0, 1.0)
    min_seats = st.number_input("Minimum seats needed", min_value=1, value=4, step=1)

    if st.button("Find spots"):
        profile = {"max_noise": max_noise, "max_distance": max_distance, "min_seats": min_seats}
        try:
            spots = load_study_spots("data/study_spots.csv")
            ranked = rank_study_spots(profile, spots, k=3)
            for spot, score, reasons in ranked:
                st.write(f"**{spot['name']}** -- Score: {score:.1f} -- Because: {', '.join(reasons)}")
        except NotImplementedError:
            st.warning("🚧 Ranking isn't implemented yet -- that's Tinker 3B's ticket.")


if __name__ == "__main__":
    spots = load_study_spots("data/study_spots.csv")
    profile = {"max_noise": "moderate", "max_distance": 1.0, "min_seats": 4}
    ranked = rank_study_spots(profile, spots, k=3)
    format_results(ranked)
