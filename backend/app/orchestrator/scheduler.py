from backend.app.models.task import Task, TaskStatus

class Scheduler:
    def get_ready_tasks(self, tasks: list[Task])->list[Task]:
        task_map={task.id: task for task in tasks}
        ready_tasks=[]
        for t in tasks:
            if t.status != TaskStatus.Pending:
                continue
            dependencies_completed=all(
                task_map[d].status==TaskStatus.Completed
                for d in t.dependencies
            )

            if dependencies_completed:
                ready_tasks.append(t)
        ready_tasks.sort(key=lambda task: task.priority, reverse=True)
        return ready_tasks
    