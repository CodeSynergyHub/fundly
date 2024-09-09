from django.urls import path

from campaign.views import CreateCampaignAPIView, CampaignRetrieveAPIView, CampaignUpdateDeleteAPIView, \
    CampaignListSearchAPIView

app_name = 'campaign'

urlpatterns = [
    path('campaign', CreateCampaignAPIView.as_view(), name='create_campaign'),
    path('campaign/<int:pk>/detail', CampaignRetrieveAPIView.as_view(), name='campaign_detail'),
    path('campaign/<int:pk>', CampaignUpdateDeleteAPIView.as_view(), name='campaign_ud'),
    path('campaign/all', CampaignListSearchAPIView.as_view(), name='campaign_list'),
]