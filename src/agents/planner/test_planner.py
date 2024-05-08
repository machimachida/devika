from pytest_mock import MockFixture

from src.agents.planner.planner import Planner
from src.llm.llm import LLM


class TestPlanner:

    def test_parse_response(self, mocker: MockFixture):
        mocker.patch.object(LLM, '__init__', return_value=None)

        # This response is generated by the prompt, "Please create a chess game in a Java Gradle project."
        response = """```
Project Name: ChessMate Gradle Game

Your Reply to the Human Prompter: Sure, I will create a step-by-step plan to build a Chess game in a Java Gradle project.

Current Focus: The main focus is to outline the stepwise process of setting up a Gradle project, designing the chess game logic and encapsulating the rules.

Plan:
- [ ] Step 1: Set up a new Gradle project using an IDE like IntelliJ IDEA, setting the programming language to Java.
- [ ] Step 2: Structure the project by creating packages for different game components - 'board', 'pieces', 'player', and 'game'.
- [ ] Step 3: Begin coding the chess 'pieces' package. Each piece (pawn, rook, knight, bishop, queen, and king) should be a class extending from an abstract class 'Piece'.
- [ ] Step 4: Within each 'Piece' subclass, define unique movements based on standard chess rules. For example, a knight can move in a 'L' pattern.
- [ ] Step 5: Move onto the 'board' package and create a class 'Board'. It should contain a 8x8 grid and the initial arrangement of the pieces.
- [ ] Step 6: Create a 'Player' class in the 'player' package. Player class should have player's information and current state of its pieces. Write functions to handle player's moves.
- [ ] Step 7: Define game logic in 'game' package, like switching turns between players, checking checkmate, or stalemate conditions.
- [ ] Step 8: Implement a simple console-based user interface to interact with the game. The user interface will show the board state and receive the user's actions.
- [ ] Step 9: Test the game extensively, check all the rules of chess game are applied, and each piece is moving as it should in the game.
- [ ] Step 10: Finally, build the Gradle project and run the tests. If vital, debug and refactor code.

Summary: The plan involves setting up a Gradle project, breaking down the chess game into components and implementing them step by step. The main considerations are creating accurate game logic and applying all chess rules. The primary challenge could be implementing complex chess rules, such as en passant and castling. Developing a user-friendly interface can also be improved in the future.
```"""
        expected_result = {
            "project": "ChessMate Gradle Game",
            "reply": "Sure, I will create a step-by-step plan to build a Chess game in a Java Gradle project.",
            "focus": "The main focus is to outline the stepwise process of setting up a Gradle project, designing the chess game logic and encapsulating the rules.",
            "plans": {
                1: "Set up a new Gradle project using an IDE like IntelliJ IDEA, setting the programming language to Java.",
                2: "Structure the project by creating packages for different game components - 'board', 'pieces', 'player', and 'game'.",
                3: "Begin coding the chess 'pieces' package. Each piece (pawn, rook, knight, bishop, queen, and king) should be a class extending from an abstract class 'Piece'.",
                4: "Within each 'Piece' subclass, define unique movements based on standard chess rules. For example, a knight can move in a 'L' pattern.",
                5: "Move onto the 'board' package and create a class 'Board'. It should contain a 8x8 grid and the initial arrangement of the pieces.",
                6: "Create a 'Player' class in the 'player' package. Player class should have player's information and current state of its pieces. Write functions to handle player's moves.",
                7: "Define game logic in 'game' package, like switching turns between players, checking checkmate, or stalemate conditions.",
                8: "Implement a simple console-based user interface to interact with the game. The user interface will show the board state and receive the user's actions.",
                9: "Test the game extensively, check all the rules of chess game are applied, and each piece is moving as it should in the game.",
                10: "Finally, build the Gradle project and run the tests. If vital, debug and refactor code.",
            },
            "summary": "The plan involves setting up a Gradle project, breaking down the chess game into components and implementing them step by step. The main considerations are creating accurate game logic and applying all chess rules. The primary challenge could be implementing complex chess rules, such as en passant and castling. Developing a user-friendly interface can also be improved in the future.",
        }

        planner = Planner("AZURE GPT")
        assert planner.parse_response(response) == expected_result
