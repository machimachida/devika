from pathlib import Path
from unittest.mock import mock_open
from .read_code import ReadCode

from src.config import Config


class TestReadCode:
    def test_read_directory_empty(self, mocker):
        mocker.patch.object(Config, '__new__', return_value=Config)
        mocker.patch.object(Config, 'get_projects_dir', return_value='/fakepath/project-name')

        # Mock os.path.join to return a path (adjust the logic as needed)
        mocker.patch('os.path.join', return_value='/fakepath/project-name')

        # Mock os.walk to simulate an empty directory
        mocker.patch('os.walk', return_value=[])

        # Instantiate ReadCode with a project name
        rc = ReadCode("Project Name")

        # Perform the method
        result = rc.read_directory()

        # Assert the result is an empty list
        assert result == []

    def test_read_directory_with_files(self, mocker):
        mocker.patch.object(Config, '__new__', return_value=Config)
        mocker.patch.object(Config, 'get_projects_dir', return_value='/fakepath/project-name')

        # Mock os.path.join to handle the path joining
        mocker.patch('os.path.join', side_effect=lambda *args: '/'.join(args))

        # Data to simulate os.walk
        files = [
            ('/fakepath/project-name', [], ['file1.py', 'file2.txt']),
        ]

        # Mock os.walk to return predefined file structure
        mocker.patch('os.walk', return_value=files)

        # Mocking open using mock_open
        m = mock_open(read_data='print("Hello, world!")')
        mocker.patch('builtins.open', m)

        # Instantiate and use ReadCode
        rc = ReadCode("Project Name")
        result = rc.read_directory()

        # Assert that we are getting correct filenames and their contents
        expected = [
            {'filename': '/fakepath/project-name/file1.py', 'code': 'print("Hello, world!")'},
            {'filename': '/fakepath/project-name/file2.txt', 'code': 'print("Hello, world!")'},
        ]
        assert result == expected
        assert m.call_count == 2  # open should be called twice

    def test_code_set_to_markdown(self, mocker):
        mocker.patch.object(Config, '__new__', return_value=Config)
        mocker.patch.object(Config, 'get_projects_dir', return_value='/fakepath/project-name')

        # Prepare a return value for read_directory using a mocker
        mocker.patch.object(ReadCode, 'read_directory', return_value=[
            {'filename': 'file1.py', 'code': 'print("Hello, Python")'},
        ])

        # Instantiate ReadCode
        rc = ReadCode("Project Name")
        markdown = rc.code_set_to_markdown()

        # Expected markdown string
        expected_markdown = "### file1.py:\n\n```\nprint(\"Hello, Python\")\n```\n\n---\n\n"

        # Check if generated markdown is correct
        assert markdown == expected_markdown

    def test_get_class_method_names(self, mocker):
        mocker.patch.object(Config, '__new__', return_value=Config)
        mocker.patch.object(Config, 'get_projects_dir', return_value='/fakepath/project-name')
        mocker.patch('os.path.join', side_effect=lambda *args: '/'.join(args))
        files = [
            ('/fakepath/project-name/src/java/com/example/lib', [], ['file2.java', 'file3.java']),
            ('/fakepath/project-name/src/java/com/example', [], ['file1.java', 'file4.java']),
        ]
        mocker.patch('os.walk', return_value=files)

        mock_file2 = mock_open(read_data='''package com.example.lib;

public class TestClass2 {
    private int number;

    public void testMethod2(String param) {
        System.out.println(param);
        System.out.println(number);
    }
}
''').return_value
        mock_file3 = mock_open(read_data='''package com.example.lib;

public class TestClass3 {
    private int number;

    public void testMethod3(String param) {
        System.out.println(param);
        System.out.println(number);
    }
    
    public void testMethod4(String param) {
        System.out.println(param);
        System.out.println(number);
    }
}
''').return_value
        mock_file1 = mock_open(read_data='''package com.example;

public class TestClass1 {
    private int number;

    public void testMethod1(String param) {
        System.out.println(param);
        System.out.println(number);
    }
}
''').return_value
        mock_file4 = mock_open(read_data='''package com.example;
        
public class TestClass4 {
    private int number1;
    private int number2;
}
''').return_value
        mocker.patch('builtins.open', side_effect=[mock_file2, mock_file3, mock_file1, mock_file4])

        rc = ReadCode("Project Name")
        classes, methods = rc.get_class_method_names()

        assert classes == {
            'com.example.TestClass4': '/fakepath/project-name/src/java/com/example/file4.java',
        }
        assert methods == {
            'com.example.TestClass1#testMethod1': '/fakepath/project-name/src/java/com/example/file1.java',
            'com.example.lib.TestClass2#testMethod2': '/fakepath/project-name/src/java/com/example/lib/file2.java',
            'com.example.lib.TestClass3#testMethod3': '/fakepath/project-name/src/java/com/example/lib/file3.java',
            'com.example.lib.TestClass3#testMethod4': '/fakepath/project-name/src/java/com/example/lib/file3.java',
        }

    def test_get_class_method_names_with_actual_files(self, mocker):
        mocker.patch.object(Config, '__new__', return_value=Config)
        mocker.patch.object(Config, 'get_projects_dir', return_value=str(Path('./data/projects')))
        rc = ReadCode("minimum")
        result = rc.get_class_method_names()
        print(result)
