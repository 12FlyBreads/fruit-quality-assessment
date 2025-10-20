# fruit_info.py

class FruitInfo:
    def __init__(self) -> None:
        # Database
        self.info_db = {
            'apple': {
                'fresh': 'Shelf life: 7–14 days (refrigerated).',
                'rotten': 'Shelf life: 0 days (discard immediately).',
                'unriped': 'Shelf life: 3–5 days until ripe (room temperature).'
            },
            'banana': {
                'fresh': 'Shelf life: 3–5 days (room temperature).',
                'rotten': 'Shelf life: 0 days (discard immediately).',
                'unriped': 'Shelf life: 2–3 days until ripe (room temperature).'
            },
            'carrot': {
                'fresh': 'Shelf life: 15–30 days (refrigerated).',
                'rotten': 'Shelf life: 0 days (discard immediately).',
                'unriped': 'Shelf life: — (usually harvested ripe).'
            },
            'orange': {
                'fresh': 'Shelf life: 10–14 days (cool and dry place).',
                'rotten': 'Shelf life: 0 days (discard immediately).',
                'unriped': 'Shelf life: 5–7 days until ripe (room temperature).'
            },
            'mango': {
                'fresh': 'Shelf life: 3–5 days (room temperature).',
                'rotten': 'Shelf life: 0 days (discard immediately).',
                'unriped': 'Shelf life: 2–4 days until ripe (room temperature).'
            },
            'default': {
                'default': 'Shelf life: varies depending on the product.'
            }
        }

    def get_info(self, fruit, quality) -> str:
        """
        Searches for information about the given fruit and quality.
        :param fruit: Fruit name (e.g., 'apple')
        :param quality: Quality label (e.g., 'fresh')
        :return: Information string about the fruit's quality.
        """

        fruit_data = self.info_db.get(fruit, {})
        
        info = fruit_data.get(quality, None)
        
        if info:
            return info
        
        return self.info_db['default']['default']