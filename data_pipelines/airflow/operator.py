from airflow.models import BaseOperator
import jinja2


class ActionOperator(BaseOperator):
    """
    Operator used to execute action class during airflow DAG run.
    """

    def __init__(self, action_class, *args, **kwargs):

        base_kwargs = {"task_id": kwargs.pop("task_id")}
        super().__init__(*args, **base_kwargs)
        self.kwargs = kwargs
        self.action_class = action_class
        self.jinja_env = jinja2.Environment()

    def execute(self, context):
        """
        Execute method that will be ran when DAG initiates
        """
        self.kwargs = self.render_template(self.kwargs, context)
        action = self.action_class(**self.kwargs)
        action.run()
