def route_question(question: str):
    """
    Supervisor Agent:
    Decides which agent should handle the user question.
    """

    q = question.lower()

    portfolio_keywords = [
        "portfolio",
        "position",
        "positions",
        "pnl",
        "profit",
        "loss",
        "symbol",
        "holding",
        "holdings",
    ]

    risk_keywords = [
        "risk",
        "exposure",
        "gross exposure",
        "net exposure",
        "concentration",
    ]

    for keyword in risk_keywords:
        if keyword in q:
            return "risk_agent"

    for keyword in portfolio_keywords:
        if keyword in q:
            return "portfolio_agent"

    return "general_agent"