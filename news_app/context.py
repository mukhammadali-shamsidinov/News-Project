from .models import News,Category
def lastest_app(request):
    context = {
        'lastest_news':News.publish.all().order_by('-published_time')[:10],
        'category':Category.objects.all()

    }
    return context