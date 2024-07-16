"""
URL configuration for django_demo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import SchemaGenerator
from rest_framework.schemas.coreapi import LinkNode, insert_into
from django_demo.settings import DEBUG


class MySchemaGenerator(SchemaGenerator):

    def get_links(self, request=None):
        """
        Return a dictionary containing all the links that should be
        included in the API schema.
        """
        links = LinkNode()
        # target = {'sys': "系统相关","index":"测试相关接口","login":"免登录相关接口"}
        paths, view_endpoints = self._get_paths_and_endpoints(request)

        # Only generate the path prefix for paths that will be included
        if not paths:
            return None
        prefix = self.determine_path_prefix(paths)

        for path, method, view in view_endpoints:
            if not self.has_view_permissions(path, method, view):
                continue
            link = view.schema.get_link(path, method, base_url=self.url)

            subpath = path[len(prefix):]

            keys = self.get_keys(subpath, method, view)
            insert_into(links, keys, link)

        return links


urlpatterns = [
    # path("admin/", admin.site.urls),
    path('login/', include('src.Login.urls')),
    path('index/', include('src.Index.urls')),
    path('sys/', include('src.Sys.urls')),
]

if DEBUG:
    urlpatterns.append(path('docs/', include_docs_urls(title='后端示例项目',
                                                       description="登录账号：admin 密码：Aa111111 相关功能的接口在一起，可以进行页面全局搜索查看",
                                                       generator_class=MySchemaGenerator)), )
