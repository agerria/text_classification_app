from fastapi import Depends
from fastapi_utils.cbv import cbv

from sqlalchemy import func

from . import router
from app.auth import AuthView

from app.shema.comparison import SIComparisonInfo
from app.logic.classifications import ClassificationLogic
from app.logic.comparison import ComparisonLogic
from app.logic.report.updater import ReportUpdater

from app.models import (
    Classification,
    Dataset
)


@cbv(router)
class ComparisonReportView(AuthView):
    @router.post('/report/info')
    async def info(self, body: SIComparisonInfo):
        # data = {}
        # for hash in body.hashs:
        #     data[hash] = ClassificationLogic.get_info(self.db, hash=hash)
        # return data
        
        columns = []
        for hash in body.hashs:
            columns.append(
                ComparisonLogic.get_classification_info(self.db, hash)
            )
        
        updater = ReportUpdater(columns)
        columns = updater.update_report()
        
        indicators = ComparisonLogic.get_indicators(self.db, body.hashs[0])
        
        return {
            'columns': columns,
            'indicators': indicators,
        }
    