"""
Contains tests of the step_summary module.
"""

import pytest

from chktex_action.chktex import Analysis, Error
from chktex_action.step_summary import build_markdown_step_summary


@pytest.fixture
def summary_fixture() -> str:
    """"""

    return """Total files: 2, total errors: 2, total warnings: 1

### Path: fail.tex

- **Type**: Error 17
- **Line**: 5
- **Message**: Something
- **Context**:

```tex

```

### Path: fail.tex

- **Type**: Warning 2
- **Line**: 10
- **Message**: Something
- **Context**:

```tex

```

### Path: another.tex

- **Type**: Error 15
- **Line**: 32
- **Message**: Something
- **Context**:

```tex

```
"""


def test_build_markdown_step_summary(
    summary_fixture: str, errors_list: list[Error]
) -> None:
    """"""

    analysis = Analysis(errors_list)
    step_summary = build_markdown_step_summary(errors_list, str(analysis))

    assert summary_fixture == step_summary
