from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from config.settings import settings


def configure_tracer():
    trace.set_tracer_provider(
        TracerProvider(resource=Resource({"service.name": "auth"}))
    )
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=settings.jaeger.host,
                agent_port=settings.jaeger.port,
            )
        )
    )


tracer = trace.get_tracer(__name__)


def d_trace(f):
    """Декоратор для трассировки"""

    def decor(*args, **kwargs):
        with tracer.start_as_current_span(f.__name__):
            return f(*args, **kwargs)

    return decor
