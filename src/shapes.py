from src.vector3d import Vector3D
from .base import Shape, HitRecord, CastEpsilon
from src.ray import Ray
from scipy.optimize import minimize

import numpy as np
#import jax
#import jax.numpy as jnp


class Ball(Shape):
    def __init__(self, center, radius):
        super().__init__("ball")
        self.center = center
        self.radius = radius

    def hit(self, ray):
        # Ray-sphere intersection
        oc = ray.origin - self.center
        a = ray.direction.dot(ray.direction)
        b = 2.0 * oc.dot(ray.direction)
        c = oc.dot(oc) - self.radius * self.radius
        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return HitRecord(False, float('inf'), None, None)
        else:
            hit, point, normal = False, None, None
            t = (-b - discriminant**0.5) / (2.0 * a)
            if t > CastEpsilon:
                hit = True
                point = ray.point_at_parameter(t)
                normal = (point - self.center).normalize()
            else:
                t = (-b + discriminant**0.5) / (2.0 * a)
                if t > CastEpsilon:
                    hit = True
                    point = ray.point_at_parameter(t)
                    normal = (point - self.center).normalize()

            return HitRecord(hit, t, point, normal)


class Cube(Shape):
    def __init__(self,center,length):
        self.center = center
        self.length = length
    
    def hit(self, ray, out = False):

        # reference: https://www.realtimerendering.com/raytracing/Ray%20Tracing_%20The%20Next%20Week.pdf
        # page 8

        # im considering the ray is in the coordinates of the object
        local_origin = ray.origin - self.center 

        l2 = self.length/2.0

        #treatment of the case with parallel rays on one/two planes
        
        x0, x1 = -l2, l2
        y0, y1 = -l2, l2
        z0, z1 = -l2, l2

        if abs(ray.direction.x) >= CastEpsilon:

            # Intersections on each plane
            tx0 = (x0 - local_origin.x) / ray.direction.x
            tx1 = (x1 - local_origin.x) / ray.direction.x

        else:
            # for each coordinate check if the origin coordinate is between the cube interval on that coordinate
            if local_origin.x < min(x0,x1) or local_origin.x > max(x0,x1):
                if out == False:
                    return HitRecord(False, float('inf'), None, None)
                else:
                    return HitRecord(False, float('inf'), None, None), float('inf')

            tx0 = -float('inf')
            tx1 = float('inf')

        if abs(ray.direction.y) >= CastEpsilon:

            ty0 = (y0 - local_origin.y) / ray.direction.y
            ty1 = (y1 - local_origin.y) / ray.direction.y

        else:

            if local_origin.y < min(y0,y1) or local_origin.y > max(y0,y1):
                if out == False:
                    return HitRecord(False, float('inf'), None, None)
                else:
                    return HitRecord(False, float('inf'), None, None), float('inf')
            ty0 = -float('inf')
            ty1 = float('inf')

        if abs(ray.direction.z) >= CastEpsilon:

            tz0 = (z0 - local_origin.z) / ray.direction.z
            tz1 = (z1 - local_origin.z) / ray.direction.z

        else:
            if local_origin.z < min(z0,z1) or local_origin.z > max(z0,z1):
                if out == False:
                    return HitRecord(False, float('inf'), None, None)
                else:
                    return HitRecord(False, float('inf'), None, None), float('inf')
            tz0 = -float('inf')
            tz1 = float('inf')

        tx_min = min(tx0,tx1)
        tx_max = max(tx0,tx1)

        ty_min = min(ty0,ty1)
        ty_max = max(ty0,ty1)

        tz_min = min(tz0,tz1)
        tz_max = max(tz0,tz1)

        t_near = [-float('inf'), None]
        t_far = [float('inf'), None]
        
        #this logic for t_near and t_far will be used to compute the normal later
        for t_min in [[tx_min,'x'], [ty_min,'y'], [tz_min,'z']]:
            if t_min[0] > t_near[0]:
                t_near[0] = t_min[0]
                t_near[1] = t_min[1]

        for t_max in [[tx_max,'x'], [ty_max,'y'], [tz_max,'z']]:
            if t_max[0] < t_far[0]:
                t_far[0] = t_max[0]
                t_far[1] = t_max[1]

        # if at least one t_min is bigger than a t_max, the ray doesn't intersect the cube
        # also, t_far needs to be bigger than zero, because the object could be behind the camera   
        if t_near[0] < t_far[0] and t_far[0] > 0:
            
            t_hit = [0.0 , None]
            # t_hit should be t_near, unless if the origin point is inside the cube, at which the hit would be t_far
            if t_near[0] > 0:
                t_hit[0] = t_near[0]
                t_hit[1] = t_near[1]
                signal = 1
            else:
                t_hit[0] = t_far[0]
                t_hit[1] = t_far[1]
                signal = -1

            point = ray.point_at_parameter(t_hit[0])

            # discover where the normal is pointing by analyzing t_hit 
            if t_hit[1] == 'x':
                if tx0 < tx1:
                    normal = Vector3D(-1*signal,0,0)
                else:
                    normal = Vector3D(1*signal,0,0)
            elif t_hit[1] == 'y':
                if ty0 < ty1:
                    normal = Vector3D(0,-1*signal,0)
                else:
                    normal = Vector3D(0,1*signal,0)
            elif t_hit[1] == 'z':
                if tz0 < tz1:
                    normal = Vector3D(0,0,-1*signal)
                else:
                    normal = Vector3D(0,0,1*signal)

            if out == False:
                return HitRecord(True, t_hit[0], point, normal)
            else:
                return HitRecord(True, t_hit[0], point, normal), t_far[0]
        
        if out == False:
            return HitRecord(False, float('inf'), None, None)
        else:
            return HitRecord(False, float('inf'), None, None), float('inf')

class Cylinder(Shape):
    def __init__(self, center, height, radius):
        self.center = center
        self.height = height
        self.radius = radius
    
    def hit(self, ray):
        # reference: https://www.doc.ic.ac.uk/~dfg/graphics/graphics2008/GraphicsLecture09.pdf
        # page 4

        # guarantee that we are using the smallest t when returning the collision
        possible_t = []
        cylinder_or_disk = []

        # im considering the ray is in the coordinates of the object, with the cylinder varying in the z-axis.
        local_origin = ray.origin - self.center

        p0 = local_origin
        p1 = Vector3D(0,0,-self.height/2)
        p2 = Vector3D(0,0,self.height/2)
        
        delta_p = p2 - p1
        delta_p0 = p0 - p1

        a = ray.direction - delta_p*(ray.direction.dot(delta_p))/(delta_p.length()**2)
        b = delta_p0 - delta_p*(delta_p0.dot(delta_p))/(delta_p.length()**2)
        a_cross_b = a.cross(b)

        # ray collision based on discriminant
        # discriminant simplification
        discriminant = 4*(self.radius**2*a.length()*a.length() - a_cross_b.length()**2)

        #if it is below zero, the ray doesn't collide with the cylinder
        if discriminant >= 0:
            # check the two solutions t_1 and t_2
            hit_t = float('inf')
            A = a.dot(a)
            B = 2*a.dot(b)
            
            t_1 = (-B - discriminant**0.5) / (2.0 * A)
            t_2 = (-B + discriminant**0.5) / (2.0 * A)

            for t in [(-B - discriminant**0.5) / (2.0 * A),(-B + discriminant**0.5) / (2.0 * A)]:
                #check if solution is valid
                if t > CastEpsilon:
                    #calculate the alpha for the t's
                    alpha = (p0.dot(delta_p)+t*ray.direction.dot(delta_p)-p1.dot(delta_p))/delta_p.dot(delta_p)

                    #alpha check
                    if 0 <= alpha <= 1:
                        possible_t.append(t)
                        cylinder_or_disk.append('cylinder')
                        break
                        

        #check the intersections of the two planes regarding the disks on the cylinder

        #upper disk using p2 calculated earlier
        normal_up = Vector3D(0,0,1)

        p2_local = p2 - local_origin
        t = p2_local.dot(normal_up)/(ray.direction.dot(normal_up))

        if t > CastEpsilon:

            # get the point in which the ray intersects the plane and see if it is smaller than the radius
            point_t = local_origin + ray.direction * t
            distance_from_center = point_t - p2

            if distance_from_center.length() <= self.radius:
                possible_t.append(t)
                cylinder_or_disk.append('upper disk')

        #bottom disk using p1 calculated earlier
        normal_bottom = Vector3D(0,0,-1)

        p1_local = p1 - local_origin
        t = p1_local.dot(normal_bottom)/(ray.direction.dot(normal_bottom))

        if t > CastEpsilon:
            point_t = local_origin + ray.direction * t
            distance_from_center = point_t - p1

            if distance_from_center.length() <= self.radius:
                possible_t.append(t)
                cylinder_or_disk.append('bottom disk')

        #check what type of that we have
        if len(possible_t) != 0:
            min_t = min(possible_t)
            index = possible_t.index(min_t)
        else:
            return HitRecord(False, float('inf'), None, None)

        if cylinder_or_disk[index] == 'cylinder':
            #generate the vector that touches the cylinder from the ray origin
            p_t = ray.origin + ray.direction * min_t
            # because we are doing the cylinder on the z-axis, the 3rd coordinate should be zero, and the other two should follow the normal of the outline
            normal = Vector3D(p_t.x - self.center.x, p_t.y - self.center.y, 0).normalize()
            point = ray.point_at_parameter(min_t)

            return HitRecord(True, min_t, point, normal)

        elif cylinder_or_disk[index] == 'upper disk':
            point = ray.point_at_parameter(min_t)
            return HitRecord(True, min_t, point, normal_up)
        
        elif cylinder_or_disk[index] == 'bottom disk':
            point = ray.point_at_parameter(min_t)
            return HitRecord(True, min_t, point, normal_bottom)

class Plane(Shape):
    def __init__(self, point, normal):
        super().__init__("plane")
        self.point = point
        self.normal = normal.normalize()

    def hit(self, ray):
        denom = self.normal.dot(ray.direction)
        if abs(denom) > 1e-6:
            t = (self.point - ray.origin).dot(self.normal) / denom
            if t >= CastEpsilon:
                point = ray.point_at_parameter(t)
                return HitRecord(True, t, point, self.normal)
        return HitRecord(False, float('inf'), None, None)

class PlaneUV(Shape):
    def __init__(self, point, normal, forward_direction):
        super().__init__("plane")
        self.point = point
        self.normal = normal.normalize()
        self.forward_direction = forward_direction.normalize()
        # compute right direction
        self.right_direction = self.normal.cross(self.forward_direction).normalize()

    def hit(self, ray):
        denom = self.normal.dot(ray.direction)
        if abs(denom) > 1e-6:
            t = (self.point - ray.origin).dot(self.normal) / denom
            if t >= CastEpsilon:
                point = ray.point_at_parameter(t)
                # Calculate UV coordinates
                vec = point - self.point
                u = vec.dot(self.right_direction)
                v = vec.dot(self.forward_direction)
                uv = Vector3D(u, v, 0)
                return HitRecord(True, t, point, self.normal, uv=uv)
        return HitRecord(False, float('inf'), None, None)

class ObjectTransform(Shape):
    def __init__(self,shape,matrix: np.matrix):
        self.shape = shape
        self.matrix = matrix
        self.center = self.shape.center

        #self.transformed_center = np.array(self.matrix @ self.shape.center) 

        # did this using numpy and implementing __rmatmul__ for matrix-Vector3D multiplication
        self.inverse = np.linalg.inv(self.matrix)
        self.inv_transpose = self.inverse.T
    
    def hit(self, ray):

        #shift the origin for the object coordinates
        shifted_origin = ray.origin - self.center 

        #get ray from world coordinates to object coordinates
        res_origin = np.array(self.inverse @ shifted_origin).flatten()
        res_direction = np.array(self.inverse @ ray.direction).flatten()

        ray_origin_object = Vector3D(res_origin[0], res_origin[1], res_origin[2])
        ray_direction_object = Vector3D(res_direction[0], res_direction[1], res_direction[2])
        local_ray = Ray(ray_origin_object, ray_direction_object)
        

        # hit_record is from the HitRecord class, receiving something like
        # HitRecord(True, t, point, self.normal)
        # we need to change the point, the normal and t then:
        hit_record = self.shape.hit(local_ray)

        if hit_record.hit == False:
            return hit_record
        else:
            
            # get point from object coordinates to world coordinates
            hit_record_point = np.array(self.matrix @ hit_record.point).flatten()

            hit_record.point = Vector3D(hit_record_point[0]+self.center.x,hit_record_point[1]+self.center.y,hit_record_point[2]+self.center.z)

            hit_record_normal = np.array(self.inv_transpose @ hit_record.normal).flatten()

            # get normal from objet coordinates to world coordinates
            hit_record.normal = Vector3D(hit_record_normal[0], hit_record_normal[1], hit_record_normal[2]).normalize()

            # get recalculated t from world coordinates
            hit_record.t = (hit_record.point - ray.origin).length()

            return hit_record

class ImplicitFunction(Shape):
    def __init__(self, function):
        super().__init__("implicit_function")
        self.func = function

    def in_out(self, point):
        return self.func(point) <= 0

class BoxImplicitFunction(ImplicitFunction):
    def __init__(self,implicit_instance, center, bissection_step=0.1,total_iterations=20,number_miniboxes=10):

        super().__init__(implicit_instance.func)

        # object's center in world coordinates
        self.center = center

        self.ImplicitFunction = implicit_instance
        self.bissection_step = bissection_step
        self.total_iterations = total_iterations
        self.number_miniboxes = number_miniboxes

        x0 = [0.0,0.0,0.0]

        #optimization for finding the minimum and maximum x
        cons = {'type': 'eq', 'fun': self.ImplicitFunction.func}
        res = minimize(lambda p: p[0], x0, constraints=cons).fun

        #optimize for each coordinate: x, y and z
        def get_limit(coord_idx, sign):
            res = minimize(lambda p: sign * p[coord_idx], x0, constraints=cons)
            return res.x[coord_idx] # Pegamos a coordenada onde o limite ocorre

        xmin, xmax = get_limit(0, 1), get_limit(0, -1)
        ymin, ymax = get_limit(1, 1), get_limit(1, -1)
        zmin, zmax = get_limit(2, 1), get_limit(2, -1)

        #center of our surface
        self.surface_center = Vector3D((xmin + xmax)/2, (ymin + ymax)/2, (zmin + zmax)/2)

        #lenght of each mini-box
        length = max(abs(xmax - xmin), abs(ymax - ymin), abs(zmax - zmin)) * 1.8

        self.big_box = Cube(center = Vector3D(0,0,0), length = length)

        mini_box_length = length/number_miniboxes
        mini_box_list = []

        #do a bunch of smaller cubes to calculate a better hit aproximation using bissection
        for step_x in range(0,number_miniboxes):
            for step_y in range(0,number_miniboxes):
                for step_z in range(0,number_miniboxes):

                    #correct mini_box center on object coordinate
                    x = step_x*mini_box_length + mini_box_length/2 - length/2
                    y = step_y*mini_box_length + mini_box_length/2 - length/2
                    z = step_z*mini_box_length + mini_box_length/2 - length/2
                    
                    mini_box = Cube(center = Vector3D(x,y,z),length=mini_box_length)
                    mini_box_list.append(mini_box)

        self.mini_box_list = mini_box_list

    def evaluate_f(self, point_local):
        p_shifted = [
            float(point_local.x + self.surface_center.x),
            float(point_local.y + self.surface_center.y),
            float(point_local.z + self.surface_center.z)
        ]
        return self.ImplicitFunction.func(p_shifted)

    def in_out_local(self, point_local):
        return self.evaluate_f(point_local) <= 0

    def in_out(self, point_world):
            #convert point on world coordinates to object coordinates
            p_local = point_world - self.center
            
            return self.in_out_local(p_local)
    
    def old_hit(self, ray):
        # ray in object coordinates
        local_ray = Ray(ray.origin - self.center, ray.direction)

        # see if the ray hits the big box
        big_box_hit = self.big_box.hit(local_ray)

        if big_box_hit.t == float('inf'):
            return big_box_hit
        else:
            
            # save every mini box with a ray intersection to sort by t later
            mini_boxes_that_hit = []

            for mini_box in self.mini_box_list:
                
                mini_box_hit, t1 = mini_box.hit(local_ray,out=True)

                if mini_box_hit.hit == True:
                    #save the mini boxes that intersect with the ray and the out times.
                    mini_boxes_that_hit.append([mini_box_hit,t1])

            #sort by the ray time on enter
            mini_boxes_that_hit.sort(key=lambda x: x[0].t)

            for item in mini_boxes_that_hit:

                point = item[0].point
                point2 = local_ray.point_at_parameter(item[1])

                #check if the signal changes between the two extrema of the ray intersections on the cube
                if self.in_out_local(point) != self.in_out_local(point2):
                    
                    #if it does, we have a hit, and we can do the bissection method 
                    t1 = item[1]
                    t0 = item[0].t
                    
                    #bissection method based on the total_iterations that we have
                    for _ in range(self.total_iterations):
                        tm = (t0 + t1) / 2

                        if self.in_out_local(local_ray.point_at_parameter(t0)) != self.in_out_local(local_ray.point_at_parameter(tm)):
                            t1 = tm
                        else:
                            t0 = tm
                    
                    t_final = (t0 + t1) / 2

                    # return the point to world coordinates
                    point_final = local_ray.point_at_parameter(t_final)
                    p_final = point_final

                    #im using jax to compute the gradient because my roomate told me if would be faster than using other methods
                    p_jax = jnp.array([
                        float(p_final.x + self.surface_center.x),
                        float(p_final.y + self.surface_center.y),
                        float(p_final.z + self.surface_center.z)
                    ])

                    grad_func = jax.jit(jax.grad(self.ImplicitFunction.func))
                    grad_val = grad_func(p_jax)

                    # convert back to world coordinates and normalize the normal vector
                    normal_final = Vector3D(float(grad_val[0]), 
                                            float(grad_val[1]), 
                                            float(grad_val[2])).normalize()

                    #point in world coordinates, the (normal_final * 0.001) is to fix shadow acne according to gemini
                    world_point_final = point_final + self.center + (normal_final * 0.001)

                    return HitRecord(True, t_final, world_point_final, normal_final)

            return HitRecord(False, float('inf'), None, None)

def hit(self, ray):
            # Transform the ray to local space
            local_ray = Ray(ray.origin - self.center, ray.direction)

            # Check where the ray enters and exits the bounding box (search interval)
            big_hit, t_exit = self.big_box.hit(local_ray, out=True)
            
            if not big_hit.hit:
                return HitRecord(False, float('inf'), None, None)

            # Define the search interval inside the box
            t_start = max(0, big_hit.t)
            t_end = t_exit
            
            # perform step only in the ray direction
            num_steps = self.number_miniboxes * 2 
            dt = (t_end - t_start) / num_steps
            
            t_prev = t_start
            # in_out_local is now fast because it has no internal loops
            val_prev = self.in_out_local(local_ray.point_at_parameter(t_prev))

            # Walk along the ray searching for a sign change
            for i in range(1, num_steps + 1):
                t_curr = t_start + i * dt
                val_curr = self.in_out_local(local_ray.point_at_parameter(t_curr))

                #check if the signal changes, if it does, we do the same thing as in the old method
                if val_prev != val_curr:
                    
                    t0, t1 = t_prev, t_curr
                    
                    for _ in range(20): 
                        tm = (t0 + t1) / 2
                        if self.in_out_local(local_ray.point_at_parameter(t0)) != self.in_out_local(local_ray.point_at_parameter(tm)):
                            t1 = tm
                        else:
                            t0 = tm
                    
                    t_final = (t0 + t1) / 2
                    p_local = local_ray.point_at_parameter(t_final)

                    # Calculate the Normal with JAX (locally to avoid Pickle issues)
                    import jax
                    import jax.numpy as jnp
                    grad_func = jax.jit(jax.grad(self.ImplicitFunction.func))
                    
                    p_jax = jnp.array([
                        float(p_local.x + self.surface_center.x),
                        float(p_local.y + self.surface_center.y),
                        float(p_local.z + self.surface_center.z)
                    ])
                    
                    grad_val = grad_func(p_jax)
                    normal_final = Vector3D(float(grad_val[0]), float(grad_val[1]), float(grad_val[2])).normalize()

                    world_point = p_local + self.center + (normal_final * 0.001)
                    return HitRecord(True, t_final, world_point, normal_final)

                val_prev = val_curr
                t_prev = t_curr

            return HitRecord(False, float('inf'), None, None)
