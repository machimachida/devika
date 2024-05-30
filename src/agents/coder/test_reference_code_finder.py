import pytest
from src.agents.coder.reference_code_finder import ReferenceCodeFinder
import src.config
from src.filesystem import ReadCode
import src.logger


class TestReferenceCodeFinder:
    @pytest.mark.parametrize(
        [
            "instruction",
            "class_names",
            "method_names"
        ],
        [
            (  # TODO: このように補足的に入れた場合でも、それらのメソッドが生成結果に必ず含まれるようにはならない。生成AIによらずシステム側で追加した方が確実。
                    """```
## 概要
タスクに紐づいているリアクション一覧を取得するAPIを作成します。

## 補足
以下のクラス・メソッドも抽出するメソッドに含めてください。
- TaskService#sendTaskNotification
- TaskService#getTasksByAssignee
```""",
                    [
                        "com.example.task.Task",
                        "com.example.user.User",
                        "com.example.task.Notification"
                    ],
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
    def test_execute_with_actual_llm(self, mocker, instruction, class_names, method_names):
        """
        実際にLLMを使用して検索を実行するテスト。
        返却される結果はLLMの出力に依存するため、具体的な結果はテストできない。
        そのため、単に結果を表示して目視で確認する。
        """

        mocker.patch.object(src.config.Config, 'get_projects_dir', return_value='/fakepath/project-name')
        class_names = {class_name: "file_path" for class_name in class_names}
        method_names = {method_name: "file_path" for method_name in method_names}
        mocker.patch.object(ReadCode, 'get_class_method_names', return_value=(
            class_names,
            method_names
        ))

        finder = ReferenceCodeFinder(base_model="AZURE GPT")
        result = finder.execute(instruction, "Project Name")
        print(result)
