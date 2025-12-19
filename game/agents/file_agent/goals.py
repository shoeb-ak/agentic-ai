from game.goals.goal import Goal

file_management_goals = [
    Goal(
        priority=1,
        name="file_management",
        description="""Manage files in the current directory by:
        1. Listing files when needed
        2. Reading file contents when needed
        3. Searching within listed files for information
        4. Providing helpful explanations about file contents"""
    ),
    Goal(
        priority=2,
        name="Terminate",
        description="Terminate the session when tasks are complete with a helpful summary"
    )
]