from opentelemetry import trace
from opentelemetry.exporter import jaeger
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor
from microservice_template_core.settings import TracerConfig, ServiceConfig
tracer = None


def get_tracer():
    global tracer
    if not tracer:
        trace.set_tracer_provider(TracerProvider())
        jaeger_exporter = jaeger.JaegerSpanExporter(
            service_name=ServiceConfig.SERVICE_NAME,
            agent_host_name=TracerConfig.JAEGER_SERVER,
            agent_port=TracerConfig.JAEGER_PORT,
        )

        trace.get_tracer_provider().add_span_processor(
            BatchExportSpanProcessor(jaeger_exporter)
        )

        tracer = trace.get_tracer(__name__)
    return tracer
