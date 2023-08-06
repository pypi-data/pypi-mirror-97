=====
Usage
=====

Write RDF-Graph of an ARCHE-URI to file::

    from acdh_arche_pyutils.client import ArcheApiClient

    endpoint = "https://arche-dev.acdh-dev.oeaw.ac.at/api/"
    client = ArcheApiClient(endpoint)
    top_cols = client.write_resource_to_file("https://arche-dev.acdh-dev.oeaw.ac.at/api/123")
    print(top_cols)
    
    # returns the name of the saved file, e.g. `123.ttl`


Fetch all TopCollection URIs and Labels::

    from acdh_arche_pyutils.client import ArcheApiClient

    endpoint = "https://arche-dev.acdh-dev.oeaw.ac.at/api/"
    client = ArcheApiClient(endpoint)
    top_cols = client.top_col_ids()

    # returns something like:
    [
        (
            'https://arche-dev.acdh-dev.oeaw.ac.at/api/18243',
            'HistoGIS'
        ),
        (
            'https://arche-dev.acdh-dev.oeaw.ac.at/api/18293',
            'Downed Allied Air Crew Database Austria'
        ),
        (
            'https://arche-dev.acdh-dev.oeaw.ac.at/api/18270',
            'Die Korrespondenz von Leo von Thun-Hohenstein'
        )
    ]

Retrieve the API-Configuration::

    from acdh_arche_pyutils.client import ArcheApiClient

    endpoint = "https://arche-dev.acdh-dev.oeaw.ac.at/api/"
    client = ArcheApiClient(endpoint)
    client.description
    # returns something like:
    {
        'rest':
            {
                'headers': 
                    {
                        'metadataReadMode': 'X-METADATA-READ-MODE',
                        'metadataParentProperty': 'X-PARENT-PROPERTY',
                        'metadataWriteMode': 'X-METADATA-WRITE-MODE',
                        'transactionId': 'X-TRANSACTION-ID'
                    },
                'urlBase': 'https://arche-dev.acdh-dev.oeaw.ac.at',
                'pathBase': '/api/'
            },
        'schema':
            {
                'id': 'https://vocabs.acdh.oeaw.ac.at/schema#hasIdentifier',
                'parent': 'https://vocabs.acdh.oeaw.ac.at/schema#isPartOf',
                'label': 'https://vocabs.acdh.oeaw.ac.at/schema#hasTitle',
                ...
            }
        }
    }