def web_search(query: str) -> str:
    """
    Mock web search tool for mini project
    """

    fake_results = [
        f"1. Top result about {query}",
        f"2. Detailed explanation of {query}",
        f"3. Related information and examples of {query}"
    ]

    return "\n".join(fake_results)