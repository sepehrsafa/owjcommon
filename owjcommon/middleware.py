import uuid


class TraceIDMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # Check if it's a HTTP request (as opposed to a websocket or other protocol)
        if scope["type"] == "http":
            # Extract headers from the scope
            headers = {
                k.decode("utf-8"): v.decode("utf-8") for k, v in scope["headers"]
            }

            # Check if trace_id exists in headers
            trace_id = headers.get("X-Trace-ID")

            # If not, generate a new trace ID
            if not trace_id:
                trace_id = str(uuid.uuid4())

            # Log the trace ID
            # logger.info(f"Received request with trace ID: {trace_id}")

            # Update the scope with the trace ID so it's available in the application
            scope["trace_id"] = trace_id

            # Custom send function to modify the response headers
            async def _send(message):
                if message.get("type") == "http.response.start":
                    # Append trace_id to the response headers
                    headers_list = message.setdefault("headers", [])
                    headers_list.append([b"X-Trace-ID", trace_id.encode("utf-8")])
                await send(message)

            # Use the custom _send function
            await self.app(scope, receive, _send)
        else:
            await self.app(scope, receive, send)
