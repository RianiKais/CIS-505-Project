# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 13:23:48 2020

@author: DAMSL
"""
import numpy as np
import math
import time
import anytree
from anytree.exporter import DotExporter
inp = 'G3'

diagnostics = 0
progress = 1

startNode = 0
endNode = 8

result = np.loadtxt(open(inp, "rb"), dtype=(str), delimiter=" ", skiprows=1)
nodes = []
distances = {}

class Node:
    def __init__(self,id, value = None):
        self.value = value
        self.id = id
    def __str__(self):
        return "(" + str(self.id) + ")"

class Edge:
    def __init__(self, start, dist, end):
        self.start = start
        self.dist = dist
        self.end = end

class Graph:
    def __init__(self, edges={}, nodes = {}):
        # { 0: [Edge]}
        self.edges = edges
        # { 0: Node}
        self.nodes = nodes
    def addNode(self, value):
        # self.nodes[len(self.nodes)] = Node(id = len(self.nodes),value = value)
        self.nodes[value] = Node(id = value,value = value)
    def addEdge(self, startId, dist, endId):
        if startId in self.edges:
            self.edges[startId].append(Edge(startId, dist, endId))
            
        else:
            self.edges[startId] = [Edge(startId, dist, endId)]  

        if endId in self.edges:
            self.edges[endId].append(Edge(endId, dist, startId))
        else:
            self.edges[endId] = [Edge(endId, dist, startId)]  

    # def treeinator(value):wher is G3?
    #     return anytree.Node(value)

    def numericShortestPath(self, startId, endId):
        # based on Geeks for Geeks
        sptSet = set([])
        # sptSet = { nodeId}
        # 1) Create a set sptSet (shortest path tree set) that keeps track of vertices included in shortest path
        #  tree, i.e., whose minimum distance from source is calculated and finalized. Initially, this set is empty.
        distances = {}
        # {nodeId: distance}
        # 2) Assign a distance value to all vertices in the input graph. Initialize all distance values as INFINITE.
        #  Assign distance value as 0 for the source vertex so that it is picked first.
        for k in self.nodes.keys():
            if(k == startId):
                distances[k] = 0
            else:
                distances[k] = math.inf 
 
        # While sptSet doesn’t include all vertices
        while len(list(sptSet)) != len(self.nodes): 
 
            temp = {}
            for k, dist in distances.items():
                if(k not in sptSet):
                    temp[k] = dist 
            # Pick a vertex u which is not there in sptSet and has minimum distance value.
            u = min(temp, key=distances.get)
            #   Include u to sptSet.
            sptSet = sptSet.union({u}) 
            # Update distance value of all adjacent vertices of u. To update the distance values, iterate through all adjacent vertices. 
            # For every adjacent vertex v, if sum of distance value of u (from source) and weight of edge u-v, is less than the distance value of v, 
            # then update the distance value of v.
            for edge in self.edges[u]:
                if(distances[u]+edge.dist  <distances[edge.end]):
                    distances[edge.end] = distances[u]+edge.dist
        if diagnostics:
            print(distances)
        return distances[endId]

    def shortestPath(self, startId, endId):
        # based on Geeks for Geeks
        # shPath = Graph.numericShortestPath(startId, endId)
        # temp_inf = []
        sptSet = set([])
        # sptSet = { nodeId}
        # 1) Create a set sptSet (shortest path tree set) that keeps track of vertices included in shortest path
        #  tree, i.e., whose minimum distance from source is calculated and finalized. Initially, this set is empty.
        distances = {}
        # {nodeId: distance}
        # 2) Assign a distance value to all vertices in the input graph. Initialize all distance values as INFINITE.
        #  Assign distance value as 0 for the source vertex so that it is picked first.
        for k in self.nodes.keys():
            if(k == startId):
                distances[k] = 0
                rootNode = anytree.Node(str(k))
            else:
                distances[k] = math.inf 
            
        r = anytree.Resolver('name')
        # While sptSet doesn’t include all vertices
        while len(list(sptSet)) != len(self.nodes): 
            # if d:
            #     p = anytree.find_by_attr(rootNode, str(u))
            #     anytree.Node(str(nod), parent=p)
            temp = {}
            for k, dist in distances.items():
                if(k not in sptSet):
                    temp[k] = dist 
            if diagnostics:
                print('temp: ',temp)
                
                print('distances: ',distances)
            # Pick a vertex u which is not there in sptSet and has minimum distance value.
            u = min(temp, key=distances.get)
            # for nod in temp_inf:
            #     if temp[nod] != math.inf:
            #         p = anytree.find_by_attr(rootNode, str(u))
            #         anytree.Node(str(nod), parent=rootNode)
            # temp_inf = []
            # for nod, dst in temp.items():
            #     if dst == math.inf:
            #         temp_inf.append(nod)
            #   Include u to sptSet.
            sptSet = sptSet.union({u}) 
            if diagnostics:
                print('sptSet: ',sptSet, '  u: ', u)
            # Update distance value of all adjacent vertices of u. To update the distance values, iterate through all adjacent vertices. 
            # For every adjacent vertex v, if sum of distance value of u (from source) and weight of edge u-v, is less than the distance value of v, 
            # then update the distance value of v.
            
            for edge in self.edges[u]:
                if progress:
                    print('edge.start: ',edge.start, '. edge.end: ',edge.end, '. edge.dist: ',edge.dist)
                # if edge.start != endId:
                #         p = anytree.find_by_attr(rootNode, str(edge.start))
                #         par = r.get(p, '..')
                #         if par != None:
                #             par = str(par)[str(par).rfind('/')+1:str(par).rfind("'")]
                #             print('par: ',par)
                #         print('Starting node for ',edge.start,': ',p, 'with its parent: ', r.get(p, '..'))
                #         if str(edge.end) != par:
                #             print('distance to add: ',distances[u])
                #             print('distances[edge.end]: ',distances[edge.end])
                #             anytree.Node(str(edge.end), parent=p, distn = int(distances[u]))
                        
                
                if(distances[u]+edge.dist  <distances[edge.end]):
                    distances[edge.end] = distances[u]+edge.dist
                    if edge.start != endId:
                        if diagnostics:
                            print(anytree.RenderTree(rootNode))
                        pAll = anytree.findall_by_attr(rootNode, str(edge.start))
                        if diagnostics:
                            print('pAll length: ', len(pAll),' containing: ', pAll)
                        while len(pAll) > 1:
                            nodeDist = [0,pAll[0]]
                            for node in pAll:
                                curNodeDist = int(str(node)[str(node).rfind('=')+1:-1])
                                if curNodeDist > nodeDist[0]:
                                    nodeDist[0] = curNodeDist
                                    nodeDist[1] = node
                            nodeDist[1].parent = None
                            pAll = anytree.findall_by_attr(rootNode, str(edge.start))
                            if diagnostics:
                                print('new pAll length: ', len(pAll),' containing: ', pAll)
                        else:
                            p = anytree.find_by_attr(rootNode, str(edge.start))
                            if diagnostics:
                                print('Starting node for ',edge.start,': ',p, 'with its parent: ', r.get(p, '..'))
                                print('p',p)
                            par = r.get(p, '..')
                            if par != None:
                                par = str(par)[str(par).rfind('/')+1:str(par).rfind("'")]
                                if diagnostics:
                                    print('par: ',par)
                                    print('Starting node for ',edge.start,': ',p, 'with its parent: ', r.get(p, '..'))
                            if str(edge.end) != par:
                                if diagnostics:
                                    print('distance to add: ',distances[u])
                                    print('distances[edge.end]: ',distances[edge.end])
                                anytree.Node(str(edge.end), parent=p, distn = int(distances[u]+edge.dist))
                else:
                    if edge.start != endId:
                        if diagnostics:
                            print(anytree.RenderTree(rootNode))
                        pAll = anytree.findall_by_attr(rootNode, str(edge.start))
                        if diagnostics:
                            print('pAll length: ', len(pAll),' containing: ', pAll)
                        while len(pAll) > 1:
                            nodeDist = [0,pAll[0]]
                            for node in pAll:
                                curNodeDist = int(str(node)[str(node).rfind('=')+1:-1])
                                if curNodeDist > nodeDist[0]:
                                    nodeDist[0] = curNodeDist
                                    nodeDist[1] = node
                            nodeDist[1].parent = None
                            pAll = anytree.findall_by_attr(rootNode, str(edge.start))
                            if diagnostics:
                                print('new pAll length: ', len(pAll),' containing: ', pAll)
                        else:
                            p = anytree.find_by_attr(rootNode, str(edge.start))
                            if diagnostics:
                                print('Starting node for ',edge.start,': ',p, 'with its parent: ', r.get(p, '..'))
                                print('p',p)
                            par = r.get(p, '..')
                            if par != None:
                                par = str(par)[str(par).rfind('/')+1:str(par).rfind("'")]
                                if diagnostics:
                                    print('par: ',par)
                                    print('Starting node for ',edge.start,': ',p, 'with its parent: ', r.get(p, '..'))
                            if str(edge.end) != par:
                                if diagnostics:
                                    print('distance to add: ',distances[u])
                                    print('distances[edge.end]: ',distances[edge.end])
                                anytree.Node(str(edge.end), parent=p, distn = int(distances[u]+edge.dist))
                    
        print('final distances: ',distances)
        
        print('\nVisual trees:')
        print('Node ID tree:')
        for pre, fill, node in anytree.RenderTree(rootNode):
            print("%s%s" % (pre, node.name))
        print('Distances tree:')
        print(anytree.RenderTree(rootNode).by_attr('distn'))
        print('Combined Node ID and Distances tree:')
        print(anytree.RenderTree(rootNode))
        print('\n\nShortest path sub-path distances:')
        pAll = anytree.findall_by_attr(rootNode, str(endId))
        if diagnostics:
            print('pAll length: ', len(pAll),' containing: ', pAll)
        while len(pAll) > 1:
            nodeDist = [0,pAll[0]]
            for node in pAll:
                curNodeDist = int(str(node)[str(node).rfind('=')+1:-1])
                if curNodeDist > nodeDist[0]:
                    nodeDist[0] = curNodeDist
                    nodeDist[1] = node
            nodeDist[1].parent = None
            pAll = anytree.findall_by_attr(rootNode, str(endId))
        finalNode = r.get(anytree.find_by_attr(rootNode, str(endId)),"")
        if diagnostics:
            print(finalNode)
        w = anytree.Walker()
        print('walking: ',w.walk(rootNode, finalNode))
        DotExporter(rootNode).to_dotfile("rootNode.dot")
        print('\n\nimage exported to rootNode.dot. Go to http://www.webgraphviz.com/ to generate visual from .dot files')
        return distances[endId]



        
         


        pass
    def __str__(self):
        print("nodes:\n", " ".join([str( self.nodes[n]) for n in self.nodes]))
        for key in self.nodes:
            node = self.nodes[key]
            print(node.id)
            if(node.id in self.edges):
                for edge in self.edges[node.id]:
                    print("  --"+ str(edge.dist) +"-->" , str(self.nodes[edge.end]))
        return ""
        # currNode = 
graph = Graph()
source =  result[:,0]
dest =  result[:,1]
weight = result[:,2]
nods = np.unique(np.concatenate((dest, source), axis=0))
for i in range(len(nods)):
    graph.addNode(int(nods[i]))
    
    
for j in range(len(source)):    
    graph.addEdge(int(source[j]),int(weight[j]),int(dest[j]))
#for source, dest, weight in result:
    #graph.addNode(int(source))    
    #graph.addNode(int(dest))
    #print(result)
    #
    #graph.addEdge(int(dest),int(weight),int(source))
if diagnostics:
    print('source: ',source)
    print('result: ',nods)
    print('graph: ',graph)
    print(graph)
start_time = time.time()
print('shortest path:',graph.numericShortestPath(startNode,endNode))
print("Execution time: --- %s seconds ---" % (time.time() - start_time))
print('Will begin to visualize tree and subpaths in 5 seconds')
time.sleep(5)
print('shortest path:',graph.shortestPath(startNode,endNode))
