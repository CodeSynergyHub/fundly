from rest_framework import serializers
from campaign.models import Campaign


class CampaignWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['title', 'description', 'goal_amount', 'start_date', 'end_date',
                  'creator_id']

    def validate_goal_amount(self, value):
        """
        Ensure that the goal_amount is positive.
        """
        if value < 0:
            raise serializers.ValidationError("Goal amount must be a positive value.")
        return value

    def create(self, validated_data):
        if validated_data.get("goal_amount") < 0:
            raise serializers.ValidationError({"goal_amount": "Goal amount must be a positive value."})
        return super().create(validated_data)


class CampaignDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['id', 'title', 'description', 'goal_amount', 'current_amount', 'start_date', 'end_date']


class CampaignReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['id', 'title', 'goal_amount', 'current_amount', 'start_date', 'end_date']
