import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
class Lattice():
    def index_cells(self, shapes, pos, N, M):
        """
        Combine a list of polygons with information about the positions of each
        polygon's vertices to produce a list of cells in the same format as the
        pyvoro package.
    
        Parameters
        ----------
        shapes : dict
            A dictionary containing the index of the polygon for each key, and a
            list of vertices in counterclockwise order for each value
        pos : dict
            A dictionary containing the index of each vertex for each key, and a
            numpy array of length 2 containing a [x,y] coordinate pair for each 
            value.
        N : int
            The height (measured in number of fundamental cells) of the lattice.
        M : int
            The width (measured in number of fundamental cells) of the lattice.
    
        Returns
        -------
        cells : list
            A list of dictionaries which contain information about each polygon in
            the NxM lattice, including neighboring cells (and which edge they
            share), the centroid of each cell, the positions of each vertex which
            makes up the cell, the volume of the cell, and how the vertices are
            joined by edges.
    
        """
        cells = []
        for shape in shapes:
            if len(shapes[shape]) == 3:
                cells.append(self.index_3_gon(shapes[shape], shape, N, M, pos))
            else:
                cells.append(self.index_12_gon(shapes[shape], shape, N, M, pos))
        return cells
    
    def index_3_gon(self, vertices, idx, N, M, pos):
        """
        Function which converts information about a 3-gon into a single cell in
        the same format used by the pyvoro package.
    
        Parameters
        ----------
        vertices : list
            A list of the vertices which make up the given 3-gon, provided in
            counterclockwise order.
        idx : int
            Value denoting the 3-gon's position in reference to every other 3-gon
            in the lattice.
        N : int
            The height (measured in number of fundamental cells) of the lattice.
        M : int
            The width (measured in number of fundamental cells) of the lattice.
        pos : dict
            A dictionary containing the index of each vertex for each key, and a
            numpy array of length 2 containing a [x,y] coordinate pair for each 
            value.
    
        Returns
        -------
        cell : dict
            A dictionary containing detailed information about the provided 3-gon
            in the same format as the pyvoro package. The information about each
            cell, or 3-gon, includes neighboring cells (and which edge they share),
            the centroid of each cell, teh positions of each vertex which makes up
            the cell, the volume of the cell, and how the vertices are joined by
            edges.
    
        """
        faces = [] # One value contained in the returned dictionary
        height = int((N/8)*3) # Height of each column, in number of polygons
        tip = vertices[0] # Vertex of 3-gon which does not lie on horizontal edge
        # Total number of n-gons found in the NxM lattice
        total = ((N/8)*(M/7)+((N/8)-1)*((M/7)-1))*3
    
        # If tip of triangle lies below flat edge
        if tip % 2 == 0:
            faces.append(
                {'adjacent_cell': idx+1,
                 'vertices': [vertices[1], vertices[2]]
                }
            )
            # Triangle has all three neighbors
            if 4*(N+1) < tip < (M*N)-(4*(N+1)) and tip % 8 != 0 and tip % 8 != 4:
                faces.extend([
                    {'adjacent_cell': idx-height+1,
                     'vertices': [vertices[0], vertices[2]]
                    },
                    {'adjacent_cell': idx+height-2,
                     'vertices': [vertices[0], vertices[1]]
                    }
                ])
            # Triangle does not have left neighbor
            elif tip < 4*(N+1):
                faces.append(
                    {'adjacent_cell': idx+height-2,
                     'vertices': [vertices[0], vertices[1]]
                    }
                )
            # Otherwise, triangle does not have right neighbor
            else:
                faces.append(
                    {'adjacent_cell': idx-height+1,
                     'vertices': [vertices[0], vertices[2]]
                    }
                )
        else: # Tip of triangle lies above flat edge
            faces.append(
                {'adjacent_cell': idx-1,
                 'vertices': [vertices[1], vertices[2]]
                }
            )
            # Triangle has all three neighbors
            if 4*(N+1) < tip < (M*N)-(4*(N+1)) and tip % 8 != 0 and tip % 8 != 4:
                faces.extend([
                    {'adjacent_cell': idx-height+2,
                     'vertices': [vertices[0], vertices[2]]
                    },
                    {'adjacent_cell': idx+height-1,
                     'vertices': [vertices[0], vertices[1]]
                    }
                ])
            # Triangle does not have left neighbor
            elif tip < 4*(N+1) and idx+height-1 < total:
                faces.append(
                    {'adjacent_cell': idx+height-1,
                     'vertices': [vertices[0], vertices[1]]
                    }
                )
            # Otherwise, triangle does not have right neighbor
            elif idx-height+2 != idx-1:
                faces.append(
                    {'adjacent_cell': idx-height+2,
                     'vertices': [vertices[0], vertices[2]]
                    }
                )
    
        # Create cell in format of pyvoro package
        cell = {
            'faces': faces,
            'original': np.array([
                (pos[vertices[0]][0]+pos[vertices[1]][0]+pos[vertices[2]][0])/3,
                (pos[vertices[0]][1]+pos[vertices[1]][1]+pos[vertices[2]][1])/3
            ]),
            'vertices': [pos[vertices[0]], pos[vertices[1]], pos[vertices[2]]],
            'volume': np.abs(
                    (pos[vertices[0]][0]*(pos[vertices[1]][1]-pos[vertices[2]][1]))+
                    (pos[vertices[1]][0]*(pos[vertices[2]][1]-pos[vertices[0]][1]))+
                    (pos[vertices[2]][0]*(pos[vertices[0]][1]-pos[vertices[1]][1]))
                )/2,
            'adjacency': [
                [vertices[0], vertices[1]],
                [vertices[0], vertices[2]],
                [vertices[1], vertices[2]]
            ]
        }
        # print(cell)
        return cell
        
    def index_12_gon(self, vertices, idx, N, M, pos):
        """
        Function which converts information about a 12-gon into a single cell in
        the same format used by the pyvoro package.
    
        Parameters
        ----------
        vertices : list
            A list of the vertices which make up the given 12-gon, provided in
            counterclockwise order.
        idx : int
            Value denoting the 12-gon's position in reference to every other 12-gon
            in the lattice.
        N : int
            The height (measured in number of fundamental cells) of the lattice.
        M : int
            The width (measured in number of fundamental cells) of the lattice.
        pos : dict
            A dictionary containing the index of each vertex for each key, and a
            numpy array of length 2 containing a [x,y] coordinate pair for each 
            value.
    
        Returns
        -------
        cell : dict
            A dictionary containing detailed information about the provided 12-gon
            in the same format as the pyvoro package. The information about each
            cell, or 12-gon, includes neighboring cells (and which edge they
            share), the centroid of each cell, teh positions of each vertex which
            makes up the cell, the volume of the cell, and how the vertices are
            joined by edges.
    
        """
        faces = [] # One value contained in the returned dictionary
        height = ((N/8)*3) # Height of each column, in number of polygons
        
        # Total number of n-gons found in the NxM lattice
        total = ((N/8)*(M/7)+((N/8)-1)*((M/7)-1))*3
    
        # Every dodecagon has a top and bottom neighbor
        faces.append([
            {'adjacent_cell': idx-1,
              'vertices': [vertices[8], vertices[9]]
            },
            {'adjacent_cell': idx+1,
              'vertices': [vertices[2], vertices[3]]
            }
        ])
        
        # If dodecagon's vertical left edge does not lie on edge of the lattice
        if idx > (height*2)-3:
            # Add neighbor on left edge
            faces.append(
                {'adjacent_cell': idx-(height*2)+3,
                 'vertices': [vertices[5], vertices[6]]
                }
            )
            # If the dodecagon doesn't lie on the bottom edge of the lattice
            if idx % ((height*2)-3) != 1 and idx-height > 0:
                # Add lower left 3-gon and 12-gon neighbors
                faces.extend([
                    {'adjacent_cell': idx-height+1,
                     'vertices': [vertices[6], vertices[7]]
                    },
                    {'adjacent_cell': idx-height,
                     'vertices': [vertices[7], vertices[8]]
                    }
                ])
            # If the dodecagon doesn't lie on the top edge of the lattice
            if idx % ((height*2)-3) == 4 and idx+height < total:
                # Add upper left 3-gon and 12-gon neighbors
                faces.extend([
                    {'adjacent_cell': idx-height+3,
                      'vertices': [vertices[3], vertices[4]]
                    },
                    {'adjacent_cell': idx-height+2,
                      'vertices': [vertices[4], vertices[5]]
                    }
                ])
        # If the dodecagon's vertical right edge does not lie on edge of lattice
        if idx < total-height:
            # Add neighbor on right edge
            faces.append(
                {'adjacent_cell': idx+(height*2)-3,
                  'vertices': [vertices[0], vertices[11]]
                }
            )
            # If the dodecagon doesn't lie on the bottom edge of the lattice
            if idx % ((height*2)-3) != 1 and idx+height < total:
                # Add lower right 3-gon and 12-gon neighbors
                faces.extend([
                    {'adjacent_cell': idx+height-3,
                      'vertices': [vertices[9], vertices[10]]
                    },
                    {'adjacent_cell': idx+height-2,
                      'vertices': [vertices[10], vertices[11]]
                    }
                ])
            # If the dodecagon doesn't lie on the top edge of the lattice
            if idx % ((height*2)-3) != 10 and idx-height > 0:
                # Add upper right 3-gon and 12-gon neighbors
                faces.extend([
                    {'adjacent_cell': idx+height-1,
                     'vertices': [vertices[0], vertices[1]]
                    },
                    {'adjacent_cell': idx+height,
                     'vertices': [vertices[1], vertices[2]]
                    }
                ])
        
        # Create cell in format of pyvoro package
        cell = {
            'faces': faces,
            'original': np.array([
                (pos[vertices[0]][0]+pos[vertices[5]][0])/2,
                (pos[vertices[2]][1]+pos[vertices[9]][1])/2
            ]),
            'vertices': [pos[vertices[0]],
                         pos[vertices[1]],
                         pos[vertices[2]],
                         pos[vertices[3]],
                         pos[vertices[4]],
                         pos[vertices[5]],
                         pos[vertices[6]],
                         pos[vertices[7]],
                         pos[vertices[8]],
                         pos[vertices[9]],
                         pos[vertices[10]],
                         pos[vertices[11]]
                         ],
            'volume': 
                3*(2+np.sqrt(3))*(pos[vertices[0]][1]-pos[vertices[11]][1])**2,
            'adjacency': [
                [vertices[0], vertices[1]],
                [vertices[1], vertices[2]],
                [vertices[2], vertices[3]],
                [vertices[3], vertices[4]],
                [vertices[4], vertices[5]],
                [vertices[5], vertices[6]],
                [vertices[6], vertices[7]],
                [vertices[7], vertices[8]],
                [vertices[8], vertices[9]],
                [vertices[9], vertices[10]],
                [vertices[10], vertices[11]],
                [vertices[11], vertices[0]]
            ]
        }
        return cell
    
    def adjust_pos(self, pos, N, M):
        """
        Modifies pos in place to scale every polyogn to fit within the unit grid.
    
        Parameters
        ----------
        pos : dict
            A dictionary containing the index of each vertex for each key, and a
            numpy array of length 2 containing a [x,y] coordinate pair for each 
            value.
        N : int
            The height (measured in number of fundamental cells) of the lattice.
        M : int
            The width (measured in number of fundamental cells) of the lattice.
    
        """
    
        for position in pos:
            pos[position][0] /= (N/8)
            pos[position][1] += ((4/7) + (2/8) + (8*(np.sqrt((1/49)+(1/64)))))/(6*(N/8))
            pos[position][1] /= (M/7)
        
    def lattice_cells(self, n, m):
        """
        Produce a NxM archimedian lattice of fundamental cells, where each 
        fundamental cell is comprised of one 4-gon and two 8-gons.
    
        Parameters
        ----------
        n : int
            The height (measured in number of fundamental cells) of the lattice.
        m : int
            The width (measured in number of fundamental cells) of the lattice.
    
        Returns
        -------
        cells: list
            A list of dictionaries which contain information about each polygon in
            the NxM lattice, including neighboring cells (and which edge they
            share), the centroid of each cell, the positions of each vertex which
            makes up the cell, the volume of the cell, and how the vertices are
            joined by edges.
    
        """
        G = nx.Graph()
        pos = {}
        triangles = []
        dodecagons = []
        shapes = {}
        
        edge_len = ((4/7) + (2/8) + (8*(np.sqrt((1/49)+(1/64)))))/12
        
        M = 7 * m
        N = 8 * n
        
        col = 1
        
        for i in range(0, N):        
            if i % 8 == 3:
                G.add_node(i)
                pos[i] = np.array([0, int(i/8)*((4*np.sqrt(edge_len**2-(edge_len/2)**2))+(3*edge_len))])
            elif i % 8 == 4:
                G.add_edge(i, i-1)
                pos[i] = np.array([0, pos[i-1][1]+edge_len])
                
            # else:
            #     G.add_node(i)
            #     pos[i] = np.array([0, ((i-3)/8)*((4*np.sqrt(edge_len**2-(edge_len/2)**2))+(3*edge_len))])
        
        while col < M: 
            # TODO: Shift lattice up to fit within lower bound of unit grid
            # TODO: Scale every polygon down to fit within unit grid
            pos[N*col] = np.array([(col-int(col/7))/M, 0])
            for row in range(0,N):
                
                offset = N*(int(col/7)+1) if int(col/7) < 2 else 2*N
                
                idx = (N * col) + row  
                
                # if idx-1 > -1 and idx % N != 0:
                #     G.add_edge(idx, idx-1)
                #     pos[idx] = np.array([(col+edge_len)/M, ((row-3)/8)*((4*np.sqrt(edge_len**2-(edge_len/2)**2))+(3*edge_len))])
                
                # Draw right edge of dodecagon
                if row % 8 == 4 and col % 7 == 6:
                    G.add_edge(idx, idx-1)
                    G.add_edge(idx, idx-N+1)
                    pos[idx] = np.array([
                        pos[idx-N+1][0]+(edge_len/2),
                        pos[idx-N+1][1]-np.sqrt(edge_len**2-(edge_len/2)**2)
                    ])
                    x_offset = 6 if int(col/7) < 1 else 7
                    dodecagons.append([
                        idx, 
                        idx-N+1, 
                        idx-(2*N)+2, 
                        idx-(4*N)+2, 
                        idx-(5*N)+1, 
                        idx-(x_offset*N),
                        idx-(x_offset*N)-1,
                        idx-(5*N)-2,
                        idx-(4*N)-3,
                        idx-(2*N)-3,
                        idx-N-2,
                        idx-1
                    ])
                # Draw top and bottom edges of dodecagon
                elif ((row % 8 == 1 and col % 7 == 4) or
                      (row % 8 == 6 and col % 7 == 4)
                ):
                    G.add_edge(idx, idx-(2*N))
                    pos[idx] = np.array([
                        pos[idx-(2*N)][0]+edge_len,
                        pos[idx-(2*N)][1]
                    ])
                # Draw edge under dodecagon's left edge
                elif row % 8 == 2 and col % 7 == 1:
                    # If dodecagon lies on left edge, only connect to left edge
                    if idx < 2*N:
                        G.add_edge(idx, idx-N+1)
                    pos[idx] = np.array([
                        pos[idx-offset+1][0]+(edge_len/2),
                        pos[idx-offset+1][1]-np.sqrt(edge_len**2-(edge_len/2)**2)
                    ])
                    # Otherwise, draw edge to previous dodecagon, making triangle
                    if idx-(N*3) > 0:
                        G.add_edge(idx, idx-(N*2)+1)
                        if row > 2:
                            G.add_edge(idx, idx-(N*3))
                            triangles.append([idx-(N*2)+1, idx-(N*3), idx])
                # Draw edge right of the top edge
                elif row % 8 == 5 and col % 7 == 5:
                    G.add_edge(idx, idx-N+1)
                    pos[idx] = np.array([
                        pos[idx-N+1][0]+np.sqrt(edge_len**2-(edge_len/2)**2), 
                        pos[idx-N+1][1]-(edge_len/2)
                    ])
                # Draw edge left of the bottom edge
                elif (row % 8 == 1 and col % 7 == 2):
                    G.add_edge(idx, idx-N+1)
                    pos[idx] = np.array([
                        pos[idx-N+1][0]+np.sqrt(edge_len**2-(edge_len/2)**2), 
                        pos[idx-N+1][1]-(edge_len/2)
                    ])
                # Draw edge on top of dodecagon's left edge
                elif row % 8 == 5 and col % 7 == 1:
                    # If dodecagon lies on left edge, only connect to left edge
                    if idx < 2*N:
                        G.add_edge(idx, idx-N-1)
                    pos[idx] = np.array([
                        pos[idx-offset-1][0]+(edge_len/2),
                        pos[idx-offset-1][1]+np.sqrt(edge_len**2-(edge_len/2)**2)
                    ])
                    # Otherwise, draw edge to previous dodecagon, making triangle
                    if idx-(N*3) > 0:
                        G.add_edge(idx, idx-(N*2)-1)
                        if row < N-3:
                            G.add_edge(idx, idx-(N*3))
                            triangles.append([idx-(N*2)-1, idx, idx-(N*3)])
                # Draw edge to the right of the bottom edge
                elif row % 8 == 2 and col % 7 == 5:
                    G.add_edge(idx, idx-N-1)
                    pos[idx] = np.array([
                        pos[idx-N-1][0]+np.sqrt(edge_len**2-(pos[idx-(4*N)][1]-pos[idx-N-1][1])**2), 
                        pos[idx-(4*N)][1]
                    ])
                # Draw edge to the left of the top edge
                elif (row % 8 == 6 and col % 7 == 2):
                    G.add_edge(idx, idx-N-1)
                    pos[idx] = np.array([
                        pos[idx-N-1][0]+np.sqrt(edge_len**2-(edge_len/2)**2), 
                        pos[idx-N-1][1]+(edge_len/2)
                    ])
                # Draw edge under the right edge
                elif (row % 8 == 3 and col % 7 == 6):
                    G.add_edge(idx, idx-N-1)
                    pos[idx] = np.array([
                        pos[idx-N-1][0]+(edge_len/2),
                        pos[idx-N-1][1]+np.sqrt(edge_len**2-(edge_len/2)**2)
                    ])
                # Draw top triangle
                elif row % 8 == 7 and col % 7 == 3:
                    G.add_edge(idx, idx-N-1)
                    G.add_edge(idx, idx+N-1)
                    # If dodecagon doesn't lie on top of lattice, connect to bottom
                    # triangle of above dodecagon
                    if row % N < N-1:
                        G.add_edge(idx, idx+1)
                    pos[idx] = np.array([
                        pos[idx-N-1][0]+(edge_len/2),
                        pos[idx-N-1][1]+np.sqrt(edge_len**2-(edge_len/2)**2)
                    ])
                    triangles.append([idx, idx-N-1, idx+N-1])
                # Draw bottom triangle
                elif row % 8 == 0 and col % 7 == 3:
                    G.add_edge(idx, idx-N+1)
                    G.add_edge(idx, idx+N+1)
                    pos[idx] = np.array([
                        pos[idx-N+1][0]+(edge_len/2),
                        pos[idx-N+1][1]-np.sqrt(edge_len**2-(edge_len/2)**2)
                    ])
                    triangles.append([idx, idx+N+1, idx-N+1])
                    
                # Add dodecagon indirectly created by adjacent polygons
                if row % 8 == 0 and col % 7 == 0 and row > 0 and col > 0:
                    dodecagons.append([
                        idx+(3*N), 
                        idx+(2*N)+1, 
                        idx+N+2, 
                        idx-(2*N)+2, 
                        idx-(3*N)+1, 
                        idx-(4*N),
                        idx-(4*N)-1,
                        idx-(3*N)-2,
                        idx-(2*N)-3,
                        idx+N-3,
                        idx+(2*N)-2,
                        idx+(3*N)-1
                    ])
            
            col += 1
        
        for i in range(len(triangles)+len(dodecagons)):
            shapes[i] = dodecagons.pop(0) if i % 3 == 1 else triangles.pop(0)
        
        self.adjust_pos(pos, N, M)
        
        # for shape in shapes:
        #     print(shape, shapes[shape])
        
        # Show nodes and labels for debugging when necessary
        # nx.draw(G, pos=pos, with_labels=True)
        # nx.draw(G, pos=pos, node_size=0)
        # plt.axis('scaled')
        # plt.show()
        
        # for position in pos:
        #     print(position)
        
        # for edge in G.edges:
        #     print(f"({pos[edge[1]][0]},{pos[edge[1]][1]}) - ({pos[edge[0]][0]},{pos[edge[0]][1]}) = {np.sqrt((pos[edge[1]][0]-pos[edge[0]][0])**2+(pos[edge[1]][1]-pos[edge[0]][1])**2)}")
        #     print(f"{edge[1]} - {edge[0]} = {np.sqrt((pos[edge[1]][0]-pos[edge[0]][0])**2+(pos[edge[1]][1]-pos[edge[0]][1])**2)}")
        
        return self.index_cells(shapes, pos, N, M)
        
if __name__ == "__main__":
    Lattice().lattice_cells(1,1)
