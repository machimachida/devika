import pytest
from src.agents.coder.reference_code_finder import ReferenceCodeFinder
from src.config import Config
from src.filesystem import ReadCode


class TestReferenceCodeFinder:
    @pytest.mark.parametrize(
        [
            "instruction",
            "class_names",
            "method_names"
        ],
        [
            (  # TODO: このように補足として抽出対象メソッドを明示的に含めた場合でも、それらのメソッドが生成結果に必ず含まれるようにはならない。生成AIによらずシステム側で追加した方が確実。
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
            ), (
                """
# 物理設計書: `addItemToBasket` メソッド

## 概要

`addItemToBasket` メソッドは、指定されたカタログ商品を買い物かごに追加するための機能を提供します。このメソッドは、顧客ID、カタログ商品ID、および数量を入力として受け取り、カタログ商品が存在するかどうかを確認し、買い物かごに追加します。

## クラス

`jp.sample.applicationcore.applicationservice.ShoppingApplicationService`

## メソッドシグネチャ
```java
public void addItemToBasket(String buyerId, long catalogItemId, int quantity) throws CatalogNotFoundException
```

## 入力パラメータ

| パラメータ名 | 型        | 説明                             |
| ------------ | --------- | -------------------------------- |
| `buyerId`    | `String`  | 顧客ID                           |
| `catalogItemId` | `long` | カタログ商品ID                   |
| `quantity`   | `int`     | 数量                             |

## 例外

| 例外名                      | 説明                                 |
| --------------------------- | ------------------------------------ |
| `CatalogNotFoundException`  | 指定されたカタログ商品が存在しない場合 |

## 処理の流れ

0. **買い物かごの取得または作成**:
    - `getOrCreateBasketForUser` メソッドを使用して、指定された `buyerId` に対応する買い物かごを取得するか、無ければ新規に作成します。

1. **カタログ商品の存在確認**:
    - `catalogDomainService` の `existAll` メソッドを使用して、指定された `catalogItemId` がカタログに存在するかどうかを確認します。存在しない場合は `CatalogNotFoundException` をスローします。

2. **カタログ商品の取得**:
    - `catalogDomainService` の `getExistCatalogItems` メソッドを使用して、指定された `catalogItemId` に対応するカタログ商品を取得します。

3. **買い物かごにアイテムを追加**:
    - `Basket` の `addItem` メソッドを使用して、買い物かごにアイテムを追加します。
    - `Basket` の `removeEmptyItems` メソッドを使用して、数量が0のアイテムを買い物かごから削除します。

4. **買い物かごの更新**:
    - `basketRepository` の `update` メソッドを使用して、変更された買い物かごをデータベースに更新します。

## 注意事項

- 顧客ID (`buyerId`) は `null` または空文字列であってはならない。
- カタログ商品が存在しない場合は `CatalogNotFoundException` をスローする。
- 買い物かごの状態が変更された場合は、必ずデータベースに対して更新処理を行うこと。
                """,
                [
                    'jp.sample.Main',
                    'jp.sample.applicationcore.applicationservice.BasketDetail',
                    'jp.sample.applicationcore.applicationservice.ShoppingApplicationService'
                    'jp.sample.applicationcore.baskets.Basket',
                    'jp.sample.applicationcore.baskets.BasketItem',
                    'jp.sample.applicationcore.baskets.BasketNotFoundException',
                    'jp.sample.applicationcore.baskets.CatalogItemInBasketNotFoundException',
                    'jp.sample.applicationcore.catalog.CatalogBrand',
                    'jp.sample.applicationcore.catalog.CatalogCategory',
                    'jp.sample.applicationcore.catalog.CatalogDomainService',
                    'jp.sample.applicationcore.catalog.CatalogItem',
                    'jp.sample.applicationcore.catalog.CatalogItemAsset',
                    'jp.sample.applicationcore.catalog.CatalogNotFoundException',
                    'jp.sample.applicationcore.order.Address',
                    'jp.sample.applicationcore.order.CatalogItemOrdered',
                    'jp.sample.applicationcore.order.EmptyBasketOnCheckoutException',
                    'jp.sample.applicationcore.order.Order',
                    'jp.sample.applicationcore.order.OrderItem',
                    'jp.sample.applicationcore.order.OrderItemAsset',
                    'jp.sample.applicationcore.order.OrderNotFoundException',
                    'jp.sample.applicationcore.order.ShipTo',
                    'jp.sample.applicationcore.applicationservice.ShoppingApplicationServiceTest',
                ],
                [
                    'jp.sample.Main#main',
                    'jp.sample.applicationcore.applicationservice.ShoppingApplicationService#setQuantities',
                    'jp.sample.applicationcore.applicationservice.ShoppingApplicationService#getBasketDetail',
                    'jp.sample.applicationcore.applicationservice.ShoppingApplicationService#checkout',
                    'jp.sample.applicationcore.applicationservice.ShoppingApplicationService#getOrCreateBasketForUser',
                    'jp.sample.applicationcore.applicationservice.ShoppingApplicationService#createBasket',
                    'jp.sample.applicationcore.applicationservice.ShoppingApplicationService#mapToOrderItem',
                    'jp.sample.applicationcore.baskets.Basket#addItem',
                    'jp.sample.applicationcore.baskets.Basket#removeEmptyItems',
                    'jp.sample.applicationcore.baskets.Basket#isInCatalogItem',
                    'jp.sample.applicationcore.baskets.BasketItem#addQuantity',
                    'jp.sample.applicationcore.baskets.CatalogItemInBasketNotFoundException#convertCatalogIds',
                    'jp.sample.applicationcore.catalog.CatalogDomainService#getExistCatalogItems',
                    'jp.sample.applicationcore.catalog.CatalogDomainService#existAll',
                    'jp.sample.applicationcore.catalog.CatalogDomainService#existCatalogItemIdInItems',
                    'jp.sample.applicationcore.order.OrderItem#addAsset',
                    'jp.sample.applicationcore.applicationservice.ShoppingApplicationServiceTest#testAddItemToBasket_NormalCase_CallUpdateMethodInRepositoryOnce',
                    'jp.sample.applicationcore.applicationservice.ShoppingApplicationServiceTest#testAddItemToBasket_NormalCase_RemoveBasketItemIfQuantityIsZero',
                    'jp.sample.applicationcore.applicationservice.ShoppingApplicationServiceTest#testAddItemToBasket_ExceptionCase_ThrowsExceptionIfBasketNotFound',
                    'jp.sample.applicationcore.applicationservice.ShoppingApplicationServiceTest#testSetQuantities_NormalCase_CallUpdateMethodInRepositoryOnce',
                    'jp.sample.applicationcore.applicationservice.ShoppingApplicationServiceTest#testSetQuantities_NormalCase_UpdateQuantityOfItemsInBasket',
                    'jp.sample.applicationcore.applicationservice.ShoppingApplicationServiceTest#testSetQuantities_ExceptionCase_ThrowsExceptionIfCatalogItemNotFoundInCatalogRepository',
                    'jp.sample.applicationcore.applicationservice.ShoppingApplicationServiceTest#testSetQuantities_ExceptionCase_ThrowsExceptionIfItemNotInBasket',
                    'jp.sample.applicationcore.applicationservice.ShoppingApplicationServiceTest#testGetBasketDetail_NormalCase_CatalogInformationCorrespondingToCatalogIdIsRetrieved',
                    'jp.sample.applicationcore.applicationservice.ShoppingApplicationServiceTest#testGetBasketDetail_ExceptionCase_ExceptionIsThrownIfBuyerIdIsNullorBlank',
                    'jp.sample.applicationcore.applicationservice.ShoppingApplicationServiceTest#testCheckout_NormalCase_AddMethodInOrderRepositoryIsCalledOnce',
                    'jp.sample.applicationcore.applicationservice.ShoppingApplicationServiceTest#testCheckout_ExceptionCase_ExceptionIsThrownIfSpecifiedBasketIsEmpty',
                    'jp.sample.applicationcore.applicationservice.ShoppingApplicationServiceTest#createDefaultShipTo',
                    'jp.sample.applicationcore.applicationservice.ShoppingApplicationServiceTest#createDefaultAddress',
                    'jp.sample.applicationcore.applicationservice.ShoppingApplicationServiceTest#createDefaultOrderItems',
                    'jp.sample.applicationcore.applicationservice.ShoppingApplicationServiceTest#createCatalogItem',
                    'jp.sample.applicationcore.applicationservice.ShoppingApplicationServiceTest#blankStringSource',
                ]
            )
        ]
    )
    def test_execute_with_actual_llm(self, mocker, instruction, class_names, method_names):
        """
        実際にLLMを使用して検索を実行するテスト。
        返却される結果はLLMの出力に依存するため、具体的な結果はテストできない。
        そのため、単に結果を表示して目視で確認する。
        """

        mocker.patch.object(Config, 'get_projects_dir', return_value='/fakepath/project-name')
        class_names = {class_name: "file_path" for class_name in class_names}
        method_names = {method_name: "file_path" for method_name in method_names}
        mocker.patch.object(ReadCode, 'get_class_method_names', return_value=(
            class_names,
            method_names
        ))

        finder = ReferenceCodeFinder(base_model="AZURE GPT")
        result = finder.execute(instruction, "Project Name")
        print(result)
