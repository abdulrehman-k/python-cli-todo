# python-cli-todo
Simple, tested command-line to-do manager built in pure Python.



```bash
git clone https://github.com/abdulrehman-k/python-cli-todo.git
cd python-cli-todo
pip install .
```

```bash
todo add "Buy groceries"   # add a task
todo list                  # show all tasks
todo list --pending        # show unfinished tasks
todo done 1                # mark task 1 as done
todo delete 1              # delete task 1
```



```bash
pip install -e ".[dev]"
pytest

