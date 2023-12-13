import datetime

from apiflask import Schema, APIBlueprint
from apiflask.fields import String

time_bp = APIBlueprint("Time", __name__, url_prefix="/time")


class TimeOut(Schema):
    time = String()


@time_bp.get("/")
@time_bp.output(TimeOut)
def get():
    return {
        "time": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
