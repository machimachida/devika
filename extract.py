import ast
import astor


def extract_class_and_method(code, class_name, method_name):
    tree = ast.parse(code)
    class_node = None
    dependencies = []

    # クラスノードと依存関係を見つける
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            class_node = node
        elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            dependencies.append(node)

    # 指定されたクラスが見つからない場合
    if not class_node:
        return "Class not found."

    # クラス内のメソッドを見つけ、抽出する
    method_node = None
    for node in class_node.body:
        if isinstance(node, ast.FunctionDef) and node.name == method_name:
            method_node = node
            break

    # 指定されたメソッドが見つからない場合
    if not method_node:
        return "Method not found."

    # コンストラクタと指定されたメソッドを含む新しいクラスを作成
    new_class = ast.ClassDef(
        name=class_node.name,
        bases=class_node.bases,
        keywords=class_node.keywords,
        body=[node for node in class_node.body if isinstance(node, ast.FunctionDef) and node.name in ['__init__', method_name]],
        decorator_list=class_node.decorator_list
    )

    # 新しいASTを作成し、依存関係と新しいクラスを含める
    new_ast = ast.Module(body=dependencies + [new_class], type_ignores=[])

    # ソースコードに変換
    return astor.to_source(new_ast)

# 使用例


code: str
# ファイルからコードを読み込む
with open("sample.py", "r") as file:
    code = file.read()

className = "Agent"
methodName = "search_queries"
extracted_code = extract_class_and_method(code, className, methodName)
print(extracted_code)

# ファイル出力
with open("extracted_code3.py", "w") as file:
    file.write(extracted_code)

