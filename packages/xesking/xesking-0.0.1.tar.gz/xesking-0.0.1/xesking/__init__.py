import sys, pygame, random

x = 600
y = 300
speedx = 20
speedy = 20
landpic = "bg" + str(random.randint(1, 5)) + ".jpg"


# 第1个参数为display,第2个参数为图片名称，第3参数为运动方式(1-3)
def look(screen, picName, way=1):
    global x, y, speedx, speedy, landpic
    picName = picName + ".png"
    myImg = pygame.image.load(picName)
    myImg2 = pygame.transform.scale(myImg, (200, 200))
    # 加载背景
    # bgImg=pygame.image.load(landpic)

    imgRect = myImg.get_rect()

    if way == 1:
        if x >= screen.get_size()[0] - 120 or x <= 0:
            speedx = -speedx
        elif y >= screen.get_size()[1] - 120 or y <= 0:
            speedy = -speedy
        x = x + speedx
        y = y + speedy
    elif way == 2:
        if x >= screen.get_size()[0] - 120 or x <= 0:
            speedx = -speedx
            y = y + 20
        elif y >= screen.get_size()[1] - 120 or y <= 0:
            y = 0
        x = x + speedx
    elif way == 3:
        if x >= screen.get_size()[0] - 120 or x <= 0:
            x = 0
        elif y >= screen.get_size()[1] - 120 or y <= 0:
            speedy = -speedy
            x = x + 20
        y = y + speedy
    # screen.blit(bgImg,(0,0))
    screen.blit(myImg2, (x, y))


def bulid(screen, imgName, x, y):
    img = pygame.image.load(imgName)
    img2 = pygame.transform.scale(img, (200, 200))
    screen.blit(img2, (x, y))


def build(screen, imgName, x, y):
    img = pygame.image.load(imgName)
    img2 = pygame.transform.scale(img, (200, 200))
    screen.blit(img2, (x, y))


def bg(screen):
    img = pygame.image.load("bg.png")
    img2 = pygame.transform.scale(img, (800, 600))
    screen.blit(img2, (0, 0))


def quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()