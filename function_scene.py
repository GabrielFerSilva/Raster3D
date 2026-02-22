# defines a scene with a ball using implicit function
import math
from src.base import BaseScene, Color
from src.shapes import Ball, PlaneUV, ImplicitFunction, BoxImplicitFunction
from src.camera import Camera
from src.vector3d import Vector3D
from src.light import PointLight, AreaLight
from src.materials import SimpleMaterial, SimpleMaterialWithShadows, TranslucidMaterial, CheckerboardMaterial

def mitchel_surface(params):
    x,y,z = params
    term1 = 4 * (x**4 + (y**2 + z**2)**2 + 17 * x**2 * (y**2 + z**2))
    term2 = 20 * (x**2 + y**2 + z**2)
    return term1 - term2 + 17

def heart_surface(params):
    x,y,z = params
    basis = (x**2 + 2.25 * y**2 + z**2 - 1)**3
    sub_term = x**2 * z**3 + 0.1125 * y**2 * z**3
    return basis - sub_term


# class name should be Scene
class Scene(BaseScene):
    def __init__(self):
        super().__init__("Function Scene")

        # light blue background
        self.background = Color(0.7, 0.8, 1)
        self.ambient_light = Color(0.1, 0.1, 0.1)
        self.max_depth = 10  # for reflections/refractions
        self.camera = Camera(
            eye=Vector3D(1, 0, .3)*10.0,
            look_at=Vector3D(0, 0, 1.8),
            up=Vector3D(0, 0, 1),
            fov=30,
            img_width=400,
            img_height=150
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

        # add a red translucent ball
        red_material = TranslucidMaterial(
            ambient_coefficient=0.05,
            diffuse_coefficient=0.2,
            diffuse_color=Color(0.5, 0, 0),
            specular_coefficient=0.1,
            specular_color=Color(1, 1, 1),
            specular_shininess=32,
            transmission_coefficient=0.8,
            refraction_index=1.5
        )
        """
        self.add(
            Ball(center=Vector3D(0, 0, 1.2), radius=1), 
            red_material
        )
        """

        # blue ball
        blue_material = SimpleMaterial(
            ambient_coefficient=1,
            diffuse_coefficient=0.2,
            diffuse_color=Color(0, 0, 0.5),
            specular_coefficient=0.5,
            specular_color=Color(1, 1, 0),
            specular_shininess=32
        )
        '''
        d = 2.2
        self.add(
            Ball(center=Vector3D(-d, -d/2, math.sqrt(2)), radius=math.sqrt(2)), 
            blue_material
        )
        '''

        '''
        heart = ImplicitFunction(heart_surface)
        
        self.add(
            BoxImplicitFunction(heart), 
            blue_material
        )
        '''

        # ground plane
        gray_material = CheckerboardMaterial(
            ambient_coefficient=1,
            diffuse_coefficient=0.8,
            square_size=1.0,
            white_color=Color(0.9, 0.9, 0.9),
            black_color=Color(0.2, 0.2, 0.2)
        )
        self.add(PlaneUV(point=Vector3D(0, 0, 0), normal=Vector3D(0, 0, 1), forward_direction=Vector3D(1, 1, 0)), gray_material)