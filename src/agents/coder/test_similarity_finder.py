import pytest
from src.agents.coder.similarity_finder import SimilarityFinder
import src.config
from src.filesystem import ReadCode
import src.logger


class TestSimilarityFinder:
    @pytest.mark.parametrize(
        [
            "step_by_step_plan",
            "method_names"
        ],
        [
            (
                """```
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
```""",
                [
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
                ],
            ),
            (
                """```
概要
タスクに紐づいているリアクション一覧を取得するAPIを作成します。
```""",
                [
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
                ],
            ),
            (  # TODO: 補足的に入れた場合でも、生成結果にそれらのメソッドが含まれることはない。生成AIによらずシステム側で追加した方が確実。
                    """```
    ## 概要
    タスクに紐づいているリアクション一覧を取得するAPIを作成します。
    
    ## 補足
    以下のクラス・メソッドも抽出するメソッドに含めてください。
    - TaskService#sendTaskNotification
    - TaskService#getTasksByAssignee
    ```""",
                    [
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
                    ],
            )
        ]
    )
    def test_execute_with_actual_llm(self, mocker, step_by_step_plan, method_names):
        """
        実際にLLMを使用して検索を実行するテスト。
        返却される結果はLLMの出力に依存するため、具体的な結果はテストできない。
        そのため、単に結果を表示して目視で確認する。
        """

        mocker.patch.object(src.config.Config, 'get_projects_dir', return_value='/fakepath/project-name')
        mocker.patch.object(ReadCode, 'get_methods_names', return_value={method_name: "file_path" for method_name in method_names})

        similarity_finder = SimilarityFinder(base_model="AZURE GPT")
        result = similarity_finder.execute(step_by_step_plan, "Project Name")
        print(result)
