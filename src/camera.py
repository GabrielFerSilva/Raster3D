# world is right-handed, z is up
import math
import random

from .ray import Ray

class Camera:
    def __init__(self, eye, look_at, up, fov, img_width, img_height):
        self.eye = eye
        # self.look_at = look_at
        # self.up = up
        # self.fov = fov
        # self.aspect_ratio = aspect_ratio
        self.img_width = img_width
        self.img_height = img_height

        aspect_ratio = img_height / img_width

        self.su = 2 * math.tan(math.radians(fov) / 2)
        self.sv = self.su * aspect_ratio

        self.w = (eye - look_at).normalize()
        up = up.normalize()
        #self.u = self.w.cross(up).normalize()
        self.u = up.cross(self.w).normalize()
        self.v = self.w.cross(self.u).normalize()

    def point_image2world(self, x, y):
        # from image coordinates to coordinates 
        # in the camera's view plane
        x_ndc = self.su * x / self.img_width - self.su / 2
        y_ndc = self.sv * y / self.img_height - self.sv / 2

        # from view plane to world coordinates
        return self.eye + self.u * x_ndc + self.v * y_ndc - self.w

    def ray(self, x, y):
        point_world = self.point_image2world(x, y)
        direction = (point_world - self.eye).normalize()
        return Ray(self.eye, direction)

class LensCamera(Camera):
    def __init__(self, eye, look_at, up, fov, img_width, img_height, focal, lens_radius):
        super().__init__(eye, look_at, up, fov, img_width, img_height)

        #we now have the focal distante and the lens radius
        self.focal = focal
        self.lens_radius = lens_radius

        # same things as in the normal camera
        self.img_width = img_width
        self.img_height = img_height

        aspect_ratio = img_height / img_width

        self.su = 2 * math.tan(math.radians(fov) / 2)
        self.sv = self.su * aspect_ratio

        self.w = (eye - look_at).normalize()
        up = up.normalize()
        #self.u = self.w.cross(up).normalize()
        self.u = up.cross(self.w).normalize()
        self.v = self.w.cross(self.u).normalize()

    #same thing
    def point_image2world(self, x, y):
        # from image coordinates to coordinates 
        # in the camera's view plane
        x_ndc = self.su * x / self.img_width - self.su / 2
        y_ndc = self.sv * y / self.img_height - self.sv / 2

        # from view plane to world coordinates
        return self.eye + self.u * x_ndc + self.v * y_ndc - self.w

    def ray(self, x, y):

        # I tought it would be possible to compute all the rays inside here, 
        # but turns out you need to do on the raster level, so besides the 
        # anti-aliasing samples we also have the lens samples in order to 
        # compute the lens field based on the lens size and the focal distance.

        # we first compute the direction going from the center of the lens pinhole
        pixel_world_pos = self.point_image2world(x, y)
        
        dir_pinhole = (pixel_world_pos - self.eye).normalize()

        # ray trought the pinhole
        p_focal = self.eye + dir_pinhole * self.focal
            
        # we then generate ue**2 + ve**2 < r**2 
        angle = 2*math.pi*random.random()
        r = self.lens_radius * math.sqrt(random.random())
        ue = r * math.cos(angle)
        ve = r * math.sin(angle)

        # the point on the lens where the ray will pass through
        lens_point = self.eye + (self.u * ue) + (self.v * ve)

        # and the direction of the ray is from the lens point to the focal point
        direction = (p_focal - lens_point).normalize()

        return Ray(lens_point, direction)