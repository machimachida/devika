from unittest.mock import mock_open
from src.agents.coder.similarity_finder import SimilarityFinder
import src.config
from src.filesystem import ReadCode
import src.logger

sample_method_names = [
    "com.example.task.TaskService#getAllTasks",
    "com.example.task.TaskService#getTaskById",
    "com.example.task.TaskService#createTask",
    "com.example.task.TaskService#updateTask",
    "com.example.task.TaskService#deleteTask",
    "com.example.user.UserService#getAllUsers",
    "com.example.user.UserService#getUserById",
    "com.example.user.UserService#createUser",
    "com.example.user.UserService#updateUser",
    "com.example.user.UserService#deleteUser",
    "com.example.user.AuthenticationService#login",
    "com.example.user.AuthenticationService#logout",
    "com.example.user.UserService#changePassword",
    "com.example.user.UserService#resetPassword",
    "com.example.task.TaskService#setTaskPriority",
    "com.example.task.TaskService#getTaskByPriority",
    "com.example.task.TaskService#updateTaskPriority",
    "com.example.task.TaskService#removeTaskPriority",
    "com.example.task.TaskService#setTaskDeadline",
    "com.example.task.TaskService#getTasksByDeadline",
    "com.example.task.TaskService#updateTaskDeadline",
    "com.example.task.TaskService#removeTaskDeadline",
    "com.example.task.TaskService#addTaskToCategory",
    "com.example.task.TaskService#getTasksByCategory",
    "com.example.task.TaskService#updateTaskCategory",
    "com.example.task.TaskService#removeTaskFromCategory",
    "com.example.task.TaskService#setTaskProgress",
    "com.example.task.TaskService#getTasksByProgress",
    "com.example.task.TaskService#updateTaskProgress",
    "com.example.task.TaskService#completeTask",
    "com.example.task.NotificationService#sendTaskNotification",
    "com.example.task.NotificationService#getTaskNotifications",
    "com.example.task.NotificationService#updateTaskNotificationSettings",
    "com.example.task.NotificationService#deleteTaskNotification",
    "com.example.task.TaskService#assignTaskToUser",
    "com.example.task.TaskService#getTasksByAssignee",
    "com.example.task.TaskService#updateTaskAssignment",
    "com.example.task.TaskService#removeTaskAssignment"
]

sample_step_by_step_plan = """```
Project Name: Janken Game

Your Reply to the Human Prompter: Sure, I'll create a plan to develop a Janken Game in a Gradle project with a suitable unit test.

Current Focus: The main objective is to code a Janken Game, establish a Gradle project, and design proper unit tests.

Plan:
- [ ] Step 1: Initiate a new Gradle project in your chosen IDE (like IntelliJ IDEA).
- [ ] Step 2: Structure the project by creating necessary package directories such as 'main' for the primary source code and 'test' for the unit tests.
- [ ] Step 3: In the 'main' package, create a Java class (for instance, 'JankenGame') to build the Janken game logic.
- [ ] Step 4: In the 'JankenGame' class, develop the game functionality including the rules (rock crushes scissors, scissors cuts paper, and paper covers rock).
- [ ] Step 5: Implement user interface, like command-line interaction, to play the game.
- [ ] Step 6: After developing the main game logic, proceed to create tests. In the 'test' package, create a new Java class for the unit tests (for instance, 'JankenGameTest').
- [ ] Step 7: Make use of a testing framework like JUnit to write the unit tests. Each test should target individual functional units of the game.
- [ ] Step 8: Run the unit tests and ensure they all pass. If any test fails, debug the test or the code functionality in question, then rerun the tests.
- [ ] Step 9: After passing all tests, run the application from the main() method of 'JankenGame' class and manually test the game flow.
- [ ] Step 10: Finalize the code, comment as necessary, and ensure the gradle project properly builds and executes your Janken game.

Summary: This plan outlines the steps to build a Janken game in a gradle project, focusing on the functionality and also the unit tests. Key considerations are correct implementation of game logic and successful passing of all unit tests. Be cognizant of potential challenges in debugging, especially if tests are failing, and make sure to thoroughly validate the game flow in the final step.
```"""

sample_user_context = "No, there is." # Web検索を開始する前に、Devikaからの質問がある場合がある。その回答がここに入る。

sample_search_results = {
    'initializing a new gradle project using intellij idea': '```\n# Getting Started with Gradle in IntelliJ IDEA\n\nThis tutorial describes how to create and run a simple Gradle project in IntelliJ IDEA.\n\n## Required plugins\nGradle and Gradle Extension (installed and enabled by default)\n\n## Tutorial versions\n- Gradle version: 7.1\n- JDK version: 14\n- JUnit version: 5\n\nThe project used in this tutorial can be found on GitHub.\n\n## Step 1: Create a project\n\nTo create a Gradle project with Java in IntelliJ IDEA:\n\n1. On the welcome screen, click New Project.\n2. Specify your project\'s name (FizzBuzz) and location.\n3. Select the Java option and Gradle.\n4. IntelliJ IDEA automatically adds a project SDK (JDK) in the JDK field. In this tutorial, we use the open JDK 14 version.\n5. Leave the default Groovy for Gradle DSL and unselect the Add sample code option.\n6. Click Create.\n\n## Step 2: Add Java code\n\nAdd a main class (`FizzBuzzProcessor`) and the following code to it:\n```java\npackage com.gradle.tutorial;\n\npublic class FizzBuzzProcessor {\n    public static void main(String[] args) {\n        for (int i = 1; i <= 100; i++) {\n            System.out.println(convert(i));\n        }\n    }\n\n    public static String convert(int fizzBuzz) {\n        if (fizzBuzz % 15 == 0) {\n            return "FizzBuzz";\n        }\n        if (fizzBuzz % 3 == 0) {\n            return "Fizz";\n        }\n        if (fizzBuzz % 5 == 0) {\n            return "Buzz";\n        }\n        return String.valueOf(fizzBuzz);\n    }\n}\n```\n\n## Step 3: Run the application with Gradle\n\nTo run the application, open the `FizzBuzzProcessor` class in the editor and select Run \'FizzBuzzProcessor.main()\'.\n\n## Step 4: Run tests\n\nAdd a test class (`FizzBuzzTest`) with tests for the `convert()` method in the `FizzBuzzProcessor` class.\n\n## Step 5: Create an executable JAR file\n\nAdd the following code to the `build.gradle` file:\n\n```groovy\njar {\n    manifest {\n        attributes "Main-Class": "com.gradle.tutorial.FizzBuzzProcessor"\n    }\n\n    from {\n        configurations.runtimeClasspath.collect { it.isDirectory() ? it : zipTree(it) }\n    }\n}\n```\n\nTo build the application, run the `build` task in the Gradle tool window.\n\n## Step 6: Run the JAR file with Gradle\n\nModify the `build.gradle` file to run the JAR file:\n\n```groovy\nplugins {\n    id \'java\'\n    id \'application\'\n}\n\napplication {\n    mainClassName = \'com.gradle.tutorial.FizzBuzzProcessor\'\n}\n```\n\nThen, run the `gradlew run` command in the Run anything window.\n```', 'implementing rock paper scissors in java': "This task does not provide any specific text or title that needs to be translated or reformatted. Rather, it suggests a website trying to authenticate a user by using Cloudflare's security services.\n\nHowever, we can provide a sample reformatting:\n\nStart of the reformatted text:\n\n```markdown\n# Website Access Confirmation\n\nWhen you visit our website www.baeldung.com, it may take a few seconds to confirm that you are a human. This is a necessary step to ensure the security of the connection before proceeding.\n\nFor any inquiries or issues, please refer to the following identifier: Ray ID: 87fe99479aa73487.\n\nOur website performance and security are powered by Cloudflare.\n```\nEnd of reformatted text.", 'creating a command-line interface in java': 'The text extracted from the PDF render of a web page does not contain enough information or context for it to be converted to Markdown. There is no specific content, topic, or details that can be formatted or organized in Markdown format. It seems like a generic error or access authentication page. In this case, additional information or more text is needed to provide a context for conversion to Markdown.', 'creating unit tests in java with junit': '```\n# JUnit 5 Tutorial\n\nThis tutorial explains unit testing with JUnit with the JUnit 5 framework (JUnit Jupiter). It explains the creation of JUnit 5 tests with the Maven and Gradle build system. It demonstrates the usage of the Eclipse IDE for developing software tests with JUnit 5 but this tutorial is also valid for tools like Visual Code or IntelliJ.\n\nTo use JUnit 5 in a Maven project, you need to:\n\n- Configure to use Java 11 or higher, as this is required by JUnit5\n- Configure the maven-surefire-plugin and maven-failsafe-plugin to be at version 2.22.2 so that they can run JUnit5\n- Add dependencies to the JUnit5 API and engine for your test code\n\nIf you want your tests to cancel after the timeout period is passed you can use the assertTimeoutPreemptively() method.\n\n## UNIT TESTS \n\n```java\npackage com.vogella.junit5;\n\nclass CalculatorTest {\n\n    Calculator calculator;\n\n    @BeforeEach                                         \n    void setUp() {\n        calculator = new Calculator();\n    }\n\n    @Test                                               \n    @DisplayName("Simple multiplication should work")   \n    void testMultiply() {\n        assertEquals(20, calculator.multiply(4, 5),     \n                "Regular multiplication should work");\n    }\n\n    @RepeatedTest(5)                                    \n    @DisplayName("Ensure correct handling of zero")\n    void testMultiplyWithZero() {\n        assertEquals(0, calculator.multiply(0, 5),   "Multiple with zero should be zero");\n        assertEquals(0, calculator.multiply(5, 0),   "Those who multiply with zero should be zero");\n    }\n}\n```\n\n### Dynamic and parameterized tests\n\nJUnit 5 supports the creation of dynamic tests via code. You can also run tests with a set of different input values with parameterized tests.\n\n```java\n@Nested\nclass NestedExampleTest{\n    @Test\n    void testMethod(){\n        //Add test Code Here\n    }\n    @Nested\n    class NestedInsideTest{\n        @Test\n        void someOtherTestMethod(){\n            //Add test Code Here\n        }\n    }\n}    \n```\n## Testing exceptions and Conditional enablement\n\n```java\n @Test\n    void testName() throws Exception{\n        // only run on Linux\n        Assumptions.assumeTrue(System.getProperty("os.name").contains("Linux"));\n        assertTrue(true);\n    }\n```\n\nReference: [JUnit5 Doc](https://junit.org/junit5/docs/current/user-guide/)\n```', 'debugging in java: strategies and tactics': '```\n# Debugging in Java: Debugging Theory and Strategies By David Reilly\n\nOne of the most challenging tasks a developer faces is testing and debugging software applications. Isolating and fixing any faults found always falls to the developer. This is where debugging comes in!\n\n## Understand the Problem\nA “bug” is a software defect, the nature of which may or may not have been identified. Bugs can be present in all phases of the software development life cycle and in all sorts of software products.\n\nThe term “debugging” is used to cover a wide range of tasks but generally applies to the process of detecting, locating, and repairing “bugs.”\n\n### Detecting Bugs\nDetecting bugs is a simple task during the early stages of software development. It becomes harder the more peculiar the bugs are and as the software gets complicated.\n\nTo identify bugs effectively, a wide range of approaches is required. These can include formalized testing methodologies like alpha, beta testing and automated bug reports.\n\n### Locating Bugs\nLocating bugs is one of the hardest tasks a developer will face. In larger systems composed of dozens or hundreds of classes, tracking down the faulty component can be a complex task.\n\nWorking with code written by other developers can be especially difficult. The problem can often be very challenging to locate, particularly if one component of a system is interacting badly with another.\n\n### Repairing Bugs\nRepairing bugs, also known as implementing a “bug-fix,” can be a tiresome and frustrating process. Once repaired, you need to distribute the updated code to all the users - a task that Java simplifies.\n\nThe strategies above provide a starting point and highlight the challenges involved in debugging Java software.\n\n```java\n// Get JVM vendor/version\nString JVM = System.getProperty ("java.vendor") + \n            " " + System.getProperty("java.version");\n// Get OS vendor/version\nString OS = System.getProperty ("os.name") + \n            " v" + System.getProperty("os.version");\n```\nThe additional system information can also be obtained from the Properties object. Not every JVM supports this information, especially earlier versions of Java and some third-party implementations.\n\nIn the article “Debugging in Java: Techniques for Bug Eradication”, you can find useful techniques to help isolate bugs in Java and determine the exact sections holding the bugs.\n```'
}


class TestSimilarityFinder:
    def test_execute_with_actual_llm(self, mocker):
        # mocker.patch.object(src.config.Config, '__new__', return_value=src.config.Config)
        mocker.patch.object(src.config.Config, 'get_projects_dir', return_value='/fakepath/project-name')
        # mocker.patch.object(src.logger.Logger, '__init__', return_value=None)
        mocker.patch(ReadCode, 'get_methods_names', return_value={method_name: "file_path" for method_name in sample_method_names})

        step_by_step_plan = "Step by step plan"

        similarity_finder = SimilarityFinder(base_model="AZURE GPT")
        result = similarity_finder.execute(step_by_step_plan, "", "Project Name")
        print(result)
