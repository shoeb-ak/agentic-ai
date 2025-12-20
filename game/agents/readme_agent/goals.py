from game.goals.goal import Goal

readme_goals = [

    Goal(
        priority=1,
        name="readme_generation",
        description="""
        Generate a high-quality README.md for the current project.

        The README MUST:
        - Follow a professional open-source README structure
        - Be clear, concise, and well-organized
        - Use Markdown headings, lists, and code blocks where appropriate
        - Be suitable for GitHub presentation
        """
    ),

    Goal(
        priority=2,
        name="structure_and_sections",
        description="""
        The README should include (when applicable):

        1. Project title and short description
        2. Overview / Purpose
        3. Core architecture or design (high-level)
        4. Key components and their responsibilities
        5. Project structure (directory layout)
        6. How to run / use the project
        7. How to extend or customize it
        8. Roadmap or future improvements
        9. License or usage notes (if inferable)

        Do NOT invent features or files that do not exist.
        """
    ),

    Goal(
        priority=3,
        name="file_analysis_strategy",
        description="""
        To generate the README:

        - First, discover available files using list_project_files
        - Read only the most relevant .py files
        - Infer architecture and behavior from actual code
        - Do NOT attempt to read every file blindly
        """
    ),

    Goal(
        priority=4,
        name="output_handling",
        description="""
        After generating the README content:

        - Write the generated README to the output directory using the appropriate write action
        - Ensure the output is valid Markdown
        """
    ),

    Goal(
        priority=5,
        name="termination_policy",
        description="""
        Terminate ONLY when:

        - The README has been fully generated and written to disk
        - Or no meaningful progress can be made after reasonable attempts

        When terminating:
        - Use the terminate tool
        - Provide a short reason (NOT the README content)
        """
    ),
]
