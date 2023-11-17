# demo hp bar decreasing to 0 until no bars left

#####################################################################
############                                             ############
############                  DEFINE                     ############
############                                             ############
#####################################################################

style default:
    # overwrite default style
    outlines [(3,"#000000",0,0)]

style prog_style:
    # style for progress text
    size 24
    color "#FFFFFF"
    outlines [(3,"#000000",0,0)]

style lvl_style:
    # style for lvl text
    size 24
    color "#FFFFFF"
    outlines [(3,"#000000",0,0)]
    bold True

image hpTxt = ParameterizedText(style='prog_style')
image lvlTxt = ParameterizedText(style='lvl_style')

image barbg:
    "images/bar/barfill.png"

image black = "#000"


#####################################################################
############                                             ############
############               PYTHON INIT                   ############
############                                             ############
#####################################################################

init python:

    class Scene(object):
        """
        Represents a label for the scene to jump to
        """

        def __init__(self, lvl, label, title, points):
            self.lvl = lvl
            self.label = label
            self.title = title
            self.completed = False
            self.points = points

        def complete(self):
            # returns title with appended string if scene previously complete
            if not self.completed:
                self.completed = True
                self.title = "(Completed) " + self.title


    class MultiBar(object):
        """
        Simulate layered bar. Depletes like multiple health bars
        """

        def __init__(self):
            self.fill = 0
            # set this up through input, not hardcode
            self.barDescList = ["Lvl5","Lvl4","Lvl3","Lvl2","Lvl1"]    
            self.iLvl = 0
            # set this up through input, not hardcode
            self.iColour = ["#fa62ff","#63d8ff","#fdff6c","#70ff70","#ff6262","#b4b4b4"]
            self.choices = [[ ] for i in range(len(self.barDescList))]

        def getColour(self,add=0):
            # returns barfill colour associated with iLvl
            return self.iColour[self.iLvl+add]
        
        def getBarDesc(self):
            # return bar lvl description
            return self.barDescList[self.iLvl]


        def createSceneList(self):
            # return scenechoice list depending on iLvl and lvl
            global lvl
            listScenes = []
            iScenes = self.choices[self.iLvl]
            
            for i in range(len(iScenes)):
                tmpScene = iScenes[i]
                if tmpScene.lvl >= lvl:
                    listScenes.append((tmpScene.title,tmpScene))

            return listScenes

        def addScene(self, iBarLvl, lvl, label, title, points):
            # create scene object and add to choiceList
            newScene = Scene(lvl, label, title, points)
            self.choices[iBarLvl].append(newScene)

    def getBarFill(barWidth,iCent):
        # return fill x crop for bar
        return int(barWidth*0.01*(100-iCent))


    #####################################################################
    ############                                             ############
    ############        PYTHON: OBJECTS AND SCENES           ############
    ############                                             ############
    #####################################################################

    lvl = 100
    hpBar = MultiBar()
    barLvlTxt = hpBar.getBarDesc()


    # create Scene objects (barLvl, applicableHP, scenelist, label, title, amountDecreased)
    hpBar.addScene(0,100,"example1","Desc1",1)
    hpBar.addScene(0,99,"example2","Desc2",15)
    hpBar.addScene(0,84,"example3","Desc3",34)


#####################################################################
############                                             ############
############               TRANSFORMS                    ############
############                                             ############
#####################################################################

transform prog_bar(prog=0):
    # progress bar position
    crop (prog,0,500,50)
    xpos 0.85
    ypos 0.45 # 0.07 + 0.38
    xanchor 0.5
    yanchor 0.5

transform prog_bar_hi(prog=0):
    # progress bar position
    crop (prog,0,500,50)
    xpos 0.85
    ypos 0.07 # 0.07 + 0.38
    xanchor 0.5
    yanchor 0.5

transform bar_txt_mid:
    # lvl txt in bar
    xpos 0.85 ypos 0.45 xanchor 0.5 yanchor 0.5

transform lvl_txt_mid:
    xpos 0.85 ypos 0.41 xanchor 0.5 yanchor 0.5

transform bar_txt_hi:
    # lvl txt in bar
    xpos 0.85 ypos 0.07 xanchor 0.5 yanchor 0.5

transform lvl_txt_hi:
    xpos 0.85 ypos 0.03 xanchor 0.5 yanchor 0.5


#####################################################################
############                                             ############
############               SCREENS                       ############
############                                             ############
#####################################################################

# nothing yet
    

#####################################################################
############                                             ############
############            LABEL FUNCTIONS                  ############
############                                             ############
#####################################################################

label bar_display(bar_trans=prog_bar, lvl_txt=lvl_txt_mid, bar_txt=bar_txt_mid):
    # initialise bar display
    show barbg onlayer gameUI at bar_trans
    show barbg:
        matrixcolor TintMatrix(hpBar.getColour(1)) * OpacityMatrix(0.5)

    show barfill onlayer gameUI at bar_trans(hpBar.fill)
    show barfill:
        matrixcolor TintMatrix(hpBar.getColour())  
    show bar onlayer gameUI at bar_trans
    show lvlTxt '[barLvlTxt]' onlayer gameUI at lvl_txt
    show hpTxt '[lvl]' onlayer gameUI at bar_txt
    return



label bar_dissolve:
    # fade away display bar
    hide barbg
    hide barfill
    hide bar
    hide lvlTxt
    hide hpTxt
    with dissolve
    return


label decrease(amount,time):
    # decrease fill bar by 'amount' points for 'time' seconds
    # show barfill at dep(time)
    # can replace 500 for barWidth
    # consider 500 lvls
    $ lvl -= amount
    $ barLvlTxt = hpBar.getBarDesc()
    show lvlTxt '[barLvlTxt]'

    $ showLvl = lvl + amount
    $ showFill =  getBarFill(500,showLvl)
    # fill step going down 0.01 (1%) per time step 
    $ bFillStep = 5
    $ bTimeStep = time/amount 
    while showLvl >= lvl:
        show barfill:
            crop(showFill,0,500,50)
        $ showFill += bFillStep
        show hpTxt '[showLvl]'
        pause bTimeStep
        $ showLvl -= 1

    $ hpBar.fill = showFill
    return

label bar_fill_restore(add):
    # show bar fill as it would be before completed scene called.
    $ lvl += add
    $ barLvlTxt = hpBar.getBarDesc()
    $ hpBar.fill = getBarFill(500,lvl)
    
    show lvlTxt '[barLvlTxt]'
    show hpTxt '[lvl]'
    show barfill:
            crop(hpBar.fill,0,500,50)
    
    return



#####################################################################
############                                             ############
############               SCRIPT START                  ############
############                                             ############
#####################################################################

label start:
    pass

label selection:
    "Make your choice."

    call bar_display(prog_bar_hi, lvl_txt_hi, bar_txt_hi)
    # get choices based on hpBar lvl, choose scene
    $ cLs = hpBar.createSceneList()
    $ currScene = renpy.display_menu(cLs)
    $ currLabel = currScene.label

    if currScene.completed:
        call bar_fill_restore(currScene.points)
        "This scene has already been completed."

    call bar_dissolve
    call expression currLabel

    # note that scene completed for next choices
    $ currScene.complete()

    jump selection

label example1:
    scene black
    call bar_display
    call decrease(1,1)
    "example1"
    return

label example2:
    scene black
    call bar_display
    call decrease(15,2)
    "example2"
    return

label example3:
    scene black
    call bar_display
    call decrease(34,3)
    "example3"
    return

return

