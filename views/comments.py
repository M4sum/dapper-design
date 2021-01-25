from flask import Response, request
from flask_restful import Resource
from mongoengine import DoesNotExist, Q
import models
import json

class CommentListEndpoint(Resource):

    def queryset_to_serialized_list(self, queryset):
        serialized_list = [
            item.to_dict() for item in queryset
        ]
        return serialized_list
    
    def get(self):
        keyword = request.args.get('keyword')
        if keyword:
            # find data where *any of the fields contain the term...
            data = models.Post.objects.filter(
                Q(title__icontains=keyword) | 
                Q(content__icontains=keyword) | 
                Q(author__icontains=keyword)
            )
        else:
            data = models.Post.objects

        # formatting the output JSON
        data = self.queryset_to_serialized_list(data)
        return Response(json.dumps(data), mimetype="application/json", status=200)

    def post(self):
        body = request.get_json()
        post = models.Post(**body).save()
        serialized_data = {
            'id': str(post.id),
            'message': 'Post {0} successfully created.'.format(post.id)
        }
        return Response(json.dumps(serialized_data), mimetype="application/json", status=201)
        
class CommentDetailEndpoint(Resource):
    def put(self, id):
        post = models.Post.objects.get(id=id)
        request_data = request.get_json()
        post.title = request_data.get('title')
        post.content = request_data.get('content')
        post.author = request_data.get('author')
        post.save()
        print(post.to_json())
        return Response(post.to_json(), mimetype="application/json", status=200)
    
    def delete(self, id):
        post = models.Post.objects.get(id=id)
        post.delete()
        serialized_data = {
            'message': 'Post {0} successfully deleted.'.format(id)
        }
        return Response(json.dumps(serialized_data), mimetype="application/json", status=200)

    def get(self, id):
        post = models.Post.objects.get(id=id)
        return Response(post.to_json(), mimetype="application/json", status=200)

def initialize_routes(api):
    api.add_resource(CommentListEndpoint, '/api/comments', '/api/comments/')
    api.add_resource(CommentDetailEndpoint, '/api/comments/<id>', '/api/comments/<id>/')
    # api.add_resource(CommentListEndpoint, '/api/posts/<post_id>/comments', '/api/posts/<post_id>/comments/')
    # api.add_resource(CommentDetailEndpoint, '/api/posts/<post_id>/comments/<id>', '/api/posts/<post_id>/comments/<id>/')