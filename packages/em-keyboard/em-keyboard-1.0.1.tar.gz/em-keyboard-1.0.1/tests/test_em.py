from unittest.mock import call, patch

import pytest

from em import cli, xerox


@pytest.mark.parametrize(
    "test_name",
    [
        "star",
        ":star:",
    ],
)
@patch("em.docopt")
@patch("em.sys.exit")
@patch("builtins.print")
def test_star(mock_print, mock_exit, mock_docopt, test_name):
    # Arrange
    mock_docopt.return_value = {"<name>": [test_name], "--no-copy": None, "-s": None}

    # Act
    cli()

    # Assert
    if xerox:
        mock_print.assert_called_once_with("Copied! ⭐")
    else:
        mock_print.assert_called_once_with("⭐")


@patch("em.docopt")
@patch("em.sys.exit")
@patch("builtins.print")
def test_not_found(mock_print, mock_exit, mock_docopt):
    # Arrange
    mock_docopt.return_value = {"<name>": ["xxx"], "--no-copy": None, "-s": None}

    # Act
    cli()

    # Assert
    mock_print.assert_called_once_with("")


@patch("em.docopt")
@patch("em.sys.exit")
@patch("builtins.print")
def test_no_copy(mock_print, mock_exit, mock_docopt):
    # Arrange
    mock_docopt.return_value = {"<name>": ["star"], "--no-copy": True, "-s": None}

    # Act
    cli()

    # Assert
    mock_print.assert_called_once_with("⭐")


@patch("em.docopt")
@patch("em.sys.exit")
@patch("builtins.print")
def test_search_star(mock_print, mock_exit, mock_docopt):
    # Arrange
    mock_docopt.return_value = {"<name>": ["star"], "--no-copy": None, "-s": True}
    expected = (
        "💫  dizzy",
        "⭐  star",
        "✳️  eight_spoked_asterisk",
    )

    # Act
    cli()

    # Assert
    for arg in expected:
        assert call(arg) in mock_print.call_args_list
