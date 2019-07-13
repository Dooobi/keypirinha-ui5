import keypirinha as kp

class ui5_doc_entry():

    name = None
    display_name = None
    lib = None
    kind = None
    visibility = None
    is_deprecated = None
    nodes = None

    def to_suggestion_item(self, plugin):
        return plugin.create_item(
                    category = plugin.ITEMCAT_CLASS,
                    label = self.name,
                    short_desc = self.lib,
                    target = self.name,
                    args_hint = kp.ItemArgsHint.ACCEPTED,   # the item can be executed directly but also accepts arguments
                    hit_hint = kp.ItemHitHint.KEEPALL       # the item and the selected argument will be tracked in history
                )