from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from events.models import Event
from .serializers import UserSerializer, EventSerializer

class RegisterAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        login(self.request, user)
        
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user_id': user.id}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        form = PasswordChangeForm(user=request.user, data=request.data)
        
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': form.errors}, status=status.HTTP_400_BAD_REQUEST)
        
   
   
        
# Event Api-Veiws




class EventListAPIView(ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventCreateAPIView(CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class EventDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

# class SubmissionCreateAPIView(CreateAPIView):
#     queryset = Submission.objects.all()
#     serializer_class = SubmissionSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         event_id = self.kwargs.get('pk')
#         event = Event.objects.get(pk=event_id)
#         serializer.save(participant=self.request.user, event=event)

class UserDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_created_events = Event.objects.filter(user=request.user)
        user_registered_events = Event.objects.filter(participants=request.user)

        # Filter out events that have already taken place
        user_registered_events = user_registered_events.exclude(
            date__lt=timezone.now().date(),
            time__lt=timezone.now().time()
        )

        user_created_events_serializer = EventSerializer(user_created_events, many=True)
        user_registered_events_serializer = EventSerializer(user_registered_events, many=True)

        return Response({
            'user_created_events': user_created_events_serializer.data,
            'user_registered_events': user_registered_events_serializer.data,
        })
        

class EventRegistrationAPIView(CreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        event_id = self.kwargs.get('pk')
        event = get_object_or_404(Event, slug=event_id)

        if event.available_slots > event.participants.count() and timezone.now() < event.registration_deadline and not event.participants.filter(id=self.request.user.id).exists():
            event.available_slots -= 1
            event.save()

            serializer.save(event=event, participant=self.request.user)
        else:
            raise serializers.ValidationError("Event registration failed")

        return Response({'message': 'Event registration successful'}, status=status.HTTP_201_CREATED)




class UnregisterFromEventAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        event = get_object_or_404(Event, slug=pk)

        if event.date < timezone.now().date() or (event.date == timezone.now().date() and event.time < timezone.now().time()):
            return Response({'reason': 'Event has already taken place.'}, status=status.HTTP_400_BAD_REQUEST)

        if request.user in event.participants.all():
            return Response({'reason': 'User is registered for this event.'}, status=status.HTTP_200_OK)
        else:
            return Response({'reason': 'User is not registered for this event.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, pk):
        event = get_object_or_404(Event, slug=pk)

        if event.date < timezone.now().date() or (event.date == timezone.now().date() and event.time < timezone.now().time()):
            return Response({'reason': 'Event has already taken place.'}, status=status.HTTP_400_BAD_REQUEST)

        if request.user in event.participants.all():
            event.available_slots += 1
            event.participants.remove(request.user)
            event.save()
            
            serializer = EventSerializer(event)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'reason': 'User is not registered for this event.'}, status=status.HTTP_404_NOT_FOUND)     
        
        
class EventSearchAPIView(ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        search_query = self.request.GET.get('search_query')
        queryset = Event.objects.all()

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        return queryset