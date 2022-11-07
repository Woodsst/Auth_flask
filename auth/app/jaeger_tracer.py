from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from config.settings import default_settings


def configure_tracer():
    trace.set_tracer_provider(TracerProvider(
        resource=Resource(
            {"service.name": "auth"})))
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=default_settings.jaeger_host,
                agent_port=default_settings.jaeger_port,
            )
        )
    )
