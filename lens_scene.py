# defines a scene with a ball using implicit function
import math
from src.base import BaseScene, Color
from src.shapes import Ball, PlaneUV, Cube
from src.camera import LensCamera
from src.vector3d import Vector3D
from src.light import PointLight, AreaLight
from src.materials import SimpleMaterial, SimpleMaterialWithShadows, TranslucidMaterial, CheckerboardMaterial

# class name should be Scene
class Scene(BaseScene):
    def __init__(self):
        super().__init__("Ball Scene")

        # light blue background
        self.background = Color(0.7, 0.8, 1)
        self.ambient_light = Color(0.1, 0.1, 0.1)
        self.max_depth = 600  # for reflections/refractions
        self.camera = LensCamera(
            eye=Vector3D(1, 0, .3)*7.0,
            look_at=Vector3D(0, 0, 1),
            up=Vector3D(0, 0, 1),
            fov=30,
            img_width=800,
            img_height=600,
            focal = 27.06,
            lens_radius= 0.05
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

        green_material = TranslucidMaterial(
            ambient_coefficient=0.05,
            diffuse_coefficient=0.2,
            diffuse_color=Color(0, 0.5, 0),
            specular_coefficient=0.1,
            specular_color=Color(1, 1, 1),
            specular_shininess=32,
            transmission_coefficient=0.8,
            refraction_index=1.5
        )
        
        green_material1 = TranslucidMaterial(
            ambient_coefficient=0.05,
            diffuse_coefficient=0.2,
            diffuse_color=Color(0, 0.4, 0.1),
            specular_coefficient=0.1,
            specular_color=Color(1, 1, 1),
            specular_shininess=32,
            transmission_coefficient=0.8,
            refraction_index=1.5
        )
        green_material2 = TranslucidMaterial(
            ambient_coefficient=0.05,
            diffuse_coefficient=0.2,
            diffuse_color=Color(0, 0.3, 0.2),
            specular_coefficient=0.1,
            specular_color=Color(1, 1, 1),
            specular_shininess=32,
            transmission_coefficient=0.8,
            refraction_index=1.5
        )
        green_material3 = TranslucidMaterial(
            ambient_coefficient=0.05,
            diffuse_coefficient=0.2,
            diffuse_color=Color(0, 0.2, 0.3),
            specular_coefficient=0.1,
            specular_color=Color(1, 1, 1),
            specular_shininess=32,
            transmission_coefficient=0.8,
            refraction_index=1.5
        )
        green_material4 = TranslucidMaterial(
            ambient_coefficient=0.05,
            diffuse_coefficient=0.2,
            diffuse_color=Color(0, 0.1, 0.4),
            specular_coefficient=0.1,
            specular_color=Color(1, 1, 1),
            specular_shininess=32,
            transmission_coefficient=0.8,
            refraction_index=1.5
        )
        green_material5 = TranslucidMaterial(
            ambient_coefficient=0.05,
            diffuse_coefficient=0.2,
            diffuse_color=Color(0, 0, 0.5),
            specular_coefficient=0.1,
            specular_color=Color(1, 1, 1),
            specular_shininess=32,
            transmission_coefficient=0.8,
            refraction_index=1.5
        )

        self.add(
            Ball(center=Vector3D(0, 0.5, 0.5), radius=0.5), 
            green_material
        )

        self.add(
            Ball(center=Vector3D(-5, -0.6, 0.5), radius=0.5), 
            green_material1
        )

        self.add(
            Ball(center=Vector3D(-10, 0.7, 0.5), radius=0.5), 
            green_material2
        )

        self.add(
            Ball(center=Vector3D(-15, -0.8, 0.5), radius=0.5), 
            green_material3
        )

        self.add(
            Ball(center=Vector3D(-20, 0.9, 0.5), radius=0.5), 
            green_material4
        )

        self.add(
            Ball(center=Vector3D(-25, -1, 0.5), radius=0.5), 
            green_material5
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