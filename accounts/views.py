from rest_auth.registration.views import RegisterView
from rest_framework import status
from rest_framework.response import Response

class RegisterView(RegisterView):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response = {
            'status': "HTTP_"+str(status.HTTP_201_CREATED)+"_CREATED",
            'message': "회원가입이 완료되었습니다.",
            'response': self.get_response_data(user)
        }
        return Response(response, headers=headers)