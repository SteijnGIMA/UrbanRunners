def rand_sourcegoal_generator(G, limit):
    """
    function to generate a number of source and goal nodes in a given graph.
    
    Parameters:
    G (networkx.MultiDiGraph) - input graph
    limit (int) - total number of source and goal pairs to generate

    returns:
    sources (list) - source nodes
    goals (list) - goal nodes
    """
    nodes = ox.graph_to_gdfs(G, nodes=True, edges=False)
    bbox = nodes.unary_union.envelope
    sources = []
    goals = []
    for n in range(limit):
        X1 = random.uniform(bbox.bounds[0], bbox.bounds[2])
        Y1 = random.uniform(bbox.bounds[1], bbox.bounds[3])
        X2 = random.uniform(bbox.bounds[0], bbox.bounds[2])
        Y2 = random.uniform(bbox.bounds[1], bbox.bounds[3])
        sources.append(ox.distance.nearest_nodes(G, X1, Y1))
        goals.append(ox.distance.nearest_nodes(G, X2, Y2))

    return sources, goals

def get_random_point_in_polygon(poly):
    """
    function to generate random point within a polygon.
    
    Parameters:
    poly (shapely.Polygon or shapely.MultiPolygon) - input polygon

    returns:
    p (shapely.Point) - random point that is within input polygon
    """
     minx, miny, maxx, maxy = poly.bounds
     while True:
         p = shapely.geometry.Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
         if poly.contains(p):
             return p
