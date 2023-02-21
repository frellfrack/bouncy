#!/usr/bin/python3
import pygame
from random import randrange,random
from math import pi,sin,cos,dist,tan,atan2,sqrt,hypot
from time import sleep
from inspect import getmembers
from pprint import pprint
# Why didn't I pay attention in maths at schooooooollllll?
class ball:	
    def __init__(self,x,y,radius, angle,speed):
        self.x = x
        self.y = y
        self.initial_y = y
        self.prev_y = y        
        self.radius = radius
        self.speed = speed
        self.angle = angle  
        c = 128 * speed
        self.colour = (
        self.sinwv(c,0.05,3,128),
        self.sinwv(c,0.05,1,128),
        self.sinwv(c,0.05,0,128)
        )      
 
        self.bounces = 0
        self.doneCollision = False
    def sinwv(self,t,frequency,offset,amp):
        return sin(frequency*t+offset)*(amp-1)+amp;
    def _bounce(self):
        self.bounces= self.bounces+1
        c = 128 * self.speed
        self. colour=(
        self.sinwv(c,0.05,3,128),
        self.sinwv(c,0.05,1,128),
        self.sinwv(c,0.05,0,128)
        )


class ship:
    def __init__(self):
        self.nodesOrginal = [
        [0,0],
        [-50,50],
        [50,50],
        [0,0]
	]
        self.nodes = [
        [0,0],
        [-50,50],
        [50,50],
        [0,0]
	]
        self.heading = 90
        self.nodelen = 4
    def rotateNodes(self):
        for i in range(0,self.nodelen,1):
            self.nodes[i][0]=cos((self.nodesOrginal[i][0] * self.heading) * pi/180)
            self.nodes[i][1]=sin((self.nodesOrginal[i][1] * self.heading) * pi/180)
        
        
class bouncy:
    def __init__(self):
        pygame.init()
        self.width=800
        self.height=600
        self.size = [self.width,self.height]
        self.screen = pygame.display.set_mode(self.size)  
        pygame.display.set_caption("Bouncy Bouncy Ooohh Such a Good Time")
        self.centreX = self.width/2
        self.centreY = self.height/2
        self.elasticity = 1
        #coordinates for corners of cube in x,y,z relative to zero 
        self.balls = [
        ]
        self.K_UP = False
        self.K_DOWN = False
        self.K_LEFT = False
        self.K_RIGHT = False

        self.numballs = 10
        for i in range(0,self.numballs,1):
        	self.balls.append(self.spawnBall())
        self.mainLoop()
    def spawnBall (self):
        x = randrange(100,self.width,1)
        y = randrange(100,self.height-100,1)
        angle = randrange(0,180)
        radius =randrange(5,40,1)
        speed = random()
        if (speed < 0.1):
             speed= 0.1
        
        
        return ball(x,y,radius, angle,speed)
        
    def sinwv(self,t,frequency,offset,amp):
        return sin(frequency*t+offset)*(amp-1)+amp;
        
    def mainLoop(self):
        self.done = False
        while not self.done:
            self.captureEvents()         
            self.do_movements ()
            self.screen.fill((0,0,0))
            self.drawBalls ()
            pygame.display.flip()
           # sleep(0.01)
        pygame.quit()

    def do_movements (self):
    
        for i in range(0, self.numballs, 1):
            self.do_movement(i)
            self.balls[i].doneCollision = False
            #if (self.balls[i].speed < 0.3):
            #    self.balls[i] = self.spawnBall ()           
        collisions  = self.detectCollisions()        
        self.doCollisions(collisions)

    def do_movement (self,i):
	# wall bounderies
        if (self.balls[i].x - self.balls[i].radius < 0 ):
             self.balls[i].x = self.balls[i].radius
             self.balls[i].speed = self.balls[i].speed * self.elasticity
             self.balls[i].angle = round(pi - self.balls[i].angle,2)
             self.balls[i]._bounce()
        elif(self.balls[i].x + self.balls[i].radius > self.width):
             self.balls[i].x = self.width - self.balls[i].radius
             self.balls[i].speed = self.balls[i].speed * self.elasticity
             self.balls[i].angle = round(pi - self.balls[i].angle,2)
             self.balls[i]._bounce()
        if (self.balls[i].y < self.balls[i].radius ): 
             self.balls[i].y = self.balls[i].radius
             self.balls[i].speed = self.balls[i].speed * self.elasticity
             self.balls[i].angle = round((pi * 2) - self.balls[i].angle,2)
             self.balls[i]._bounce()
        elif (self.balls[i].y + self.balls[i].radius > self.height ):
             self.balls[i].y = self.height - self.balls[i].radius
             self.balls[i].speed = self.balls[i].speed * self.elasticity
             self.balls[i].angle = round((pi * 2) - self.balls[i].angle,2)
             self.balls[i]._bounce()

        self.balls[i].x += cos(self.balls[i].angle) * self.balls[i].speed
        self.balls[i].y -= sin(self.balls[i].angle) * self.balls[i].speed

    def detectCollisions(self):
        collisions = []
        for ball1 in range(0,self.numballs,1):
    	    for ball2 in range(0,self.numballs,1):
    	    	if (ball1 != ball2):
                    dx = self.balls[ball1].x-self.balls[ball2].x
                    dy = self.balls[ball1].y-self.balls[ball2].y
                    distance = sqrt((dx * dx) + (dy * dy))
                    radsum = self.balls[ball1].radius+self.balls[ball2].radius
                    if (distance <= radsum and distance > radsum-1):
                          collisions.append([ball1,ball2])   
        return collisions
    def doCollisions(self,collisions):
        numCollisions = len(collisions)
        if (numCollisions>0):
             for i in range(0,numCollisions):
                 self.doCollision(collisions[i][0],collisions[i][1])

    def doCollision(self,ball1,ball2):
        dx = self.balls[ball1].x - self.balls[ball2].x
        dy = self.balls[ball1].y - self.balls[ball2].y
        dist = sqrt((dx * dx) + (dy * dy))
        radsum = self.balls[ball1].radius+self.balls[ball2].radius
        if (dist <= radsum):
            self.balls[ball1]._bounce()	    
            self.balls[ball2]._bounce()  
            tangent = atan2(dy, dx)
            angle = 0.5 * pi + tangent
            (self.balls[ball1].speed) = (self.balls[ball2].speed)
            angle1 =  2 * tangent - self.balls[ball1].angle
            angle2 =  2 * tangent - self.balls[ball2].angle
            speed1 = self.balls[ball2].speed * self.balls[ball1].speed * self.elasticity
            speed2 = self.balls[ball1].speed * self.balls[ball2].speed * self.elasticity
            if(self.balls[ball1].doneCollision == False):
                (self.balls[ball1].angle,self.balls[ball1].speed) = (angle1,speed1)
                self.balls[ball1].x += sin(angle)
                self.balls[ball1].y -= cos(angle)
                self.balls[ball1].doneCollision=True
            if(self.balls[ball2].doneCollision == False):
                (self.balls[ball2].angle,self.balls[ball1].speed) = (angle2,speed2)
                self.balls[ball2].x -= sin(angle)
                self.balls[ball2].y += cos(angle)
                self.balls[ball2].doneCollision=True
  
    def drawBalls(self):         
        for i in range(0,self.numballs,1):
            c = 128 * self.balls[i].speed
            self.balls[i].colour=(
            self.sinwv(c,0.05,3,128),
            self.sinwv(c,0.05,1,128),
            self.sinwv(c,0.05,0,128)
            )
            pygame.draw.circle(self.screen,self.balls[i].colour,[self.balls[i].x,self.balls[i].y],self.balls[i].radius)
                        
    def captureEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                self.done=True    
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_UP):
                    self.K_UP = True
                elif (event.key == pygame.K_DOWN):
                    self.K_DOWN = True
                elif (event.key == pygame.K_LEFT):
                    self.K_LEFT = True
                elif (event.key == pygame.K_RIGHT):
                    self.K_RIGHT = True
            elif event.type == pygame.KEYUP:
                if (event.key == pygame.K_UP):
                    self.K_UP = False
                elif (event.key == pygame.K_DOWN):
                    self.K_DOWN = False
                elif (event.key == pygame.K_LEFT):
                    self.K_LEFT = False
                elif (event.key == pygame.K_RIGHT):
                    self.K_RIGHT = False
                
                               

if __name__ == "__main__":
    bcy =  bouncy()
