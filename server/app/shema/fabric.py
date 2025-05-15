from .base import OrmModel, BaseModel

class SContourData(BaseModel):
    xx: list[float]
    yy: list[float]
    Z: list[list[int]]

class SPointData(BaseModel):
    x: list[float]
    y: list[float]
    classes: list[float]
    names: list[str]

class SDecisionBoundaryData(BaseModel):
    contour: SContourData
    training_points: SPointData
    test_points: SPointData