"""
Views for Answer API
"""
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from core.models import Answer, User
from answer import serializers

class AnswerViewSet(viewsets.ModelViewSet):
    """View for manage Answer APIs"""
    serializer_class = serializers.AnswerDetailSerializer
    queryset = Answer.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.AnswerDetailSerializer
        
        return self.serializer_class

    # 유저의 응답 저장
    def create(self, request, *args, **kwargs):
        """Create or update user's answers"""
        # print(request.data)  # 들어오는 데이터 확인
        user = request.user
        answers_data = request.data.get('answers', [])

        if not answers_data:  # 빈 데이터 체크
            return Response({"message": "No answers provided."}, status=status.HTTP_400_BAD_REQUEST)

        # 기존 응답이 있는 경우 업데이트, 없으면 새로 생성
        answer_obj, created = Answer.objects.get_or_create(user=user)
        answer_obj.answer = answers_data
        answer_obj.save()

        return Response({"message": "Answers saved successfully."}, status=status.HTTP_201_CREATED)


    # 모든 유저의 답안 가져오기
    @action(detail=False, methods=['get'], url_path='all-answers')
    def get_all_answers(self, request):
        """Retrieve all users' answers"""
        user = request.user
        user_gender = user.gender

        # 본인을 제외한 성별이 같은 유저
        same_gender_users = User.objects.filter(gender=user_gender).exclude(id=user.id)
       
        # 해당 사용자들의 답안 가져오기
        all_answers = Answer.objects.filter(user__in=same_gender_users)
        serializer = self.get_serializer(all_answers, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)