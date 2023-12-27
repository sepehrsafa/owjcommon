from fastapi import Request


def get_trace_id(request: Request) -> str:
    """
    Dependency to extract trace_id from the request scope.
    """
    return request.scope.get("trace_id")
