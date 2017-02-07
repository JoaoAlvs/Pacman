import pygame
from random import*
from time import*
board_dimensions=[350,390]
pacman_length=20
wall_length=5
speed1=4
speed2=2
class Text:
    def __init__(self,x,y,size):
        self.x=x
        self.y=y
        self.size=size
 
    def update(self,screen,text):
        cover=pygame.Surface([len(text)*self.size//2.1,self.size*0.7])
        cover.fill([0,0,30])
        screen.blit(cover,(self.x,self.y))
        myscore=pygame.font.Font(None,self.size)
        label=myscore.render(text,True,(255,255,255))
        textrect=(self.x,self.y)            
        screen.blit(label,textrect)
class Button(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.Surface([10,10])
        self.image.fill([255,255,255])
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
class Ghost(pygame.sprite.Sprite):
    def __init__(self,x,y,color):
        super().__init__()
        self.color=color
        self.image=pygame.Surface([pacman_length,pacman_length])
        self.image.fill(color)
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.direction=[0,speed1]
        self.moves=[False,True,True,False]
        self.edible=False
        self.wait=False
        self.waitcount=0
        self.speed=speed1
    def move(self,level):
        if self.wait:
            self.waitcount+=1
            if self.waitcount==30*3:
                self.rect.x=wall_length+8*pacman_length
                self.rect.y=wall_length+6*pacman_length
                self.wait=False
                self.change_color(self.color)
                self.edible=False
        else:
            if self.edible:
                if max(abs(self.direction[0]),abs(self.direction[1]))==speed1 and (self.rect.x-wall_length)%pacman_length==0 and (self.rect.y-wall_length)%pacman_length==0:
                    self.direction[0]=self.direction[0]*speed2/speed1
                    self.direction[1]=self.direction[1]*speed2/speed1
            else:
                if max(abs(self.direction[0]),abs(self.direction[1]))==speed2 and (self.rect.x-wall_length)%pacman_length==0 and (self.rect.y-wall_length)%pacman_length==0:
                    self.direction[0]=self.direction[0]*speed1/speed2
                    self.direction[1]=self.direction[1]*speed1/speed2
            if (self.rect.x-wall_length)%pacman_length==0 and (self.rect.y-wall_length)%pacman_length==0:
                choices=[]
                self.rect.x+=self.direction[0]
                self.rect.y+=self.direction[1]
                hitlist=pygame.sprite.spritecollide(self,level.wall_list,False)
                if not hitlist:
                    choices.append([self.direction[0],self.direction[1]]*2)
                self.rect.x-=self.direction[0]
                self.rect.y-=self.direction[1]
                self.rect.x+=self.direction[1]
                self.rect.y+=self.direction[0]
                hitlist=pygame.sprite.spritecollide(self,level.wall_list,False)
                if not hitlist:
                    choices.append([self.direction[1],self.direction[0]]*2)
                self.rect.x-=self.direction[1]
                self.rect.y-=self.direction[0]
                self.rect.x-=self.direction[1]
                self.rect.y-=self.direction[0]
                hitlist=pygame.sprite.spritecollide(self,level.wall_list,False)
                if not hitlist:
                    choices.append([-self.direction[1],-self.direction[0]]*2)
                self.rect.x+=self.direction[1]
                self.rect.y+=self.direction[0]
                a=randrange(0,len(choices))
                self.rect.x+=choices[a][0]
                self.rect.y+=choices[a][1]
                self.direction=[choices[a][0],choices[a][1]]
            else:
                self.rect.x+=self.direction[0]
                self.rect.y+=self.direction[1]
            if self.rect.x>board_dimensions[0]:
                self.rect.x=0-pacman_length+wall_length
            elif self.rect.x<0-pacman_length:
                self.rect.x=board_dimensions[0]-wall_length
    def change_color(self,color):
        self.image.fill(color)
                    
class Food(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.Surface([5,5])
        self.image.fill([255,255,255])
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
class Wall(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height):
        super().__init__() 
        self.image=pygame.Surface([width,height])
        self.image.fill([0,0,125])
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
class Level:
    def __init__(self):
        buttons=[Button(wall_length+pacman_length/2-5,wall_length+1.5*pacman_length-5),Button(wall_length+16.5*pacman_length-5,wall_length+1.5*pacman_length-5),Button(wall_length+pacman_length/2-5,wall_length+17.5*pacman_length-5),Button(wall_length+16.5*pacman_length-5,wall_length+17.5*pacman_length-5)]
        self.button_list=pygame.sprite.Group()
        for i in buttons:
            self.button_list.add(i)
        ghosts=[Ghost(wall_length+8*pacman_length,wall_length+6*pacman_length,[255,0,0]),Ghost(wall_length+8*pacman_length,wall_length+6*pacman_length,[0,255,0]),Ghost(wall_length+8*pacman_length,wall_length+6*pacman_length,[0,255,255]),Ghost(wall_length+8*pacman_length,wall_length+6*pacman_length,[125,0,125])]
        self.ghost_list=pygame.sprite.Group()
        for i in ghosts:
            self.ghost_list.add(i)
        food=[[wall_length+pacman_length/2-2.5+pacman_length*(i%17),wall_length+pacman_length/2-2.5+(i//17)*pacman_length] for i in range(17*19)]
        remove=[[1,1],[3,1],[4,1],[6,1],[7,1],[8,1],[9,1],[10,1],[12,1],[13,1],[15,1],[1,2],[6,2],[10,2],[15,2],[1,3],[2,3],[4,3],[6,3],[10,3],[12,3],[14,3],[15,3],[8,3],[4,4],[8,4],[12,4],[0,5],[2,5],[3,5],[4,5],[5,5],[6,5],[8,5],[10,5],[11,5],[12,5],[13,5],[14,5],[16,5],[0,6],[4,6],[12,6],[16,6],[2,7],[4,7],[12,7],[14,7],[0,8],[1,8],[2,8],[14,8],[15,8],[16,8],[2,9],[4,9],[12,9],[14,9],[0,10],[4,10],[12,10],[16,10],[0,11],[2,11],[4,11],[5,11],[6,11],[8,11],[10,11],[11,11],[12,11],[14,11],[16,11],[0,12],[2,12],[8,12],[14,12],[16,12],[0,13],[2,13],[3,13],[4,13],[6,13],[8,13],[10,13],[12,13],[13,13],[14,13],[16,13],[6,14],[10,14],[1,15],[2,15],[4,15],[6,15],[7,15],[8,15],[9,15],[10,15],[12,15],[14,15],[15,15],[1,16],[4,16],[12,16],[15,16],[1,17],[3,17],[4,17],[5,17],[6,17],[8,17],[10,17],[11,17],[12,17],[13,17],[15,17],[8,18],[6,9],[7,9],[8,9],[9,9],[10,9],[6,8],[7,8],[8,8],[9,8],[10,8],[6,7],[7,7],[8,7],[9,7],[10,7],[0,1],[16,1]]
        for i in remove:
            food[i[0]+17*i[1]]=1
        self.food_list=pygame.sprite.Group()        
        for i in food:
            if i!=1:
                item=Food(i[0],i[1])
                self.food_list.add(item)
        walls=[[wall_length+6*pacman_length,wall_length+7*pacman_length,5*pacman_length,wall_length],[wall_length+6*pacman_length,wall_length+7*pacman_length,wall_length,3*pacman_length],[11*pacman_length,wall_length+7*pacman_length,wall_length,3*pacman_length],[wall_length+6*pacman_length,wall_length+10*pacman_length-wall_length,5*pacman_length,wall_length],[0,0,board_dimensions[0],5],[0,0,5,2*wall_length+5*pacman_length],[0,wall_length+5*pacman_length,wall_length+pacman_length,wall_length],[pacman_length,wall_length+5*pacman_length,wall_length,2*pacman_length],[0,7*pacman_length,pacman_length+wall_length,wall_length],[0,board_dimensions[1]-5,board_dimensions[0],5],[board_dimensions[0]-5,0,5,2*wall_length+5*pacman_length],[board_dimensions[0]-wall_length-pacman_length,wall_length+5*pacman_length,wall_length+pacman_length,wall_length],[board_dimensions[0]-pacman_length-wall_length,wall_length+5*pacman_length,wall_length,2*pacman_length],[board_dimensions[0]-pacman_length-wall_length,7*pacman_length,pacman_length+wall_length,wall_length],[board_dimensions[0]-pacman_length-wall_length,wall_length+10*pacman_length,wall_length,4*pacman_length],[board_dimensions[0]-pacman_length-wall_length,14*pacman_length,pacman_length+wall_length,wall_length],[board_dimensions[0]-pacman_length-wall_length,10*pacman_length+wall_length,pacman_length+wall_length,wall_length],[0,wall_length+10*pacman_length,wall_length+pacman_length,wall_length],[pacman_length,wall_length+10*pacman_length,wall_length,4*pacman_length],[0,14*pacman_length,pacman_length+wall_length,wall_length],[0,14*pacman_length,wall_length,5*pacman_length+wall_length],[board_dimensions[0]-wall_length,14*pacman_length,wall_length,5*pacman_length+wall_length]]
        self.wall_list=pygame.sprite.Group()
        innerWalls=[[wall_length+pacman_length,wall_length+pacman_length,pacman_length,3*pacman_length],[wall_length+3*pacman_length,wall_length+pacman_length,2*pacman_length,pacman_length],[wall_length+6*pacman_length,wall_length+pacman_length,5*pacman_length,pacman_length],[wall_length+12*pacman_length,wall_length+pacman_length,2*pacman_length,pacman_length],[wall_length+15*pacman_length,wall_length+pacman_length,pacman_length,3*pacman_length],[wall_length+pacman_length,wall_length+3*pacman_length,2*pacman_length,pacman_length],[wall_length+6*pacman_length,wall_length+pacman_length,pacman_length,3*pacman_length],[wall_length+10*pacman_length,wall_length+pacman_length,pacman_length,3*pacman_length],[wall_length+8*pacman_length,wall_length+3*pacman_length,pacman_length,3*pacman_length],[wall_length+4*pacman_length,wall_length+3*pacman_length,pacman_length,5*pacman_length],[wall_length+12*pacman_length,wall_length+3*pacman_length,pacman_length,5*pacman_length],[wall_length+14*pacman_length,wall_length+3*pacman_length,2*pacman_length,pacman_length],[wall_length+2*pacman_length,wall_length+5*pacman_length,5*pacman_length,pacman_length],[wall_length+10*pacman_length,wall_length+5*pacman_length,5*pacman_length,pacman_length],[0,wall_length+8*pacman_length,wall_length+3*pacman_length,pacman_length],[wall_length+14*pacman_length,wall_length+8*pacman_length,wall_length+3*pacman_length,pacman_length],[wall_length+2*pacman_length,wall_length+7*pacman_length,pacman_length,3*pacman_length],[wall_length+14*pacman_length,wall_length+7*pacman_length,pacman_length,3*pacman_length],[wall_length+4*pacman_length,wall_length+9*pacman_length,pacman_length,3*pacman_length],[wall_length+12*pacman_length,wall_length+9*pacman_length,pacman_length,3*pacman_length],[wall_length+4*pacman_length,wall_length+11*pacman_length,3*pacman_length,pacman_length],[wall_length+10*pacman_length,wall_length+11*pacman_length,3*pacman_length,pacman_length],[wall_length+8*pacman_length,wall_length+11*pacman_length,pacman_length,3*pacman_length],[wall_length+2*pacman_length,wall_length+11*pacman_length,pacman_length,2*pacman_length],[wall_length+14*pacman_length,wall_length+11*pacman_length,pacman_length,2*pacman_length],[wall_length+2*pacman_length,wall_length+13*pacman_length,3*pacman_length,pacman_length],[wall_length+12*pacman_length,wall_length+13*pacman_length,3*pacman_length,pacman_length],[wall_length+10*pacman_length,wall_length+13*pacman_length,pacman_length,3*pacman_length],[wall_length+6*pacman_length,wall_length+13*pacman_length,pacman_length,3*pacman_length],[wall_length+6*pacman_length,wall_length+15*pacman_length,5*pacman_length,pacman_length],[wall_length+8*pacman_length,wall_length+17*pacman_length,pacman_length,2*pacman_length],[wall_length+3*pacman_length,wall_length+17*pacman_length,4*pacman_length,pacman_length],[wall_length+10*pacman_length,wall_length+17*pacman_length,4*pacman_length,pacman_length],[wall_length+4*pacman_length,wall_length+15*pacman_length,pacman_length,3*pacman_length],[wall_length+12*pacman_length,wall_length+15*pacman_length,pacman_length,3*pacman_length],[wall_length+pacman_length,wall_length+15*pacman_length,2*pacman_length,pacman_length],[wall_length+14*pacman_length,wall_length+15*pacman_length,2*pacman_length,pacman_length],[wall_length+pacman_length,wall_length+15*pacman_length,pacman_length,3*pacman_length],[wall_length+15*pacman_length,wall_length+15*pacman_length,pacman_length,3*pacman_length]]
        for i in walls:
            wall=Wall(i[0],i[1],i[2],i[3])
            self.wall_list.add(wall)
        for i in innerWalls:
            wall=Wall(i[0],i[1],i[2],i[3])
            self.wall_list.add(wall)
        
class PacMan(pygame.sprite.Sprite):
    def __init__(self,x,y,radius):
        super().__init__()
        self.image=pygame.Surface([radius,radius])
        self.image.fill([250,250,0])
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.queue=[-speed1,0]
        self.direction=[-speed1,0]
    def change_direction(self,x,y):
        self.queue=[x,y]
    def move(self,level):
        self.rect.x+=self.queue[0]
        self.rect.y+=self.queue[1]
        hitlist=pygame.sprite.spritecollide(self,level.wall_list,False)
        if hitlist:
            self.rect.x-=self.queue[0]
            self.rect.y-=self.queue[1]
            self.rect.x+=self.direction[0]
            self.rect.y+=self.direction[1]
            seclist=pygame.sprite.spritecollide(self,level.wall_list,False)
            if seclist:
                self.rect.x-=self.direction[0]
                self.rect.y-=self.direction[1]
        else:
            self.direction[0]=self.queue[0]
            self.direction[1]=self.queue[1]


                
        if self.rect.x<-pacman_length:
            self.rect.x=board_dimensions[0]-wall_length
            self.rect.y=self.rect.y
        if self.rect.x>board_dimensions[0]:
            self.rect.x=wall_length
            
def main():
    pygame.init()
    screen=pygame.display.set_mode([board_dimensions[0],board_dimensions[1]+70])
    pygame.display.set_caption("Pacman")
    player=PacMan(wall_length+8*pacman_length,wall_length+14*pacman_length,pacman_length)
    moving_players=pygame.sprite.Group()
    moving_players.add(player)
    clock=pygame.time.Clock()
    score_count=Text(50,410,15)
    score_label=Text(10,410,15)
    board=Level()
    score_value=0
    ghost_value=200
    for i in range(3):
        done=False
        edible=False
        count=0
        while not done:
            count+=1
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    return
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_LEFT:
                        player.change_direction(-4,0)
                    elif event.key==pygame.K_RIGHT:
                        player.change_direction(4,0)
                    elif event.key==pygame.K_DOWN:
                        player.change_direction(0,4)
                    elif event.key==pygame.K_UP:
                        player.change_direction(0,-4)
                    elif event.key==pygame.K_SPACE:
                        unpause=False
                        while not unpause:
                            for event in pygame.event.get():
                                if event.type==pygame.KEYDOWN:
                                    if event.key==pygame.K_SPACE:
                                        unpause=True
            for i in board.ghost_list:
                i.move(board)
            player.move(board)
            screen.fill([0,0,30])
            score_label.update(screen,"Score: ")
            score_count.update(screen,str(score_value))
            board.button_list.draw(screen)
            board.wall_list.draw(screen)
            board.food_list.draw(screen)
            board.ghost_list.draw(screen)
            moving_players.draw(screen)
            foodlist=pygame.sprite.spritecollide(player,board.food_list,False)
            if edible:
                if count==30*6:
                    ghost_value=200
                    edible=False
                    for i in board.ghost_list:
                        i.change_color(i.color)
                        i.edible=False
                elif count>30*3:
                    for i in board.ghost_list:
                        if i.edible:
                            if count%15==0 or count%15==1:
                                i.change_color([255,255,255])
                            elif count%15==2:
                                i.change_color([60,60,255])
            for i in foodlist:
                score_value+=10
                board.food_list.remove(i)
            buttonlist=pygame.sprite.spritecollide(player,board.button_list,False)
            if buttonlist:
                edible=True
                count=0
                for i in buttonlist:
                    board.button_list.remove(i)
                for i in board.ghost_list:
                    i.change_color([60,60,255])
                    i.edible=True
            ghostlist=pygame.sprite.spritecollide(player,board.ghost_list,False)
            if ghostlist:
                if ghostlist[0].edible:
                    score_value+=ghost_value
                    ghost_value*=2
                    ghostlist[0].waitcount=0
                    ghostlist[0].wait=True
                    ghostlist[0].rect.y=wall_length+8*pacman_length
                    ghostlist[0].rect.x=wall_length+8*pacman_length
                    ghostlist[0].change_color(ghostlist[0].color)
                    ghostlist[0].edible=False
                else:
                    done=True
            pygame.display.flip()
            clock.tick(30)
        player.rect.x=wall_length+8*pacman_length
        player.rect.y=wall_length+14*pacman_length
        for i in board.ghost_list:
            i.change_color(i.color)
            i.rect.x=wall_length+8*pacman_length
            i.rect.y=wall_length+6*pacman_length
        ghost_value=200
        clock.tick(1/3)
    pygame.quit()
                
main()