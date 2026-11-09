# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/GrandBalaxon/Habits-Tracker/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                   |    Stmts |     Miss |   Cover |   Missing |
|----------------------- | -------: | -------: | ------: | --------: |
| config/\_\_init\_\_.py |        2 |        0 |    100% |           |
| config/celery.py       |        7 |        0 |    100% |           |
| config/urls.py         |        6 |        0 |    100% |           |
| habits/admin.py        |        8 |        0 |    100% |           |
| habits/apps.py         |        6 |        0 |    100% |           |
| habits/models.py       |       51 |       18 |     65% |41, 44-60, 70-71, 76, 81-82, 84-86 |
| habits/pagination.py   |        4 |        0 |    100% |           |
| habits/serializers.py  |       43 |        3 |     93% | 19, 72-73 |
| habits/services.py     |       57 |        4 |     93% |91-92, 113-114 |
| habits/signals.py      |        8 |        1 |     88% |        11 |
| habits/tasks.py        |       29 |       20 |     31% |17-45, 51-56 |
| habits/urls.py         |        4 |        0 |    100% |           |
| habits/views.py        |       41 |        0 |    100% |           |
| users/admin.py         |        8 |        0 |    100% |           |
| users/apps.py          |        3 |        0 |    100% |           |
| users/models.py        |       33 |        8 |     76% |  9, 17-25 |
| users/serializers.py   |       25 |       13 |     48% |26, 29-33, 36-42 |
| users/urls.py          |        4 |        0 |    100% |           |
| users/views.py         |       38 |        4 |     89% |29, 42, 55, 68 |
| **TOTAL**              |  **377** |   **71** | **81%** |           |

2 empty files skipped.


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/GrandBalaxon/Habits-Tracker/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/GrandBalaxon/Habits-Tracker/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/GrandBalaxon/Habits-Tracker/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/GrandBalaxon/Habits-Tracker/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2FGrandBalaxon%2FHabits-Tracker%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/GrandBalaxon/Habits-Tracker/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.