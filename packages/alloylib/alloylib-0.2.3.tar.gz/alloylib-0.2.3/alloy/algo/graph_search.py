# Copyright - Transporation, Bots, and Disability Lab - Carnegie Mellon University
# Released under MIT License

import heapq
import sys
is_py2 = sys.version[0] == '2'
if is_py2:
    import Queue as queue
else:
    import queue as queue

__all__ = [
    'dijkstra_search', 'breath_first_search', 'depth_first_search'
]


class SearchQueue(object):
    """Interface that provide different version of search
    """

    def push(self, obj, **kwargs):
        """Push object

        parameters
        ----------
        obj : Object
            What you want to add 
        kwargs : dict
            parameters
        """
        raise NotImplementedError()

    def pop(self):
        """Return the object in this queue based on implementation
        """
        raise NotImplementedError()

    def update(self, obj, **kwargs):
        pass

    def __len__(self):
        raise NotImplementedError("Please use one of the base class")

class PrioritySearchQueue(SearchQueue):

    def __init__(self):
        self._pheap = []

    def push(self, obj, **kwargs):
        if 'cost' not in kwargs:
            raise RuntimeError('PriorityQueue push must have cost')
        heapq.heappush(self._pheap, (kwargs['cost'], obj))

    def pop(self):
        cost, obj = heapq.heappop(self._pheap)
        return obj, {'cost': cost}

    def update(self, obj, **kwargs):
        for h in self._pheap:
            if h[1] == obj:
                self._pheap.remove(h)
                break
        heapq.heappush(self._pheap, (kwargs['cost'], obj))

    def __len__(self):
        return len(self._pheap)


class LIFOSearchQueue(SearchQueue): #Depth First Search
    def __init__(self):
        self._queue = []

    def push(self, obj, **kwargs):
        self._queue.append(obj)

    def pop(self):
        return self._queue.pop(), None

    def __len__(self):
        return len(self._queue)

class FIFOSearchQueue(SearchQueue):
    def __init__(self):
        self._queue = []

    def push(self, obj, **kwargs):
        self._queue.append(obj)

    def pop(self):
        return self._queue.pop(0), None

    def __len__(self):
        return len(self._queue)    


def _base_search(queue_type, start_id, end_id, child_func, edge_func=None):
    """
    Search for the shortest path between two points given the start id to the end id

    paramaters
    ----------
    edge_func : function(C,A,B)
        function that has calculates the score from A to B. C is the parent of A
    child_func : function(A)
        function that returns all the child of the given the id of the node, A.
    start_id : string
        starting node id
    end_id : string
        ending node id 

    return
    ------
    list
        A list of the IDs that starts from the start id to end id. If no path was found, an empty list is returned.
    """
    #initialize the support dicts
    parent_list = dict()
    cost_list = dict()
    #pheap = [] #priority heap
    found_flag = False

    parent_list[start_id] = start_id
    #initialize the starting cost 
    cost_list[start_id] = 0
    #push the start node onto the heap
    #internal_queue = PrioritySearchQueue()
    internal_queue = queue_type
    internal_queue.push(start_id, cost=0)
    #heapq.heappush(pheap, (0, start_id))
        
    #start looping through the priority queue
    while len(internal_queue) != 0:
        #pop the smaller item
        curr_id, curr_param = internal_queue.pop()
        #dist_to_id, curr_id = heapq.heappop(pheap)
        #quit if we reach target
        if curr_id == end_id:
            found_flag = True
            break
        #get the list of child ids given current id
        children = child_func(curr_id)
        #get the parent ID
        parent_id = parent_list[curr_id]
        #remove the parent from the child_func if already exist
        if parent_id in children:
            children.remove(parent_id)

        for child_id in children:
            #calculate the cost to move from the current id to the child id
            if edge_func:
                cost = edge_func(parent_id, curr_id, child_id)
            else:
                cost = 0
            #get real cost from the beginning
            cost += cost_list[curr_id]
            #we already visited the children before
            if child_id in cost_list:
                #update if the cost is less
                if cost < cost_list[child_id]:
                    #update existing data
                    parent_list[child_id] = curr_id
                    cost_list[child_id] = cost   
                    #update the queue            
                    internal_queue.update(child_id, cost=0) 
            else:
                #update data
                parent_list[child_id] = curr_id
                cost_list[child_id] = cost
                #push to queue
                internal_queue.push(child_id, cost=cost)

    if found_flag:
        curr_id = end_id
        travel_list = [curr_id]
        while curr_id != start_id:
            curr_id = parent_list[curr_id]
            travel_list.insert(0, curr_id)
        return travel_list
    else:
        return []


def dijkstra_search(start, goal, child_func, cost_func):
    """
    Search for the shortest path between start and goal. Search using the ID of each node
    and child function that returns all the children of given node.

    paramaters
    ----------
    edge_func : function(C,A,B)
        function that has calculates the score from A to B. C is the parent of A
    child_func : function(A)
        function that returns all the child of the given the id of the node, A.
    start_id : string
        starting node id
    end_id : string
        ending node id 

    return
    ------
    list
        A list of the IDs that starts from the start id to end id. If no path was found, an empty list is returned.
    """
    return _base_search(PrioritySearchQueue(), start, goal, child_func, edge_func=cost_func)

def breath_first_search(start, goal, child_func):
    """Search for the first path between the start and goal using breath-first search. 

    paramaters
    ----------
    start : string
        starting node id
    goal : string
        ending node id 
    child_func : function(A)
        function that returns all the child of the given the node, A.
    return
    ------
    list
        A list of the IDs that starts from the start id to end id. If no path was found, an empty list is returned.
    """
    return _base_search(FIFOSearchQueue(), start, goal, child_func)

def depth_first_search(start, goal, child_func):
    """Search for the first path between the start and goal using depth-first search. Search using the ID of each node
    and child function that returns all the children of given node.

    Note: The order of children node evaluated starts from the end of the node and not the front

    paramaters
    ----------
    start : string
        starting node id
    goal : string
        ending node id 
    child_func : function(A)
        function that returns all the child of the given the node, A.
    return
    ------
    list
        A list of the IDs that starts from the start id to end id. If no path was found, an empty list is returned.
    """
    return _base_search(LIFOSearchQueue(), start, goal, child_func)