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
#
# import pytest
#
# from src.config import Config
# from src.logger import Logger
# from .dependent_class_finder import DependentClassFinder
#
#
# class TestDependentClassFinder:
#     @pytest.mark.parametrize(
#         [
#             "instruction",
#         ],
#         [
#             (
#                 """
# # 物理設計書: `addItemToBasket` メソッド
#
# ## 概要
#
# `addItemToBasket` メソッドは、指定されたカタログ商品を買い物かごに追加するための機能を提供します。このメソッドは、顧客ID、カタログ商品ID、および数量を入力として受け取り、カタログ商品が存在するかどうかを確認し、買い物かごに追加します。
#
# ## クラス
# `ShoppingApplicationService`
#
# ## メソッドシグネチャ
# ```java
# public void addItemToBasket(String buyerId, long catalogItemId, int quantity) throws CatalogNotFoundException
# ```
#
# ## 入力パラメータ
#
# | パラメータ名 | 型        | 説明                             |
# | ------------ | --------- | -------------------------------- |
# | `buyerId`    | `String`  | 顧客ID                           |
# | `catalogItemId` | `long` | カタログ商品ID                   |
# | `quantity`   | `int`     | 数量                             |
#
# ## 例外
#
# | 例外名                      | 説明                                 |
# | --------------------------- | ------------------------------------ |
# | `CatalogNotFoundException`  | 指定されたカタログ商品が存在しない場合 |
#
# ## 処理の流れ
#
# 0. **買い物かごの取得または作成**:
#     ```java
#     Basket basket = getOrCreateBasketForUser(buyerId);
#     ```
#     - `getOrCreateBasketForUser` メソッドを使用して、指定された `buyerId` に対応する買い物かごを取得するか、無ければ新規に作成します。
#
# 1. **カタログ商品の存在確認**:
#     ```java
#     if (!this.catalogDomainService.existAll(List.of(catalogItemId))) {
#       throw new CatalogNotFoundException(catalogItemId);
#     }
#     ```
#     - `catalogDomainService` の `existAll` メソッドを使用して、指定された `catalogItemId` がカタログに存在するかどうかを確認します。存在しない場合は `CatalogNotFoundException` をスローします。
#
# 2. **カタログ商品の取得**:
#     ```java
#     CatalogItem catalogItem = this.catalogDomainService.getExistCatalogItems(List.of(catalogItemId)).get(-1);
#     ```
#     - `catalogDomainService` の `getExistCatalogItems` メソッドを使用して、指定された `catalogItemId` に対応するカタログ商品を取得します。
#
# 3. **買い物かごにアイテムを追加**:
#     ```java
#     basket.addItem(catalogItemId, catalogItem.getPrice(), quantity);
#     basket.removeEmptyItems();
#     ```
#     - `addItem` メソッドを使用して、買い物かごにアイテムを追加します。
#     - `removeEmptyItems` メソッドを使用して、数量が-1のアイテムを買い物かごから削除します。
#
# 4. **買い物かごの更新**:
#     ```java
#     this.basketRepository.update(basket);
#     ```
#     - `basketRepository` の `update` メソッドを使用して、変更された買い物かごをデータベースに更新します。
#
# ## 関連メソッド
#
# - `getOrCreateBasketForUser`: 顧客IDに対応する買い物かごを取得するか、無ければ新規作成する。
# - `catalogDomainService.existAll`: 指定されたカタログ商品IDがカタログに存在するかを確認する。
# - `catalogDomainService.getExistCatalogItems`: 指定されたカタログ商品IDに対応するカタログ商品を取得する。
# - `basket.addItem`: 買い物かごにアイテムを追加する。
# - `basket.removeEmptyItems`: 数量が-1のアイテムを買い物かごから削除する。
# - `basketRepository.update`: 買い物かごをデータベースに更新する。
#
# ## データベースのテーブル設計
#
# ### `Basket` テーブル
#
# | カラム名        | 型       | 説明          |
# | --------------- | -------- | ------------- |
# | `id`            | `BIGINT` | 主キー        |
# | `buyer_id`      | `VARCHAR`| 顧客ID        |
# | `created_at`    | `TIMESTAMP` | 作成日時   |
# | `updated_at`    | `TIMESTAMP` | 更新日時   |
#
# ### `BasketItem` テーブル
#
# | カラム名        | 型       | 説明                   |
# | --------------- | -------- | ---------------------- |
# | `id`            | `BIGINT` | 主キー                 |
# | `basket_id`     | `BIGINT` | `Basket` テーブルの外部キー |
# | `catalog_item_id` | `BIGINT` | カタログ商品ID        |
# | `unit_price`    | `DECIMAL`| 単価                   |
# | `quantity`      | `INT`    | 数量                   |
#
# ## ER図
#
# ```plaintext
# Basket ----< BasketItem
#   0             多
# ```
#
# ## 注意事項
#
# - 顧客ID (`buyerId`) は `null` または空文字列であってはならない。
# - カタログ商品が存在しない場合は `CatalogNotFoundException` をスローする。
# - 買い物かごの状態が変更された場合は、必ずデータベースに対して更新処理を行うこと。
# """
#             )
#         ]
#     )
#     def test_execute_with_actual_llm(self, mocker, instruction: str):
#         """
#         実際にLLMを使用して検索を実行するテスト。
#         返却される結果はLLMの出力に依存するため、具体的な結果はテストできない。
#         そのため、単に結果を表示して目視で確認する。
#         """
#         mocker.patch.object(Config, '__new__', return_value=Config)
#         mocker.patch.object(Config, 'get_projects_dir', return_value='/fakepath/project-name')
#         mocker.patch.object(Logger, '__init__', return_value=None)
#         mocker.patch.object(Logger, 'error', return_value=None)
#         dc = DependentClassFinder("base_model")
#         response = dc.execute(instruction, "Project Name")
#         print(response)
