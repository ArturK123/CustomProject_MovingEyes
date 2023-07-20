def getMovingValues(startX, startY, endX, endY):
    movingValues = []

    try:
        steps_number = max( abs(endX-startX), abs(endY-startY) )

        stepx = float(endX-startX)/steps_number
        stepy = float(endY-startY)/steps_number

        for i in range(steps_number+1):
            movingValues.append([int(startX + stepx*i), int(startY + stepy*i)])
            #print(int(startX + stepx*i), int(startY + stepy*i))
    except:
        pass
    return movingValues