class TaskManager:
    """Manages user-specific tasks in a dictionary-based storage."""
    def __init__(self):
        self._tasks_by_users = {}

    def add_task(self, user_id: int, task: str) -> None:
        """Registers a new task for a specific user.

        Args:
            user_id (int): The Discord user ID.
            task (str): The name/description of the task to add.

        Raises:
            ValueError: If the task already exists in the user's list.
        """
        if user_id not in self._tasks_by_users:
            self._tasks_by_users[user_id] = []

        if task in self._tasks_by_users[user_id]:
            raise ValueError(f'You already have a task named "{task}" setted!')

        self._tasks_by_users[user_id].append(task)            

    def remove_task(self, user_id: int, task: str) -> bool:
        """Removes a task from a user's list and marks it as complete.

        Args:
            user_id (int): The Discord user ID.
            task (str): The name of the task to be removed.

        Raises:
            ValueError: If the user has no tasks or the specific task is not found.

        Returns:
            bool: True if the operation was successful.
        """
        if user_id not in self._tasks_by_users or task not in self._tasks_by_users[user_id]:
            raise ValueError(f'You have no tasks named "{task}"!')

        self._tasks_by_users[user_id].remove(task) 
        return True  
    
    # Shows the task list of a user
    def get_tasks(self, user_id: int) -> list[str]:
        """Retrieves a copy of the user's current task list.

        Args:
            user_id (int): The Discord user ID.

        Raises:
            ValueError: If the user's task list is empty or does not exist.

        Returns:
            list[str]: A list of task strings.
        """
        tasks = self._tasks_by_users.get(user_id, [])
        if not tasks:
            raise ValueError('You have no tasks!')
        return tasks.copy()
    