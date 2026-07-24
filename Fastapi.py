from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="Calculator API",
    description="Simple but powerful Calculator built with FastAPI",
    version="1.0"
)

# ==========================
# Pydantic Models
# ==========================

class CalculationRequest(BaseModel):
    num1: float
    num2: float
    operation: str = Body(
        ...,
        description="Choose: add, subtract, multiply, divide"
    )


class CalculationResponse(BaseModel):
    num1: float
    num2: float
    operation: str
    result: float
    message: str = "Calculation successful"


# ==========================
# Home Route
# ==========================

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Calculator API</title>
        </head>
        <body style="font-family:Arial;text-align:center;margin-top:50px;">
            <h1>🧮 Calculator API is Running!</h1>
            <p>Go to <a href="/docs">/docs</a> to test the calculator.</p>
        </body>
    </html>
    """


# ==========================
# Main Calculator
# ==========================

@app.post("/calculate", response_model=CalculationResponse)
def calculate(data: CalculationRequest):

    num1 = data.num1
    num2 = data.num2
    op = data.operation.lower()

    if op == "add":
        result = num1 + num2
        message = f"{num1} + {num2} = {result}"

    elif op == "subtract":
        result = num1 - num2
        message = f"{num1} - {num2} = {result}"

    elif op == "multiply":
        result = num1 * num2
        message = f"{num1} × {num2} = {result}"

    elif op == "divide":
        if num2 == 0:
            raise HTTPException(
                status_code=400,
                detail="Cannot divide by zero!"
            )

        result = num1 / num2
        message = f"{num1} / {num2} = {result}"

    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid operation. Use add, subtract, multiply, divide."
        )

    return CalculationResponse(
        num1=num1,
        num2=num2,
        operation=op,
        result=result,
        message=message
    )


# ==========================
# Individual Endpoints
# ==========================

@app.get("/add")
def add(a: float, b: float):
    return {"result": a + b}


@app.get("/subtract")
def subtract(a: float, b: float):
    return {"result": a - b}


@app.get("/multiply")
def multiply(a: float, b: float):
    return {"result": a * b}


@app.get("/divide")
def divide(a: float, b: float):

    if b == 0:
        raise HTTPException(
            status_code=400,
            detail="Cannot divide by zero!"
        )

    return {"result": a / b}


# ==========================
# Bonus: History (In-Memory)
# ==========================

calculations_history = []


@app.post("/calculate_history")
def calculate_with_history(data: CalculationRequest):

    result = calculate(data)

    calculations_history.append(result.model_dump())

    return result


@app.get("/history")
def get_history():
    return {
        "total_calculations": len(calculations_history),
        "history": calculations_history[-10:]
    }