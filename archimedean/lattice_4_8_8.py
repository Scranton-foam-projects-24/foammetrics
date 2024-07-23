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
            if len(shapes[shape]) == 4:
                cells.append(self.index_4_gon(shapes[shape], shape, N, M, pos))
            else:
                cells.append(self.index_8_gon(shapes[shape], shape, N, M, pos))
        return cells
    
    def index_4_gon(self, vertices, idx, N, M, pos):
        """
        Function which converts information about a 4-gon into a single cell in
        the same format used by the pyvoro package.
    
        Parameters
        ----------
        vertices : list
            A list of the vertices which make up the given 4-gon, provided in
            counterclockwise order.
        idx : int
            Value denoting the 4-gon's position in reference to every other 4-gon
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
            A dictionary containing detailed information about the provided 4-gon
            in the same format as the pyvoro package. The information about each
            cell, or 4-gon, includes neighboring cells (and which edge they share),
            the centroid of each cell, teh positions of each vertex which makes up
            the cell, the volume of the cell, and how the vertices are joined by
            edges.
    
        """
        faces = []
        height = (2*int(N/4))-1
        if vertices[0] % N == 4:
            faces.append([
                {'adjacent_cell': idx+1,
                 'vertices': [vertices[0], vertices[1]]
                },
                {'adjacent_cell': idx-1,
                 'vertices': [vertices[2], vertices[3]]
                }
            ])
            if vertices[0] > N * 4:
                faces.append(
                    {'adjacent_cell': idx-1,
                     'vertices': [vertices[1], vertices[2]]
                    }
                )
            if vertices[0] < (N*M)-(N*2):
                faces.append(
                    {'adjacent_cell': idx+height,
                     'vertices': [vertices[0], vertices[3]]
                    }
                )
        elif vertices[0] % N == 2:
            faces.append([
                {'adjacent_cell': idx-height,
                 'vertices': [vertices[1], vertices[2]]
                },
                {'adjacent_cell': idx+height,
                 'vertices': [vertices[0], vertices[3]]
                }
            ])
            if vertices[0] % N == N-2:
                faces.append(
                    {'adjacent_cell': idx-1,
                     'vertices': [vertices[0], vertices[1]]
                    }
                )
            elif vertices[0] % N == 2:
                faces.append(
                    {'adjacent_cell': idx+1, 
                     'vertices': [vertices[0], vertices[1]]
                    }
                )
        else:
            faces.append([
                {'adjacent_cell': idx+1,
                 'vertices': [vertices[0], vertices[1]]
                },
                {'adjacent_cell': idx-1,
                 'vertices': [vertices[2], vertices[3]]
                },
            ])
            if idx-height-1 > 0:
                faces.append(
                    {'adjacent_cell': idx-height,
                     'vertices': [vertices[1], vertices[2]]
                    }
                )
            if idx+height+1 < N*M:
                faces.append(
                    {'adjacent_cell': idx+height,
                     'vertices': [vertices[0], vertices[3]]
                    }
                )
    
        # Create cell in format of pyvoro package
        cell = {
            'faces': faces,
            'original': np.array([
                (pos[vertices[0]][0]+pos[vertices[1]][0])/2,
                (pos[vertices[0]][1]+pos[vertices[3]][1])/2
            ]),
            'vertices': [
                pos[vertices[0]],
                pos[vertices[1]],
                pos[vertices[2]],
                pos[vertices[3]]
            ],
            'volume': np.sqrt(2)+1,
            'adjacency': [
                [vertices[0], vertices[1]],
                [vertices[1], vertices[2]],
                [vertices[2], vertices[3]],
                [vertices[3], vertices[0]]
            ]
        }
        return cell
    
    def index_8_gon(self, vertices, idx, N, M, pos):
        """
        Function which converts information about a 8-gon into a single cell in
        the same format used by the pyvoro package.
    
        Parameters
        ----------
        vertices : list
            A list of the vertices which make up the given 8-gon, provided in
            counterclockwise order.
        idx : int
            Value denoting the 8-gon's position in reference to every other 8-gon
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
            A dictionary containing detailed information about the provided 8-gon
            in the same format as the pyvoro package. The information about each
            cell, or 8-gon, includes neighboring cells (and which edge they share),
            the centroid of each cell, teh positions of each vertex which makes up
            the cell, the volume of the cell, and how the vertices are joined by
            edges.
    
        """
        faces = []
        height = (2*int(N/4))-1
        # Handle octagons which are completely enclosed by other polygons
        if vertices[0] % 4 == 0:
            faces.append([
                # Octagon neighbor up and to the right
                {'adjacent_cell': idx+height+1, 
                 'vertices': [vertices[0], vertices[1]]
                },
                # Square immediately above this octagon
                {'adjacent_cell': idx+1, 
                 'vertices': [vertices[1], vertices[2]]
                },
                # Octagon neighbor up and to the left
                {'adjacent_cell': idx-height+1,
                 'vertices': [vertices[2], vertices[3]]
                },
                # Square immediately to the left of this octagon
                {'adjacent_cell': idx-height,
                 'vertices': [vertices[3], vertices[4]]
                },
                # Octagon neighbor down and to the left
                {'adjacent_cell': idx-height-1,
                 'vertices': [vertices[4], vertices[5]]
                },
                # Square immediately below this octagon
                {'adjacent_cell': idx-1,
                 'vertices': [vertices[5], vertices[6]]
                },
                # Octagon neighbor down and to the right
                {'adjacent_cell': idx+height-1,
                 'vertices': [vertices[6], vertices[7]]
                },
                # Square immediately to the right of this octagon
                {'adjacent_cell': idx+height,
                 'vertices': [vertices[0], vertices[7]]
                },
            ])
        # Handle octagons which may (not) be on the edge of the lattice
        else:
            # If octagon doesn't lie on left edge of lattice
            if vertices[0] > N*4:
                faces.append(
                    {'adjacent_cell': idx-height, 
                     'vertices': [vertices[3], vertices[4]]
                    })
                # If octagon doesn't lie on top edge and left edge of lattice
                if vertices[0] % N < N-2:
                    faces.append(
                        {'adjacent_cell': idx-height+1, 
                         'vertices': [vertices[2], vertices[3]]
                        })
                # If octagon doesn't lie on bottom edge and left edge of lattice
                if vertices[0] % N > 2:
                    faces.append(
                        {'adjacent_cell': idx-height-1, 
                         'vertices': [vertices[4], vertices[5]]
                        })
            # If octagon doesn't lie on right edge of lattice
            if vertices[0] < (M*N)-N:
                faces.append(
                    {'adjacent_cell': idx+height, 
                     'vertices': [vertices[0], vertices[7]]
                    })
                if vertices[0] % N < N-2:
                    # If octagon doesn't lie on top edge and right edge of lattice
                    faces.append(
                        {'adjacent_cell': idx+height+1, 
                         'vertices': [vertices[0], vertices[1]]
                        })
                if vertices[0] % N > 2:
                    # If octagon doesn't lie on bottom edge and right edge of lattice
                    faces.append(
                        {'adjacent_cell': idx+height-1, 
                         'vertices': [vertices[6], vertices[7]]
                        })
            # If octagon doesn't lie on top edge of lattice
            if vertices[0] % N < N-2:
                faces.append(
                    {'adjacent_cell': idx+1, 
                     'vertices': [vertices[1], vertices[2]]
                    })
            # If octagon doesn't lie on bottom edge of lattice
            if vertices[0] % N > 2:
                faces.append(
                    {'adjacent_cell': idx-1, 
                     'vertices': [vertices[5], vertices[6]]
                    })
            
        # Create cell in format of pyvoro package
        side_len = pos[vertices[0]][1] - pos[vertices[7]][1]
        area = side_len/(2*np.sin(np.pi/8))
        cell = {
            'faces': faces,
            'original': np.array([
                (pos[vertices[0]][0] + pos[vertices[3]][0])/2,
                (pos[vertices[1]][1] + pos[vertices[6]][1])/2
            ]),
            'vertices': [
                pos[vertices[0]],
                pos[vertices[1]],
                pos[vertices[2]],
                pos[vertices[3]],
                pos[vertices[4]],
                pos[vertices[5]],
                pos[vertices[6]],
                pos[vertices[7]]
            ],
            'volume': area,
            'adjacency': [
                [vertices[0], vertices[1]],
                [vertices[1], vertices[2]],
                [vertices[2], vertices[3]],
                [vertices[3], vertices[4]],
                [vertices[4], vertices[5]],
                [vertices[5], vertices[6]],
                [vertices[6], vertices[7]],
                [vertices[7], vertices[0]]
            ]
        }
        return cell
    
    def adjust_octagon(self, pos, idx, N, M):
        """
        Helper function to adjust the position of each vertex of an 8-gon to make
        the edges of the 8-gon the same length
    
        Parameters
        ----------
        pos : dict
            A dictionary containing the index of each vertex for each key, and a
            numpy array of length 2 containing a [x,y] coordinate pair for each 
            value.
        idx : int
            Value denoting the 8-gon's position in reference to every other 4-gon
            in the lattice.
        N : int
            The height (measured in number of fundamental cells) of the lattice.
        M : int
            The width (measured in number of fundamental cells) of the lattice.
    
        """
        # If octagon lies on left edge
        if idx-(3*N) < N:
            pos[idx-(3*N)] = np.array([
                pos[idx-(3*N)][0] + (np.sqrt(2)-1)/(4*M),
                pos[idx-(3*N)][1] + (np.sqrt(2)-1)/(4*N)
            ])
            pos[idx-(3*N)-1] = np.array([
                pos[idx-(3*N)-1][0] + (np.sqrt(2)-1)/(4*M),
                pos[idx-(3*N)-1][1] - (np.sqrt(2)-1)/(4*N)
            ])
        # If octagon lies on right edge
        if idx > (M*N)-N:
            pos[idx] = np.array([
                pos[idx][0] - (np.sqrt(2)-1)/(4*M),
                pos[idx][1] + (np.sqrt(2)-1)/(4*N)
            ])
            pos[idx-1] = np.array([
                pos[idx-1][0] - (np.sqrt(2)-1)/(4*M),
                pos[idx-1][1] - (np.sqrt(2)-1)/(4*N)
            ])
        # If octagon lies on top edge
        if (idx-N+1) % N == N-1:
            pos[idx-N+1] = np.array([
                pos[idx-N+1][0] + (np.sqrt(2)-1)/(4*M),
                pos[idx-N+1][1] - (np.sqrt(2)-1)/(4*N)
            ])
            pos[idx-(2*N)+1] = np.array([
                pos[idx-(2*N)+1][0] - (np.sqrt(2)-1)/(4*M),
                pos[idx-(2*N)+1][1] - (np.sqrt(2)-1)/(4*N)
            ])
        # If octagon lies on bottom edge
        if (idx-N-2) % N == 0:
            pos[idx-N-2] = np.array([
                pos[idx-N-2][0] + (np.sqrt(2)-1)/(4*M),
                pos[idx-N-2][1] + (np.sqrt(2)-1)/(4*N)
            ])
            pos[idx-(2*N)-2] = np.array([
                pos[idx-(2*N)-2][0] - (np.sqrt(2)-1)/(4*M),
                pos[idx-(2*N)-2][1] + (np.sqrt(2)-1)/(4*N)
            ])
    
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
        squares = []
        octagons = []
        shapes = {}
        M = m * 4
        N = n * 4
        
        for col in range(0, M):
            # Start every new column of points with an initial point
            pos[N*col] = np.array([col/M, 0])
            
            # If the point is part of the bottom edge of an octagon
            if col > 0 and col % 4 == 2:
                G.add_edge(N*col, N*col-N)
            
            # For every vertex going starting at the bottom of column and going up
            for row in range(0, N):
                idx = (N * col) + row
                
                # If the node added is the top of a vertical edge of an octagon
                if 1 < row % 4 < 3 and idx-1 in G.nodes:
                    G.add_edge(idx, idx-1)
                
                if idx not in pos.keys():
                    pos[idx] = np.array([col/M, row/N])
    
                # Handle diagonal edges of octagons
                if col < M-1:
                    # If vertex is right vertex of bottom flat edge ...
                    if row % 4 == 0 and col % 4 == 2:
                        # ... make connection with vertex up 1 unit, right 1 unit
                        G.add_edge(idx, idx+N+1)
                    # If vertex is bottom vertex of left vertical edge ...
                    if row % 4 == 1 and col % 4 == 0:
                        # ... make connection with vertex down 1 unit, right 1 unit
                        G.add_edge(idx, idx+N-1)
                    # If vertex is top vertex of left vertical edge ...
                    if row % 4 == 2 and col % 4 == 0:
                        # ... make connection with vertex up 1 unit, right 1 unit
                        G.add_edge(idx, idx+N+1)
                    # If vertex is right vertex of top flat edge ...
                    if row % 4 == 3 and col % 4 == 2:
                        # ... make connection with vertex down 1 unit, right 1 unit
                        G.add_edge(idx, idx+N-1)
                
                # Add octagon (row, col)
                if col % 4 == 3 and col > 0 and idx in G.nodes and row % 4 == 2:
                    octagons.append([
                        idx, 
                        idx-N+1, 
                        idx-(2*N)+1, 
                        idx-(3*N), 
                        idx-(3*N)-1, 
                        idx-(2*N)-2, 
                        idx-N-2, 
                        idx-1
                    ])
                    self.adjust_octagon(pos, idx, N, M)
                
                # Handle squares inside of and horizontally connecting octagons
                if 0 < row % 4 < 3 and idx in G.nodes:
                    # Remove square inside octagon
                    if 0 < col % 4 < 3:
                        G.remove_node(idx)
                    # Connect octagon to right neighbor, also forming square
                    elif col % 4 == 3 and idx+N < N*M:
                        G.add_edge(idx, idx+N)
                        if row % 4 == 2:
                            squares.append([
                                idx+N,
                                idx,
                                idx-1,
                                idx+N-1
                            ])
                            # Adjust position of square's vertices to correct edge
                            # lengths of octagon, staring with next col's vertices
                            pos[idx+N] = np.array([
                                pos[idx][0] + (1/M) + (np.sqrt(2)-1)/(4*M),
                                pos[idx][1] + (np.sqrt(2)-1)/(4*N)
                            ])
                            pos[idx+N-1] = np.array([
                                pos[idx-1][0] + (1/M) + (np.sqrt(2)-1)/(4*M),
                                pos[idx-1][1] - (np.sqrt(2)-1)/(4*N)
                            ])
                            # Adjust prev col's vertices
                            pos[idx] = np.array([
                                pos[idx][0] - (np.sqrt(2)-1)/(4*M),
                                pos[idx][1] + (np.sqrt(2)-1)/(4*N)
                            ])
                            pos[idx-1] = np.array([
                                pos[idx-1][0] - (np.sqrt(2)-1)/(4*M),
                                pos[idx-1][1] - (np.sqrt(2)-1)/(4*N)
                            ])
                
                # Handle squares vertically connecting octagons
                if col % 4 == 2 and (row % 4 == 0 or row % 4 == 3):
                    # Make flat top and bottom edges of octagon
                    G.add_edge(idx, idx-N)
                    if (idx + 1) % N > 0 :
                        # Connect octagon to top neighbor, also forming square
                        G.add_edge(idx, idx+1)
                        if row % 4 == 0 and row > 0:
                            squares.append([
                                idx,
                                idx-N,
                                idx-N-1,
                                idx-1
                            ])
                            # Adjust position of square's vertices to correct edge
                            # lengths of octagon
                            pos[idx] = np.array([
                                pos[idx][0] + (np.sqrt(2)-1)/(4*M),
                                pos[idx][1] + (np.sqrt(2)-1)/(4*N)
                            ])
                            pos[idx-N] = np.array([
                                pos[idx-N][0] - (np.sqrt(2)-1)/(4*M),
                                pos[idx-N][1] + (np.sqrt(2)-1)/(4*N)
                            ])
                            pos[idx-N-1] = np.array([
                                pos[idx-N-1][0] - (np.sqrt(2)-1)/(4*M),
                                pos[idx-N-1][1] - (np.sqrt(2)-1)/(4*N)
                            ])
                            pos[idx-1] = np.array([
                                pos[idx-1][0] + (np.sqrt(2)-1)/(4*M),
                                pos[idx-1][1] - (np.sqrt(2)-1)/(4*N)
                            ])
                            
                # Additional handling of squares vertically connecting octagons
                if col % 4 == 1 and (row % 4 == 0 or row % 4 == 3):
                    # Make left edge of squares that vertically connect octagons
                    if (idx + 1) % N > 0:
                        G.add_edge(idx, idx+1)
                        # Add octagon indirectly created by adjacent polygons
                        if row % 4 == 0 and row > 0 and col > 1:
                            octagons.append([
                                idx, 
                                idx-N+1, 
                                idx-(2*N)+1, 
                                idx-(3*N), 
                                idx-(3*N)-1, 
                                idx-(2*N)-2, 
                                idx-N-2, 
                                idx-1
                            ])
        
        for i in range((2 * len(octagons)) - 1):
            shapes[i] = octagons.pop(0) if i % 2 == 0 else squares.pop(0)
        
        # Show centroids for debugging when necessary
        # for i, cell in enumerate(index_cells(shapes, pos, N, M)):
        #     center = i + len(pos)
        #     pos[center] = cell['original']
        #     if center+1 < len(shapes)+len(pos):
        #         G.add_node(center)
            
        # Show nodes and labels for debugging when necessary
        # nx.draw(G, pos=pos, with_labels=True)
        # nx.draw(G, pos=pos, node_size=0)
        # plt.axis('scaled')
        # plt.show()
        
        return self.index_cells(shapes, pos, N, M)

if __name__ == "__main__":
    Lattice().lattice_cells(4,4)
