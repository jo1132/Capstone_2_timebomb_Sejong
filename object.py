from random import randint
import time

class Obj:
    tracks=[]
    def __init__(self,i,xi,yi,max_age):
        self.i=i
        self.x=xi
        self.y=yi
        self.tracks=[]
        self.done=False
        self.state='0'
        self.age=0
        self.max_age=max_age
        self.dir=None

    def getTracks(self):
        return self.tracks

    def getId(self): #For the ID
        return self.i

    def getState(self):
        return self.state

    def getDir(self):
        return self.dir

    def getX(self):  #for x coordinate
        return self.x

    def getY(self):  #for y coordinate
        return self.y

    def updateCoords(self, xn, yn):
        self.age = 0
        self.tracks.append([self.x, self.y])
        self.x = xn
        self.y = yn

    def setDone(self):
        self.done = True

    def timedOut(self):
        return self.done

    #line(left, right)
    def going_LEFT_IN(self, mid_start, mid_end):
        if len(self.tracks)>=2:
            if self.state=='0':
                if self.tracks[-1][0]>mid_start and self.tracks[-2][0]<=mid_start:
                    state='1'
                    self.dir='left_in'
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    
    def going_LEFT_OUT(self, mid_start, mid_end):
        if len(self.tracks)>=2:
            if self.state=='0':
                if self.tracks[-1][0]>mid_end and self.tracks[-2][0]<=mid_end:
                     state='1'
                     self.dir='left_out'
                     return True
                else:
                     return False
            else:
                return False
        else:
            return False        

    def going_RIGHT_IN(self,mid_start,mid_end):
        if len(self.tracks)>=2:
            if self.state=='0':
                if self.tracks[-1][0]<mid_end and self.tracks[-2][0]>=mid_end:
                    state='1'
                    self.dir='right_in'
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
            
    def going_RIGHT_OUT(self, mid_start, mid_end):
        if len(self.tracks)>=2:
            if self.state=='0':
                if self.tracks[-1][0]<mid_start and self.tracks[-2][0]>=mid_start:
                    state='1'
                    self.dir='right_out'
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def going_CAR_IN(self, mid_start, mid_end):
        if len(self.tracks)>=2:
            if self.state=='0':
                if self.tracks[-1][1]>=mid_start and self.tracks[-2][1]<mid_start:
                    state='1'
                    self.dir='in'
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def going_CAR_OUT(self, mid_start, mid_end):
        if len(self.tracks)>=2:
            if self.state=='0':
                if self.tracks[-1][1]>=mid_end and self.tracks[-2][1]<mid_end:
                    state='1'
                    self.dif='out'
                    return True
                else:
                    return False
            else:
                return False
                

    def going_invade_left(self, mid_start, mid_end):
        if len(self.tracks)>=2:
            if self.state=='0':
                if self.tracks[-1][0]<=mid_start and self.tracks[-2][0]>mid_start:
                    state='1'
                    self.dif='left'
                    return True
                else:
                    return False
            else:
                return False

    def going_invade_right(self, mid_start, mid_end):
        if len(self.tracks)>=2:
            if self.state=='0':
                if self.tracks[-1][0]>=mid_end and self.tracks[-2][0]<mid_end:
                    state='1'
                    self.dif='right'
                    return True
                else:
                    return False
            else:
                return False

    def age_one(self):
        self.age+=1
        if self.age>self.max_age:
            self.done=True
        return  True
    
#Class2

class MultiObj:
    def __init__(self,objs,xi,yi):
        self.objs=objs
        self.x=xi
        self.y=yi
        self.tracks=[]
        self.done=False
