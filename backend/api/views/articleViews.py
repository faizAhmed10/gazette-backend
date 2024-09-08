from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from api.serializers.articleSerializer import *
from api.models import *
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination

def check_author(user):
    return Authors.objects.filter(user=user).exists()
    
class ArticlePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# CREATE ARTICLE
@api_view(['POST'])
def create_article(request):
    author = request.user
    if check_author(author):
        try:
            data = request.data
            image = request.FILES.get('image')
            category = Category.objects.get(name=data.get('category'))
            author_instance = Authors.objects.get(user=author)
            
            article = Article.objects.create(
                author= author_instance,
                image = image,
                title = data.get('title'),
                sub_title=data.get('sub_title'),
                category=category,
                content= data.get('content'),
                status= data.get('status')
            )
            article.save()
            serializer = ArticleSerializer(article, many=False)
            return Response(serializer.data)

        except Category.DoesNotExist:
            return Response({"details": "Category not found"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            message = {'details': str(e)}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    return Response("Unauthorized", status=status.HTTP_400_BAD_REQUEST)
        
# GET ARTICLE
@api_view(['GET'])
def get_fresh_articles(request):
    try:
        last_24_hours = timezone.now() - timedelta(hours=24)

        articles = Article.objects.filter(publish_date__gte=last_24_hours, status="published")   
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        message = {'details': str(e)}
        return Response(message, status=status.HTTP_400_BAD_REQUEST) 
    
@api_view(['GET'])
def get_articles(request):
    try:
        author_name = request.query_params.get('author')
        category_name = request.query_params.get('category')
        date = request.query_params.get('date')
        
        articles = Article.objects.filter(status="published")
        
        if author_name:
            articles = articles.filter(author__name=author_name)
        
        if category_name:
            articles = articles.filter(category__name=category_name)
        
        if date:
            articles = articles.filter(publish_date__date=date)
            
        paginator = ArticlePagination()
        result_page = paginator.paginate_queryset(articles, request)
        
        if not result_page:
            return Response({"details": "No articles found"}, status=status.HTTP_204_NO_CONTENT)
        serializer = ArticleSerializer(result_page , many=True)
        
        return paginator.get_paginated_response(serializer.data)
    except Exception as e:
        return Response({"details": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_article(request, id):
    try:
        article = Article.objects.get(id=id)
        serializer = ArticleSerializer(article, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"details": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_my_articles(request):
    author = request.user
    if check_author(author):
        try:
            author_instance = Authors.objects.get(user=author)
            articles = Article.objects.filter(author=author_instance)
            serializer = ArticleSerializer(articles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    else:
        return Response("Unauthorized", status=status.HTTP_400_BAD_REQUEST)

# UPDATE ARTICLE
@api_view(['PUT'])
def update_article(request, id):
    author = request.user
    if check_author(author):
        try:
            data = request.data
            article = Article.objects.get(id=id)
            image = request.FILES.get('image')
            category = Category.objects.get(name=data.get('category'))
            
            article.title = data.get('title')
            article.sub_title = data.get('sub_title')
            article.category = category
            article.content = data.get('content')    
            article.status = data.get('status').lower()       
            if image:
                article.image = image
                
            article.save()
            return Response("Article updated successfully", status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    else:
        return Response("Unauthorized", status=status.HTTP_400_BAD_REQUEST)

# DELETE ARTILCE
@api_view(['DELETE'])
def delete_article(request, id):
    author = request.user
    if check_author(author):
        try:
            article = get_object_or_404(Article, id=id)
            if article:
                article.delete()
            return Response("Article deleted successfully", status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

# CATEGORY

@api_view(['GET', 'POST'])
def category_list_create(request):
    
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = CategorySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET'])
def get_authors(request):
    user = request.user
    try:
        authors = Authors.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"details": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_categories(request):
    user = request.user
    try:
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"details": str(e)}, status=status.HTTP_400_BAD_REQUEST)