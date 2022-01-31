from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import FastAPI, Query, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import List, Optional
from pathlib import Path
import nimporter
import traceback
import logging
import io

# from fractal import generateFractal
from nimFractal import pyGenFractal

nimporter.build_nim_extensions(root=Path("../"), danger=True)


class FractalConfig(BaseModel):
    colorA: Optional[List[int]]
    colorB: Optional[List[int]]
    translationX: Optional[float]
    translationY: Optional[float]
    transformation: Optional[float]
    fractalType: Optional[str]
    iterations: Optional[int]


def format_exception(e: Exception) -> str:
    return "".join(traceback.format_exception(type(e), e, e.__traceback__, 4))


# def save_to_mem(img) -> io.BytesIO:
#     image_mem = io.BytesIO()
#     img.save(image_mem, "PNG")
#     image_mem.seek(0)
#     return image_mem


app = FastAPI(
    title="CUhackit Fractal Project",
    version="1.0.0",
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=[
                "http://localhost:3000",
                "http://127.0.0.1:3000",
                "https://fractals.tech",
            ],
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            allow_headers=["*", "Authorization"],
            expose_headers=["*", "Authorization"],
        )
    ],
)

logger = logging.getLogger("main")


def log_exception(e: Exception) -> None:
    """Logs a nicely formatted exception"""

    if isinstance(e, (HTTPException, StarletteHTTPException)):
        return

    traceback_lines = format_exception(e).strip("\n").split("\n")

    for line in traceback_lines:
        logger.error(line)


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


# normally I would run this in a threadpool, but this is not supported by nimporter
@app.post("/fractal")
async def fractal(config: FractalConfig):
    image = pyGenFractal(
        config.translationX,
        config.translationY,
        config.transformation,
        *config.colorA,
        *config.colorB,
        config.fractalType,
        config.iterations,
    )

    return StreamingResponse(io.BytesIO(image))


@app.get("/gallery")
async def gallery():
    return FileResponse("gallery.html")
