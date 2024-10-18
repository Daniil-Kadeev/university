import copy as cp
from math import pi, sin, atan
import matplotlib.pyplot as plt
from itertools import chain
from scipy.interpolate import UnivariateSpline
from numpy import arange

'''Исходные данные
В схему вводятся элементы трубопровода. Реализовано два типа элементов: труба и местное сопротивление
Труба имеет следующие типы: круглая, прямоугольная, треугольная ; параметры: длина, диаметр (для круглой), длина, ширина,высота (для прямоугольной), длина, длины сторон (для треугольной)
Местное сопротивление имеет следующие типы: числовое значение, резкое расширение, резкое сужение, плавное расширение, плавное сужение;
параметры: кси (для числового значения), диаметры входа и выхода, длина (последнее для плавного сужения расширения)
Для правильного расчёта введены заглушки. Суммирование сопротивления ведется паралльно если минимально количество номеров элемента в цепи нечетное [XXX, XXX], иначе - последовательно [XXX]'''

#_____________________________________________________________________________________
# Блок задачи исходных параметров:

def get_copy(val, element):
    cop = []
    baza = element['number']
    len_baza = len(baza)
    t = baza[-1]
    for i in range(val):
        baza[-1] = i + t
        element['number'] = baza
        cop.append(cp.deepcopy(element))
    return cop

scheme = (
    {'number': [0], 'types': 'pipe', 'subtypes': 'circle', 'parametre': {'length': 1.7, 'diameter': 2 * 10 ** (-2)}},
    {'number': [1], 'types': 'resistance', 'subtypes': 'Q', 'parametre': {'value': 4, 'diameter': 2 * 10 ** (-2)}},
    {'number': [2], 'types': 'pipe', 'subtypes': 'circle', 'parametre': {'length': 0.2, 'diameter': 2 * 10 ** (-2)}},
    *list(chain(get_copy(25, {'number': [3, 0], 'types': 'pipe', 'subtypes': 'circle', 'parametre': {'length': 2, 'diameter': 0.5 * 10 ** (-2)}}))),
    {'number': [4], 'types': 'pipe', 'subtypes': 'circle', 'parametre': {'length': 0.3, 'diameter': 2 * 10 ** (-2)}},
    {'number': [5], 'types': 'resistance', 'subtypes': 'Q', 'parametre': {'value': 4, 'diameter': 2 * 10 ** (-2)}},
    {'number': [6], 'types': 'pipe', 'subtypes': 'circle', 'parametre': {'length': 1.2, 'diameter': 2 * 10 ** (-2)}},
    {'number': [7], 'types': 'resistance', 'subtypes': 'Q', 'parametre': {'value': 3.6, 'diameter': 2 * 10 ** (-2)}},
    {'number': [8, 0, 0], 'types': 'resistance', 'subtypes': 'Q', 'parametre': {'value': 4.9, 'diameter': 2 * 10 ** (-2)}},
    {'number': [8, 0, 1], 'types': 'pipe', 'subtypes': 'circle', 'parametre': {'length': 0.2, 'diameter': 2 * 10 ** (-2)}},
    {'number': [8, 0, 2], 'types': 'resistance', 'subtypes': 'SE', 'parametre': {'diameter_entrance': 2 * 10 ** (-2 ), 'diameter_exit': 8 * 10 ** (-2)}},
    {'number': [8, 0, 3], 'types': 'pipe', 'subtypes': 'circle', 'parametre': {'length': 0.05, 'diameter': 8 * 10 ** (-2)}},
    *list(chain(get_copy(2, {'number': [8, 0, 4, 0], 'types': 'pipe', 'subtypes': 'rectangle', 'parametre': {'length': 0.5, 'long': 0.5 * 10 ** (-2), 'widht': 1 * 10 ** (-2)}}))),
    {'number': [8, 0, 5], 'types': 'pipe', 'subtypes': 'circle', 'parametre': {'length': 0.05, 'diameter': 8 * 10 ** (-2)}},
    {'number': [8, 0, 6], 'types': 'resistance', 'subtypes': 'SN', 'parametre': {'diameter_entrance': 8 * 10 ** (-2 ), 'diameter_exit': 2 * 10 ** (-2)}},
    {'number': [8, 0, 7], 'types': 'pipe', 'subtypes': 'circle', 'parametre': {'length': 0.24, 'diameter': 2 * 10 ** (-2)}},
    {'number': [8, 0, 8], 'types': 'resistance', 'subtypes': 'Q', 'parametre': {'value': 3.4, 'diameter': 2 * 10 ** (-2)}},
    {'number': [8, 1, 0], 'types': 'resistance', 'subtypes': 'Q', 'parametre': {'value': 3.4, 'diameter': 2 * 10 ** (-2)}},
    {'number': [8, 1, 1], 'types': 'pipe', 'subtypes': 'circle', 'parametre': {'length': 0.2, 'diameter': 2 * 10 ** (-2)}},
    {'number': [8, 1, 2], 'types': 'resistance', 'subtypes': 'SmE', 'parametre': {'diameter_entrance': 2 * 10 ** (-2), 'diameter_exit': 8 * 10 ** (-2), 'length': 0.015}},
    *list(chain(get_copy(66 * 19, {'number': [8, 1, 3, 0], 'types': 'pipe', 'subtypes': 'triangle', 'parametre': {'length': 0.2, 'a': 0.577 * 10 ** (-2), 'b': 0.577 * 10 ** (-2), 'c': 0.577 * 10 ** (-2)}}))),
    {'number': [8, 1, 4], 'types': 'resistance', 'subtypes': 'SmN', 'parametre': {'diameter_entrance': 8 * 10 ** (-2), 'diameter_exit': 2 * 10 ** (-2), 'length': 0.015}},
    {'number': [8, 1, 5], 'types': 'pipe', 'subtypes': 'circle', 'parametre': {'length': 0.24, 'diameter': 2 * 10 ** (-2)}},
    {'number': [8, 1, 6], 'types': 'resistance', 'subtypes': 'Q', 'parametre': {'value': 2.6, 'diameter': 2 * 10 ** (-2)}},
    {'number': [8, 2], 'types': 'zaglushka'},
    {'number': [9], 'types': 'resistance', 'subtypes': 'Q', 'parametre': {'value': 3.4, 'diameter': 2 * 10 ** (-2)}},
    {'number': [10], 'types': 'pipe', 'subtypes': 'circle', 'parametre': {'length': 0.1, 'diameter': 2 * 10 ** (-2)}},
)
wlovennost = -1
g = 9.81 # сила тяжести
v = 1.004 * 10 ** (-6) # вязкость жидкости
Re_f = 'u * d / v'
predel_V = 3 # максимальный расход, задается в л/мин
step = 0.01 # шаг по расходу
nachal_V = 0.05
V_massive = [V / 60 / 10 ** 3 * step for V in range(int(nachal_V / step), int(predel_V / step + 1))] # генерация массива с расходами
TX_nasosa = [
    [0, 0.5, 1, 1.5, 2, 2.5, 3],
    [0.15, 0.16, 0.20, 0.22, 0.20, 0.12, 0.025],
    [0, 0.2, 0.4, 0.5, 0.5, 0.3, 0.05]
]
spl = UnivariateSpline(TX_nasosa[0], TX_nasosa[1])
xs = arange(0, 3, 0.005)
spl_kpd = UnivariateSpline(TX_nasosa[0], TX_nasosa[2])
xs_kpd = arange(0, 3, 0.005)

#_______________________________________________________________________________________________________________________
#Расчётный блок
def resist_pipe_circle(val, V): # расчёт гидравлического сопротивления для круглого сечения
    global lambd, Re_f, g
    l, d = val['length'], val['diameter']
    S = pi * d ** 2 / 4
    u = V / S
    Re = eval(Re_f)
    la = lambd(Re)
    h = la * l / d * u ** 2 / 2 / g
    return h

def resist_pipe_rectangle(val, V): # расчёт гидравлического сопротивления для прямоугольного сечения
    global lambd, Re_f, g
    l, a, b = val['length'], val['long'], val['widht']
    p = a + b
    S = a * b
    d = 4 * S / p / 2
    u = V / S
    Re = eval(Re_f)
    la = lambd(Re)
    h = la * l / d * u ** 2 / 2 / g
    return h

def resist_pipe_triangle(val, V): # расчёт гидравлического сопротивления для треугольного сечения
    global lambd, Re_f, g
    l, a, b, c = val['length'], val['a'], val['b'], val['c']
    p = (a + b + c) / 2
    S = (p * (p - a) * (p - b) * (p - c)) ** (1 / 2)
    d = 2 * S / p
    u = V / S
    Re = eval(Re_f)
    la = lambd(Re)
    h = la * l / d * u ** 2 / 2 / g
    return h

def resist_resistange_Q(val, V): # расчёт гидравлического сопротивления для определенного коэффициента кси
    global lambd, Re_f, g
    ksi, d = val['value'], val['diameter']
    S = pi * d ** 2 / 4
    u = V / S
    Re = eval(Re_f)
    la = lambd(Re)
    h = ksi * u ** 2 / 2 / g
    return h

def resist_resistange_SE(val, V): # расчёт гидравлического сопротивления для резкого расширения
    global lambd, Re_f, g
    d1, d2 = val['diameter_entrance'], val['diameter_exit']
    S1 = pi * d1 ** 2 / 4
    S2 = pi * d2 ** 2 / 4
    ksi = 1 - S1 / S2
    u = V / S1
    d = d1
    Re = eval(Re_f)
    la = lambd(Re)
    h = ksi * u ** 2 / 2 / g
    return h

def resist_resistange_SN(val, V): # расчёт гидравлического сопротивления для резкого сужения
    global lambd, Re_f, g
    d1, d2 = val['diameter_entrance'], val['diameter_exit']
    S1 = pi * d1 ** 2 / 4
    S2 = pi * d2 ** 2 / 4
    ksi = (1 - S2 / S1) / 2
    u = V / S2
    d = d2
    Re = eval(Re_f)
    la = lambd(Re)
    h = ksi * u ** 2 / 2 / g
    return h

def resist_resistange_SmE(val, V): # расчёт гидравлического сопротивления для плавного расширения
    global lambd, Re_f, g
    d1, d2, l = val['diameter_entrance'], val['diameter_exit'], val['length']
    alpha = (atan((d2 - d1) / 2 / l)) / 2
    S1 = pi * d1 ** 2 / 4
    S2 = pi * d2 ** 2 / 4
    u = V / S1
    d = d1
    Re = eval(Re_f)
    la = lambd(Re)
    n = S2 / S1
    ksi = la / 8 / sin(alpha / 2) * (1 - 1 / n ** 2) + sin(alpha) * (1 - 1 / n) ** 2
    h = ksi * u ** 2 / 2 / g
    return h

def resist_resistange_SmN(val, V): # расчёт гидравлического сопротивления для плавного сужения
    global lambd, Re_f, g
    d1, d2, l = val['diameter_entrance'], val['diameter_exit'], val['length']
    alpha = (atan((d1 - d2) / 2 / l)) / 2
    S1 = pi * d1 ** 2 / 4
    S2 = pi * d2 ** 2 / 4
    u = V / S2
    d = d2
    Re = eval(Re_f)
    la = lambd(Re)
    n = S1 / S2
    ksi = (la / 8 / sin(alpha / 2) * (1 - 1 / n ** 2) + sin(alpha) * (1 - 1 / n) ** 2) / 2
    h = ksi * u ** 2 / 2 / g
    return h

def lambd(Re): # определение формулы для лямбда
    return {
            Re < 2300: 64 / Re,
            Re >= 2300: 0.316 / Re ** 0.25
            }[True]

def get_resist_element(val, V): # распознование типа и подтипа -> расчёт указанного элемента
    if val['types'] == 'zaglushka':
        return 'zaglushka'
    calculation_resist = {
        'pipe': 0 if val['types'] != 'pipe' else {'circle': resist_pipe_circle(val['parametre'], V) if val['subtypes'] == 'circle' else 0,          # расчёт круглого сечения
                                                  'rectangle': resist_pipe_rectangle(val['parametre'], V) if val['subtypes'] == 'rectangle' else 0, # расчёт прямоугольного сечения
                                                  'triangle': resist_pipe_triangle(val['parametre'], V) if val['subtypes'] == 'triangle' else 0},   # расчёт треугольного сечения
        'resistance': 0 if val['types'] != 'resistance' else {'Q': resist_resistange_Q(val['parametre'], V) if val['subtypes'] == 'Q' else 0,       # числовое значение местного сопротивления
                                                              'SE': resist_resistange_SE(val['parametre'], V) if val['subtypes'] == 'SE' else 0,    # расчёт резкого расширения
                                                              'SN': resist_resistange_SN(val['parametre'], V) if val['subtypes'] == 'SN' else 0,    # расчёт резкого сужения
                                                              'SmE': resist_resistange_SmE(val['parametre'], V) if val['subtypes'] == 'SmE' else 0, # расчёт плавного расширения
                                                              'SmN': resist_resistange_SmN(val['parametre'], V) if val['subtypes'] == 'SmN' else 0} # расчёт плавного сужения
    }
    h = 0
    if calculation_resist['pipe'] != 0: # блок вывода результата вычислений
        if calculation_resist['pipe']['circle'] != 0:
            h = calculation_resist['pipe']['circle']
        elif calculation_resist['pipe']['rectangle'] != 0:
            h = calculation_resist['pipe']['rectangle']
        elif calculation_resist['pipe']['triangle'] != 0:
            h = calculation_resist['pipe']['triangle']
        else:
            print("Ошибка в подтипе", val )
    elif calculation_resist['resistance'] != 0:
        if calculation_resist['resistance']['Q'] != 0:
            h = calculation_resist['resistance']['Q']
        elif calculation_resist['resistance']['SE'] != 0:
            h = calculation_resist['resistance']['SE']
        elif calculation_resist['resistance']['SN'] != 0:
            h = calculation_resist['resistance']['SN']
        elif calculation_resist['resistance']['SmE'] != 0:
            h = calculation_resist['resistance']['SmE']
        elif calculation_resist['resistance']['SmN'] != 0:
            h = calculation_resist['resistance']['SmN']
    else:
        print("Ошибка в типе", val)
    if h == 0:
        print('Ошибка в расчёте сопротивления ', val)
    return h
#_______________________________________________________________________________________________________________________
# блок нахождения сопротивления параллельного соединения
def nearest(massive, target):
    return(min(massive, key=lambda x : abs(x - target)))

def parallel_def(data): # суммирование графиков, берется график с минимальным сопротивлением и по нему проходит цикл
    global step
    for i in range(len(data)):
        if len(data[i]) < 2:
            dat = list(chain(data[i]))
            del data[i]
            data.insert(i, *dat)
    minimum = [max(parallel) for parallel in data]
    index_minimum = minimum.index(min(minimum))
    rashod_m = []
    counter = 0
    for i in range(len(data[index_minimum])): # в цикле находятся ближайшие сопротивления и по их индексам генерируется расход (расход зависит от индекса)
        rashod = 0
        mini = data[index_minimum][i]
        for j in data:
            blizshayshee = min(j, key=lambda x : abs(x - mini))
            index = j.index(blizshayshee)
            rashod += index * (1 / 60 / 10 ** 3 * step)
        rashod_m.append(rashod)
    sopr_list = []
    for V in V_massive: #
        bliv = nearest(rashod_m, V)
        ind = rashod_m.index(bliv)
        sopr_list.append(data[index_minimum][ind])
    for resist in sopr_list:
        counter = sopr_list.count(resist)
        if counter > 1:
            index_count = sopr_list.index(resist)
            try:
                raznost = (- sopr_list[index_count] + sopr_list[index_count + counter]) / counter
                for i in range(counter - 1):
                    sopr_list[index_count + 1 + i] = sopr_list[index_count] + raznost * (i + 1)
            except:
                #print('Error')
                raznost = (- sopr_list[index_count] + sopr_list[index_count + counter - 1]) / counter
                for i in range(counter - 1):
                    sopr_list[index_count + 1 + i] = sopr_list[index_count] + raznost * (i + 1)
    plt.figure(figsize=(8, 5))
    plt.ylabel('Сопротивление, м')
    plt.xlabel('Расход, л/мин')
    plt.grid()
    for i in range(len((data))):
        plt.plot(list(map(lambda num: num/ (1 / 60 / 10 ** 3),  V_massive)), data[i], label='Участок ' + str(i))
    #plt.plot(list(map(lambda num: num/ (1 / 60 / 10 ** 3), rashod_m)), data[index_minimum], label='Суммарный график')
    plt.plot(list(map(lambda num: num / (1 / 60 / 10 ** 3), V_massive)), sopr_list, label='Суммарный график')
    plt.legend()
    plt.show()
    return sopr_list
#_______________________________________________________________________________________________________________________
def get_resist_scheme(scheme): #обрезаем и передаем часть с одинаковыми первыми номерами, номер где произошло повторение
    print('enter')
    global wlovennost
    popravka = 0 #учет того, что параллельное соединение записывается под одним первым числом
    error_popravka = 0 #поправка на заглушки
    wlovennost += 1
    resist = []  # массив со значениями сопротивлений
    val = []  # масив с номерами трубопроводов
    for i in scheme:  # получение массива с номерами элементов трубопровода
        val.append(i['number'])
    soedinenie = min([len(i) for i in val]) #определение типа соединения по длине номера
    try:
        first = [val[peremennaya_0][0 + wlovennost] for peremennaya_0 in range(len(val))]  # Просмотр первых чисел номеров на повтор и отправка повторных элементов в функцию, где производятся такие же действия
    except IndexError:
        error_popravka += 1
    for i in range(max(first)+1):  # Создание массивов в количестве последовательных соединений
        resist.append([])
    for i in range(max(first) + 1):
        replay = first.count(i)
        if replay == 1:  # расчёт сопротивление элемента трубопровода под номером Х (параллельные расчитавыются при обрезке и передачи в рекурсивную функцию, где они приобретают номер типа Х в замен Х, Х)
            for V in V_massive:
                vozvrat = get_resist_element(scheme[i + popravka], V)
                if vozvrat == 'zaglushka':
                    del resist[i]
                    break
                resist[i].append(vozvrat)

        elif replay > 1:# and sxod_flag:
            give_scheme = cp.deepcopy(scheme[i + popravka: replay + i + popravka])
            iterac = 0
            resist[i] = [get_resist_scheme(give_scheme)]
            popravka += replay - 1 + error_popravka  # учет того, что параллельное соединение записывается под одним первым числом
        #grapfik_scheme(V_massive, resist[i])
        print(resist[i][263])
    if soedinenie%2: #у последовательных соединений нечетное количество чисел в нумерации, если неверно - использовать заглушки hi kostili:)
        for i in range(len(resist)):
            if len(resist[i]) < 2:
                dat = list(chain(resist[i]))
                del resist[i]
                resist.insert(i, *dat)
        sum_resist_massive = []
        for i in range(len(resist[0])):
            sum_resist = 0
            for j in range(len(resist)):
                sum_resist += resist[j][i]
            sum_resist_massive.append(sum_resist)
        wlovennost -= 1
        print('exit porsled')
        #grapfik_scheme(V_massive, sum_resist_massive)
        return sum_resist_massive
    else:
        wlovennost -= 1
        print('exit parallel')
        #grapfik_scheme(V_massive, parallel_def(resist))
        return parallel_def(resist)
#_______________________________________________________________________________________________________________________

def grapfik_scheme(x, y):
    plt.figure(figsize=(8, 5))
    plt.ylabel('Сопротивление, м')
    plt.xlabel('Расход, л/мин')
    plt.grid()
    plt.plot(list(map(lambda num: num/ (1 / 60 / 10 ** 3),  x)), y)
    plt.show()

def grapfik_elements(data, rashod_m, index_minimum, resist): #постоение графиков с сумированием
    plt.figure(figsize=(8, 5))
    plt.ylabel('Сопротивление, м')
    plt.xlabel('Расход, л/мин')
    plt.grid()
    i = 0
    for h in data:
        plt.plot(list(map(lambda num: num/ (1 / 60 / 10 ** 3),  V_massive)), h, label=str(i))
        i += 1
    plt.plot(list(map(lambda num: num / (1 / 60 / 10 ** 3), V_massive)), resist, label=str('Summ'))
    plt.legend()
    plt.show()

resist = get_resist_scheme(scheme)
mnov = 2
plt.figure(figsize=(8, 5))
plt.ylabel('Сопротивление, м')
plt.xlabel('Расход, л/мин')
plt.grid()
plt.plot(list(map(lambda num: num / (1 / 60 / 10 ** 3*mnov), V_massive)), resist, label='Сопротивление сети')
plt.plot(xs, spl(xs), label='ТХ насоса')
plt.legend()
plt.twinx()
plt.plot(xs_kpd, spl_kpd(xs_kpd), label='КПД')
plt.legend()
plt.show()