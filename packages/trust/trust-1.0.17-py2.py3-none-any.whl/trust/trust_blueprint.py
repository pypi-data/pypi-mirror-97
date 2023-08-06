import trust
import flask
import os


def trust_blueprint(finder):
    domain = flask.Blueprint("trust", __name__)

    @domain.route("/", defaults={"path": ""}, methods=["GET"])
    @domain.route("/<path:path>", methods=["GET"])
    def handle_all(path):
        try:
            if path == "favicon.ico":
                flask.current_app.logger.info(
                    "favicon.ico was requested to Trust blueprint which will "
                    "respond with HTTP 404.")
                return "404 Not Found", 404

            request = flask.request
            query = "/" + path
            response_mode = request.args.get("response-mode", "json")
            optional = request.args.get("optional", 0) == 1
            credentials = (
                request.authorization
                if request.authorization and request.authorization.username
                else trust.Credentials.get_empty()
            )

            engine = trust.Trust(finder)
            response = engine.process(
                query, response_mode, credentials, optional)

            headers = {
                "Content-Length": str(len(response)),
                "Content-Type": _get_mime(response_mode) + "; charset=utf-8"
            }

            return response, 200, headers

        except trust.exceptions.NodeNotFoundException:
            return "404 Not Found", 404

        except Exception as e:
            flask.current_app.logger.exception(e)
            raise

    def _get_mime(response_mode):
        return {
            "json": "application/json"
        }.get(response_mode, "text/plain")

    return domain
