# defines a scene with a ball using implicit function
import math
import numpy as np
from src.base import BaseScene, Color
from src.shapes import Cube, Cylinder, PlaneUV, ObjectTransform, Ball
from src.camera import Camera
from src.vector3d import Vector3D
from src.light import PointLight, AreaLight
from src.materials import SimpleMaterial, SimpleMaterialWithShadows, TranslucidMaterial, CheckerboardMaterial

# class name should be Scene
class Scene(BaseScene):
    def __init__(self):
        super().__init__("Object Transform Scene")

        # light blue background
        self.background = Color(0.7, 0.8, 1)
        self.ambient_light = Color(0.1, 0.1, 0.1)
        self.max_depth = 30  # for reflections/refractions
        self.camera = Camera(
            eye=Vector3D(1, 0, .3)*10.0,
            look_at=Vector3D(0, 0, 1.8),
            up=Vector3D(0, 0, 1),
            fov=30,
            img_width=800,
            img_height=600
        )
        self.lights = [
            # add a point light
            #PointLight(position=Vector3D(0, 1, 1)*10, color=Color(1, 1, 1), intensity=1.6),
            AreaLight(
                position=Vector3D(0, 1, 1)*10,
                look_at=Vector3D(0, 0, 0),
                up=Vector3D(0, 0, 1),
                width=4,
                height=4,
                color=Color(1, 1, 1),
                intensity=1.6
            )
        ]

        '''
        # add a red translucent Cylinder
        red_material = TranslucidMaterial(
            ambient_coefficient=0.05,
            diffuse_coefficient=0.5,
            diffuse_color=Color(0.5, 0, 0),
            specular_coefficient=0.1,
            specular_color=Color(1, 1, 1),
            specular_shininess=32,
            transmission_coefficient=0.8,
            refraction_index=1.5
        )
        self.add(
            Cylinder(center=Vector3D(0, 0, 1.2), height=1, radius=0.5), 
            red_material
        )
        '''
        blue_material2 = SimpleMaterial(
            ambient_coefficient=1,
            diffuse_coefficient=0.2,
            diffuse_color=Color(0, 0.5, 0),
            specular_coefficient=0.5,
            specular_color=Color(1, 1, 0),
            specular_shininess=32
        )
        
        self.add(
            Cylinder(center=Vector3D(0, 0, 1.2), height=1, radius=0.5), 
            blue_material2
        )
        
        red_material = SimpleMaterial(
            ambient_coefficient=1,
            diffuse_coefficient=0.2,
            diffuse_color=Color(0.5, 0, 0),
            specular_coefficient=0.5,
            specular_color=Color(1, 1, 0),
            specular_shininess=32
        )

        blue_material = SimpleMaterial(
            ambient_coefficient=1,
            diffuse_coefficient=0.2,
            diffuse_color=Color(0, 0, 0.5),
            specular_coefficient=0.5,
            specular_color=Color(1, 1, 0),
            specular_shininess=32
        )

        green_material = SimpleMaterial(
            ambient_coefficient=1,
            diffuse_coefficient=0.2,
            diffuse_color=Color(0, 0.5, 0),
            specular_coefficient=0.5,
            specular_color=Color(1, 1, 0),
            specular_shininess=32
        )

        yellow_material = SimpleMaterial(
            ambient_coefficient=1,
            diffuse_coefficient=0.2,
            diffuse_color=Color(0.5, 0.5, 0),
            specular_coefficient=0.5,
            specular_color=Color(1, 1, 0),
            specular_shininess=32
        )
        d = 1.1
        
        self.add(
            Cube(center=Vector3D(d, d, math.sqrt(2)), length=1), 
            green_material
        )
        
        m_escala_simples = np.matrix([
            [1.0, 0, 0],  # Triplica o tamanho no eixo X
            [0, 1.5, 0],
            [0, 0, 1.0]
        ])
        
        
        funny_cube = Cube(center=Vector3D(-d, -d/2, math.sqrt(2)), length=math.sqrt(2))
        self.add(
            ObjectTransform(funny_cube,m_escala_simples), 
            blue_material
        )
        
        #rotated cylinder

        theta = np.radians(30)
        c, s = np.cos(theta), np.sin(theta)

        # 2. Criar uma matriz de Rotação no eixo Y
        # [ cos  0  sin ]
        # [  0   1   0  ]
        # [-sin  0  cos ]
        rotation_y = np.matrix([
            [c,  0, s],
            [0,  1, 0],
            [-s, 0, c]
        ])

        rotated_cylinder = Cylinder(center=Vector3D(0.5, 0.5, 1.7), height=1, radius=0.5)
        self.add(
            ObjectTransform(rotated_cylinder,rotation_y), 
            yellow_material
        )

        # rotated paraboloid

        # for creating the paraboloid
        S = np.diag([1.0, 2.0, 1.0])
    
        # Matriz de Rotação no eixo X
        theta = np.radians(50)
        c, s = np.cos(theta), np.sin(theta)

        R = np.array([
            [1,  0,  0],
            [0,  c, -s],
            [0,  s,  c]
        ])

        RS = R @ S

        Paraboloid = Ball(center=Vector3D(0, -0.3, 1), radius=0.5)
        self.add(
            ObjectTransform(Paraboloid,RS), 
            red_material
        )

        # ground plane
        gray_material = CheckerboardMaterial(
            ambient_coefficient=1,
            diffuse_coefficient=0.8,
            square_size=1.0,
            white_color=Color(0.9, 0.9, 0.9),
            black_color=Color(0.2, 0.2, 0.2)
        )
        self.add(PlaneUV(point=Vector3D(0, 0, 0), normal=Vector3D(0, 0, 1), forward_direction=Vector3D(1, 1, 0)), gray_material)