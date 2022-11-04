import math
import random
import copy

class ConflictPlayer:
    def __init__(self, x, y, health, speed, meleeSpeed, meleeDamage, rangeDamage, rangeSpeed, rangeMultishot):
        self.x = x
        self.y = y
        self.health = health
        self.speed = speed
        self.meleeSpeed = meleeSpeed
        self.meleeDamage = meleeDamage
        self.rangeDamage = rangeDamage
        self.rangeSpeed = rangeSpeed
        self.rangeMultishot = rangeMultishot

class PlayerBullet:
    def __init__(self, x, y, speed, angle, direction):
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle
        self.direction = direction
        self.isActive = True

    def update(self):
        # Movement
        self.x += math.sin(math.radians(self.angle)) * self.speed * self.direction
        self.y += (math.cos(math.radians(self.angle)) * self.speed) * -1
        if (self.x < 0 or self.x > 1000) or (self.y < 0 or self.y > 1000):
            self.isActive = False

class EnemyBullet:
    def __init__(self, x, y, speed, angle, direction, damage):
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle
        self.direction = direction
        self.isActive = True
        self.damage = damage

    def update(self):
        # Movement
        self.x += math.sin(math.radians(self.angle)) * self.speed * self.direction
        self.y += (math.cos(math.radians(self.angle)) * self.speed) * -1
        if (self.x < 0 or self.x > 1000) or (self.y < 0 or self.y > 1000):
            self.isActive = False

class PlayerSlash:
    def __init__(self, x, y, speed, angle, lifetime, direction):
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle
        self.lifetime = lifetime
        self.isActive = True
        self.direction = direction

    def update(self):
        # Movement
        self.x += math.sin(math.radians(self.angle)) * self.speed * self.direction
        self.y += (math.cos(math.radians(self.angle)) * self.speed) * -1

        self.lifetime -= 1
        if self.lifetime <= 0:
            self.isActive = False

# Special Enemies - 1: Shotgun
class ConflictEnemy:
    def __init__(self, x, y, health, colour, speed, isRanged, rangeLine, minDamage, maxDamage, bulletSpeed, highValueTarget, specialID, attackCooldown, ammo):
        self.x = x
        self.y = y
        self.health = health
        self.colour = colour
        self.speed = speed
        self.isRanged = isRanged
        self.rangeLine = rangeLine
        self.minDamage = minDamage
        self.maxDamage = maxDamage
        self.damage = random.choice(range(minDamage, maxDamage))
        self.bulletSpeed = bulletSpeed
        self.highValueTarget = highValueTarget
        self.specialID = specialID
        self.attackCooldown = attackCooldown
        self.ammo = ammo

        self.barricadeAttack = False
        self.firing = False
        self.nextAttack = 0

        self.size = 40

    def update(self, barricadeHP, playerY, playerX, conflictPhase):
        if conflictPhase:
            if (self.x <= 20 and not self.isRanged) or (self.x <= self.rangeLine and self.isRanged):  # Attack Behaviour
                if self.isRanged:  # Ranged Attack
                    if self.nextAttack <= 0:
                        self.firing = True
                        self.nextAttack = self.attackCooldown
                        self.ammo -= 1
                        if self.ammo <= 0:
                            self.isRanged = False
                    else:
                        self.nextAttack -= 1
                else:  # Melee Attack
                    if self.y < playerY - 20:
                        self.y += self.speed
                    else:
                        self.y -= self.speed
            elif (self.x <= 120 and barricadeHP > 0):  # Breakdown Behaviour
                if self.nextAttack <= 0:
                    self.barricadeAttack = True
                    self.nextAttack = self.attackCooldown
                else:
                    self.nextAttack -= 1
            else: # Movement Behaviour
                self.x -= self.speed
        else:
            if self.isRanged:  # Ranged behaviour
                if self.nextAttack <= 0:
                        self.firing = True
                        self.nextAttack = self.attackCooldown
                else:
                    self.nextAttack -= 1
            else:  # Melee Behaviour
                # y movement
                if playerY - 10 <= self.y <= playerY + 10:
                    pass
                elif self.y >= playerY - 10:
                    self.y -= self.speed
                elif self.y <= playerY:
                    self.y += self.speed

                # x movement
                if playerX - 10 <= self.x <= playerX + 10:
                    pass
                elif self.x >= playerX - 10:
                    self.x -= self.speed
                elif self.x <= playerX:
                    self.x += self.speed

class ConflictManager:
    def __init__(self, wave, difficulty):
        self.wave = wave
        self.difficulty = difficulty

        self.initialDelay = 250
        self.spawnSpeed = 100 - (2 * wave)
        if wave >= 16:
            self.spawnSpeed = 50
        if difficulty >= 3:
            self.spawnSpeed = self.spawnSpeed / 2
        self.nextSpawn = self.spawnSpeed + random.choice(range(-5, 10))
        self.incomingEnemies = []
        self.enemyCounts = []
        self.hasBoss = False
        self.bossUnit = ConflictEnemy(0, 0, 0, (0, 0, 0), 0, False, 0, 0, 5, 0, False, 0, 0, 0)
        self.spawnedAll = False
        self.stormOver = False

        # Enemy constants
        self.meleeInfantry = ConflictEnemy(1000, random.choice(range(10, 850)), 5, (255, 0, 0), 2, False, 0, 10, 20, 0, False, 0, 20, 0)
        self.rangedInfantry = ConflictEnemy(1000, random.choice(range(10, 850)), 4, (50, 0, 0), 2.5, True, 600, 4, 7, 7, False, 0, 40, 20)
        self.meleeSpeed = ConflictEnemy(1000, random.choice(range(10, 850)), 3, (200, 200, 200), 4.5, False, 0, 16, 21, 0, False, 0, 10, 0)
        self.rangedShotgun = ConflictEnemy(1000, random.choice(range(10, 850)), 9, (50, 0, 50), 1.5, True, 400, 5, 9, 7, False, 1, 100, 8)
        self.meleeHeavy = ConflictEnemy(1000, random.choice(range(10, 850)), 15, (100, 100, 100), 1.6, False, 0, 41, 62, 0, False, 0, 25, 0)
        self.rangedFighter = ConflictEnemy(1000, random.choice(range(10, 850)), 8, (255, 71, 71), 2.5, True, 500, 3, 6, 7, False, 0, 20, 50)
        self.demon = ConflictEnemy(1000, random.choice(range(10, 850)), 12, (100, 0, 0), 3, False, 500, 36, 46, 7, False, 2, 15, 15)
        
        # Bosses
        self.sledgeQueen = ConflictEnemy(1000, random.choice(range(10, 850)), 70, (144, 3, 252), 0.7, False, 0, 75, 80, 0, True, 0, 15, 0)
        self.scavGeneral = ConflictEnemy(1000, random.choice(range(10, 850)), 160, (60, 60, 60), 1.5, True, 500, 4, 6, 7, True, 0, 6, 500)
        self.yosef = ConflictEnemy(1000, random.choice(range(10, 850)), 250, (200, 200, 200), 1.5, True, 600, 3, 5, 8, True, 1, 6, 1200)
        self.shadow = ConflictEnemy(1000, random.choice(range(10, 850)), 600, (0, 150, 0), 1, False, 600, 3, 5, 8, True, 0, 10, 1200)
        
    def setEnemies(self):
        if self.wave == 1:
            self.incomingEnemies = [self.meleeInfantry]
            self.enemyCounts = [5]
        elif self.wave == 2:
            self.incomingEnemies = [self.meleeInfantry]
            self.enemyCounts = [9]
        elif self.wave == 3:
            self.incomingEnemies = [self.meleeInfantry, self.rangedInfantry]
            self.enemyCounts = [6, 1]
        elif self.wave == 4:
            self.incomingEnemies = [self.meleeInfantry, self.rangedInfantry]
            self.enemyCounts = [9, 4]
        elif self.wave == 5: # Sledge Queen's Team
            self.incomingEnemies = [self.meleeInfantry, self.rangedInfantry]
            self.enemyCounts = [12, 7]
            self.hasBoss = True
            self.bossUnit = self.sledgeQueen
        elif self.wave == 6:
            self.incomingEnemies = [self.meleeInfantry, self.rangedInfantry, self.meleeSpeed]
            self.enemyCounts = [13, 8, 5]
        elif self.wave == 7:
            self.incomingEnemies = [self.meleeInfantry, self.rangedInfantry, self.meleeSpeed]
            self.enemyCounts = [17, 11, 9]
        elif self.wave == 8:
            self.incomingEnemies = [self.meleeInfantry, self.rangedShotgun]
            self.enemyCounts = [24, 8]
        elif self.wave == 9:
            self.incomingEnemies = [self.meleeHeavy, self.rangedInfantry, self.rangedShotgun, self.meleeSpeed]
            self.enemyCounts = [7, 16, 10, 15]
        elif self.wave == 10: # SCAV war
            self.incomingEnemies = [self.meleeInfantry, self.rangedInfantry, self.meleeSpeed, self.rangedShotgun, self.meleeHeavy]
            self.enemyCounts = [30, 18, 16, 15, 9]
            self.hasBoss = True
            self.bossUnit = self.scavGeneral
        elif self.wave == 11:
            self.incomingEnemies = [self.meleeHeavy, self.rangedInfantry, self.meleeInfantry, self.rangedFighter]
            self.enemyCounts = [12, 20, 25, 11]
        elif self.wave == 12:
            self.incomingEnemies = [self.rangedShotgun, self.rangedFighter, self.meleeSpeed, self.meleeInfantry]
            self.enemyCounts = [18, 17, 24, 30]
        elif self.wave == 13:
            self.incomingEnemies = [self.demon, self.rangedInfantry, self.meleeHeavy]
            self.enemyCounts = [16, 26, 19]
        elif self.wave == 14:
            self.incomingEnemies = [self.meleeHeavy, self.demon, self.rangedShotgun, self.rangedFighter]
            self.enemyCounts = [20, 24, 20, 18]
        elif self.wave == 15: # Last Stand
            self.incomingEnemies = [self.meleeHeavy, self.meleeSpeed, self.rangedFighter, self.rangedShotgun]
            self.enemyCounts = [25, 30, 26, 25]
            self.hasBoss = True
            self.bossUnit = self.yosef
        else:  # Wave Ultima
            self.incomingEnemies = [self.meleeInfantry, self.rangedInfantry, self.meleeSpeed, self.meleeHeavy, self.rangedShotgun, self.rangedFighter, self.demon, self.sledgeQueen, self.scavGeneral, self.yosef]
            self.enemyCounts = [30, 30, 40, 35, 35, 40, 35, 3, 3, 2]
            self.hasBoss = True
            self.bossUnit = self.shadow

        if self.difficulty == 1:
            for i in range(0, len(self.enemyCounts)):
                self.enemyCounts[i] = int(math.floor(self.enemyCounts[i] / 2))
        elif self.difficulty == 4:
            for i in range(0, len(self.enemyCounts)):
                self.enemyCounts[i] = int(math.floor(self.enemyCounts[i] * 2))

    def update(self):
        if self.initialDelay <= 0:
            self.nextSpawn -= 1
        else:
            self.initialDelay -= 1
        
        if self.nextSpawn <= 0 and not self.spawnedAll:
            self.nextSpawn = self.spawnSpeed + random.choice(range(-10, 10))
            gotEnemy = False
            selectedEnemy = 0
            while not gotEnemy:
                selectedEnemy = self.incomingEnemies.index(random.choice(self.incomingEnemies))
                if self.enemyCounts[selectedEnemy] > 0:
                    gotEnemy = True

            self.enemyCounts[selectedEnemy] -= 1
            total = 0
            for i in self.enemyCounts:
                total += i
            if total <= 0:
                self.spawnedAll = True
            return self.incomingEnemies[selectedEnemy]
            
        else:
            return ConflictEnemy(0, 0, 0, (0, 0, 0), 0, False, 0, 0, 5, 0, False, 0, 0, 0)

class ScavangeManager:
    def __init__(self, wave, difficulty):
        self.wave = wave
        self.difficulty = difficulty
        self.timeLeft = random.choice(range(70, 90))
        self.gracePeriod = random.choice(range(1500, 2300))

        self.reduceTime = 100

        # Enemy constants
        self.meleeInfantry = ConflictEnemy(1000, random.choice(range(10, 850)), 5, (255, 0, 0), 2, False, 0, 10, 20, 0, False, 0, 20, 0)
        self.rangedInfantry = ConflictEnemy(1000, random.choice(range(10, 850)), 4, (50, 0, 0), 2.5, True, 600, 4, 7, 7, False, 0, 40, 20)
        self.meleeSpeed = ConflictEnemy(1000, random.choice(range(10, 850)), 3, (200, 200, 200), 4.5, False, 0, 16, 21, 0, False, 0, 10, 0)
        self.rangedShotgun = ConflictEnemy(1000, random.choice(range(10, 850)), 9, (50, 0, 50), 1.5, True, 400, 5, 9, 7, False, 1, 100, 8)
        self.meleeHeavy = ConflictEnemy(1000, random.choice(range(10, 850)), 15, (100, 100, 100), 1.6, False, 0, 41, 62, 0, False, 0, 25, 0)
        self.rangedFighter = ConflictEnemy(1000, random.choice(range(10, 850)), 8, (255, 71, 71), 2.5, True, 500, 3, 6, 7, False, 0, 20, 50)
        self.demon = ConflictEnemy(1000, random.choice(range(10, 850)), 12, (100, 0, 0), 3, False, 500, 36, 46, 7, False, 2, 15, 15)

    def update(self):
        self.reduceTime -= 1
        if self.reduceTime <= 0:
            self.reduceTime = 100
            self.timeLeft -= 1
        if self.timeLeft <= 0:
            self.gracePeriod -= 1

    def generateArea(self, difficulty, night):
        genEnemies = []
        genScrap = []
        availableEnemies = [self.meleeInfantry]

        if night >= 4:
            availableEnemies.append(self.rangedInfantry)
        if night >= 7:
            availableEnemies.append(self.meleeSpeed)
        if night >= 9:
            availableEnemies.append(self.rangedShotgun)
        if night >= 13:
            availableEnemies.append(self.meleeHeavy)
            availableEnemies.append(self.rangedFighter)
        
        if ((random.choice(range(1, 100)) <= (45 + 3 * night)) or night == 10) and not night == 16:
            numGenerated = ((int(random.choice(range(1, (difficulty + 1)))) + int(night / 5)))
            for i in range(0, numGenerated):
                newEnemy = copy.deepcopy(random.choice(availableEnemies))
                newEnemy.y = random.choice(range(50, 850))
                newEnemy.x = random.choice(range(500, 850))
                newEnemy.damage = int(newEnemy.damage / 2)
                genEnemies.append(newEnemy)

        if random.choice(range(1, 100)) < 80:
            scrapGenerated = random.choice(range(1, 4)) + int(night / 5)
            for i in range(0, scrapGenerated):
                genScrap.append([random.choice(range(500, 800)), random.choice(range(50, 850))])

        return genEnemies, genScrap
