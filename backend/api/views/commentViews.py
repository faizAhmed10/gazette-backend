from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from api.serializers.commentSerializer import CommentSerializer
from api.models import Article, Comment
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

class CommentPagination(PageNumberPagination):
    page_size = 5  # Number of comments per page
    page_size_query_param = 'page_size'
    max_page_size = 50

@api_view(['POST'])
def create_comment(request, id):
    user = request.user
    data = request.data

    try:
        comment_text = data['comment']
        article = get_object_or_404(Article, id=id)
        parent_id = data.get('parent')

        parent_comment = Comment.objects.get(id=parent_id) if parent_id else None

        comment = Comment.objects.create(
            user=user,
            comment=comment_text,
            article=article,
            parent=parent_comment
        )

        return Response({"detail": "Comment successful!"}, status=status.HTTP_201_CREATED)

    except Comment.DoesNotExist:
        return Response({"detail": "Parent comment not found."}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"details": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# GET COMMENTS
@api_view(['GET'])
def get_comments(request, id):
    try:
        article = get_object_or_404(Article, id=id)
        all_comments = Comment.objects.filter(article=article)

        # Build a dictionary to hold comments and replies
        comment_dict = {}
        for comment in all_comments:
            comment_dict[comment.id] = {
                'id': comment.id,
                'user': comment.user.username,
                'comment': comment.comment,
                'created_at': comment.created_at,
                'replies': [],
                'parent': comment.parent.id if comment.parent else None
            }

        # Populate replies (flattening all replies under the original parent)
        for comment in all_comments:
            if comment.parent:
                # Add to the original parent comment's replies
                comment_dict[comment.parent.id]['replies'].append(comment_dict[comment.id])

        # Filter top-level comments (those without a parent)
        top_level_comments = [comment for comment in comment_dict.values() if comment['parent'] is None]

        # Paginate top-level comments
        paginator = CommentPagination()
        result_page = paginator.paginate_queryset(top_level_comments, request)

        if not result_page:
            return Response({"details": "No comments found"}, status=status.HTTP_204_NO_CONTENT)

        return paginator.get_paginated_response(result_page)

    except Exception as e:
        return Response(
            {"details": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

# DELETE COMMENT
@api_view(['DELETE'])
def delete_comment(request, id):
    user = request.user
    try:
        comment = get_object_or_404(Comment, id=id, user=user)
        comment.delete()
        return Response({"detail": "Comment deleted successfully"}, status=status.HTTP_200_OK)

    except Comment.DoesNotExist:
        return Response({"detail": "Comment not found or you do not have permission to delete it."}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
