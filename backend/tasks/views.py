from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response#used to send data back as JSON
from .models import Task, Submission
from .serializers import TaskSerializer, SubmissionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def task_list(request):

    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TaskSerializer(
        data=request.data,
        context={'request': request}
        )

        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data)
         
        return Response(serializer.errors)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def submission_list(request):

    if request.method == 'GET':
        submissions = Submission.objects.all()
        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SubmissionSerializer(
    data=request.data,
    context={'request': request}
)

        if serializer.is_valid():
           serializer.save(user=request.user)
           return Response(serializer.data)

        return Response(serializer.errors)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task(request, pk):
    try:
        task = Task.objects.get(id=pk)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"})

    # 🔐 ONLY creator or assigned user can update
    if request.user != task.created_by and request.user != task.assigned_to:
        return Response({"error": "Not allowed"})

    serializer = TaskSerializer(task, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def review_submission(request, pk):
    try:
        submission = Submission.objects.get(id=pk)
    except Submission.DoesNotExist:
        return Response({"error": "Submission not found"})

    # Only task creator can review
    if request.user != submission.task.created_by:
        return Response({"error": "Only task creator can review"})

    status = request.data.get("review_status")
    feedback = request.data.get("feedback")

    if status not in ['APPROVED', 'REJECTED']:
        return Response({"error": "Invalid status"})

    submission.review_status = status
    submission.feedback = feedback
    submission.reviewed_by = request.user
    submission.save()

    return Response({"message": "Submission reviewed"})