"""
scenario_advisor.py -- Scenario-based relationship advice engine.

Supports 23 life scenarios across emotional, practical, experience, and development
dimensions. Each scenario generates structured advice tailored to the partner profile.

Psychological frameworks referenced:
  - Gottman's Sound Relationship House (Gottman & Silver, 1999)
  - Attachment Theory (Bowlby, 1969)
  - Nonviolent Communication (Rosenberg, 2003)
  - Active-Constructive Responding (Gable et al., 2004)
  - Novelty-Arousal Theory (Aron et al., 2000)
  - Self-Expansion Theory (Aron & Aron, 1986)
  - Equity Theory (Adams, 1963)
  - Rusbult's Investment Model (Rusbult, 1980)
  - Positivity Resonance Theory (Fredrickson, 2013)
"""

import json
import argparse


SCENARIO_REGISTRY = {
    # Emotional & Conflict
    "angry_partner":       {"category": "emotional",    "label": "Partner is Angry / Silent Treatment",   "framework": "Gottman De-escalation + Attachment-based repair"},
    "comfort_needed":      {"category": "emotional",    "label": "Partner Needs Comfort",                 "framework": "Empathic attunement + Co-regulation theory"},
    "apology":             {"category": "emotional",    "label": "Sincere Apology",                       "framework": "Gottman repair attempts + Nonviolent Communication"},
    "jealousy_insecurity": {"category": "emotional",    "label": "Jealousy or Insecurity",                "framework": "Attachment theory + Cognitive reappraisal"},
    # Celebration & Gifting
    "anniversary":         {"category": "celebration",  "label": "Anniversary",                           "framework": "Love language expression + Shared meaning creation"},
    "birthday":            {"category": "celebration",  "label": "Partner Birthday",                      "framework": "Love language + MBTI preference mapping"},
    "holiday":             {"category": "celebration",  "label": "Holiday / Seasonal Occasion",           "framework": "Love language + Cultural context"},
    "celebration":         {"category": "celebration",  "label": "Celebrating Partner Win",               "framework": "Active-constructive responding (Gable et al., 2004)"},
    # Date & Experience
    "date_planning":       {"category": "experience",   "label": "Date Planning",                         "framework": "Novelty-arousal theory (Aron et al., 2000) + Personality fit"},
    "travel_planning":     {"category": "experience",   "label": "Travel Planning",                       "framework": "Travel compatibility + Big Five trait alignment"},
    "intimacy_building":   {"category": "experience",   "label": "Deepening Intimacy",                    "framework": "Sternberg Triangular Theory + Vulnerability research (Brown)"},
    "daily_warmth":        {"category": "experience",   "label": "Daily Warmth and Micro-Moments",        "framework": "Positivity resonance theory (Fredrickson, 2013)"},
    "personal_growth":     {"category": "experience",   "label": "Supporting Individual Growth",          "framework": "Self-expansion theory (Aron and Aron, 1986)"},
    # Practical Life
    "chores_negotiation":  {"category": "practical",    "label": "Household Chores Division",             "framework": "Equity theory (Adams, 1963) + Conscientiousness analysis"},
    "financial_discussion":{"category": "practical",    "label": "Money Conversations",                   "framework": "Financial compatibility + Values alignment"},
    "cohabitation":        {"category": "practical",    "label": "Moving In Together",                    "framework": "Interdependence theory + Autonomy-togetherness balance"},
    "digital_habits":      {"category": "practical",    "label": "Screen Time and Digital Boundaries",    "framework": "Boundary negotiation + Attachment security"},
    # Relationship Development
    "long_distance":       {"category": "development",  "label": "Long-Distance Relationship",            "framework": "Attachment security + Shared ritual creation"},
    "family_meeting":      {"category": "development",  "label": "Meeting Each Others Families",          "framework": "Family systems theory + Social anxiety management"},
    "social_boundaries":   {"category": "development",  "label": "Friend Groups and Social Circles",      "framework": "Boundary theory + Extraversion/introversion dynamics"},
    "career_support":      {"category": "development",  "label": "Career Stress and Support",             "framework": "Responsive caregiving + Stress-buffering hypothesis"},
    "health_care":         {"category": "development",  "label": "Health and Illness Support",            "framework": "Caregiving system + Attachment security activation"},
    "future_planning":     {"category": "development",  "label": "Future Planning Conversations",         "framework": "Commitment model (Rusbult) + Values alignment"},
}

ATTACHMENT_NOTES = {
    "anxious":  "Partner likely needs explicit reassurance and consistent presence.",
    "avoidant": "Partner likely needs space before re-engagement; avoid pressure.",
    "secure":   "Partner can generally engage with direct, honest communication.",
    "fearful":  "Partner may oscillate between wanting closeness and pulling away.",
}


def get_advice(profile_path, scenario, context=""):
    """
    Generate scenario-specific advice tailored to the partner profile.

    Args:
        profile_path: Path to partner profile.json.
        scenario: Scenario type key from SCENARIO_REGISTRY.
        context: Optional user-provided description of the specific situation.

    Returns:
        Structured advice dict with immediate action, scripts, and strategy.
    """
    print(f"Loading profile: {profile_path}")
    with open(profile_path, encoding="utf-8") as f:
        profile = json.load(f)

    meta = SCENARIO_REGISTRY.get(scenario, {
        "category": "general",
        "label": scenario,
        "framework": "General relationship psychology",
    })

    attachment = profile.get("attachment_style", "unknown").lower()
    love_language = profile.get("love_language", "unknown")

    advice = {
        "scenario": scenario,
        "scenario_label": meta["label"],
        "category": meta["category"],
        "framework": meta["framework"],
        "partner_context": {
            "name": profile.get("name", "Partner"),
            "attachment_style": attachment,
            "love_language": love_language,
            "mbti": profile.get("mbti", "unknown"),
            "astrological_sign": profile.get("astrological_sign", "unknown"),
        },
        "attachment_guidance": ATTACHMENT_NOTES.get(
            attachment, "Tailor approach based on observed patterns."
        ),
        "user_context": context,
        "immediate_action": (
            f"[LLM generates: {scenario} + {attachment} attachment + {love_language} love language]"
        ),
        "what_to_say": [
            "[LLM generates 2-3 word-for-word scripts tailored to partner profile]"
        ],
        "what_not_to_say": [
            "[LLM generates 2-3 specific phrases to avoid, with reasons]"
        ],
        "long_term_strategy": (
            "[LLM generates one behavioral shift addressing the underlying dynamic]"
        ),
        "love_language_application": (
            f"[How to apply {love_language!r} specifically in this scenario]"
        ),
    }

    print(json.dumps(advice, ensure_ascii=False, indent=2))
    return advice


def list_scenarios():
    """Print all available scenarios organized by category."""
    cats = {}
    for k, m in SCENARIO_REGISTRY.items():
        cats.setdefault(m["category"], []).append((k, m["label"]))
    print("\nAvailable Scenarios:\n")
    for cat, items in cats.items():
        print(f"  [{cat.upper()}]")
        for k, lbl in items:
            print(f"    {k:<30} {lbl}")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scenario-based relationship advice engine"
    )
    parser.add_argument("--profile", help="Path to partner profile.json")
    parser.add_argument("--scenario", help="Scenario type (use --list to see all)")
    parser.add_argument("--context", default="", help="Description of the specific situation")
    parser.add_argument("--list", action="store_true", help="List all available scenarios")
    args = parser.parse_args()

    if args.list:
        list_scenarios()
    elif args.profile and args.scenario:
        get_advice(args.profile, args.scenario, args.context)
    else:
        parser.print_help()
