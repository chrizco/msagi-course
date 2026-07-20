from app.agents import (
    evaluate_draft,
    generate_draft,
    generate_hashtags,
    generate_ideas,
)


def create_linkedin_content(request):
    """Run all agents in the correct order."""

    ideas = generate_ideas(request)

    selected_idea = ideas[0]

    draft = generate_draft(
        request,
        selected_idea,
    )

    hashtags = generate_hashtags(
        request,
        draft,
    )

    evaluation = evaluate_draft(
        request,
        draft,
    )

    return {
        "ideas": ideas,
        "selected_idea": selected_idea,
        "draft": draft,
        "confidence": evaluation["confidence"],
        "reason": evaluation["reason"],
        "hashtags": hashtags,
    }