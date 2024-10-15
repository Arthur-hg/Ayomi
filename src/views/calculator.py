from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from src.api.calculator.db import OperationRecord
from src.api.calculator.managers import CalcultorStack
from src.extensions import get_db_session

router = APIRouter()


@router.post("/calc/")
async def process_operation(payload: Any = Body(None), session: Session = Depends(get_db_session)):
    try:
        result = CalcultorStack(session).calc(payload["operation"])
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except:
        raise HTTPException(status_code=500, detail="Something went wrong")

    return {"result": result}


@router.get("/calc/")
async def get_all_operation_as_csv(session: Session = Depends(get_db_session)):
    records = OperationRecord.get_all(session)

    csv = "operation,result\n"
    for record in records:
        csv += f"{record.operation},{record.result}\n"

    return {"history": csv}
