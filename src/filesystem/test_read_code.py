from unittest.mock import mock_open
from .read_code import ReadCode


class TestReadCode:
    def test_read_directory_empty(self, mocker):
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
