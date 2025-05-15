from app import admin

from .user import User, UserAdmin
from .dataset import Dataset, DatasetAdmin
from .dataset_data import DatasetRow, DatasetRowAdmin
from .classification import Classification, ClassificationAdmin
from .classification_fold import ClassificationFold
from .tasks import Task, TaskAdmin

admin.add_view(UserAdmin)
admin.add_view(DatasetAdmin)
admin.add_view(DatasetRowAdmin)
admin.add_view(ClassificationAdmin)
admin.add_view(TaskAdmin)