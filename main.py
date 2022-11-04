import pygame
import time
import math
import copy
from actors import *

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode([900, 900])

# Fonts
mainFont = pygame.font.SysFont('Agency FB', 25)
textFont = pygame.font.SysFont('Agency FB', 30)
titleFont = pygame.font.SysFont('Agency FB', 50)

# 1 = Main Menu, 2 = Transitional Text, 3 = Scavange, 4 = Prepare, 5 = Conflict, 6 = Game Over, 7 = Victory
gamePhase = 1

# Game Stats
night = 0
difficulty = 1  # 1: Easy, 2: Normal, 3: Hard, 4: Insane

# Player Stats
pHealth = 100
pMaxHealth = 100
pMeleeSpeed = 10
pMeleeDamage = 1
pMeleeRange = 8
pRangeDamage = 2
pRangeSpeed = 15
pRangeMultishot = 1

pAmmo = 20
pScrap = 0

# Text
textDelay = 0
text = ""
textLastingTime = 0

# Constants
playerConflictSpeed = 4
playerRangeDelay = 0
playerMeleeDelay = 0

# Conflict Phase
conflictPlayer = ConflictPlayer(0, 0, 0, 0, 0, 0, 0, 0, 0)
conflictManager = ConflictManager(0, 0)
barricadeHealth = 30

# Scavange Phase
scavangeManager = ScavangeManager(0, 0)
pAcidDamage = 50
scrapBoxes = []
dangerAnnouncement = False

# Transition Phase
nextDrop = 30
drops = []

# Display Variables
meleeLevel = 1
gunLevel = 1
mouseClicked = False

# Actors
enemies = []
enemyBullets = []
playerBullets = []
playerSlash = []

def calculateAngle(x1, y1, x2, y2):
    a = 0
    b = 300
    c = 0

    c = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    a = math.sqrt((x2 - x1) ** 2 + (y2 - (y1 + b)) ** 2)

    angle = (a ** 2) - (b ** 2) - (c ** 2)
    angle /= (2 * b * c)
    angle = math.degrees(math.acos(angle))

    return angle

def transition():
    global conflictPlayer
    global conflictManager

    global textDelay
    global text
    global textLastingTime

    global enemies
    global enemyBullets
    global playerBullets
    global playerSlash

    global scavangeManager
    global pAcidDamage
    global scrapBoxes

    global nextDrop
    global drops

    global night

    textLastingTime = 0
    
    if gamePhase == 1:
        pass
    elif gamePhase == 2:
        nextDrop = 5
        drops = []
        night += 1
    elif gamePhase == 3:
        drops = []
        enemies = []
        enemyBullets = []
        playerBullets = []
        playerSlash = []
        scrapBoxes = []
        conflictPlayer = ConflictPlayer(10, 410, pHealth, playerConflictSpeed, pMeleeSpeed, pMeleeDamage, pRangeDamage, pRangeSpeed, pRangeMultishot)
        
        scavangeManager = ScavangeManager(night, difficulty)
        pAcidDamage = 50

        if night == 10 or night == 16:
            scavangeManager.timeLeft = 120
    elif gamePhase == 4:
        pass
    elif gamePhase == 5:
        enemies = []
        enemyBullets = []
        playerBullets = []
        playerSlash = []
        
        conflictPlayer = ConflictPlayer(20, 410, pHealth, playerConflictSpeed, pMeleeSpeed, pMeleeDamage, pRangeDamage, pRangeSpeed, pRangeMultishot)
        conflictManager = ConflictManager(night, difficulty)
        conflictManager.setEnemies()
        textDelay = 80
        text = random.choice(["Warning. Enemy hostiles detected.", "Incoming hostiles.", "Enemy forces approaching."])
        textLastingTime = 150
    elif gamePhase == 6:
        nextDrop = 5
        drops = []
    elif gamePhase == 7:
        pass
    else:
        print("ERROR: Game phase" + str(gamePhase) + " not defined.")

def logic():
    global pMeleeSpeed
    global pRangeSpeed
    global pRangeDamage
    global playerRangeDelay
    global playerMeleeDelay
    global playerBullets
    global pRangeMultishot
    global playerSlash
    global enemies
    global pMeleeDamage
    global pMeleeRange
    
    global playerBullets
    global pAmmo
    global pHealth
    global pMaxHealth
    global pScrap
    global pAcidDamage

    global barricadeHealth
    global conflictPlayer
    global enemyBullets

    global meleeLevel
    global gunLevel

    global conflictManager
    global scavangeManager

    global textDelay
    global text
    global textLastingTime

    global mouseClicked

    global gamePhase
    global dangerAnnouncement

    global scrapBoxes

    global nextDrop
    global drops
    global gameRunning

    global difficulty
    
    if gamePhase == 1:
        nextDrop -= 1
        if nextDrop <= 0:
            nextDrop = random.choice(range(10, 40))
            drops.append([900, random.choice(range(0, 900)), (random.choice(range(50, 100))) / -50, (random.choice(range(-100, 100))) / 50, random.choice(range(5, 10))])
        for i in drops:
            i[0] += i[2]
            i[1] += i[3]
            if not (0 <= i[0] <= 1000 or 0 <= i[1] <= 1000):
                drops.remove(i)

        # Mouse Input
        left, middle, right = pygame.mouse.get_pressed()
        if left and not mouseClicked:
            mouseClicked = True
            mPosX, mPosY = pygame.mouse.get_pos()

            if (391 <= mPosX <= 508) and (343 <= mPosY <= 367):
                gamePhase = 2
                difficulty = 1
                transition()
            elif (382 <= mPosX <= 520) and (382 <= mPosY <= 403):
                gamePhase = 2
                difficulty = 2
                transition()
            elif (391 <= mPosX <= 514) and (417 <= mPosY <= 437):
                gamePhase = 2
                difficulty = 3
                transition()
            elif (364 <= mPosX <= 543) and (449 <= mPosY <= 474):
                gamePhase = 2
                difficulty = 4
                transition()
                
        elif not left:
            mouseClicked = False
    elif gamePhase == 2:  # Transitional phase
        nextDrop -= 1
        if nextDrop <= 0:
                nextDrop = random.choice(range(10, 40))
                drops.append([900, random.choice(range(0, 900)), (random.choice(range(50, 100))) / -50, (random.choice(range(-100, 100))) / 50, random.choice(range(5, 10))])
        for i in drops:
            i[0] += i[2]
            i[1] += i[3]
            if not (0 <= i[0] <= 1000 or 0 <= i[1] <= 1000):
                drops.remove(i)

        # Mouse Input
        left, middle, right = pygame.mouse.get_pressed()
        if left and not mouseClicked:
            mouseClicked = True
            mPosX, mPosY = pygame.mouse.get_pos()

            if (352 <= mPosX <= 541) and (796 <= mPosY <= 828):
                gamePhase = 3
                playerRangeDelay = 30
                transition()
                
        elif not left:
            mouseClicked = False
    elif gamePhase == 3:
        scavangeManager.update()
        if not dangerAnnouncement and scavangeManager.timeLeft <= 0:
            dangerAnnouncement = True
            textDelay = 20
            text = random.choice(["Storm incoming. It can't reach the safezone.", "Storm incoming. Delta Team back to base.", "The storm is arriving rapidly."])
            textLastingTime = 180
        elif scavangeManager.timeLeft > 0:
            dangerAnnouncement = False
        if scavangeManager.gracePeriod <= 0:
            if nextDrop <= 0:
                nextDrop = random.choice(range(1, 2))
                drops.append([900, random.choice(range(0, 900)), (random.choice(range(50, 100))) / -20, (random.choice(range(-100, 100))) / 20, random.choice(range(5, 10))])
            for i in drops:
                i[0] += i[2]
                i[1] += i[3]
                if (conflictPlayer.x <= i[0] <= conflictPlayer.x + 40) and (conflictPlayer.y <= i[1] <= conflictPlayer.y + 40):
                    pHealth -= 5 * difficulty
                    drops.remove(i)
                elif not (0 <= i[0] <= 1000 or 0 <= i[1] <= 1000):
                    drops.remove(i)
            nextDrop -= 1
        
        for bullet in playerBullets:
            bullet.update()
            for enemy in enemies:
                if (enemy.x <= bullet.x <= (enemy.x + enemy.size)) and (enemy.y <= bullet.y <= (enemy.y + enemy.size)):
                    try:
                        playerBullets.remove(bullet)
                        enemy.health -= pRangeDamage
                    except ValueError:
                        pass

        for slash in playerSlash:
            slash.update()
            for enemy in enemies:
                if (enemy.x <= slash.x <= (enemy.x + enemy.size)) and (enemy.y <= slash.y <= (enemy.y + enemy.size)):
                    try:
                        playerSlash.remove(slash)
                        enemy.health -= pRangeDamage
                    except ValueError:
                        pass

        for bullet in enemyBullets:
            bullet.update()
            if (conflictPlayer.x <= bullet.x <= conflictPlayer.x + 40) and (conflictPlayer.y <= bullet.y <= conflictPlayer.y + 40):
                pHealth -= bullet.damage
                enemyBullets.remove(bullet)
        
        for enemy in enemies:
            enemy.update(0, conflictPlayer.y + 20, conflictPlayer.x + 20, False)
            if ((enemy.x + (enemy.size / 2) >= conflictPlayer.x and enemy.x <= conflictPlayer.x + 40)) and (enemy.y + (enemy.size / 2) >= conflictPlayer.y and enemy.y <= conflictPlayer.y + 40):
                enemies.remove(enemy)
                pHealth -= enemy.damage
            elif enemy.firing:
                enemy.firing = False
                
                angle = calculateAngle(enemy.x + (enemy.size / 2), enemy.y + (enemy.size / 2), conflictPlayer.x + 20, conflictPlayer.y + 20)
                direction = 1
                if conflictPlayer.x + 20 < enemy.x + (enemy.size / 2):
                    direction = -1

                newEnemyBullet = EnemyBullet(enemy.x + (enemy.size / 2), enemy.y + (enemy.size / 2), enemy.bulletSpeed, angle, direction, enemy.damage)
                enemyBullets.append(newEnemyBullet)
                
                if enemy.specialID == 1:  # Shotgun behaviour
                    angle = calculateAngle(enemy.x + (enemy.size / 2), enemy.y + (enemy.size / 2), conflictPlayer.x + 20, conflictPlayer.y + 20) + 30
                    direction = 1
                    if conflictPlayer.x + 20 < enemy.x + (enemy.size / 2):
                        direction = -1
                    newEnemyBullet = EnemyBullet(enemy.x + (enemy.size / 2), enemy.y + (enemy.size / 2), enemy.bulletSpeed, angle, direction, enemy.damage)
                    enemyBullets.append(newEnemyBullet)
                    
                    angle = calculateAngle(enemy.x + (enemy.size / 2), enemy.y + (enemy.size / 2), conflictPlayer.x + 20, conflictPlayer.y + 20) - 30
                    direction = 1
                    if conflictPlayer.x + 20 < enemy.x + (enemy.size / 2):
                        direction = -1
                    newEnemyBullet = EnemyBullet(enemy.x + (enemy.size / 2), enemy.y + (enemy.size / 2), enemy.bulletSpeed, angle, direction, enemy.damage)
                    enemyBullets.append(newEnemyBullet)

        for box in scrapBoxes:
            if (box[0] <= conflictPlayer.x <= box[0] + 50 or box[0] <= conflictPlayer.x + 40 <= box[0] + 50 or box[0] <= conflictPlayer.x + 20 <= box[0] + 50) and (box[1] <= conflictPlayer.y <= box[1] + 30 or box[1] <= conflictPlayer.y + 20 <= box[1] + 30 or box[1] <= conflictPlayer.y + 40 <= box[1] + 30):
                pScrap += (int(random.choice(range(8, 15)) * (1 - (difficulty / 10))))
                scrapBoxes.remove(box)

        if pHealth <= 0:
            gamePhase = 6
            transition()
        
        # Keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            conflictPlayer.y -= playerConflictSpeed
            if conflictPlayer.y < 0:
                conflictPlayer.y = 0
        elif keys[pygame.K_s]:
            conflictPlayer.y += playerConflictSpeed
            if conflictPlayer.y > 860:
                conflictPlayer.y = 860

        if keys[pygame.K_a]:
            conflictPlayer.x -= playerConflictSpeed
            if conflictPlayer.x < -40:  # Load into preparation phase
                gamePhase = 4
                transition()
        elif keys[pygame.K_d]:
            conflictPlayer.x += playerConflictSpeed
            if conflictPlayer.x > 900:
                conflictPlayer.x = 0
                scrapBoxes = []
                enemyBullets = []
                enemies = []
                playerSlash = []
                playerBullets = []
                enemies, scrapBoxes = scavangeManager.generateArea(difficulty, night)
        
        playerRangeDelay -= 1
        playerMeleeDelay -= 1
        
        # Mouse input
        left, middle, right = pygame.mouse.get_pressed()
        if left:
            if pAmmo > 0 and playerRangeDelay <= 0:
                pAmmo -= 1
                calculatedAngle = 0
                mouseX, mouseY = pygame.mouse.get_pos()
                startX = conflictPlayer.x + 20
                startY = conflictPlayer.y + 20

                angle = calculateAngle(startX, startY, mouseX, mouseY)
                initialMultiplier = 0

                direction = 1
                if mouseX < conflictPlayer.x + 20:
                    direction = -1

                for i in range(0, pRangeMultishot):
                    if initialMultiplier == 0:
                        spawnedBullet = PlayerBullet(conflictPlayer.x + 20, conflictPlayer.y + 20, 15, angle, direction)
                        playerBullets.append(spawnedBullet)
                    else:
                        spawnedBullet = PlayerBullet(conflictPlayer.x + 20, conflictPlayer.y + 20, 15, angle + (15 * initialMultiplier), direction)
                        playerBullets.append(spawnedBullet)
                        spawnedBullet = PlayerBullet(conflictPlayer.x + 20, conflictPlayer.y + 20, 15, angle - (15 * initialMultiplier), direction)
                        playerBullets.append(spawnedBullet)
                    initialMultiplier += 1
                
                playerRangeDelay = pRangeSpeed
        elif right and playerMeleeDelay <= 0:
            calculatedAngle = 0
            mouseX, mouseY = pygame.mouse.get_pos()
            startX = conflictPlayer.x + 20
            startY = conflictPlayer.y + 20

            direction = 1
            if mouseX < conflictPlayer.x + 20:
                direction = -1
            
            angle = calculateAngle(startX, startY, mouseX, mouseY)

            spawnedSlash = PlayerSlash(conflictPlayer.x + 20, conflictPlayer.y + 20, 20, angle, pMeleeRange, direction)
            playerSlash.append(spawnedSlash)
            playerMeleeDelay = pMeleeSpeed
    elif gamePhase == 4:  # Preparation Phase
        # Mouse Input
        left, middle, right = pygame.mouse.get_pressed()
        if left and not mouseClicked:
            xPosStarts = [66, 74, 28, 461, 535, 548, 307, 382]
            xPosEnds = [432, 429, 465, 891, 810, 802, 588, 517]
            yPosStarts = [177, 357, 541, 178, 359, 537, 692, 857]
            yPosEnds = [213, 393, 573, 209, 388, 569, 717, 885]
            
            mouseClicked = True
            mPosX, mPosY = pygame.mouse.get_pos()

            for i in range(0, len(xPosStarts)):
                if (xPosStarts[i] <= mPosX <= xPosEnds[i]) and (yPosStarts[i] <= mPosY <= yPosEnds[i]):
                    if i == 0 and pScrap >= 15 and pHealth < pMaxHealth:  # Health upgrade
                        pScrap -= 15
                        pHealth += 20
                        if pHealth > pMaxHealth:
                            pHealth = pMaxHealth
                    elif i == 1 and pScrap >= 10:  # Ammo upgrade
                        pScrap -= 10
                        pAmmo += 5
                    elif i == 2 and pScrap >= 20:  # Barricade upgrade
                        pScrap -= 20
                        barricadeHealth += 10
                    elif i == 3 and pScrap >= int(40 + (25 * ((pMaxHealth - 100) / 20))):  # Max Health upgrade
                        pScrap -= int(40 + (25 * ((pMaxHealth - 100) / 20)))
                        pMaxHealth += 20
                        pHealth += 20
                    elif i == 4 and pScrap >= (55 + (meleeLevel * 25)) and meleeLevel < 5:  # Melee upgrade
                        pScrap -= (55 + (meleeLevel * 25))
                        meleeLevel += 1
                        pMeleeSpeed -= 1
                        pMeleeDamage += 1
                        pMeleeRange += 2
                    elif i == 5 and pScrap >= (65 + (gunLevel * 35)) and gunLevel < 5:  # Ranged upgrade
                        pScrap -= (65 + (gunLevel * 35))
                        pRangeDamage += 2
                        pRangeSpeed -= 2
                        gunLevel += 1
                    elif i == 6 and pScrap >= (120 + (pRangeMultishot * 90)) and pRangeMultishot < 3: # Multishot upgrade
                        pScrap -= (120 + (pRangeMultishot * 90))
                        pRangeMultishot += 1
                    elif i == 7:  # Begin night
                        gamePhase = 5
                        playerRangeDelay = 30
                        transition()
                    break
        elif not left:
            mouseClicked = False
    elif gamePhase == 5:  # Conflict Phase
        if pHealth <= 0:
            gamePhase = 6
            transition()
        
        for bullet in playerBullets:
            bullet.update()
            for enemy in enemies:
                if (enemy.x <= bullet.x <= (enemy.x + enemy.size)) and (enemy.y <= bullet.y <= (enemy.y + enemy.size)):
                    try:
                        playerBullets.remove(bullet)
                        enemy.health -= pRangeDamage
                    except ValueError:
                        pass

        for slash in playerSlash:
            slash.update()
            for enemy in enemies:
                if (enemy.x <= slash.x <= (enemy.x + enemy.size)) and (enemy.y <= slash.y <= (enemy.y + enemy.size)):
                    try:
                        playerSlash.remove(slash)
                        enemy.health -= pRangeDamage
                    except ValueError:
                        pass

        for enemy in enemies:
            if enemy.specialID == 2:  # Demon behaviour
                if enemy.x > 900:
                    enemy.x = random.choice(range(600, 800))
            
            enemy.update(barricadeHealth, conflictPlayer.y + 20, conflictPlayer.x + 20, True)
            if enemy.barricadeAttack:
                enemy.barricadeAttack = False
                barricadeHealth -= 1
            elif enemy.firing:
                enemy.firing = False
                
                angle = calculateAngle(enemy.x + (enemy.size / 2), enemy.y + (enemy.size / 2), conflictPlayer.x + 20, conflictPlayer.y + 20)
                direction = 1
                if conflictPlayer.x + 20 < enemy.x + (enemy.size / 2):
                    direction = -1

                newEnemyBullet = EnemyBullet(enemy.x + (enemy.size / 2), enemy.y + (enemy.size / 2), enemy.bulletSpeed, angle, direction, enemy.damage)
                enemyBullets.append(newEnemyBullet)
                
                if enemy.specialID == 1:  # Shotgun behaviour
                    angle = calculateAngle(enemy.x + (enemy.size / 2), enemy.y + (enemy.size / 2), conflictPlayer.x + 20, conflictPlayer.y + 20) + 30
                    direction = 1
                    if conflictPlayer.x + 20 < enemy.x + (enemy.size / 2):
                        direction = -1
                    newEnemyBullet = EnemyBullet(enemy.x + (enemy.size / 2), enemy.y + (enemy.size / 2), enemy.bulletSpeed, angle, direction, enemy.damage)
                    enemyBullets.append(newEnemyBullet)
                    
                    angle = calculateAngle(enemy.x + (enemy.size / 2), enemy.y + (enemy.size / 2), conflictPlayer.x + 20, conflictPlayer.y + 20) - 30
                    direction = 1
                    if conflictPlayer.x + 20 < enemy.x + (enemy.size / 2):
                        direction = -1
                    newEnemyBullet = EnemyBullet(enemy.x + (enemy.size / 2), enemy.y + (enemy.size / 2), enemy.bulletSpeed, angle, direction, enemy.damage)
                    enemyBullets.append(newEnemyBullet)
            
            if (enemy.x <= conflictPlayer.x + 40) and (enemy.y + (enemy.size / 2) >= conflictPlayer.y and enemy.y <= conflictPlayer.y + 40):
                enemies.remove(enemy)
                pHealth -= enemy.damage

        for bullet in enemyBullets:
            bullet.update()
            if (conflictPlayer.x <= bullet.x <= conflictPlayer.x + 40) and (conflictPlayer.y <= bullet.y <= conflictPlayer.y + 40):
                pHealth -= bullet.damage
                enemyBullets.remove(bullet)

        result = conflictManager.update()
        if result.x != 0:
            newEnemy = copy.deepcopy(result)
            newEnemy.y = random.choice(range(10, 850))
            newEnemy.damage = random.choice(range(newEnemy.minDamage, newEnemy.maxDamage))
            newEnemy.rangeLine += random.choice(range(-150, 150))
            enemies.append(newEnemy)

        if conflictManager.spawnedAll and conflictManager.hasBoss and len(enemies) <= 2:
            conflictManager.hasBoss = False
            newEnemy = copy.deepcopy(conflictManager.bossUnit)
            newEnemy.y = 410
            newEnemy.damage = random.choice(range(newEnemy.minDamage, newEnemy.maxDamage))
            enemies.append(newEnemy)
            textDelay = 0
            text = "Warning: Heavily armoured hostile approaching."
            textLastingTime = 150

        if len(enemies) <= 0 and not conflictManager.hasBoss and conflictManager.spawnedAll and not conflictManager.stormOver:
            textDelay = 0
            text = random.choice(["No hostiles detected.", "Wave cleared.", "Area secured."])
            textLastingTime = 150
            conflictManager.stormOver = True

        if conflictManager.stormOver and textLastingTime <= 0:
            if (difficulty == 1 and night >= 5) or (difficulty == 2 and night >= 10) or (difficulty == 3 and night >= 15) or (difficulty == 4 and night >= 16):
                gamePhase = 7
                transition()
            else:
                gamePhase = 2
                transition()
        
        playerRangeDelay -= 1
        playerMeleeDelay -= 1

        # Keyboard Input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            conflictPlayer.y -= playerConflictSpeed
            if conflictPlayer.y < 0:
                conflictPlayer.y = 0
        elif keys[pygame.K_s]:
            conflictPlayer.y += playerConflictSpeed
            if conflictPlayer.y > 860:
                conflictPlayer.y = 860

        # Mouse Input
        left, middle, right = pygame.mouse.get_pressed()
        if left:
            if pAmmo > 0 and playerRangeDelay <= 0:
                pAmmo -= 1
                calculatedAngle = 0
                mouseX, mouseY = pygame.mouse.get_pos()
                startX = conflictPlayer.x + 20
                startY = conflictPlayer.y + 20

                angle = calculateAngle(startX, startY, mouseX, mouseY)
                initialMultiplier = 0

                direction = 1
                if mouseX < conflictPlayer.x + 20:
                    direction = -1

                for i in range(0, pRangeMultishot):
                    if initialMultiplier == 0:
                        spawnedBullet = PlayerBullet(conflictPlayer.x + 20, conflictPlayer.y + 20, 15, angle, direction)
                        playerBullets.append(spawnedBullet)
                    else:
                        spawnedBullet = PlayerBullet(conflictPlayer.x + 20, conflictPlayer.y + 20, 15, angle + (15 * initialMultiplier), direction)
                        playerBullets.append(spawnedBullet)
                        spawnedBullet = PlayerBullet(conflictPlayer.x + 20, conflictPlayer.y + 20, 15, angle - (15 * initialMultiplier), direction)
                        playerBullets.append(spawnedBullet)
                    initialMultiplier += 1
                
                playerRangeDelay = pRangeSpeed
        elif right and playerMeleeDelay <= 0:
            calculatedAngle = 0
            mouseX, mouseY = pygame.mouse.get_pos()
            startX = conflictPlayer.x + 20
            startY = conflictPlayer.y + 20

            direction = 1
            if mouseX < conflictPlayer.x + 20:
                direction = -1

            angle = calculateAngle(startX, startY, mouseX, mouseY)

            spawnedSlash = PlayerSlash(conflictPlayer.x + 20, conflictPlayer.y + 20, 20, angle, pMeleeRange, direction)
            playerSlash.append(spawnedSlash)
            playerMeleeDelay = pMeleeSpeed
    elif gamePhase == 6:  # Game Over Screen
        nextDrop -= 1
        if nextDrop <= 0:
            nextDrop = random.choice(range(10, 40))
            drops.append([900, random.choice(range(0, 900)), (random.choice(range(50, 100))) / -50, (random.choice(range(-100, 100))) / 50, random.choice(range(5, 10))])
        for i in drops:
            i[0] += i[2]
            i[1] += i[3]
            if not (0 <= i[0] <= 1000 or 0 <= i[1] <= 1000):
                drops.remove(i)

        # Mouse Input
        left, middle, right = pygame.mouse.get_pressed()
        if left and not mouseClicked:
            mouseClicked = True
            mPosX, mPosY = pygame.mouse.get_pos()

            if (352 <= mPosX <= 541) and (796 <= mPosY <= 828):
                gameRunning = False
        elif not left:
            mouseClicked = False
    elif gamePhase == 7:
        nextDrop -= 1
        if nextDrop <= 0:
            nextDrop = random.choice(range(10, 40))
            drops.append([900, random.choice(range(0, 900)), (random.choice(range(50, 100))) / -50, (random.choice(range(-100, 100))) / 50, random.choice(range(5, 10))])
        for i in drops:
            i[0] += i[2]
            i[1] += i[3]
            if not (0 <= i[0] <= 1000 or 0 <= i[1] <= 1000):
                drops.remove(i)

        # Mouse Input
        left, middle, right = pygame.mouse.get_pressed()
        if left and not mouseClicked:
            mouseClicked = True
            mPosX, mPosY = pygame.mouse.get_pos()

            if (352 <= mPosX <= 541) and (796 <= mPosY <= 828):
                gameRunning = False
        elif not left:
            mouseClicked = False
    else:
        print("ERROR: Game phase" + str(gamePhase) + " not defined.")

def draw():
    global mainFont
    global pAmmo
    global pHealth
    global barricadeHealth
    global pMaxHealth
    global pRangeMultishot

    global playerBullets
    global playerSlash
    global enemies
    global enemyBullets

    global textDelay
    global text
    global textLastingTime

    global meleeLevel
    global gunLevel

    global pScrap
    global scrapBoxes
    global drops

    global scavangeManager
    
    if gamePhase == 1:
        screen.fill((20, 20, 20))
        for drop in drops:
            pygame.draw.circle(screen, (200, 200, 200), (int(drop[0]), int(drop[1])), drop[4])
        
        introText = titleFont.render("DECAYING WINTER", False, (255, 255, 255))
        screen.blit(introText, (450 - introText.get_rect().width / 2, 70))
        introText = textFont.render("The Winter awaits its next victim.", False, (255, 255, 255))
        screen.blit(introText, (450 - introText.get_rect().width / 2, 120))
        introText = textFont.render("Select difficulty:", False, (255, 255, 255))
        screen.blit(introText, (450 - introText.get_rect().width / 2, 300))
        introText = textFont.render("== Easy ==", False, (255, 255, 255))
        screen.blit(introText, (450 - introText.get_rect().width / 2, 335))
        introText = textFont.render("== Normal ==", False, (255, 255, 255))
        screen.blit(introText, (450 - introText.get_rect().width / 2, 370))
        introText = textFont.render("== Hard ==", False, (255, 255, 255))
        screen.blit(introText, (450 - introText.get_rect().width / 2, 405))
        introText = textFont.render("== Impossible ==", False, (255, 255, 255))
        screen.blit(introText, (450 - introText.get_rect().width / 2, 440))
    elif gamePhase == 2:  # Transitional Phase
        screen.fill((20, 20, 20))
        for drop in drops:
            pygame.draw.circle(screen, (200, 200, 200), (int(drop[0]), int(drop[1])), drop[4])

        if night == 1:
            introText = textFont.render("You have an empty base that needs resources.", False, (212, 127, 0))
            screen.blit(introText, (450 - introText.get_rect().width / 2, 100))
            introText = textFont.render("Collect brown boxes and harvest the scrap from them.", False, (212, 127, 0))
            screen.blit(introText, (450 - introText.get_rect().width / 2, 135))
            introText = textFont.render("Move to the right side of the screen to move to a new area.", False, (212, 127, 0))
            screen.blit(introText, (450 - introText.get_rect().width / 2, 170))
            introText = textFont.render("Move to the left side of the screen to return to base and use the scrap.", False, (212, 127, 0))
            screen.blit(introText, (450 - introText.get_rect().width / 2, 205))
            introText = textFont.render("Collect brown boxes and harvest the scrap from them.", False, (212, 127, 0))
            screen.blit(introText, (450 - introText.get_rect().width / 2, 240))
            introText = textFont.render("Be wary of the enemy that waits outside for you. They are the SCAVs.", False, (212, 127, 0))
            screen.blit(introText, (450 - introText.get_rect().width / 2, 275))

            introText = textFont.render("WASD: Move", False, (212, 127, 0))
            screen.blit(introText, (450 - introText.get_rect().width / 2, 345))
            introText = textFont.render("Left Mouse Button: Fire gun", False, (212, 127, 0))
            screen.blit(introText, (450 - introText.get_rect().width / 2, 380))
            introText = textFont.render("Right Mouse Button: Slash with melee", False, (212, 127, 0))
            screen.blit(introText, (450 - introText.get_rect().width / 2, 415))
            
            introText = textFont.render("Get back to base before the storm arrives and kills you.", False, (212, 127, 0))
            screen.blit(introText, (450 - introText.get_rect().width / 2, 485))
            introText = textFont.render("Once you return to base, you cannot go outside until the storm clears.", False, (212, 127, 0))
            screen.blit(introText, (450 - introText.get_rect().width / 2, 520))
        elif night == 5:
            introText = textFont.render("A high general of the enemy, the SCAVs, have been called in to destroy you.", False, (212, 127, 0))
            screen.blit(introText, (450 - introText.get_rect().width / 2, 100))
            introText = textFont.render("Her name is Sledge Queen, and she leads a band of highly-trained SCAV units.", False, (212, 127, 0))
            screen.blit(introText, (450 - introText.get_rect().width / 2, 135))
            introText = textFont.render("Expect a massive attack from her and her team this night.", False, (212, 127, 0))
            screen.blit(introText, (450 - introText.get_rect().width / 2, 170))
        elif night == 10:
            introText = textFont.render("The SCAVs have gathered a massive army outside, and something is brewing.", False, (212, 127, 0))
            screen.blit(introText, (450 - introText.get_rect().width / 2, 100))
            introText = textFont.render("They are preparing for the SCAV war. They're preparing to declare war.", False, (212, 127, 0))
            screen.blit(introText, (450 - introText.get_rect().width / 2, 135))
            introText = textFont.render("They're all preparing to delcare war on you as an individual.", False, (212, 127, 0))
            screen.blit(introText, (450 - introText.get_rect().width / 2, 170))
        elif night == 15:
            introText = textFont.render("The SCAVs numbers have begun to dwindle, and you are becoming strong.", False, (212, 127, 0))
            screen.blit(introText, (450 - introText.get_rect().width / 2, 100))
            introText = textFont.render("Their leader, Yosef, has prepared a final assault on your base.", False, (212, 127, 0))
            screen.blit(introText, (450 - introText.get_rect().width / 2, 135))
            introText = textFont.render("Prepare for the night. Upgrade your weapons. End Yosef's life.", False, (212, 127, 0))
            screen.blit(introText, (450 - introText.get_rect().width / 2, 170))
        elif night == 16:
            introText = textFont.render("So you think you're so good?", False, (212, 127, 0))
            screen.blit(introText, (450 - introText.get_rect().width / 2, 100))
            introText = textFont.render("Do you think Yosef was the hardest challenge in this game? Did you want a harder challenge?", False, (212, 127, 0))
            screen.blit(introText, (450 - introText.get_rect().width / 2, 135))
            introText = textFont.render("Maybe for others, but you are different. You wanted a challenge. You weren't satisfied before.", False, (212, 127, 0))
            screen.blit(introText, (450 - introText.get_rect().width / 2, 170))
            introText = textFont.render("So you know what?", False, (212, 127, 0))
            screen.blit(introText, (450 - introText.get_rect().width / 2, 205))
            introText = textFont.render("You win. Here's your challenge.", False, (212, 127, 0))
            screen.blit(introText, (450 - introText.get_rect().width / 2, 275))
            introText = textFont.render("Wave Ultima is beginning.", False, (212, 127, 0))
            screen.blit(introText, (450 - introText.get_rect().width / 2, 310))
        else:
            introText = textFont.render("The storm has cleared away.", False, (212, 127, 0))
            screen.blit(introText, (450 - introText.get_rect().width / 2, 100))
            introText = textFont.render("Delta Team move out. Search for supplies.", False, (212, 127, 0))
            screen.blit(introText, (450 - introText.get_rect().width / 2, 135))

        introText = textFont.render("> Begin next night <", False, (212, 127, 0))
        screen.blit(introText, (450 - introText.get_rect().width / 2, 800))
        introText = textFont.render("Current Night: " + str(night), False, (212, 127, 0))
        screen.blit(introText, (450 - introText.get_rect().width / 2, 835))
    elif gamePhase == 3:
        screen.fill((0, 0, 0))
        for drop in drops:
            pygame.draw.circle(screen, (200, 200, 200), (int(drop[0]), int(drop[1])), drop[4])

        for box in scrapBoxes:
            pygame.draw.rect(screen, (140, 45, 0),pygame.Rect(box[0], box[1], 50, 30))
        
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(conflictPlayer.x, conflictPlayer.y, 40, 40))
        for bullet in playerBullets:
            pygame.draw.circle(screen, (200, 200, 0), (int(bullet.x), int(bullet.y)), 10)
            if not bullet.isActive:
                playerBullets.remove(bullet)

        for bullet in enemyBullets:
            pygame.draw.circle(screen, (200, 0, 0), (int(bullet.x), int(bullet.y)), 10)
            if not bullet.isActive:
                enemyBullets.remove(bullet)

        for slash in playerSlash:
            if slash.isActive:
                pygame.draw.circle(screen, (60, 60, 60), (int(slash.x), int(slash.y)), 7)
            else:
                playerSlash.remove(slash)

        for enemy in enemies:
            if enemy.health > 0:
                pygame.draw.rect(screen, enemy.colour, pygame.Rect(enemy.x, enemy.y, enemy.size, enemy.size))
            else:
                enemies.remove(enemy)

        # Render Text
        ammoText = mainFont.render("Health: " + str(pHealth), False, (255, 255, 255))
        screen.blit(ammoText, (30, 10))
        ammoText = mainFont.render("Ammo: " + str(pAmmo), False, (255, 255, 255))
        screen.blit(ammoText, (30, 35))
        ammoText = mainFont.render("Scrap: " + str(pScrap), False, (255, 255, 255))
        screen.blit(ammoText, (30, 60))

        timeText = "ERROR"
        if scavangeManager.timeLeft > 0:
            if (math.floor(scavangeManager.timeLeft % 60)) < 10:
                timeText = str(math.floor(scavangeManager.timeLeft / 60)) + ":0" + str(math.floor(scavangeManager.timeLeft % 60))
            else:
                timeText = str(math.floor(scavangeManager.timeLeft / 60)) + ":" + str(math.floor(scavangeManager.timeLeft % 60))
        ammoText = mainFont.render("Time Left: " + timeText, False, (255, 255, 255))
        screen.blit(ammoText, (30, 870))
    elif gamePhase == 4:  # Preparation Phase
        screen.fill((40, 40, 40))
        mainText = textFont.render("Night " + str(night) + " - Peparation Phase", False, (255, 255, 255))
        screen.blit(mainText, (450 - mainText.get_rect().width / 2, 820))
        mainText = textFont.render("> Begin Night <", False, (255, 255, 255))
        screen.blit(mainText, (450 - mainText.get_rect().width / 2, 850))
        mainText = textFont.render("Scrap: " + str(pScrap), False, (255, 255, 255))
        screen.blit(mainText, (450 - mainText.get_rect().width / 2, 20))
        
        mainText = textFont.render("Current Health: " + str(pHealth) + "/" + str(pMaxHealth), False, (255, 255, 255))
        screen.blit(mainText, (250 - mainText.get_rect().width / 2, 140))
        mainText = textFont.render("> Craft Medkit (15 scrap --> 20 health) <", False, (255, 255, 255))
        screen.blit(mainText, (250 - mainText.get_rect().width / 2, 175))

        mainText = textFont.render("Ammo In Reserve: " + str(pAmmo), False, (255, 255, 255))
        screen.blit(mainText, (250 - mainText.get_rect().width / 2, 320))
        mainText = textFont.render("> Craft Ammo (10 scrap --> 5 bullets) <", False, (255, 255, 255))
        screen.blit(mainText, (250 - mainText.get_rect().width / 2, 355))

        mainText = textFont.render("Barricade Health: " + str(barricadeHealth), False, (255, 255, 255))
        screen.blit(mainText, (250 - mainText.get_rect().width / 2, 500))
        mainText = textFont.render("> Reinforce Barricade (20 scrap --> 10 health) <", False, (255, 255, 255))
        screen.blit(mainText, (250 - mainText.get_rect().width / 2, 535))

        mainText = textFont.render("Max Health: " + str(pMaxHealth), False, (255, 255, 255))
        screen.blit(mainText, (675 - mainText.get_rect().width / 2, 140))
        mainText = textFont.render("> Reinforce Armour (" + str(int(40 + (25 * ((pMaxHealth - 100) / 20)))) + " scrap --> +20 health) <", False, (255, 255, 255))
        screen.blit(mainText, (675 - mainText.get_rect().width / 2, 175))

        mainText = textFont.render("Melee: Level " + str(meleeLevel), False, (255, 255, 255))
        screen.blit(mainText, (675 - mainText.get_rect().width / 2, 320))
        if meleeLevel < 5:
            mainText = textFont.render("> Upgrade Melee (" + str(55 + (meleeLevel * 25)) + " scrap) <", False, (255, 255, 255))
            screen.blit(mainText, (675 - mainText.get_rect().width / 2, 355))

        mainText = textFont.render("Gun: Level " + str(gunLevel), False, (255, 255, 255))
        screen.blit(mainText, (675 - mainText.get_rect().width / 2, 500))
        if gunLevel < 5:
            mainText = textFont.render("> Upgrade Gun (" + str(65 + (gunLevel * 35)) + " scrap) <", False, (255, 255, 255))
            screen.blit(mainText, (675 - mainText.get_rect().width / 2, 535))

        mainText = textFont.render("Multishot: Level " + str(pRangeMultishot), False, (255, 255, 255))
        screen.blit(mainText, (450 - mainText.get_rect().width / 2, 650))
        if pRangeMultishot < 3:
            mainText = textFont.render("> Upgrade Barrel (" + str(120 + (pRangeMultishot * 90)) + " scrap) <", False, (255, 255, 255))
            screen.blit(mainText, (450 - mainText.get_rect().width / 2, 685))
    elif gamePhase == 5:  # Conflict Phase
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(conflictPlayer.x, conflictPlayer.y, 40, 40))

        if barricadeHealth > 0:
            pygame.draw.rect(screen, (70, 70, 70), pygame.Rect(100, 0, 20, 900))

        for bullet in playerBullets:
            pygame.draw.circle(screen, (200, 200, 0), (int(bullet.x), int(bullet.y)), 10)
            if not bullet.isActive:
                playerBullets.remove(bullet)

        for bullet in enemyBullets:
            pygame.draw.circle(screen, (200, 0, 0), (int(bullet.x), int(bullet.y)), 10)
            if not bullet.isActive:
                enemyBullets.remove(bullet)

        for slash in playerSlash:
            if slash.isActive:
                pygame.draw.circle(screen, (60, 60, 60), (int(slash.x), int(slash.y)), 7)
            else:
                playerSlash.remove(slash)

        for enemy in enemies:
            if enemy.health > 0:
                pygame.draw.rect(screen, enemy.colour, pygame.Rect(enemy.x, enemy.y, enemy.size, enemy.size))
            else:
                enemies.remove(enemy)

        # Render Text
        ammoText = mainFont.render("Health: " + str(pHealth), False, (255, 255, 255))
        screen.blit(ammoText, (30, 10))
        ammoText = mainFont.render("Ammo: " + str(pAmmo), False, (255, 255, 255))
        screen.blit(ammoText, (30, 35))
        ammoText = mainFont.render("Barricade Health: " + str(barricadeHealth), False, (255, 255, 255))
        screen.blit(ammoText, (30, 870))
        
    elif gamePhase == 6:
        screen.fill((20, 20, 20))
        for drop in drops:
            pygame.draw.circle(screen, (200, 200, 200), (int(drop[0]), int(drop[1])), drop[4])
        
        introText = textFont.render("You have fallen.", False, (212, 127, 0))
        screen.blit(introText, (450 - introText.get_rect().width / 2, 100))
        introText = textFont.render("The winter claims another soul.", False, (212, 127, 0))
        screen.blit(introText, (450 - introText.get_rect().width / 2, 135))

        introText = textFont.render("> Close Game <", False, (212, 127, 0))
        screen.blit(introText, (450 - introText.get_rect().width / 2, 800))
        introText = textFont.render("Final Night: " + str(night), False, (212, 127, 0))
        screen.blit(introText, (450 - introText.get_rect().width / 2, 835))
        
    elif gamePhase == 7:
        screen.fill((20, 20, 20))
        for drop in drops:
            pygame.draw.circle(screen, (200, 200, 200), (int(drop[0]), int(drop[1])), drop[4])
        
        introText = textFont.render("You have survived the harsh winter for " + str(night) + " nights.", False, (212, 127, 0))
        screen.blit(introText, (450 - introText.get_rect().width / 2, 100))
        if difficulty == 1:
            introText = textFont.render("Try a harder challenge next time.", False, (212, 127, 0))
            screen.blit(introText, (450 - introText.get_rect().width / 2, 135))
        elif difficulty == 2:
            introText = textFont.render("A mediocre score, but still not your best.", False, (212, 127, 0))
            screen.blit(introText, (450 - introText.get_rect().width / 2, 135))
        elif difficulty == 3:
            introText = textFont.render("A grand achievment. You have proven yourself to be a proud survivor.", False, (212, 127, 0))
            screen.blit(introText, (450 - introText.get_rect().width / 2, 135))
        else:
            introText = textFont.render("Congratulations. You are now a pro gamer.", False, (212, 127, 0))
            screen.blit(introText, (450 - introText.get_rect().width / 2, 135))

        introText = textFont.render("> Close Game <", False, (212, 127, 0))
        screen.blit(introText, (450 - introText.get_rect().width / 2, 800))
    else:
        print("ERROR: Game phase" + str(gamePhase) + " not defined.")

    # Draw text
    if textDelay <= 0 and textLastingTime > 0:
        dialougeText = textFont.render("Agent: " + text, False, (212, 127, 0))
        screen.blit(dialougeText, (450 - dialougeText.get_rect().width / 2, 850))
        textLastingTime -= 1
    else:
        textDelay -= 1

    pygame.display.flip()

transition()

gameRunning = True
while gameRunning:
    ev = pygame.event.get()
    
    logic()

    for event in ev:
        if event.type == pygame.QUIT:
            gameRunning = False

    draw()
    time.sleep(0.01)

pygame.quit()
