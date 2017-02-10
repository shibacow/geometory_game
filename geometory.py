#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys,random
import pygame
from pygame.locals import *
from pygame.color import *
import pymunk
import pymunk.pygame_util
import math
import re
from pymunk import vec2d
import json
point=None
def draw_collision(arbiter, space, data):
    #print("hoge")
    global point
    for c in arbiter.contact_point_set.points:
        r = max( 3, abs(c.distance*5) )
        r = int(r)
        p = tuple(map(int, c.point_a))
        point=p

    is_segment=any([c for  c in arbiter.shapes if isinstance(c,pymunk.shapes.Segment)])
    if not is_segment:
        point=None

        #print("p={}".format(p))
        #pygame.draw.circle(data["surface"], THECOLORS["red"], p, r, 0)

def init():
    pygame.init()
    screen=pygame.display.set_mode((610,610),RESIZABLE)
    screen2=screen.subsurface(Rect(0,0,600,600))

    pygame.display.set_caption("幾何")
    pygame.display.set_caption("Joints.Just wait ant the L will tips over")
    clock = pygame.time.Clock()
    space = pymunk.Space()
    space.gravity = (0.0,0.0)
    return screen,screen2,clock,space

def up_position(body,dt):
    print("body={} dt={}".format(body,dt))
def get_resource(space,surface):
    o=json.load(open('out3.json'))
    maxx=10
    radius=14
    body = pymunk.Body(100000,100000)
    body.position=(300,-1*surface.get_height())
    body.filter=pymunk.ShapeFilter(categories=2)
    for i,k in enumerate(o[:-1]):
        p1=k
        p2=o[i+1]
        x1=float(p1['x'])
        y1=-1*float(p1['y'])
        x2=float(p2['x'])
        y2=-1*float(p2['y'])
        (x1,y1)=pymunk.pygame_util.from_pygame((x1,y1),surface)
        (x2,y2)=pymunk.pygame_util.from_pygame((x2,y2),surface)

        l=pymunk.Segment(body,(x1,y1),(x2,y2),1)
        l.filter=pymunk.ShapeFilter(categories=2)
        space.add(l)
        print("i={} k={}".format(i,k))
    return body

def add_ball(space,x):
    global debault_color
    mass=10
    radius=14
    inetia = pymunk.moment_for_circle(mass,0,radius,(0,0))
    body = pymunk.Body(mass,inetia)
    #x = random.randint(120,380)
    body.position = x,350
    body.filter=pymunk.ShapeFilter(categories=1)
    #body.torque = 5000
    body.velocity=(0.0,-1)
    shape = pymunk.Circle(body,radius,(0,0))
    space.add(body,shape)
    return shape

def static_ball(space,b):
    def mk_static_body(b,x,y):
        static_body = pymunk.Body(body_type = pymunk.Body.STATIC)
        static_body.position = vec2d.Vec2d(x,y)
        l = static_body.position.get_distance(b.position) * 0.9
        damping=15
        stiffness=20
        j = pymunk.DampedSpring(static_body, b, (0,0), (0,0), l,stiffness,damping)
        space.add(j)
    x=b.position.x
    y=b.position.y-200
    mk_static_body(b,x,y)
    y2=b.position.y+200
    mk_static_body(b,x,y2)

    #static_body.position
    #j = pymunk.PivotJoint(static_body, b, static_body.position)


def add_joint(space,a,b):
    j3 = pymunk.constraint.PinJoint(a,b,(0,0),(0,0))
    #j3.collide_bodies=False
    #j3.max_force=1000
    space.add(j3)

class AnimateResize(object):
    def __init__(self,outr_init,inner_init,sz,space,mouse_pos):
        self.initx=outr_init[0]
        self.inity=outr_init[1]
        self.innerx=inner_init[0]
        self.innery=inner_init[1]
        self.sx=sz[0]
        self.sy=sz[1]
        self.velocity_x=(self.sx-self.initx)/10
        self.velocity_y=(self.sy-self.inity)/10
        self.scale=[1,2,3,4]
        self.is_finish=False
        diffx=(self.sx - self.innerx) / 2
        diffy=(self.sy - self.innery) /2
        self.diffp = (diffx,diffy)
        bd = space.point_query_nearest(mouse_pos, pymunk.inf, pymunk.ShapeFilter(mask=1))
        if bd:
            #self.default_color=bd.shape.color
            bd.shape.color=THECOLORS['pink']
            self.bd=bd

    def update(self):
        d=self.scale.pop()
        self.sx=self.sx - d*self.velocity_x
        self.sy=self.sy - d*self.velocity_y
        screen = pygame.display.set_mode((int(self.sx), int(self.sy)),RESIZABLE)
        screen2=screen.subsurface(Rect(0,0,int(self.innerx),int(self.innery)))
        draw_options = pymunk.pygame_util.DrawOptions(screen2)
        if not self.scale:
            self.is_finish=True
            self.bd.shape.color=pymunk.space_debug_draw_options.SpaceDebugColor(r=52, g=152, b=219, a=255)
            p=self.bd.shape.body.position
            self.bd.shape.body.position=(p.x + self.diffp[0],p.y+self.diffp[1])
        return (screen,screen2,draw_options)
    def start(self,event):
        screen = pygame.display.set_mode((event.w, event.h),RESIZABLE)
        screen2=screen.subsurface(Rect(0,0,int(self.innerx),int(self.innery)))
        draw_options = pymunk.pygame_util.DrawOptions(screen2)
        return (screen,screen2,draw_options)


class ImageDraw(object):
    def __init__(self,fname,point):
        print(fname)
        self.img = pygame.image.load(fname).convert()
        self.point=point
    def in_rect(self,point,surface):
        w=surface.get_width()
        h=surface.get_height()
        x=self.point[0] - point[0]
        y=point[1]
        if 0 < x < w:
            pt=pymunk.pygame_util.to_pygame((x,y),surface)
            surface.blit(self.img,pt)


def main():
    global point
    (screen,screen2,clock,space) = init()
    draw_options = pymunk.pygame_util.DrawOptions(screen2)
    add_ball(space,400)
    add_ball(space,350)
    add_ball(space,300)
    add_ball(space,250)
    add_ball(space,200)
    add_ball(space,150)
    add_ball(space,100)
    img_draws=[]
    fname=("images.bmp","kendo.bmp","propose2.bmp",\
        "wedding.bmp","rumia.bmp","smile.bmp",)*4
    for i,f in enumerate(fname):
        path="img/"+f
        x=(i+4)*1000
        y=50
        img_draws.append(ImageDraw(path,(x,y)))
    print(len(img_draws))
    bodies=space.bodies
    bodies=sorted(bodies,key=lambda x:x.position.x,reverse=True)
    for i,a in enumerate(bodies):
        if i+1<len(bodies):
            b=bodies[i+1]
            add_joint(space,a,b)
    running=True
    is_interactive = False
    constraints = space.constraints
    back_recouce=get_resource(space,screen2)
    camera_x=0
    verocity=2
    ar=None
    ch = space.add_collision_handler(0, 0)
    ch.data["surface"] = screen2
    ch.post_solve = draw_collision
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit(0)
            elif event.type ==  MOUSEBUTTONDOWN and not is_interactive:
                #is_interactive = True
                pass
            elif event.type == MOUSEBUTTONUP:
                is_interactive = False
            elif event.type == VIDEORESIZE:
                if not ar:
                    mouse_pos = pymunk.pygame_util.get_mouse_pos(screen)
                    ar=AnimateResize((610,610),(600,600),(event.w,event.h),space,mouse_pos)

                    #print(mouse_pos)
                    (screen,screen2,draw_options)=ar.start(event)
        if is_interactive:
            mouse_pos = pymunk.pygame_util.get_mouse_pos(screen)
            bd = space.point_query_nearest(mouse_pos, 10, pymunk.ShapeFilter())
            if bd:
                bd.shape.body.position=mouse_pos
        if ar and not ar.is_finish:
            (screen,screen2,draw_options)=ar.update()
        if ar and ar.is_finish:
            ar=None
        space.step(1/50.0)
        camera_x+=verocity

        screen.fill((255,255,255))
        screen2.fill((0,0,0))
        sl=space.shapes
        sl=[s for s in sl if isinstance(s,pymunk.shapes.Segment)]
        for s in sl:
            p0=(s.a[0]-verocity,s.a[1])
            p1=(s.b[0]-verocity,s.b[1])
            s.unsafe_set_endpoints(p0,p1)
        space.debug_draw(draw_options)
        if point:
            pt=pymunk.pygame_util.to_pygame(point,screen2)
            pygame.draw.circle(screen2, THECOLORS["red"], pt, 20, 0)
            point = None
        for i in img_draws:
            i.in_rect((camera_x,50),screen2)

        #p2=(600,600)
        #if p2:
        #    pt=pymunk.pygame_util.to_pygame(p2,screen2)
        #    pygame.draw.circle(screen2, THECOLORS["green"], pt, 20, 0)
        #    p2 = None

        pygame.display.flip()
        clock.tick(50)
        pygame.display.set_caption("幾何:fps: " + str(clock.get_fps()))


if __name__=='__main__':
    sys.exit(main())
