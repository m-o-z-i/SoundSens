#!/usr/bin/python

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

class Cube(object):

    def __init__(self, position, color):
        self.position = position
        self.color = color

    # Cube information
    num_faces = 6

    vertices = [ (-0.3, -0.05, 0.5),
                 (0.3, -0.05, 0.5),
                 (0.3, 0.05, 0.5),
                 (-0.3, 0.05, 0.5),
                 (-0.3, -0.05, -0.5),
                 (0.3, -0.05, -0.5),
                 (0.3, 0.05, -0.5),
                 (-0.3, 0.05, -0.5) ]

    normals = [ (0.0, 0.0, +1.0),  # front
                (0.0, 0.0, -1.0),  # back
                (+1.0, 0.0, 0.0),  # right
                (-1.0, 0.0, 0.0),  # left
                (0.0, +1.0, 0.0),  # top
                (0.0, -1.0, 0.0) ]  # bottom

    vertex_indices = [ (0, 1, 2, 3),  # front
                       (4, 5, 6, 7),  # back
                       (1, 5, 6, 2),  # right
                       (0, 4, 7, 3),  # left
                       (3, 2, 6, 7),  # top
                       (0, 1, 5, 4) ]  # bottom

    verticesStick = [ (-0.04, -0.5, 0.04),
                      (0.04, -0.5, 0.04),
                      (0.04, 0.0, 0.04),
                      (-0.04, 0.0, 0.04),
                      (-0.04, -0.5, -0.04),
                      (0.04, -0.5, -0.04),
                      (0.04, 0.0, -0.04),
                      (-0.04, 0.0, -0.04) ]

    def setColor(self, color):
        self.color = color

    def render(self):
        then = pygame.time.get_ticks()
        glColor(self.color)

        vertices = self.vertices
        verticesStick = self.verticesStick

        # Draw all 6 faces of the cube
        glBegin(GL_QUADS)
        for face_no in xrange(self.num_faces):
            glNormal3dv(self.normals[face_no])
            v1, v2, v3, v4 = self.vertex_indices[face_no]
            glVertex(vertices[v1])
            glVertex(vertices[v2])
            glVertex(vertices[v3])
            glVertex(vertices[v4])
        glEnd()
        
        # draw cylinder
        glBegin(GL_QUADS)
        for face_no in xrange(self.num_faces):
            glNormal3dv(self.normals[face_no])
            v1, v2, v3, v4 = self.vertex_indices[face_no]
            glVertex(verticesStick[v1])
            glVertex(verticesStick[v2])
            glVertex(verticesStick[v3])
            glVertex(verticesStick[v4])
        glEnd()