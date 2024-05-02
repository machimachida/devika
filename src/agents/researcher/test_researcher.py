from .researcher import Researcher
from src.bert.sentence import SentenceBert

plan_text = """plan ::  ```
Project Name: Janken Gradle Game

Your Reply to the Human Prompter: Sure, let's build a Janken game using a Gradle project. This game will include tests to ensure the functionality is correct.

Current Focus: Creating a Java application using Gradle, implementing the Janken game logic and writing the necessary test cases.

Plan:
- [ ] Step 1: Create a new Gradle project using an IDE like IntelliJ. This will be a Java application.
- [ ] Step 2: Define initial project structure, including creating source and test directories.
- [ ] Step 3: Draft a design for the Janken game. This includes identifying the main classes and their interactions. The classes might include Player, Computer, and Game at least, and interactions will include actions like choosing a move and determining the winner.
- [ ] Step 4: Implement the defined classes and their functions in the source directory.
- [ ] Step 5: Introduce game logic into the Game class. This will include the rules of Janken (Rock, Paper, Scissors).
- [ ] Step 6: Code the logic for accepting input from the Player and randomly generating input for the Computer. 
- [ ] Step 7: Compile and run the project with Gradle to verify the basic flow of the game.
- [ ] Step 8: Write unit tests for the game logic, such as testing all possible outcomes of a round (Player win, Computer win, draw).
- [ ] Step 9: Use a testing framework like JUnit and Gradle's built-in test command to run and validate the tests.
- [ ] Step 10: Iterate over steps 4-9, refining code and adding additional tests as necessary. 

Summary: This plan creates a Janken game using a Gradle-based Java project. The main tasks include project setup, game design and implementation, and test writing. The plan aims to cover all essential parts of the game, including player input, computer decision-making, the game rules, and result determination. The JUnit testing framework is used for writing tests to validate the game logic and ensure the application functions as expected. The key challenge can be ensuring all possible outcomes are covered in the tests and that game rules are correctly implemented. 
```
"""

focus = "Creating a Java application using Gradle, implementing the Janken game logic and writing the necessary test cases"

class TestResearcher:
    def test_execute_with_actual_llm(self):
        researcher = Researcher(base_model="AZURE GPT")
        keyword_tuples = SentenceBert(focus).extract_keywords()
        collected_context_keywords: list[str] = []
        for keyword_tuple in keyword_tuples:
            collected_context_keywords.append(keyword_tuple[0])
        response = researcher.execute(plan_text, collected_context_keywords, "Janken Gradle Game")
        assert response is not False
        assert "queries" in response
        assert "ask_user" in response
        assert len(response["queries"]) > 0
        assert len(response["ask_user"]) > 0
