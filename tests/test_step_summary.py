"""
Contains tests of the step_summary module.
"""

import pytest

from chktex_action.chktex import Analysis, Error
from chktex_action.step_summary import build_markdown_step_summary


@pytest.fixture(name="step_summary_fixture")
def summary_fixture() -> str:
    """
    Returns the correct Markdown markup for a step summary file.
    """

    return r"""Total files: 2, total errors: 2, total warnings: 1

### Path: fail.tex

- **Type**: Error 17
- **Line**: 5
- **Message**: Something went wrong.
- **Context**:

```tex
\end{document
    ^
```

### Path: fail.tex

- **Type**: Warning 2
- **Line**: 10
- **Message**: Something went wrong.
- **Context**:

```tex
\begin{document}
^^^^^^
```

### Path: another.tex

- **Type**: Error 15
- **Line**: 32
- **Message**: Something went wrong.
- **Context**:

```text
No context
```
"""


def test_build_markdown_step_summary(
    step_summary_fixture: str, error_list: list[Error]
) -> None:
    """
    Tests the build_markdown_step_summary function.
    """

    # Actual
    analysis = Analysis(error_list)
    step_summary = build_markdown_step_summary(error_list, str(analysis))

    # Assertions
    assert step_summary_fixture == step_summary
