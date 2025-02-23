from scripts.storage import storage
import uuid
import time

class history:
    histoies = {
        'txt2img': [],
        'txt2img_neg': [],
        'img2img': [],
        'img2img_neg': [],
    }
    favorites = {
        'txt2img': [],
        'txt2img_neg': [],
        'img2img': [],
        'img2img_neg': [],
    }
    max = 100
    storage = storage()

    def __init__(self):
        for type in self.histoies:
            self.histoies[type] = self.storage.get('history.' + type)
            if self.histoies[type] is None:
                self.histoies[type] = []
                self.__save_histories(type)

        for type in self.favorites:
            self.favorites[type] = self.storage.get('favorite.' + type)
            if self.favorites[type] is None:
                self.favorites[type] = []
                self.__save_favorites(type)

    def __save_histories(self, type):
        self.storage.set('history.' + type, self.histoies[type])

    def __save_favorites(self, type):
        self.storage.set('favorite.' + type, self.favorites[type])

    def get_histoies(self, type):
        histoies = self.histoies[type]
        for history in histoies:
            history['is_favorite'] = self.is_favorite(type, history['id'])
        return histoies

    def is_favorite(self, type, id):
        for favorite in self.favorites[type]:
            if favorite['id'] == id:
                return True
        return False

    def get_favorites(self, type):
        return self.favorites[type]

    def push_history(self, type, tags, prompt, name=''):
        if len(self.histoies[type]) >= self.max:
            self.histoies[type].pop(0)
        item = {
            'id': str(uuid.uuid1()),
            'time': int(time.time()),
            'name': name,
            'tags': tags,
            'prompt': prompt,
        }
        self.histoies[type].append(item)
        self.__save_histories(type)
        return item

    def get_latest_history(self, type):
        if len(self.histoies[type]) > 0:
            return self.histoies[type][-1]
        return None

    def set_history(self, type, id, tags, prompt, name):
        for history in self.histoies[type]:
            if history['id'] == id:
                history['tags'] = tags
                history['prompt'] = prompt
                history['name'] = name
                self.__save_histories(type)
                if self.is_favorite(type, id):
                    self.set_favorite(type, id, tags, prompt, name)
                return True
        return False

    def set_favorite(self, type, id, tags, prompt, name):
        for favorite in self.favorites[type]:
            if favorite['id'] == id:
                favorite['tags'] = tags
                favorite['prompt'] = prompt
                favorite['name'] = name
                self.__save_favorites(type)
                return True
        return False

    def set_history_name(self, type, id, name):
        for history in self.histoies[type]:
            if history['id'] == id:
                history['name'] = name
                self.__save_histories(type)
                for favorite in self.favorites[type]:
                    if favorite['id'] == id:
                        favorite['name'] = name
                        self.__save_favorites(type)
                return True
        return False

    def set_favorite_name(self, type, id, name):
        for favorite in self.favorites[type]:
            if favorite['id'] == id:
                favorite['name'] = name
                self.__save_favorites(type)
                for history in self.histoies[type]:
                    if history['id'] == id:
                        history['name'] = name
                        self.__save_histories(type)
                return True
        return False

    def dofavorite(self, type, id):
        if self.is_favorite(type, id):
            return False
        for history in self.histoies[type]:
            if history['id'] == id:
                self.favorites[type].append(history)
                self.__save_favorites(type)
                return True
        return False

    def unfavorite(self, type, id):
        if not self.is_favorite(type, id):
            return False
        for favorite in self.favorites[type]:
            if favorite['id'] == id:
                self.favorites[type].remove(favorite)
                self.__save_favorites(type)
                return True
        return False

    def remove_history(self, type, id):
        for history in self.histoies[type]:
            if history['id'] == id:
                self.histoies[type].remove(history)
                self.__save_histories(type)
                return True
        return False

    def remove_histories(self, type):
        self.histoies[type] = []
        self.__save_histories(type)
        return True

