import os
import random
import sys
import pygame as pg
import time

WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}

bb_accs = [ a for a in range(1, 11)]

os.chdir(os.path.dirname(os.path.abspath(__file__)))

    
def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectまたは爆弾Rect
    戻り値：タプル（横方向判定結果、縦方向判定結果）
    画面内ならTrue, 画面外ならFalse
    """

    yoko, tate = True, True
    if  rct.left < 0 or WIDTH < rct.right:       #画面外であったら
        yoko = False
    if rct.top < 0  or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate




def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_naki_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    kk_naki_rct = kk_naki_img.get_rect(center=(WIDTH-750,HEIGHT/2))
    kk_naki_rct2 = kk_naki_img.get_rect(center=(WIDTH-350,HEIGHT/2))
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game over", True, (255, 255, 255))
    txt_rect = txt.get_rect(center=(WIDTH/2,HEIGHT/2))
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img  = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0,WIDTH), random.randint(0, HEIGHT)
    vx , vy = +5, +5
    black_img = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(black_img, (0, 0, 0), [0,0,WIDTH,HEIGHT])
    black_img.set_alpha(200)
    clock = pg.time.Clock()
    tmr = 0
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct): #こうかとんRectと爆弾Rectが重なったら
            screen.blit(black_img, [0,0])
            screen.blit(kk_naki_img, kk_naki_rct )
            screen.blit(kk_naki_img, kk_naki_rct2 )
            screen.blit(txt, txt_rect)
            pg.display.update()
            time.sleep(5)
            return 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]

        for key, mv in DELTA.items():

            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
                
        kk_rct.move_ip(sum_mv)

        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])   #画面の外だったら
        bb_rct.move_ip(avx, avy)
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        
        if not yoko:
            vx *= -1
            
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
