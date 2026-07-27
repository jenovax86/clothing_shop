from django.http import HttpResponse


def test(request: HttpResponse) -> HttpResponse:
    return HttpResponse("Hello World!")
