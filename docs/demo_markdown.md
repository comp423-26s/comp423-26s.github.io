# Demo Markdown

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

## Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.
        
## Code Snippets

The following code snippet demonstrates line numbering as well as adding callout notes.

```python linenums="1"
foo: string = "bar"
for i in range(1, 3):
    print(i)  # (1)!

def f() -> int:
    return 42
```

1. :man_raising_hand: printing `i` will result in `1`, `2`, and then the loop completes

### Example of pulling code snippets from a file (and highlighting)

* `linenums` is where line numbering starts from
* `title` is added above the block of code to describe content
* `hl_lines` is optional and can highlight specific lines of code (offset from 1, regardless of line numbering start)

```python linenums="2" title="foo.py" hl_lines="3"
--8<-- "docs/demo_code.py:2:5"
```

## Graphics with `mermaid` (to be explored)

``` mermaid
sequenceDiagram
    participant WorkingDir as Working Directory
    participant Changed as Changed
    participant Staged as Staged
    participant Committed as Commit

    WorkingDir ->> Changed: Modify File
    Changed ->> Staged: git add
    Staged ->> Committed: git commit
    Changed ->> WorkingDir: git restore <file>
    Staged ->> Changed: git restore --staged <file>
    Committed ->> WorkingDir: git checkout <commit> <file>
```

| Method      | Description                          |
| ----------- | ------------------------------------ |
| `GET`       | :material-check:     Fetch resource  |
| `PUT`       | :material-check-all: Update resource |
| `DELETE`    | :material-close:     Delete resource |

| Date   | Topic              |                                    Links                                    |
| :----- | :----------------- | :-------------------------------------------------------------------------: |
| W 1/9  | Welcome to COMP423 | [:material-youtube:](https://youtube.com){: aria-label="YouTube Video" } [:material-file-powerpoint:](#){: aria-label="PowerPoint Slides" } |
| F 1/11 | git Repositories   |                      [:material-youtube:](https://foo){: aria-label="YouTube Video" }                      |


=== "C"

    ``` c
    #include <stdio.h>

    int main(void) {
      printf("Hello world!\n");
      return 0;
    }
    ```

=== "C++"

    ``` c++
    #include <iostream>

    int main(void) {
      std::cout << "Hello world!" << std::endl;
      return 0;
    }
    ```

!!! note

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.