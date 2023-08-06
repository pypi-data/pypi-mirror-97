#!/usr/bin/python3
# coding: utf-8

from tkinter import *
from tkinter.ttk import *

class enisebook():
    
    def __init__(self,**kwargs):
        # lecture des arguments
        self.__title   = kwargs.pop('title','Enise Book')
        self.__height  = kwargs.pop('height',200)
        self.__width   = kwargs.pop('width',300)
        self.__bgcolor = kwargs.pop('bgcolor','ivory')
        self.__fgcolor = kwargs.pop('fgcolor','black')
        self.__init    = kwargs.pop('init',lambda a:None)
        self.__click   = kwargs.pop('click',lambda a,b:None)
        self.__key     = kwargs.pop('key',lambda a,b:None)
        self.__action  = kwargs.pop('action',lambda a,b:None)
        self.__hover   = kwargs.pop('hover',lambda a,b:None)
        self.__close   = kwargs.pop('close',lambda book:book.end())
        self.__font    = kwargs.pop('font','TkFixedFont 12')
        self.__images  = []
        self.__links   = {}
        self.__items = []
        self.__startX  = kwargs.pop('startX',20) # position du premier caractère
        self.__startY  = kwargs.pop('startY',20)
        self.__y  = self.__startY
        self.__Ywd = 0 # position en Y du début de la fenetre de vue
        self.__step = kwargs.pop('step','10')
        
        
        
        # la fenêtre
        self.__root       = Tk()
        self.__root.title(self.__title)
        
        # Gestion du redimensionnement de l'application
        self.__root.columnconfigure(1, weight = 1)
        self.__root.rowconfigure(1, weight = 1)
        
        # Zone de texte (Canvas)
        self.__text = Canvas(self.__root,background=self.__bgcolor,width = self.__width , height = self.__height,yscrollincrement=self.__step)
        self.__text.grid(column=1,row=1,sticky=(N, S, E, W))
        
        self.__text.bind("<Button-1>", self.__clickManager)
        self.__text.bind("<MouseWheel>", self._on_mousewheel)
        
        
        # Frame pour la saisie et le bouton de validation
        # self.__frame = Frame(self.__root)
        # self.__frame.grid(column=1,row=2,sticky=(N, S, E, W))
        # self.__frame.columnconfigure(1,weight=1)
        # 
        # # Champ de saisie
        # self.__actionString = StringVar(self.__frame)
        # self.__entryBox = Entry(self.__frame,foreground="green",font = 'TkFixedFont 12',textvariable=self.__actionString)
        # self.__entryBox.grid(column=1,row=1,sticky=(N, S, E, W))
        # 
        # # Bouton de validation
        # self.__validateButton = Button(self.__frame, text='Valider', command=self.__actionManager)
        # self.__validateButton.grid(column=2,row=1)
        
        # Par défaut
        #self.disableAction()
        self.__text.focus()
            
        # Initiatilisation
        self.__init(self)
        
        # callback de KeyPress
        self.__root.bind(  '<KeyPress>', self.__keyManager)
        # callback de fermeture de la fenêtre
        self.__root.protocol("WM_DELETE_WINDOW", self.__bookclose)
        
        # boucle d'événements
        self.__root.mainloop()
    
    # def __setAction(self,etat):
    #     self.__validateButton.config(state=etat)
    #     self.__entryBox.config(state=etat)
    # 
    # def __actionManager(self):
    #     self.__action(self,{"action" : self.__actionString.get()})
    
    def __clickManager(self,event):
        try :
            a, = self.__text.find_closest(event.x,event.y+self.__Ywd)
        except ValueError :
            return
        if a in self.__links : self.__click(self,self.__links[a])

    def __keyManager(self,event):
        if event.keysym == "Up" :
            self.scrollText(-1)
        if event.keysym == "Down" :
            self.scrollText(1)
        self.__key(self,event)
    
    def __enterLink(self,event):
        self.__text.config(cursor="hand2")
    
    def __leaveLink(self,event):
        self.__text.config(cursor="")
    
    def __bookclose(self):
        self.__close(self)
          
    # def deleteAction(self):
    #     self.__actionString.set('')
    #       
    # def disableAction(self):
    #     self.__setAction(DISABLED)
    # 
    # def enableAction(self):
    #     self.__setAction(NORMAL)
    
    
    # Descend le curseur d'insertion d'un certain nombre de pixels
    def __moveCursor(self,delta):
        self.__y += delta
        d = self.__y - self.__Ywd - self.__height
        if  d > 0 :
            self.scrollText(d // int(self.__step)+3)
    
    # Réaction à l'évènement de scroll de souris
    def _on_mousewheel(self, event):
        self.scrollText(-1*(event.delta//60))
    
    # Efface tout le texte
    def clearText(self):
        listeObj = self.__text.find_all()
        for obj in listeObj :
            self.__text.delete(obj)
        self.__y = self.__startY
        self.__text.config(cursor="")
        self.scrollText(- self.__Ywd // int(self.__step))
    
    # Permet de scroller la fenêtre d'affichage vers le haut ou le bas
    # L'unité étant donné par self.__step)
    # Cette fonction ne fait rien si on est en haut du livre ou à la dernière ligne du texte
    def scrollText(self,n):
        if self.__Ywd <= 0 and n < 0 : return # haut du livre
        if self.__Ywd >= self.__y - int(self.__step) * 4 and n > 0 : return # bas du livre
        self.__text.yview_scroll(n,'units')
        self.__Ywd += int(self.__step) * n
    
    
    # Saut de ligne
    def newLine(self):
        self.addText(" ","emptyLine")
    
    # Ajoute du texte    
    def addText(self,texte,listeTags="Paragraphe"):
        if len(texte) == 0 : texte = ' '
        t = self.__text.create_text(self.__startX,self.__y,text=texte,anchor='nw',font=self.__font,tags=listeTags,width = self.__width-self.__startX,fill = self.__fgcolor)
        x1,y1,x2,y2 = self.__text.bbox(t)
     #   self.__text.create_rectangle(x1,y1,x2,y2,outline='red')
        self.__moveCursor(y2-y1)
        self.__items.append(t)
        return t
    
    # Ajoute une image 
    def addImage(self,fichier,align='center'):
        img = PhotoImage(file=fichier)
        if img not in self.__images : self.__images.append(img)
        self.newLine()
        i = self.__text.create_image(0,self.__y,anchor ='nw',image=img)
        x1,y1,x2,y2 = self.__text.bbox(i)
        if align != 'left':
            delta = (self.__width - (x2 - x1))
            if align == 'right'  : self.__text.move(i,delta,0)
            if align == 'center' : self.__text.move(i,delta//2,0) 
     #   self.__text.create_rectangle(x1,y1,x2,y2,outline='green')
        self.__moveCursor(y2-y1)
        self.__items.append(i)
        return i
    
    # Ajoute un lien
    def addLink(self,texte,code):
        c = self.addText(texte,'link')
        self.__text.itemconfigure(c,fill='blue')
        self.__links[c] =  {'texte' : texte,'code' : code}
        self.__text.tag_bind(c, "<Enter>", self.__enterLink)
        self.__text.tag_bind(c,"<Leave>", self.__leaveLink)
        self.__items.append(c)
        print(self.__links)
    
    # Efface un seul lien
    def __delLink(self,lk):
            x1,y1,x2,y2 = self.__text.bbox(lk)
            delta = y2 - y1
            self.__moveCursor(- delta)
            self.__text.delete(lk)
            # On remonte tous les autres items
            i = self.__items.index(lk)
            listItems = self.__items[i+1:]
            for item in listItems:
                self.__text.move(item,0,-delta) 
                
    # Efface tous les liens
    def delLinks(self):
        for c in self.__links :
            self.__delLink(c)
        self.__links.clear()
        self.__text.config(cursor="")
    
    # Affiche une ligne horizontale avec la taille en pourcentage de la largeur
    def addRule(self,percent):
        self.newLine()
        dx = int((self.__width * (1-percent))/2)
        r = self.__text.create_line(dx,self.__y,self.__width-dx,self.__y,tags="line",width = 1,fill = self.__fgcolor)
        x1,y1,x2,y2 = self.__text.bbox(r)
        self.__items.append(r)
        self.newLine()
        return r
    
    def end(self):
        self.__root.destroy()    

    