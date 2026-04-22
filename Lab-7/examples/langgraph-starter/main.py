from pprint import pprint

from graph import build_graph


def main() -> None:
    graph = build_graph()

    initial_state = {
        "session_id": "lab7-demo",
        "user_request": "Draft an email update to the user about the travel itinerary.",
        "current_step": "start",
        "approval_required": False,
        "approved": None,
        "retry_count": 0,
        "timeout_ms": 8000,
        "last_error": None,
        "final_response": None,
    }

    print("\nInitial state:\n")
    pprint(initial_state)

    print("\nRunning graph...\n")
    final_state = graph.invoke(initial_state)

    print("\nFinal state:\n")
    pprint(final_state)


if __name__ == "__main__":
    main()
