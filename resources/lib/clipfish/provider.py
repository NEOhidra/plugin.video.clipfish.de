from resources.lib.kodion.utils import FunctionCache

__author__ = 'bromix'

from resources.lib.clipfish.client import Client
from resources.lib.kodion.items import DirectoryItem, VideoItem
from resources.lib import kodion


class Provider(kodion.AbstractProvider):
    def __init__(self):
        kodion.AbstractProvider.__init__(self)

        self._client = None
        self._local_map.update({'clipfish.categories': 30500,
                                'clipfish.highestrated': 30501,
                                'clipfish.mostviewed': 30502})
        pass

    def get_client(self, context):
        if not self._client:
            self._client = Client()
            pass

        return self._client

    def get_alternative_fanart(self, context):
        return self.get_fanart(context)

    def get_fanart(self, context):
        return context.create_resource_path('media', 'fanart.jpg')

    def get_wizard_supported_views(self):
        return ['default', 'episodes', 'tvshows']

    def _do_videos(self, context, json_data):
        result = []

        videos = json_data.get('videos', [])
        for video in videos:
            video_item = VideoItem(video['title'], video['video_url_wifi_quality'],
                                   image=video['media_content_thumbnail_large'])
            video_item.set_fanart(self.get_fanart(context))
            video_item.set_plot(video['description'])
            video_item.set_duration_from_seconds(int(video['media_length']))
            video_item.set_studio('clipfish.de')
            video_item.add_artist('clipfish.de')
            result.append(video_item)
            pass

        return result

    @kodion.RegisterProviderPath('^/show/(?P<show_id>\d+)/$')
    def _on_show(self, context, re_match):
        context.set_content_type(kodion.constants.content_type.EPISODES)

        result = []

        show_id = re_match.group('show_id')
        category = context.get_param('category', 'mostrecent')
        page = int(context.get_param('page', '1'))

        # root of show
        if page == 1 and category == 'mostrecent':
            # highestrated
            highestrated_item = DirectoryItem(context.localize(self._local_map['clipfish.highestrated']),
                                              context.create_uri(['show', show_id],
                                                                 {'page': page, 'category': 'highestrated'}))
            highestrated_item.set_fanart(self.get_fanart(context))
            result.append(highestrated_item)

            # mostviewed
            mostviewed_item = DirectoryItem(context.localize(self._local_map['clipfish.mostviewed']),
                                            context.create_uri(['show', show_id],
                                                               {'page': page, 'category': 'mostviewed'}))
            mostviewed_item.set_fanart(self.get_fanart(context))
            result.append(mostviewed_item)
            pass

        client = self.get_client(context)
        json_data = client.get_videos_of_show(show_id=show_id, category=category, page=page)
        result.extend(self._do_videos(context, json_data))

        return result

    @kodion.RegisterProviderPath('^/category/(?P<category_id>\d+)/$')
    def _on_category(self, context, re_match):
        context.set_content_type(kodion.constants.content_type.TV_SHOWS)
        context.add_sort_method(kodion.constants.sort_method.LABEL)

        result = []

        category_id = re_match.group('category_id')
        client = self.get_client(context)
        json_data = context.get_function_cache().get(FunctionCache.ONE_MINUTE * 10, client.get_categories)
        for category in json_data:
            if category['id'] == category_id:
                specials = category['specials']
                for show in specials:
                    show_item = DirectoryItem(show['title'], context.create_uri(['show', show['id']]),
                                              image=show['img_topbanner_ipad'])
                    show_item.set_fanart(self.get_fanart(context))
                    result.append(show_item)
                    pass
                break
            pass

        return result

    @kodion.RegisterProviderPath('^/categories/$')
    def _on_categories(self, context, re_match):
        result = []

        client = self.get_client(context)
        json_data = context.get_function_cache().get(FunctionCache.ONE_MINUTE * 10, client.get_categories)
        for category in json_data:
            title = category['title']
            category_item = DirectoryItem(title, context.create_uri(['category', category['id']]),
                                          image=context.create_resource_path('media', 'clipfish.png'))
            category_item.set_fanart(self.get_fanart(context))
            result.append(category_item)
            pass

        return result

    def on_root(self, context, re_match):
        result = []

        # highlights

        # categories
        categories_item = DirectoryItem(context.localize(self._local_map['clipfish.categories']),
                                        context.create_uri(['categories']),
                                        image=context.create_resource_path('media', 'clipfish.png'))
        categories_item.set_fanart(self.get_fanart(context))
        result.append(categories_item)

        # all videos

        return result

    pass