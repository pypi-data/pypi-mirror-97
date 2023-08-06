import logging
from typing import List

from texta_entity_linker.entity_linker import EntityLinker


logging.basicConfig(
    format='%(levelname)s %(asctime)s: %(message)s',
    datefmt='%d.%m.%Y %H:%M:%S',
    level=logging.INFO
)


class EntityLinkerWrapper:
    """
    Takes the MLP generator as input, reads all the content and
    takes the whole input to produce detailed person information
    from the emails content.
    """


    def __init__(self, abbreviations_filepath: str = None):
        self.abbreviations_file = abbreviations_filepath
        self.concatenator = EntityLinker(self.abbreviations_file) if abbreviations_filepath else EntityLinker()


    def concat_from_generator(self, generator):
        """
        Takes a generator as an input which contains tuples containing the MLP
        and attachment information, parses their Texta Facts and then does entity-linking
        on the whole set.
        :param generator: Generator which yields a two-element tuple with dictionaries.
        :return: Yields all the linked information of the entities.
        """
        container = []
        for mlp_output, attachments in generator:
            container.append(mlp_output)

            for attachment in attachments:
                container.append(attachment)

        self.concatenator.from_json(container)

        logging.info("Starting the entity linking process, this might take some time...")
        self.concatenator.link_entities()

        for person_info in self.concatenator.to_json():
            if isinstance(person_info, dict):
                yield person_info
            elif isinstance(person_info, list):
                for item in person_info:
                    yield item


    def concat_from_list(self, mlp_output: List[dict]):
        self.concatenator.from_json(mlp_output)
        self.concatenator.link_entities()
        return self.concatenator.to_json()
