from .models import TargetTransaction
from .schedules import app


@app.task
def interest_append() -> None:
    """Task for interest append every day."""
    TargetTransaction.interest_append()
