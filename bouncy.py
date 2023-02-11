#!/usr/bin/python3

from random import randrange,random

import pygame
from math import pi,sin,cos
from time import sleep
# Why didn't I pay attention in maths at schooooooollllll?
class ball:	
    def __init__(self,x,y,radius, ball_angle,ball_speed,screen_width,screen_height,ball_colour):
        self.ball_x = x
        self.ball_y = y
        self.ball_radius =radius
        self.ball_speed=ball_speed
        self.ball_angle = ball_angle        
        self.screen_width=screen_width
        self.screen_height=screen_height
        self.ball_colour = ball_colour
        self.bounces = 0
    def sinwv(self,t,frequency,offset,amp):
        return sin(frequency*t+offset)*(amp-1)+amp;
    def _bounce(self):
        self.bounces= self.bounces+1
        c = randrange(0,180)
        self.ball_colour=(
        self.sinwv(c,0.05,3,128),
        self.sinwv(c,0.05,1,128),
        self.sinwv(c,0.05,0,128)
        )
    def do_movement (self):
        self.ball_x += cos(self.ball_angle) * self.ball_speed;
        self.ball_y += sin(self.ball_angle) * self.ball_speed;
        if ( self.ball_x - self.ball_radius < 0 ):
            self.ball_x = self.ball_radius
            self.ball_angle = pi - self.ball_angle
            self._bounce()
        elif(self.ball_x + self.ball_radius > self.screen_width ):
             self.ball_x = self.screen_width - self.ball_radius
             self.ball_angle = pi - self.ball_angle
             self._bounce()
        if (self.ball_y < self.ball_radius ): 
             self.ball_y = self.ball_radius
             self.ball_angle = ( pi * 2 ) - self.ball_angle
             self._bounce()
        elif (self.ball_y + self.ball_radius > self.screen_height ):
             self.ball_y = self.screen_height - self.ball_radius
             self.ball_angle = ( pi * 2 ) - self.ball_angle
             self._bounce()
class bouncy:
    def __init__(self):
        pygame.init()
        self.width=800
        self.height=600
        self.size = [self.width,self.height]
        self.screen = pygame.display.set_mode(self.size)  
        pygame.display.set_caption("Bouncy")

        self.centreX = self.width/2
        self.centreY = self.height/2
               
        #coordinates for corners of cube in x,y,z relative to zero 
        self.balls = [
        #ball(self.width/3,self.height/3,40, 20,4,self.width,self.height,(255,0,100))
        ]
        self.numballs = 10
        for i in range(0,self.numballs):
        	self.spawnBall()
        	
        self.mainLoop()
    def spawnBall (self):

        x = randrange(100,self.width,1)
        y = randrange(100,self.height-100,1)
        ball_angle = randrange(0,180)
        radius =randrange(1,50,1)
        ball_speed = random()
        c = randrange(0,180)
        ball_colour=(
        self.sinwv(c,0.05,3,128),
        self.sinwv(c,0.05,1,128),
        self.sinwv(c,0.05,0,128)
        )
        self.balls.append(
        ball(x,y,radius, ball_angle,ball_speed,self.width,self.height,ball_colour)
        )
    def sinwv(self,t,frequency,offset,amp):
        return sin(frequency*t+offset)*(amp-1)+amp;
        
    def mainLoop(self):
        self.done = False
        while not self.done:
            self.captureEvents()
            self.screen.fill((0,0,0))
            #self.captureCollisions()
            self.drawBalls ()
            pygame.display.flip()
            sleep(0.01)
        pygame.quit()
   
    def drawBalls(self):
    	for i in range(0, self.numballs, 1):
            self.balls[i].do_movement()
            pygame.draw.circle(self.screen, self.balls[i].ball_colour, [self.balls[i].ball_x,self.balls[i].ball_y], self.balls[i].ball_radius)

    def captureEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                self.done=True     
                                  
if __name__ == "__main__":
    bcy =  bouncy()
