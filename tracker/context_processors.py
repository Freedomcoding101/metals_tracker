from .models import MetalsData

def subheader_context(request):
    # Initialize empty data
    subheader_data = {}

    # Fetch metals data if user is authenticated
    if request.user.is_authenticated:
        try:
            metals_data, created = MetalsData.objects.get_or_create(owner=request.user.profile)
            subheader_data['gold_price'] = metals_data.current_gold_price
            subheader_data['silver_price'] = metals_data.current_silver_price
            subheader_data['platinum_price'] = metals_data.current_platinum_price
        except MetalsData.DoesNotExist:
            subheader_data['gold_price'] = 'N/A'
            subheader_data['silver_price'] = 'N/A'
            subheader_data['platinum_price'] = 'N/A'

    return subheader_data
