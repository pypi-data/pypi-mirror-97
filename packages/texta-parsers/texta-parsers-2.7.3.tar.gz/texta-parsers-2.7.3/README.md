# texta-parsers

A Python package for file parsing.

The main class in the package is **DocParser**. The package also supports sophisticated parsing of emails which is implemented in class **EmailParser**. If you only need to parse emails then you can specify it with parameter `parse_only_extensions`. It is possible to use **EmailParser** independently as well but then attachments will not be parsed. 


## Requirements

Most of the file types are parsed with **[tika](http://tika.apache.org/)**. Other tools that are required:

| Tool | File Type |
|---|---|
| pst-utils | .pst  |
| digidoc-tool | .ddoc .bdoc .asics .asice |
| rar-nonfree  | .rar |
| lxml | XML HTML |

Installation of required packages on Ubuntu/Debian:

`sudo apt-get install pst-utils rar python3-lxml cmake build-essential -y`

`sudo sh install-digidoc.sh`

Requires our custom version of Apache TIKA with relevant Tesseract language packs installed:

`sudo docker run -p 9998:9998 docker.texta.ee/texta/texta-parsers-python/tikaserver:latest`

## Installation

Base install (without MLP & Face Analyzer):

`pip install texta-parsers`

Install with MLP:

`pip install texta-parsers[mlp]`

Install with Face Analyzer:

`pip install texta-parsers[face-analyzer]`

Install with whole bundle:

`pip install texta-parsers[mlp,face-analyzer]`


## Testing

`python -m  pytest -rx -v tests`


## Description

#### DocParser

A file parser. Input can either be in bytes or a path to the file as a string. See [user guide](https://git.texta.ee/texta/email-parser/-/wikis/DocParser/User-Guide/Getting-started) more information. DocParser also includes EmailParser.

#### EmailParser

For parsing email messages and mailboxes. Supported file formats are Outlook Data File (**.pst**), mbox (**.mbox**) and EML (**.eml**). Can be used separately from DocParser but then attachments are not parsed.
User guide can be found [here](https://git.texta.ee/texta/email-parser/-/wikis/EmailParser/User-Guide/Getting-started) and documentation [here](https://git.texta.ee/texta/email-parser/-/wikis/EmailParser/Documentation/1.2.1).


#### Entity Linker Pipeline

EntityLinkers wrapper can only be used if the previous generator passed through
it belongs to the MLP processor (it needs mlp-processed documents to function).

In the following example, the mailbox "Корзина.mbox" will be parsed by the EmailParser,
processed by the Texta MLP worker to enhance the text with additional information about its entities.
Those entities are then loaded into the memory to be used as the Entity Linkers input.

Finally the entity linked results will be passed over to the Elasticsearch worker, to save them into an index
of the users choice (note that mapping problems might happen when pushing into an already existing index)

*For this example, an install of the texta-mlp package and a running instance of our Tika build is necessary.*

```python
from texta_mlp.mlp import MLP

from texta_parsers.email_parser import EmailParser
from texta_parsers.tools.entity_linker_wrapper import EntityLinkerWrapper
from texta_parsers.tools.elastic import ESImporter
from texta_parsers.tools.mlp_processor import MLPProcessor

index_name = "personage_info"

mlp = MLP(language_codes=["et", "en", "ru"])
concat_wrapper = EntityLinkerWrapper()
mlp_wrapper = MLPProcessor(mlp)
elastic_importer = ESImporter("http://localhost:9200", index_prefix="rus")
email_parser = EmailParser()

generator = email_parser.parse("tests/data/Корзина.mbox")
generator = mlp_wrapper.apply_mlp(generator)

# Generator takes input in the form of a tuple containing the mlp output dictionary and a list (for attachments).
generator = concat_wrapper.concat_from_generator(generator)
pipeline_end = elastic_importer.push_linked_entities_into_elastic(generator, index_name)
```

All the entity-linked information should not be in an index named "personage_info"

