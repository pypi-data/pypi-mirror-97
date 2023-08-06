from microservice_template_core.tools.flask_restplus import api
from flask_restx import Resource
from microservice_template_core.tools.logger import get_logger
from microservice_template_core.tools.prometheus_metrics import Prom
from microservice_template_core.tools.tracer import get_tracer


logger = get_logger()
tracer = get_tracer()

ns = api.namespace('core-endpoints', description='Core endpoints')


@ns.route('/health')
class Health(Resource):

    def get(self):
        """
            Return general health check result
        """
        with tracer.start_as_current_span("core-endpoint-health-get"):
            Prom.core_endpoint_get_health_count.inc(1)
            logger.debug(
                msg="Core endpoint test",
                extra={"tags": {
                        "route": "core-endpoints/health"
                    }}
            )

        return {"msg": "Healthy"}, 200
