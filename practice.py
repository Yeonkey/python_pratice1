from random import *

# 일반 유닛
class Unit:
    def __init__(self, name, hp, speed):
        self.name = name #초기화
        self.hp = hp #초기화
        self.speed = speed #초기화
        print("{0}유닛이 생성되었습니다.".format(name))#self.name도 상관없음

    def move(self, location):
        print("[지상 유닛 이동]")
        print("{0}유닛이 {1} 방향으로 이동합니다. [속도 {2}]".format(self.name, location, self.speed))

    def damaged(self, damage):
        print("{0}유닛이 {1}데미지를 입었습니다.".format(self.name, damage))
        self.hp -= damage
        print("{0}유닛의 현재 체력은 {1}입니다.".format(self.name, self.hp))
        if self.hp <=0:
            print("{0}유닛이 파괴되었습니다.".format(self.name))

#공격 유닛
class AttackUnit(Unit): # (공격유닛은 일반유닛을 상속 받아서 만들어짐)
    def __init__(self, name, hp, speed, damage):
        Unit.__init__(self, name, hp, speed) # 상속 접근법
        self.damage = damage #상속된거 이외에 추가로 공격력 설정
        #print("{0} 유닛이 생성 되었습니다".format(self.name))
        #print("체력 : {0}, 공격력 {1}".format(self.hp, self.damage))

    def attack(self, location):
        print("{0}유닛이 {1}방향으로 적군을 공격 합니다. [공격력 {2}]".format(self.name, location, self.damage))
        #self.name 자신에 있는 멤버 변수를 출력, location은 전달 받은 값을 씀

    def damaged(self, damage):
        print("{0}유닛이 {1}데미지를 입었습니다.".format(self.name, damage))
        self.hp -= damage
        print("{0}유닛의 현재 체력은 {1}입니다.".format(self.name, self.hp))
        if self.hp <=0:
            print("{0}유닛이 파괴되었습니다.".format(self.name))

#마린 class
class Marine(AttackUnit):
    def __init__(self):
        AttackUnit.__init__(self, "마린", 40, 1, 5)
    def stimpack(self):
        if self.hp > 10:
            self.hp -= 10
            print("{0}유닛이 스팀팩을 사용합니다. (HP 10 감소)".format(self.name))
        else:
            print("{0}유닛은 체력이 부족하여 스팀팩을 사용하지 못합니다.".format(self.name))

#탱크 class
class Tank(AttackUnit):
    seize_developed = False
    def __init__(self):
        AttackUnit.__init__(self, "탱크", 150, 1, 35)
        self.seize_mode = False
    def set_seize_mode(self):
        if Tank.seize_developed == False:
            return
        #시즈모드가 아닐때 -> 시즈모드
        if self.seize_mode == False:
            print("{0}유닛이 시즈모드로 전환합니다.".format(self.name))
            self.damage *= 2
            self.seize_mode = True

        #시즈모드일때 -> 시즈모드 해제
        else :
            print("{0}유닛이 시즈모드를 해제합니다.".format(self.name))
            self.damage /= 2
            self.seize_mode = False

#날 수 있는 기능을 가진 클래스
class Flyable:
    def __init__(self, flying_speed):
        self.flying_speed = flying_speed

    def fly(self, name, location):
        print("{0}유닛이 {1}방향으로 날아갑니다. [속도 {2}]".format(name, location, self.flying_speed))

#공중 공격 유닛 클래스
class FlyableAttackUnit(AttackUnit, Flyable): #다중상속
    def __init__(self, name, hp, damage, flying_speed):
        AttackUnit.__init__(self, name, hp, 0, damage) #지상 speed는 0
        Flyable.__init__(self, flying_speed) #멤버변수 초기화

    def move(self, location): #move 재정의
        print("[공중 유닛 이동]")
        self.fly(self.name, location)

# 레이스 class
class Warith(FlyableAttackUnit):
    def __init__(self):
        FlyableAttackUnit.__init__(self, "레이스", 80, 20, 5)
        self.clocked = False # 클로킹 모드 (해제 상태)

    def clocking(self):
        if self.clocked == True:
            print("{0}유닛이 클로킹 모드 해제합니다.".format(self.name))
            self.clocked = False
        else:
            print("{0}유닛이 클로킹 모드 설정합니다.".format(self.name))
            self.clocked = True


def game_start():
    print("[알림] 새로운 게임을 시작합니다.")

def game_over():
    print("Player : gg")
    print("[Player] 님이 게임에서 퇴장하셨습니다.")


#실제 게임 시작
game_start()
#마린 3기
m1 = Marine()
m2 = Marine()
m3 = Marine()
#탱크 2기
t1 = Tank()
t2 = Tank()
#레이스 1기
w1 = Warith()

#유닛 일괄 관리
attack_units = []
attack_units.append(m1)
attack_units.append(m2)
attack_units.append(m3)
attack_units.append(t1)
attack_units.append(t2)
attack_units.append(w1)

# 전군 이동
for unit in attack_units:
    unit.move("1시")

# 탱크 시즈모드 개발
Tank.seize_developed = True
print("[알림] 탱크 시즈 모드 개발이 완료되었습니다.")

# 공격 모드 준비 (마린 : 스팀팩, 탱크 : 시즈모드, 레이스 : 클로킹)
for unit in attack_units:
    if isinstance(unit, Marine):
        unit.stimpack()
    elif isinstance(unit, Tank):
        unit.set_seize_mode()
    elif isinstance(unit, Warith):
        unit.clocking()

# 전군 공격
for unit in attack_units:
    unit.attack("1시")

# 전군 피해
for unit in attack_units:
    unit.damaged(randint(5, 21)) # 공격은 랜덤으로 받음 (5~20)

# 게임 종료
game_over()