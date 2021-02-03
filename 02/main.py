import json
import math


def correlation(x, y, fields):
    avg1 = 0
    avg2 = 0
    for field in fields:
        avg1 = avg1 + x[field]
        avg2 = avg2 + y[field]
    avg1 = avg1 / len(x)
    avg2 = avg2 / len(y)
    a = 0
    b = 0
    c = 0
    for field in fields:
        a = a + (x[field] - avg1) * (y[field] - avg2)
        b = b + ((x[field] - avg1) ** 2)
        c = c + ((y[field] - avg2) ** 2)
        cc = a / math.sqrt(b * c)
    return cc


def data():
    with open("tree2.json", encoding='utf-8') as json_file:
        coffee = json.load(json_file)
        x = coffee[0]
        coffee.pop(0)
        resp = dict()
        fields = ['flavor', 'sweetness', 'mouthfeel', 'sourness', 'roast']
        print('%-18s' % 'Кофе', '%-4s' % 'ЕР', "|", '%-5s' % 'МР', "|", '%s' % 'S', "|", '%s' % 'DF', "|", 'CR')
        print('------------------------┼-------┼---┼----┼-----')

        for y in coffee:
            res = abs(x['flavor'] - y['flavor']) + abs(x['sweetness'] - y['sweetness']) + abs(
                x['mouthfeel'] - y['mouthfeel']) + abs(x['sourness'] - y['sourness']) + abs(x['roast'] - y['roast'])
            res2 = math.sqrt((x['flavor'] - y['flavor']) ** 2 + (x['sweetness'] - y['sweetness']) ** 2 + (
                    x['mouthfeel'] - y['mouthfeel']) ** 2 + (x['sourness'] - y['sourness']) ** 2 + (
                                     x['roast'] - y['roast']) ** 2)
            s = abs(x['node'] - y['node'])
            dif = 0
            for field in y:
                if field in fields:
                    dif += 1 if x[field] != y[field] else 0

            cc = correlation(x, y, fields)

            print('%-16s' % y['name'], '{:>6}'.format(res), "|", "%.2f" % res2, "|", s, "|", '{:>2}'.format(dif), "|", "%.2f" % cc)

        return resp


def main():
    data()


if __name__ == "__main__":
    main()
