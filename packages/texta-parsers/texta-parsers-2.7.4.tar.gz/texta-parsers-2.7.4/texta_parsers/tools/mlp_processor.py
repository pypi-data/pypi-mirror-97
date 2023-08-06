import logging

logging.basicConfig(
    format='%(levelname)s %(asctime)s: %(message)s',
    datefmt='%d.%m.%Y %H:%M:%S',
    level=logging.INFO
)


class MLPProcessor:
    """
    A wrapper class to apply MLP to DocParser documents.
    """
    def __init__(self, mlp):
        self.mlp = mlp
        self.IGNORE_FIELDS = ("texta_facts", "properties", "texta_face_vectors")


    def apply_mlp(self, generator, analyzers=["all"]):
        """ Applies MLP to objects in a given generator.
        """
        for item in generator:
            # check if email (it returns a tuple because of attachments)
            if isinstance(item, tuple):
                email, attachments = item
                self._apply_mlp_to_mails(email, attachments, analyzers)
            else:
                self._apply_mlp_to_item(item, analyzers)
            yield item


    def _apply_mlp(self, document: dict, field: str, analyzers: list):
        if (field not in document):
            return
        content = document.get(field, "")

        if content:
            mlp_res = self.mlp.process(content, analyzers=analyzers)
            mlp_res_path = field + "_mlp"
            # Add the MLP output dictionary.
            document[mlp_res_path] = mlp_res["text"] 

            facts = []
            for f in mlp_res["texta_facts"]:
                f["doc_path"] = f"{mlp_res_path}.text"
                facts.append(f)

            if facts:
                document["texta_facts"] = facts


    def _apply_mlp_to_mails(self, email: dict, attachments: list, analyzers: list):
        self._apply_mlp(email, "body", analyzers)
        for attachment in attachments:
            self._apply_mlp(attachment, "content", analyzers)


    def _apply_mlp_to_item(self, item: dict, analyzers: list):
        # apply it to all fields as we don't know anything about the item or it's fields
        item_copy = item.copy()
        for key in item_copy.keys():
            if key not in self.IGNORE_FIELDS:
                self._apply_mlp(item, key, analyzers)

