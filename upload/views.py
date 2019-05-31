from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, Http404
from posts.models import Post, Label
from upload.forms import UploadForm
from django.contrib import messages
import csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class UploadView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'upload/upload.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form'] = UploadForm()
        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            
            try:
                author = request.user.groups.get(name='author')
                print(author)
            except Exception as e:
                raise Http404('Not found')
        return super().get(request)

    def post(self, request):
        if not request.user.is_superuser:
            try:
                author = request.user.groups.get(name='author')
                print(author)
            except Exception as e:
                raise Http404('Not found')
        try:
            file = request.FILES['file']
            fs = FileSystemStorage()
            new_filename = file.name.replace(" ", "_")
            filename = fs.save(os.path.join(BASE_DIR, 'uploads/%s' % new_filename), file)
            print('filename: ', filename)
            upload_file_url = '/' + fs.url(filename)
            idx = upload_file_url.rindex('/') + 1
            path_file = upload_file_url[idx:len(upload_file_url)]
            posts = []
            with open(upload_file_url, 'r', newline='', encoding='utf-8') as csvFile:
                reader = csv.reader(csvFile, quoting=csv.QUOTE_MINIMAL)
                next(reader)
                for row in reader:
                    post = dict(name=row[0], thumbnail=row[1], new=row[2], min_range=row[3], max_range=row[4],
                                content=row[5], content_activity=row[6], preview=row[7], tags=row[8])
                    posts.append(post)
                print(posts)
            csvFile.close()
        except Exception as e:
            return JsonResponse(dict(error="%s" % e))
        form = UploadForm()
        return render(request, self.template_name, dict(posts=posts, file=path_file, length=len(posts),
                                                        form=UploadForm()))


class UploadPostsView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            try:
                author = request.user.groups.get(name='author')
                print(author)
            except Exception as e:
                raise Http404('Not found')

        upload_folder = os.path.join(BASE_DIR, 'uploads/')
        upload_file = os.path.join(upload_folder, kwargs['filename'])
        posts = []
        results = []
        ids = []
        try:
            with open(upload_file, 'r', newline='', encoding='utf-8') as csvFile:
                reader = csv.reader(csvFile, quoting=csv.QUOTE_MINIMAL)
                next(reader)
                for row in reader:
                    post = dict(name=row[0], thumbnail=row[1],
                                new=True if (row[2] == 'yes' or row[2] == 'True' or row[2] == 'true') else False,
                                min_range=row[3], max_range=row[4], content=row[5], content_activity=row[6],
                                preview=row[7], user=self.request.user, tags=row[8])
                    posts.append(post)
            csvFile.close()
            os.remove(upload_file)
        except Exception as e:
            raise Http404('Not found')

        for post in posts:
            try:
                tags = post['tags'].split(', ')
                post.pop('tags')
                print(tags)
                print(post)
                result = Post.objects.create(**post)
                ids.append(result.pk)

                for tag_item in tags:
                    try:
                        tag = Label.objects.get(name=tag_item)
                        print('getted tag: ', tag)
                    except Exception as e:
                        print(e)
                        print("tag with name: %s not exist" % tag_item)
                        tag = Label.objects.create(name=tag_item)
                        print('created tag:', tag)

                    tag.posts.add(result)

            except Exception as e:
                result = dict(type='error', error=str(e))
                pass
            print(result)
            results.append(result)
        print(results)
        s = ', '
        str_ids = s.join([str(post_id) for post_id in ids])
        print(str_ids)
        messages.success(request, 'Posts with ids: %s has been added.' % str_ids)

        return render(request, 'upload/posts-loaded.html', dict(results=results))
