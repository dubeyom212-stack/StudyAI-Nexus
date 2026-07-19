def create_plan(weaknesses):

    plans = {

        "Limits from Graphs and Tables":
            "Review limit notation, one-sided limits, and continuity. Complete 10 AP-style limit problems.",

        "Derivative Definition and Rules":
            "Practice power, product, quotient, and chain rules. Complete derivative multiple-choice questions.",

        "Related Rates":
            "Review translating word problems into equations. Practice 5 related rates AP questions.",

        "Mean Value Theorem":
            "Review conditions of the theorem and practice identifying when it applies.",

        "Fundamental Theorem of Calculus":
            "Practice connecting derivatives and integrals with accumulation functions.",

        "Infinite Series":
            "Review convergence tests including ratio, comparison, and alternating series tests.",


        "Protein Structure and Enzyme Function":
            "Review enzyme structure, activation energy, and factors affecting enzyme activity. Practice AP Biology questions.",

        "DNA Structure and Replication":
            "Review DNA replication steps, enzymes involved, and replication direction.",

        "Transcription and Translation":
            "Practice explaining how DNA becomes RNA and proteins. Review mutations and gene expression.",

        "Natural Selection":
            "Practice explaining evolutionary changes using evidence and population examples.",


        "Atomic Structure and Periodic Trends":
            "Review electron configurations, periodic trends, and atomic behavior.",

        "Stoichiometry":
            "Practice mole conversions, limiting reactants, and percent yield problems.",

        "Chemical Equilibrium":
            "Review Le Chatelier's principle and equilibrium calculations.",

        "Acid Base Chemistry":
            "Practice pH calculations, buffers, and acid-base reactions.",


        "Primitive Types and Variables":
            "Practice Java data types, variables, casting, and common coding mistakes.",

        "Writing Classes":
            "Practice constructors, instance variables, methods, and object-oriented design.",

        "Arrays":
            "Practice traversing arrays, searching, and modifying elements.",

        "Recursion":
            "Review recursive methods and tracing recursive calls.",


        "DBQ Essay Skills":
            "Practice analyzing documents, creating a thesis, and connecting evidence to historical arguments.",

        "LEQ Essay Skills":
            "Practice writing historical arguments with contextualization and specific evidence.",

        "SAQ Analysis":
            "Practice answering short-answer questions using precise historical evidence."

    }


    plan = []

    for topic in weaknesses:

        task = plans.get(
            topic,
            f"Review {topic} and complete AP-style practice problems."
        )

        plan.append(
            {
                "topic": topic,
                "task": task
            }
        )

    return plan
