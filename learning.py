"""Priorities based on recorded attempts, with confidence as a labeled fallback."""
from datetime import datetime, timedelta


def topic_status(topics, attempts, ratings):
    rows = []
    for topic in topics:
        done = [a for a in attempts if a.topic == topic and a.feedback is not None]
        latest = done[0] if done else None
        if latest:
            points = sum(latest.feedback["earned"])
            age = datetime.utcnow() - latest.created_at
            status = "Needs practice" if points < 3 else "Review due" if age >= timedelta(days=3) else "On track"
            evidence = f"{points}/3 on latest attempt · {len(done)} completed"
            priority = 0 if points < 3 else 1 if status == "Review due" else 4
        else:
            rating = ratings.get(topic)
            status = "Not tested"
            evidence = f"Confidence {rating}/5 · no practice evidence" if rating else "No practice evidence yet"
            priority = 2 if rating and rating <= 2 else 3
        rows.append(dict(topic=topic, status=status, evidence=evidence, priority=priority, latest=latest))
    return sorted(rows, key=lambda row: row["priority"])


def build_plan(rows, minutes):
    """A small, executable session; every task links to a concrete practice topic."""
    chosen = rows[:max(1, min(3, minutes // 10))]
    each, remainder = divmod(minutes, len(chosen))
    return [dict(row, minutes=each + (i < remainder),
                 instruction=(row["latest"].feedback["next_step"] if row["latest"] and row["priority"] == 0
                              else f"Answer one new question on {row['topic']} without notes. Explain your reasoning, then use the feedback to correct one step."))
            for i, row in enumerate(chosen)]
