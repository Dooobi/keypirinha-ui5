import keypirinha as kp
import keypirinha_util as kpu
import keypirinha_net as kpnet
import json
from .ui5_doc_entry import ui5_doc_entry as ui5_doc_entry

class ui5(kp.Plugin):
    """
    Plugin for easy access to UI5 documentation.
    """

    # NEUE URL VERWENDEN:
    # https://sapui5.hana.ondemand.com/test-resources/sap/m/designtime/apiref/api.json

    ITEMCAT_CLASS = kp.ItemCategory.USER_BASE + 1
    ITEMCAT_NAMESPACE = kp.ItemCategory.USER_BASE + 2

    all_ui5_nodes = []

    def __init__(self):
        super().__init__()

    def on_start(self):
        path = 'res://%s/%s'%(self.package_full_name(), 'icons/c.png')
        print(path)

        self.set_actions(self.ITEMCAT_CLASS, [
            self.create_action(
                name="copy",
                label="Copy",
                short_desc="Copy the name of the answer")])
        self.set_actions(self.ITEMCAT_NAMESPACE, [
            self.create_action(
                name="browser",
                label="Open in browser",
                short_desc="Open the namespace in the SAPUI5 documentation")])

        self.icon_handle_class = self.load_icon(path)
        self._parse_ui5_doc()

    def on_catalog(self):
        self.set_catalog([
            self.create_item(
                category = kp.ItemCategory.KEYWORD,
                label = "UI5",
                short_desc = "Documentation",
                target = "UI5",
                args_hint = kp.ItemArgsHint.ACCEPTED,   # the item can be executed directly but also accepts arguments
                hit_hint = kp.ItemHitHint.KEEPALL       # the item and the selected argument will be tracked in history
            )
        ])

    def on_suggest(self, user_input, items_chain):
        # Don't add suggestion items if items_chain is empty
        # (UI5 catalog item was not yet selected)
        if not items_chain:
            return

        kinds = []
        suggestion_items = []
        for ui5_entry in self.all_ui5_nodes:
            suggestion_items.append(ui5_entry.to_suggestion_item(self))
            # if (ui5_entry.nodes not in kinds):
            if ui5_entry.kind != "namespace" and ui5_entry.nodes is not None and len(ui5_entry.nodes) > 0:
                kinds.append(ui5_entry.name + ": " + str(len(ui5_entry.nodes)))

        for kind in kinds:
            print(kind)

        self.set_suggestions(suggestion_items)
        # self.set_suggestions([self.create_item(
        #     category=self.ITEMCAT_CLASS,
        #     label="Button",
        #     short_desc="sap.m.Button",
        #     target="sap.m.Button",
        #     args_hint=kp.ItemArgsHint.ACCEPTED,
        #     hit_hint=kp.ItemHitHint.IGNORE,
        #     icon_handle=self.icon_handle_class
        # )])

    def on_execute(self, item, action):
        pass

    def on_activated(self):
        pass

    def on_deactivated(self):
        pass

    def on_events(self, flags):
        pass

    def _parse_ui5_doc(self):
        opener = kpnet.build_urllib_opener()

        with opener.open("https://sapui5.hana.ondemand.com/docs/api/api-index.json") as response_file:
            response = response_file.read()
            
            j = json.loads(response.decode('utf-8'))

            for j_symbol in j['symbols']:
                self._parse_ui5_doc_node(j_symbol)

    def _parse_ui5_doc_node(self, j_node):
        ui5_entry = ui5_doc_entry()
        ui5_entry.name = j_node['name']
        ui5_entry.kind = j_node['kind']
        ui5_entry.visibility = j_node['visibility']
        ui5_entry.lib = j_node['lib']
        ui5_entry.display_name = j_node['displayName']
        ui5_entry.is_deprecated = j_node['bIsDeprecated']
        ui5_entry.nodes = []

        if 'nodes' in j_node:
            for j_child_node in j_node['nodes']:
                ui5_child_node = self._parse_ui5_doc_node(j_child_node)
                ui5_entry.nodes.append(ui5_child_node)
        
        self.all_ui5_nodes.append(ui5_entry)
        return ui5_entry
