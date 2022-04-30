from airflow.models import BaseOperator


class ActionOperator(BaseOperator):
    """
    Operator used to execute action class during airflow DAG run.
    """

    ui_color = "black"
    ui_fgcolor = "#ce8dd8"

    def __init__(self, action_class, *args, **kwargs):

        base_kwargs = {"task_id": kwargs.pop("task_id")}
        super().__init__(*args, **base_kwargs)
        self.kwargs = kwargs
        self.action_class = action_class

    def execute(self, context):
        """
        Execute method that will be ran when DAG initiates
        """
        kwargs = self.render_template(self.kwargs, context)
        action = self.action_class(**kwargs)
        action.run()
