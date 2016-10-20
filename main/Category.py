class Category(object):
    def __init__(self, name, parent_id, uniq_name, offers_num, visual, models_num, children_count, type, advertising_model,
                 link, id):
        self.name = name
        self.parent_id = parent_id
        self.uniq_name = uniq_name
        self.offers_num = offers_num
        self.visual = visual
        self.models_num = models_num
        self.children_count = children_count
        self.type = type
        self.advertising_model = advertising_model
        self.link = link
        self.id = id
