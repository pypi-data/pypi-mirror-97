def create_flask_app(
    import_name: str, cors: bool = True, health_check: bool = True, **kwargs
):
    from flask import Flask, jsonify
    from flask_cors import CORS

    app = Flask(import_name, **kwargs)
    if cors:
        CORS(app)

    if health_check:

        @app.route("/health-check", methods=["GET"])
        def health_check_view():
            return jsonify({"code": "0000", "msg": "health"})

    return app
