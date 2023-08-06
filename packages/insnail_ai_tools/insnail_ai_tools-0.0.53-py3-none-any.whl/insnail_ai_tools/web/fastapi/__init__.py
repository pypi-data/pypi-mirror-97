def create_fast_api_app(cors: bool = True, health_check: bool = True, **kwargs):
    from fastapi import FastAPI
    from starlette.middleware.cors import CORSMiddleware

    app = FastAPI(**kwargs)
    if cors:
        # 跨域
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    if health_check:

        @app.get("/health-check")
        async def health_check_view():
            return {"code": "0000", "msg": "health"}

    return app
