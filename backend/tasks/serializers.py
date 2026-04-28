from rest_framework import serializers
from .models import Task, Submission


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['created_by']


class SubmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Submission
        fields = '__all__'
        read_only_fields = ['user']

    def validate(self, data):
        description = data.get('description')
        link = data.get('link')
        file = data.get('file')

        # 🔴 Rule 1: At least one field required
        if not description and not link and not file:
            raise serializers.ValidationError(
                "Provide at least description, link, or file."
            )

        request = self.context.get('request')
        user = request.user
        task = data.get('task')

        # 🔴 Rule 2: Duplicate link check
        if link:
            if Submission.objects.filter(user=user, task=task, link=link).exists():
                raise serializers.ValidationError(
                    "Duplicate submission detected for this task."
                )

        return data