import rdflib
import requests
import yaml
import os
import timeit
from collections import defaultdict
from SPARQLWrapper import SPARQLWrapper, JSON, BASIC, POST
from tqdm import tqdm
from acdh_arche_pyutils.utils import (
    camel_to_snake,
    create_query_sting,
    id_from_uri
)


class ArcheApiClient():
    """Main Class to interact with ARCHE-API """

    def __init__(
        self,
        arche_endpoint,
        out_dir='.'
    ):
        """ initializes the class
        :param arche_endpoint: The ARCHE endpoint e.g. `https://arche-dev.acdh-dev.oeaw.ac.at/api/`
        :type endpoint: str

        :param out_dir: a path to serialize data to, defaults to '.'
        :type out_dir: str

        :return: A ArcheApiClient instance
        :rtype: class:`achd_arch_pyutils.client.ArcheApiClient`
        """
        super().__init__()
        self.endpoint = arche_endpoint
        self.out_dir = out_dir
        self.describe_url = f"{arche_endpoint}describe"
        print(f'Fetching description for endpoint: {self.endpoint}')
        self.info = requests.get(self.describe_url)
        self.description = yaml.load(self.info.text, Loader=yaml.FullLoader)
        self.rest = self.description['rest']
        self.schema = self.description['schema']
        self.base_url = self.rest['urlBase']
        self.path_base = self.rest['pathBase']
        self.fetched_endpoint = f"{self.base_url}{self.path_base}"
        for key, value in self.schema.items():
            if isinstance(value, str):
                setattr(self, camel_to_snake(key), value)
        for key, value in self.schema['classes'].items():
            if isinstance(value, str):
                setattr(self, camel_to_snake(key), value)
        self.serialization_map = {
            'nt': 'application/n-triples',
            'ttl': 'text/turtle',
            'xml': 'application/rdf%2Bxml'
        }

    def top_col_ids(self):
        """returns of list of tuples (hasIdentifier, hasTitle) of all TopCollection"""
        items = defaultdict(list)
        query_params = {
            "property[0]": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
            "value[0]": self.top_collection,
            "readMode": 'ids'
        }
        query_string = create_query_sting(query_params)
        r = requests.get(f"{self.fetched_endpoint}search?{query_string}")
        g = rdflib.Graph().parse(data=r.text, format='ttl')
        for x in g.subject_objects(predicate=rdflib.URIRef(self.label)):
            items[x[0]].append(x[1])
        list_items = []
        for key, value in items.items():
            list_items.append((f"{key}", value))
        return list_items

    def get_resource(self, res_uri, format='nt'):
        """ fetches the given resource and its ancestors/parents

        :param res_uri: an ARCHE URI
        :type res_uri: str

        :return: A `rdflib.Graph` object
        :rtype: rdflib.Graph
        """
        query_params = {
            "readMode": "relatives",
            "parentProperty": self.parent,
            "format": self.serialization_map[format]
        }
        query_string = create_query_sting(query_params)
        url = f"{res_uri}/metadata?{query_string}"
        print(f"fetching and parsing data for URI: {res_uri}, calling endpoint \n {url}")
        start = timeit.default_timer()
        g = rdflib.Graph().parse(location=url, format=format)
        stop = timeit.default_timer()
        print(f"fetching and parsing done in {stop - start}")
        return g

    def write_resource_to_file(self, res_uri, format='nt'):
        """
        writes a resource (and its parents/children) to file on disk

        :param res_uri: An ARCHE-URI
        :type res_uri: str
        :param format: The serialisation format, defaults to 'ttl' -> turtle\
            use 'xml' for RDF/XML
        :type format: str

        :return: The location of the file
        :rtype: str
        """
        file_name = f"{id_from_uri(res_uri)}.{format}"
        save_path = os.path.join(self.out_dir, file_name)
        if format == 'ttl':
            format = 'turtle'
        else:
            format = 'xml'
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        g = self.get_resource(res_uri)
        g.serialize(save_path, format=format, encoding='utf8')
        return save_path


class ArcheToTripleStore(ArcheApiClient):
    """ A class to post ARCHE data to a Triplestore """
    def __init__(
        self,
        triple_store,
        user=None,
        pw=None,
        headers={
            'Content-Type': 'text/turtle;charset=utf-8'
        },
        **kwargs
    ):
        super().__init__(**kwargs)
        self.triple_store = triple_store
        self.user = user
        self.pw = pw
        self.headers = headers
        self.queries = {
            'count_triples': "SELECT (count(*) as ?cnt) WHERE {?s ?p ?o.}",
            'delete_all': "DELETE { ?s ?p ?o } WHERE { ?s ?p ?o }"
        }

    def count_triples(self):
        """ counts all existing triples in the triple store

        :return: The triple count
        :rtype: int
        """
        sparql_query = self.queries['count_triples']
        sparql_serv = SPARQLWrapper(self.triple_store)
        sparql_serv.setReturnFormat(JSON)
        sparql_serv.setQuery(sparql_query)
        result = sparql_serv.query().convert()
        triple_count = result['results']['bindings'][0]['cnt']['value']
        try:
            return int(triple_count)
        except ValueError:
            return triple_count

    def delete_triples(self):
        """ deletes everything """
        sparql_query = self.queries['delete_all']
        sparql_serv = SPARQLWrapper(self.triple_store)
        sparql_serv.setHTTPAuth(BASIC)
        sparql_serv.setMethod(POST)
        sparql_serv.setCredentials(self.user, self.pw)
        sparql_serv.setReturnFormat(JSON)
        sparql_serv.setQuery(sparql_query)
        result = sparql_serv.query().convert()
        return result

    def post_resource(self, res_id):
        """ posts the given resource to the triple store

        :param res_uri: An ARCHE-URI
        :type res_uri: str

        :return: The HTTP status code of the response and its body
        :rtype: list
        """
        res = self.get_resource(res_id)
        try:
            r = requests.post(
                self.triple_store,
                headers=self.headers,
                auth=(self.user, self.pw),
                data=res.serialize(format='ttl')
            )
        except requests.ConnectionError as e:
            return [500, f"{e}"]
        return [r.status_code, r.text]

    def post_all_resources(self):
        """ posts all TopCols to Triple Store

        :return: A list of status codes and response texts and top-col-id
        :rtype: list

        """
        top_ids = [x[0] for x in self.top_col_ids()]
        for x in tqdm(top_ids, total=len(top_ids)):
            response = self.post_resource(x)
            print(f"posting data for URI: {x};\
                \n import response: \n {response}")
        return "done"
