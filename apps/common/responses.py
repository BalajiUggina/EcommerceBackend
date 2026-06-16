from rest_framework.response import Response

# resuable method for success response
def success_response(
    message,
    data=None,
    status_code=200
):
    return Response(
        {
            "success":True,
            "message": message,
            "data": data
        },
        status=status_code
    )

# # resuable method for failed response
def error_response(
    message,
    errors=None,
    status_code=400
):
    return Response(
        {
            "success":False,
            "message": message,
            "errors": errors
        },
        status=status_code
    )