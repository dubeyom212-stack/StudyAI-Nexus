from topic_map import topic_dependencies
from ap_weights import ap_weights



def analyze_diagnostic(subject, scores):

    weak_topics = []
    strong_topics = []


    for topic, score in scores.items():

        if score <= 2:
            weak_topics.append(topic)

        elif score >= 4:
            strong_topics.append(topic)



    readiness = calculate_readiness(
        subject,
        scores
    )


    prediction = predict_ap_score(
        readiness,
        weak_topics,
        strong_topics
    )


    profile = generate_profile(
        subject,
        weak_topics,
        strong_topics
    )


    recommendation = generate_recommendation(
        subject,
        weak_topics
    )


    root_causes = find_root_causes(
        subject,
        weak_topics
    )


    return {

        "subject": subject,

        "readiness": readiness,

        "prediction": prediction,

        "profile": profile,

        "strengths": strong_topics,

        "weaknesses": weak_topics,

        "root_causes": root_causes,

        "recommendation": recommendation

    }




def calculate_readiness(subject, scores):


    if subject not in ap_weights:

        return 0



    total = 0
    possible = 0



    for topic, score in scores.items():

        weight = ap_weights[subject].get(
            topic,
            1
        )

        total += score * weight

        possible += 5 * weight



    if possible == 0:
        return 0



    return round((total / possible) * 100)





def predict_ap_score(readiness, weaknesses, strengths):


    if readiness >= 85 and len(weaknesses) <= 1:

        return {

            "score": "5",

            "confidence": "High",

            "explanation":
            "Your readiness is high and your remaining weaknesses are limited."

        }



    elif readiness >= 70:

        return {

            "score": "4",

            "confidence": "Moderate to High",

            "explanation":
            "You have a strong foundation, but improving weak areas could "
            "increase your chance of a top score."

        }



    elif readiness >= 55:

        return {

            "score": "3",

            "confidence": "Moderate",

            "explanation":
            "You show partial mastery. Focus on weak concepts and AP-style "
            "practice to move upward."

        }



    else:

        return {

            "score": "2 or below",

            "confidence": "Developing",

            "explanation":
            "Your fundamentals need reinforcement before advanced practice."

        }







def generate_profile(subject, weaknesses, strengths):

    if weaknesses:

        return (
            "Your results show areas where your understanding can improve. "
            "Focus on building connections between concepts instead of only "
            "memorizing information."
        )


    return (
        "Your foundation appears strong. Continue practicing under exam "
        "conditions to improve consistency."
    )





def generate_recommendation(subject, weaknesses):

    if not weaknesses:

        return (
            "Continue completing timed practice exams and reviewing mistakes."
        )


    return (
        f"For {subject}, prioritize: "
        + ", ".join(weaknesses[:3])
        + ". Strengthening these areas should have the biggest impact."
    )





def find_root_causes(subject, weaknesses):

    causes = []


    if subject not in topic_dependencies:

        return causes



    for weakness in weaknesses:

        if weakness in topic_dependencies[subject]:

            causes.append({

                "topic": weakness,

                "requires": topic_dependencies[subject][weakness]

            })


    return causes
