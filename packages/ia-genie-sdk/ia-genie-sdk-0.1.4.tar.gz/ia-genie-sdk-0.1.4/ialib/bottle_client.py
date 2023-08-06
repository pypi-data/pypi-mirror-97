"""Implements the "Bottle" interface."""
import uuid
from typing import Dict, List, Any
import io
import json

import requests

from ialib.genie_metalanguage import *
from ialib.genome_info import Genome


class QueryError(Exception):
    """Raised if any query to any node returns an error."""
    pass


class ConnectionError(Exception):
    """Raised if any query to any node returns an error."""
    pass

def remove_unique_id(response: dict) -> dict:
    """Return *response* with the key 'unique_id' removed regardless of nesting."""
    if isinstance(response, dict):
        if 'unique_id' in response:
            del (response['unique_id'])
        for value in response.values():
            if isinstance(value, dict):
                 remove_unique_id(value)
    return response

class BottleClient:
    """Interface for interacting with bottles."""
    def __init__(self, bottle_info):
        """
        Provide bottle information in a dictionary.

        ex:
        from ialib.BottleClient import BottleClient

        bottle_info = {'api_key': 'ABCD-1234',
                    'name': 'genie-bottle',
                    'domain': 'intelligent-artifacts.com',
                    'secure': False}

        bottle = BottleClient(bottle_info)
        bottle.connect()

        bottle.setIngressNodes(['P1'])
        bottle.setQueryNodes(['P1'])

        """
        self.genome = None
        self.bottle_info = bottle_info
        self.name = bottle_info['name']
        self.domain = bottle_info['domain']
        self.api_key = bottle_info['api_key']
        self.ingress_nodes = []
        self.query_nodes = []
        self.headers = {'X-API-KEY': self.api_key}
        self.all_nodes = []
        self.failures = []
        self.system_failures = []
        self._connected = False
        self.genome = None
        self.genie = None
        self.local = False
        self.send_unique_ids = True
        self.summarize_for_single_node = False
        if 'secure' not in self.bottle_info or self.bottle_info['secure']:
            self.secure = True
        else:
            self.secure = False
        self.url = 'https://{name}.{domain}/'.format(**self.bottle_info)
        if 'local' in self.bottle_info and self.bottle_info['local']:
            self.url = 'http://localhost/'
            self.local = True

    def __repr__(self) -> str:
        return '<{name}.{domain}| secure: %r, connected: %s, genie: %s, \
                  ingress_nodes: %i, query_nodes: %i, failures: %i>'.format(
                      **self.bottle_info) % (
                          self.secure, self._connected, self.genie, len(self.ingress_nodes), len(self.query_nodes), len(self.failures))

    def receive_unique_ids(self, should_set: bool = True) -> bool:
        self.send_unique_ids = should_set
        return self.send_unique_ids

    def connect(self) -> Dict:
        """Grabs the bottle's genie's genome for node definitions."""
        response_data = requests.get(self.url + 'connect', verify=self.secure, headers=self.headers).json()
        if 'status' not in response_data or response_data['status'] != 'okay':
            self._connected = False
            raise ConnectionError("Connection failed!", response_data)

        self.genome = Genome(response_data['genome'])
        self.genie = response_data['genome']['agent']
        self.all_nodes = [{"name": i['name'], "id": i['id']} for i in self.genome.primitives.values()]
        if response_data['connection'] == 'okay':
            self._connected = True
        else:
            self._connected = False

        return {'connection': response_data['connection'], 'genie': response_data['genie']}

    def set_ingress_nodes(self, nodes: List = None) -> List:
        """Use list of primitive names to define where data will be sent."""
        if nodes is None:
            nodes = []
        self.ingress_nodes = [{'id': self.genome.primitive_map[node], 'name': node} for node in nodes]
        return self.ingress_nodes

    def set_query_nodes(self, nodes: List = None) -> List:
        """Use list of primitive names to define which nodes should return answers."""
        if nodes is None:
            nodes = []
        self.query_nodes = [{'id': self.genome.primitive_map[node], 'name': node} for node in nodes]
        return self.query_nodes



    def _query(self, query_method: Any, path: str, data: Dict = None, nodes: List = None, unique_id: str = None) -> List:
        """Internal helper function to make an RPC call with the given *query* and *data*."""
        if not self._connected:
            raise ConnectionError('Not connected to a bottle. You must call `connect()` on a BottleClient instance before making queries')
        result = []
        if unique_id is not None:
            if data:
                    data['unique_id'] = unique_id
            else:
                data = {'unique_id': unique_id}

        if isinstance(nodes[0], str):
            nodes = [{'name': name, 'id': self.genome.primitive_map[name]} for name in nodes]
        for node in nodes:
            full_path = f'{self.url}{node["id"]}/{path}'
            try:
                if data is not None:
                    response = query_method(full_path, verify=self.secure, headers=self.headers,
                                            json={'data': data})
                else:
                    response = query_method(full_path, verify=self.secure, headers=self.headers)
                response.raise_for_status()
                response = response.json()
                if response['status'] != 'okay':
                    self.failures.append({node['name']: {'message': response['messsage']}})
                if not self.send_unique_ids:
                    response = remove_unique_id(response['message'])
                else:
                    response = response['message']
                if self.summarize_for_single_node and len(nodes) == 1:
                    result = response
                else:
                    result.append({node['name']: response})
            except Exception as exception:
                self.failures.append({node['name']: {'class': exception.__class__.__name__, 'message': str(exception)}})
                raise QueryError("Query Failure:", {'class': exception.__class__.__name__, 'message': str(exception)}) from exception
        if unique_id is not None:
            return result, unique_id
        return result

    def set_summarize_for_single_node(self, value: bool):
        self.summarize_for_single_node = value

    def observe(self, data: Dict = None, nodes: List = None) -> List:
        """Exclusively uses the 'observe' call.  All commands must be provided via Genie Metalanguage data."""
        if nodes is None:
            nodes = self.ingress_nodes
        return self._query(requests.post, 'observe', data=data, nodes=nodes)

    def observe_event(self, data: Dict = None, unique_id: str = None) -> List:
        """Exclusively uses the 'observe' call.  All commands must be provided via Genie Metalanguage data."""
        results = []
        if unique_id is None:
            unique_id = str(uuid.uuid4())
        for node, node_data in data.items():
            result, uid = self._query(requests.post, 'observe', node_data, nodes=[node], unique_id=unique_id)
            results.append(result)
        if len(results) == 1:
            results = results[0]
        return results, uid

    def observe_classification(self, data=None, nodes: List = None):
        """
        Best practice is to send a classification to all [ingress and] query nodes as a singular symbol in the last event.
        This function does that for us.
        """
        if not self._connected:
            raise ConnectionError('Not connected to a bottle. You must call `connect()` on a BottleClient instance before making queries')
        if nodes is None:
            nodes = self.query_nodes
        return self._query("observe", data, nodes=nodes)

    def show_status(self, nodes: List = None) -> List:
        """Return the current status of the bottle."""
        if nodes is None:
            nodes = self.all_nodes
        return self._query(requests.get, '/status', nodes=nodes)

    def learn(self, nodes: List = None) -> List:
        """Return the learn results."""
        if nodes is None:
            nodes = self.ingress_nodes
        return self._query(requests.post, 'learn', nodes=nodes)

    def get_wm(self, nodes: List = None) -> List:
        """Return information about Working Memory."""
        if nodes is None:
            nodes = self.all_nodes
        return self._query(requests.get, 'working-memory', nodes=nodes)

    def get_predictions(self, unique_id: str = None, nodes: List = None) -> List:
        """Return prediction result data."""
        if nodes is None:
            nodes = self.query_nodes
        return self._query(requests.post, 'predictions', nodes=nodes, unique_id=unique_id)

    def get_hive_prediction_utility(self) -> dict:
        """Return prediction result data."""
        return requests.get(f'{self.url}predictions/utility', headers=self.headers).json()

    def clear_wm(self, nodes: List = None) -> List:
        """Clear the Working Memory of the Genie."""
        if nodes is None:
            nodes = self.ingress_nodes
        return self._query(requests.post, 'working-memory/clear', nodes=nodes)

    def clear_all_memory(self, nodes: List = None) -> List:
        """Clear both the Working Memory and persisted memory."""
        if nodes is None:
            nodes = self.ingress_nodes
        return self._query(requests.post, 'clear-all-memory', nodes=nodes)

    def get_percept_data(self, nodes: List = None) -> List:
        """Return percept data."""
        if nodes is None:
            nodes = self.query_nodes
        return self._query(requests.get, 'percept-data', nodes=nodes)

    def get_cognition_data(self, nodes: List = None) -> List:
        """Return cognition data."""
        if nodes is None:
            nodes = self.query_nodes
        return self._query(requests.get, 'cognition-data', nodes=nodes)

    def get_cogitated(self, nodes: List = None) -> List:
        """Return cogitated data."""
        if nodes is None:
            nodes = self.query_nodes
        return self._query(requests.get, 'cogitated', nodes=nodes)

    def get_decision_table(self, nodes: List = None) -> List:
        """Return a decision table."""
        if nodes is None:
            nodes = self.query_nodes
        return self._query(requests.get, 'decision-table', nodes=nodes)

    def get_action_data(self, nodes: List = None) -> List:
        """Return action data."""
        if nodes is None:
            nodes = self.query_nodes
        return self._query(requests.get, 'action-data', nodes=nodes)

    def change_genes(self, gene_data: Dict) -> List:
        """
        Use primitive names.
        This will do live updates to an existing agent, rather than stopping an agent and starting a new one as per 'injectGenome'.
        gene_data of form:

            {node-name: {gene: value}}

        where node-id is the ID of a primitive or manipulative.

        Only works on primitive nodes at this time.
        """
        if not self._connected:
            raise ConnectionError('Not connected to a bottle. You must call `connect()` on a BottleClient instance before making queries')
        self.genome.change_genes(gene_data)
        result = []
        for node, updates in gene_data.items():  ## only primitive nodes at this time.
            for gene, value in updates.items():
                response = requests.post(f'{self.url}{self.genome.primitive_map[node]}/genome', verify=self.secure, headers=self.headers, json={'data': {gene: value}}).json()
                if 'error' in response or response["message"] != 'updated-genes':
                    self.system_failures.append({node: response})
                    print("System Failure:", {node: response})
                result.append({node: response["message"]})
        return result

    def inject_genome(self, genome: Dict) -> Dict:
        """Halt all primitives in the current bottle and start those described in *genome*.

        *genome* must be either a JSON-serializable object or a file-like object.
        """
        if not self._connected:
            raise ConnectionError('Not connected to a bottle. You must call `connect()` on a BottleClient instance before making queries')
        if isinstance(genome, io.TextIOBase):
            genome = json.load(genome)

        self.genome.change_genes(genome)
        response = requests.post(f'{self.url}genome', verify=self.secure, headers=self.headers, json={'genome': genome})

        if response.status_code != 200:
            self.system_failures.append({'bottle-api': response.json()})
            print("System Failure:", {'bottle-api': response.json()})

        return response.json()

    def get_cost_benefit(self, nodes: List = None) -> List:
        """Return cost benefit"""
        if nodes is None:
            nodes = self.query_nodes
        return self._query('getCostBenefit', nodes=nodes)

    def get_gene(self, gene: Dict, nodes: List = None) -> List[Dict[str, Dict[str, str]]]:
        """
        Use primitive names.
        This will return the gene-value of an existing agent, gene_data of form (similar to that
        of the change_genes method):

            {node-name: gene}

        where node-name is the ID of a primitive or manipulative.

        Only works on primitive nodes at this time.
        """
        if not self._connected:
            raise ConnectionError('Not connected to a bottle. You must call `connect()` on a BottleClient instance before making queries')
        result = []
        for node_name, attribute in gene.items():
            try:
                response = requests.get(f'{self.url}{self.genome.primitive_map[node_name]}/gene/{attribute}', verify=self.secure,
                                        headers=self.headers).json()['message']
                result.append({node_name: {attribute : response}})

            except Exception as exception:
                self.failures.append({node_name: exception})
                raise Exception("Query Failure:", {node_name: exception})

        return result

    def get_model(self, data: Dict, nodes: List = None) -> List[Dict[str, Dict[str, str]]]:
        """
        Returns model.

        data : {primitive_name : name}

        Model name is unique, so it should not matter that we query all nodes, only
        one model will be found. How will the absense of a name in a primitive be
        conveyed?
        """
        if not self._connected:
            raise ConnectionError('Not connected to a bottle. You must call `connect()` on a BottleClient instance before making queries')
        result = []
        for node_name, model_name in data.items():
            try:
                response = requests.get(f'{self.url}{self.genome.primitive_map[node_name]}/model/{model_name}', headers=self.headers, verify=self.secure).json()['message']
                result.append({node_name: {model_name : response}})

            except Exception as exception:
                self.failures.append({node_name: exception})
                raise Exception("Query Failure:", {node_name: exception})

        return result

    def get_name(self, nodes: List = None) -> List[Dict[str, str]]:
        """
        """
        if nodes is None:
            nodes = self.all_nodes
        return self._query(requests.get, 'name', nodes=nodes)

    def get_time(self, nodes: List = None) -> List:
        """
        """
        if nodes is None:
            nodes = self.all_nodes
        return self._query(requests.get, 'time', nodes=nodes)

    def get_vector(self, data: Dict) -> List:
        """
        """
        if not self._connected:
            raise ConnectionError('Not connected to a bottle. You must call `connect()` on a BottleClient instance before making queries')
        result = []
        for node_name, vector_name in data.items():
            try:
                response = requests.post(self.url, verify=self.secure, json={"method": "getVector", "params": {"api_key": self.api_key, "primitive_id": self.genome.primitive_map[node_name], "data": vector_name},
                     "jsonrpc": "2.0", "id": 1}).json()['result']
                result.append({node_name: {vector_name: response}})

            except Exception as exception:
                self.failures.append({node_name: exception})
                raise Exception("Query Failure:", {node_name: exception})

        return result

    def increment_recall_threshold(self, data: Dict) -> List[Dict[str, Any]]:
        """
        TODO: update local genome
        TODO: Change param name 'data' -> 'increment'
        """
        if not self._connected:
            raise ConnectionError('Not connected to a bottle. You must call `connect()` on a BottleClient instance before making queries')
        result = []
        for node_name, val in data.items():
            try:
                response = requests.post(f'{self.url}{self.genome.primitive_map[node_name]}/gene/increment-recall-threshold', verify=self.secure, headers=self.headers, json={'data': val}).json()['message']
                result.append({node_name: {"recall_threshold": response}})

            except Exception as exception:
                self.failures.append({node_name: exception})
                raise Exception("Query Failure:", {node_name: exception})

        return result

    def show_predictions_knowledge_details(self) -> List:
        """
        """
        return []

    def start_acting(self, nodes: List = None) -> List[Dict[str, Any]]:
        """
        Allow query nodes to start acting.

        TODO: Should user be able to specify which nodes.
        """
        if nodes is None:
            nodes = self.query_nodes
        return self._query(requests.post, 'acting/start', nodes=nodes)

    def start_sleeping(self, nodes: List = None) -> List[Dict[str, Any]]:
        """
        Tells all nodes to start sleeping.

        TODO: Should user be able to specify which nodes.
        """
        if nodes is None:
            nodes = self.all_nodes
        return self._query(requests.post, 'sleeping/start', nodes=nodes)

    def stop_acting(self, nodes: List = None) -> List[Dict[str, Any]]:
        """
        Stop query nodes from acting.

        TODO: Should user be able to specify which nodes.
        """
        if nodes is None:
            nodes = self.query_nodes
        return self._query(requests.post, 'acting/stop', nodes=nodes)

    def stop_sleeping(self, nodes: List = None) -> List[Dict[str, Any]]:
        """
        Wakes up all sleeping nodes.

        TODO: Should user be able to specify which nodes.
        """
        if nodes is None:
            nodes = self.all_nodes
        return self._query(requests.post, 'sleeping/stop', nodes=nodes)

    def ping(self, nodes: List = None) -> List[Dict[str, Any]]:
        """Ping a node to ensure it's up."""
        if nodes is None:
            nodes = self.all_nodes

        if not self._connected:
            raise ConnectionError(
                'Not connected to a bottle. You must call `connect()` on a BottleClient instance before making queries')

        return requests.get(f'{self.url}ping', headers=self.headers).json()

    def define_mood(self, mood_data: Dict) -> List:
        """
        *mood_data* should be of the format:
            {node-name: {emotion: weight}}

        where node-name is the *name* of a primitive or manipulative.
        """
        if not self._connected:
            raise ConnectionError(
                'Not connected to a bottle. You must call `connect()` on a BottleClient instance before making queries')
        results = []
        for node, mood_list in mood_data.items():  ## only primitive nodes at this time.
            response = requests.post(f'{self.url}{self.genome.primitive_map[node]}/mood/define', verify=self.secure,
                                     headers=self.headers, json={'data': mood_list}).json()
            if 'error' in response or response["message"] != 'updated-genes':
                self.system_failures.append({node: response})
                print("System Failure:", {node: response})
                if len(mood_data) == 1 and self.summarize_for_single_node:
                    return response['message']
            results.append({node: response["message"]})
        return results


    def set_mood(self, mood_data: Dict) -> List:
        """
        *mood_data* should be of the format:
            {node-name: {mood: value}}

        where node-name is the *name* of a primitive or manipulative.
        """
        if not self._connected:
            raise ConnectionError(
                'Not connected to a bottle. You must call `connect()` on a BottleClient instance before making queries')
        results = []
        for node, mood_dict in mood_data.items():  ## only primitive nodes at this time.
            response = requests.post(f'{self.url}{self.genome.primitive_map[node]}/mood/set', verify=self.secure,
                                     headers=self.headers, json={'data': mood_dict}).json()
            if 'error' in response or response["message"] != 'updated-genes':
                self.system_failures.append({node: response})
            if len(mood_data) == 1 and self.summarize_for_single_node:
                return response['message']
            results.append({node: response["message"]})
        return results
