from rest_framework import serializers

class TaskInputSerializer(serializers.Serializer):
    title = serializers.CharField()

    due_date = serializers.DateField(required=False, allow_null=True)

    estimated_hours = serializers.FloatField(required=False, allow_null=True, min_value=0)

    importance = serializers.IntegerField(required=False, default=5)

    dependencies = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True
    )

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_importance(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError("Importance must be between 1 and 10.")
        return value
