class TaskManager:
    def __init__(self):
        self._tasks_by_users = {}

    # Add a task
    # Return False if task already exists
    def add_task(self, user_id: int, task: str) -> bool:
        if user_id not in self._tasks_by_users:
            self._tasks_by_users[user_id] = []

        if task in self._tasks_by_users[user_id]:
            return False

        self._tasks_by_users[user_id].append(task) 
        return True               
        
    # Remove a task
    # Return False if task or user dont exists
    def remove_task(self, user_id: int, task: str) -> bool:
        if user_id not in self._tasks_by_users:
            return False

        if task not in self._tasks_by_users[user_id]:
            return False

        self._tasks_by_users[user_id].remove(task) 
        return True  
    
    # Shows the task list of a user
    def get_tasks(self, user_id: int) -> list[str]:
        return self._tasks_by_users.get(user_id, []).copy()
    