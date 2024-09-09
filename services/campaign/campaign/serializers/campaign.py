from rest_framework import serializers
from campaign.models import Campaign


class CampaignWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['title', 'description', 'goal_amount', 'start_date', 'end_date',
                  'creator_id']


class CampaignDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['id', 'title', 'description', 'goal_amount', 'current_amount', 'start_date', 'end_date']


class CampaignReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['id', 'title', 'goal_amount', 'current_amount', 'start_date', 'end_date']
