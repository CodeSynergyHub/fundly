from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from campaign.models import Campaign
from campaign.permissions import IsCampaignOwner
from campaign.serializers import CampaignReadSerializer
from campaign.serializers.campaign import (
    CampaignWriteSerializer,
    CampaignDetailSerializer,
)


class CreateCampaignAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CampaignWriteSerializer

    def create(self, request, *args, **kwargs):
        try:
            request.data['creator_id'] = request.user.id
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Campaign created successfully',
                                 'id': serializer.instance.id},
                                status=status.HTTP_201_CREATED)
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CampaignRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CampaignDetailSerializer
    queryset = Campaign.objects.all()

    def retrieve(self, request, *args, **kwargs):
        try:
            campaign = self.get_object()
            serializer = self.serializer_class(campaign)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Campaign not found'}, status=status.HTTP_404_NOT_FOUND)


class CampaignUpdateDeleteAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsCampaignOwner]
    queryset = Campaign.objects.all()
    serializer_class = CampaignWriteSerializer

    def put(self, request, *args, **kwargs):
        try:
            campaign = self.get_object()
            # if campaign.creator_id != request.user.id:
            #     return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.serializer_class(campaign, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Campaign updated successfully'}, status=status.HTTP_200_OK)
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'message': 'Campaign not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        try:
            campaign = self.get_object()
            # if campaign.creator_id != request.user.id:
            #     return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

            campaign.delete()
            return Response({'message': 'Campaign deleted successfully'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Campaign not found'}, status=status.HTTP_404_NOT_FOUND)


class CampaignListSearchAPIView(generics.ListAPIView):
    serializer_class = CampaignReadSerializer
    queryset = Campaign.objects.all()

    def get_queryset(self):
        title = self.request.query_params.get("title")
        if title:
            return Campaign.objects.filter(title__icontains=title)
        return Campaign.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            campaigns = self.get_queryset()
            serializer = self.serializer_class(campaigns, many=True)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
