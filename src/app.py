from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import FastAPI, Query, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from fastapi.staticfiles import StaticFiles
import traceback
import logging
import PIL
import io

from fractals.triangle import serpinskiTriangle


def format_exception(e: Exception) -> str:
    return "".join(traceback.format_exception(type(e), e, e.__traceback__, 4))


def log_exception(e: Exception, logger: logging.Logger) -> None:
    """Logs a nicely formatted exception"""

    if isinstance(e, (HTTPException, StarletteHTTPException)):
        return

    traceback_lines = format_exception(e).strip("\n").split("\n")

    for line in traceback_lines:
        logger.error(line)

def save_to_mem(img: PIL.Image) -> io.BytesIO:
    image_mem = io.BytesIO()
    img.save(image_mem)
    image_mem.seek(0)
    return image_mem

app = FastAPI(
    title="CUhackit Fractal Project",
    version="1.0.0",
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3000"],
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            allow_headers=["*", "Authorization"],
            expose_headers=["*", "Authorization"],
        )
    ]
)

logger = logging.getLogger("main")


@app.on_event("startup")
async def on_startup():
    pass


@app.on_event("shutdown")
async def on_shutdown():
    pass


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(req: Request, e: Exception) -> JSONResponse:
    log_exception(e)
    return JSONResponse(status_code=e.status_code, content={"detail": e.detail})


@app.exception_handler(Exception)
async def general_exception_handler(req: Request, e: Exception) -> JSONResponse:
    log_exception(e)
    return JSONResponse(
        status_code=500,
        content={
            "detail": f"An internal server error ocurred: {type(e).__qualname__} {e}",
        },
    )


@app.exception_handler(RequestValidationError)
async def req_validation_exception_handler(req: Request, e: Exception) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": e.errors()})

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def index():
    return FileResponse("index.html")

@app.get("/fractal/{fractal_type}")
async def fractal(fractal_type: str, scale: float = Query(...)):
    # params:
    # colors
    image: PIL.Image = None

    if fractal_type == "triangle":
        image = serpinskiTriangle()

    if image is None:
        raise HTTPException(status_code=404, detail="No fractal found")

    return StreamingResponse(save_to_mem(image))
