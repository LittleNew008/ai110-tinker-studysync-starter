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

    # Each factor earns a base amount for meeting the profile plus a graded
    # bonus for beating it, so spots that all "match" still get different scores.
    # Maximums: noise 2.5 + distance 1.5 + seats 1.0 = 5.0.
    spot_noise = NOISE_ORDER[spot["noise_level"]]
    max_noise = NOISE_ORDER[profile["max_noise"]]
    if spot_noise <= max_noise:
        score += 2.0 + 0.5 * (spot_noise < max_noise)
        reasons.append("quiet enough")
    else:
        score -= 1.0
        reasons.append("too noisy")

    max_distance = profile["max_distance"]
    if spot["distance_miles"] <= max_distance:
        closeness = 1 - spot["distance_miles"] / max_distance if max_distance > 0 else 1
        score += 0.75 + 0.75 * closeness
        reasons.append("close enough")
    else:
        score -= 1.0
        reasons.append("too far")

    min_seats = max(profile["min_seats"], 1)
    if spot["seats_available"] >= min_seats:
        surplus = min(1.0, (spot["seats_available"] - min_seats) / min_seats)
        score += 0.5 + 0.5 * surplus
        reasons.append("enough seats")
    else:
        score -= 1.0
        reasons.append("not enough seats")

    return round(score, 2), reasons


def rank_study_spots(profile: dict, spots: list, k: int = 3) -> list:
    """
    Score every study spot, then return the top k as (spot, score, reasons)
    tuples, sorted by score descending.
    """
    scored = []
    for spot in spots:
        score, reasons = score_study_spot(profile, spot)
        scored.append((spot, score, reasons))
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]


def format_results(ranked: list) -> None:
    """Print each ranked study spot with its score and reasons, one line each."""
    for rank, (spot, score, reasons) in enumerate(ranked, start=1):
        print(f"{rank}. {spot['name']} -- Score: {score:.1f} -- Because: {', '.join(reasons)}")


def closest_louder_alternative(profile: dict, spots: list, ranked: list):
    """
    Return the nearest spot that is louder than the profile allows and isn't
    already in `ranked`, or None. The noise weight keeps these out of the top k,
    so this surfaces the trade-off the ranking would otherwise hide.
    """
    shown = {spot["id"] for spot, _, _ in ranked}
    louder = [
        s for s in spots
        if s["id"] not in shown
        and NOISE_ORDER[s["noise_level"]] > NOISE_ORDER[profile["max_noise"]]
    ]
    return min(louder, key=lambda s: s["distance_miles"], default=None)


def describe_alternative(spot: dict) -> str:
    return (
        f"Closest option louder than your limit: {spot['name']} -- "
        f"{spot['distance_miles']} mi, {spot['noise_level']}, {spot['seats_available']} seats"
    )


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
            alternative = closest_louder_alternative(profile, spots, ranked)
            if alternative:
                st.caption(describe_alternative(alternative))
        except NotImplementedError:
            st.warning("🚧 Ranking isn't implemented yet -- that's Tinker 3B's ticket.")


if __name__ == "__main__":
    spots = load_study_spots("data/study_spots.csv")
    profile = {"max_noise": "moderate", "max_distance": 1.0, "min_seats": 4}
    ranked = rank_study_spots(profile, spots, k=3)
    format_results(ranked)
    alternative = closest_louder_alternative(profile, spots, ranked)
    if alternative:
        print(describe_alternative(alternative))
