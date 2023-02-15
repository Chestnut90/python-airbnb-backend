from rest_framework.decorators import api_view


@api_view()  # default ["GET"]
def make_error_and_report_to_sentry(request):
    raise Exception("Error")
