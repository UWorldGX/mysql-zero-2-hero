# coding=utf-8
import json
from urllib import request, error
from uuid import uuid4
from os.path import exists

DATA_LINK: str = 'http://localhost:8888'  # MTR 在线线路图地址 末尾不要加"/"
WORLD: int = 0  # 0: 主世界, 1: 下界, 2: 末地  注: 使用 4.0.0 时无效
STYLE: str = 'sh'  # bj: 北京地铁 sh: 上海地铁 mtr: 港铁
USE_MTR_400: bool = False  # 如果使用 4.0.0 就改成 True
HIGH_SPEED_RAILWAY: bool = False  # 设置为 True 将高速铁路线路自动设置为中国铁路样式
IGNORE_OTHER_LINES: bool = False  # 设置为 True 忽略除重轨、轻轨和高铁外的线路并使 REPLACE_OTHER_LINES 无效
REPLACE_OTHER_LINES: bool = True  # 设置为 False 就不会将除重轨、轻轨和高铁外的线路替换为有轨电车样式
SCALE: float = 0.1  # 缩放倍数

# 初始化各类
DATA_LINK += '/mtr/api/map/stations-and-routes' if USE_MTR_400 else '/data'
STYLES = {
    'bj': [['bjsubway-basic', {'open': True}], [],
           [{'outOfStation': False}, 'bjsubway-basic', 'bjsubway-int', 'gzmtr-virtual-int', True]],
    'mtr': [['mtr', {'rotate': 0, 'transfer': [[]]}], ['mtr-light-rail'], [{}, 'mtr', '', 'mtr-unpaid-area']],
    'sh': [['shmetro-basic', {}], [],
           [{'rotate': 0, 'height': 10, 'width': 13}, 'shmetro-basic', 'shmetro-int', 'shmetro-virtual-int']]
}
hsr_name = 'china-railway' if HIGH_SPEED_RAILWAY else 'single-color'

# 初始化 / 获取数据
exec_data = {'options': {'type': 'directed', 'multi': True, 'allowSelfLoops': True}, 'attributes': {}, 'nodes': [],
             'edges': []}
station_data = {}
stations_attributes = {}
stations_attributes_record = {}


def fetch_data(link: str) -> str:
    req = request.Request(link)
    try:
        with request.urlopen(req) as res:
            return json.loads(res.read().decode('UTF-8'))
    except error.HTTPError as e:
        print(f'Error fetching data: {e.code} {e.reason}')
    except error.URLError as e:
        print(f'Error fetching data: {e.reason}')
    exit(1)


def convert_stations(name: str, attributes: dict):
    global station_data, exec_data
    temp = set()
    for key, station in stations.items():
        station_id = uuid4().hex[:10]
        while station_id in temp:
            station_id = uuid4().hex[:10]
        temp.add(station_id)
        station_data[key] = station_id
        stations_attributes[station_id] = 0
        yield {
            'key': f'stn_{station_id}',
            'attributes': {
                'visible': True,
                'zIndex': 0,
                'x': station['x'] * SCALE,
                'y': station['z'] * SCALE,
                'type': name,
                name: {
                    'names': station['name'],
                    'nameOffsetX': 'middle',
                    'nameOffsetY': 'bottom',
                    **attributes
                }
            }
        }


invalid_routes = set()
line_ids = set()
virtual_int_exec = set()


def convert_routes(light_rail: str = ''):
    global station_data, stations_attributes, exec_data, invalid_routes, line_ids, virtual_int_exec
    light_rail_name = light_rail if light_rail else 'single-color'
    for route in routes:
        color = True
        if route['type'] == 'train_light_rail':
            line_name = light_rail_name
        elif route['type'] == 'train_high_speed':
            line_name = hsr_name
            color = not HIGH_SPEED_RAILWAY
        elif route['type'] == 'train_normal':
            line_name = 'single-color'
        else:
            if IGNORE_OTHER_LINES:
                continue
            line_name = 'bjsubway-tram' if REPLACE_OTHER_LINES else 'single-color'
        for station in range(len(route['stations']) - 1):
            station_pair = (route['stations'][station].split('_')[0], route['stations'][station + 1].split('_')[0])
            if station_pair in invalid_routes:
                continue
            line_id = uuid4().hex[:10]
            while line_id in line_ids:
                line_id = uuid4().hex[:10]
            line_ids.add(line_id)
            exec_data['edges'].append(
                {'key': 'line_' + line_id, 'source': 'stn_' + station_data[route['stations'][station].split('_')[0]],
                 'target': 'stn_' + station_data[route['stations'][station + 1].split('_')[0]],
                 'attributes': {'visible': True, 'zIndex': 0, 'type': 'diagonal',
                                'diagonal': {'startFrom': 'from', 'offsetFrom': 0, 'offsetTo': 0,
                                             'roundCornerFactor': 10},
                                'style': line_name,
                                line_name: {
                                    'color': ['other', 'other', route['color'], '#fff']} if color else {},
                                'reconcileId': ''}})
            yield {
                'key': f'line_{line_id}',
                'source': f'stn_{station_data[station_pair[0]]}',
                'target': f'stn_{station_data[station_pair[1]]}',
                'attributes': {
                    'visible': True,
                    'zIndex': 0,
                    'type': 'diagonal',
                    'diagonal': {
                        'startFrom': 'from',
                        'offsetFrom': 0,
                        'offsetTo': 0,
                        'roundCornerFactor': 10
                    },
                    'style': line_name,
                    line_name: {
                        'color': ['other', 'other', route['color'], '#fff'] if color else {}
                    },
                    'reconcileId': ''
                }
            }
            invalid_routes.add((station_pair[1], station_pair[0]))
            for connection in stations[station_pair[0]]['connections']:
                if (station_pair[0], connection) not in virtual_int_exec:
                    virtual_int_exec.add((connection, station_pair[0]))
        for station in route['stations']:
            if station_data[station.split('_')[0]] not in stations_attributes_record:
                stations_attributes_record[station_data[station.split('_')[0]]] = []
            if route['name'] in stations_attributes_record[station_data[station.split('_')[0]]]:
                continue
            stations_attributes[station_data[station.split('_')[0]]] += 1
            stations_attributes_record[station_data[station.split('_')[0]]].append(route['name'])


def update_stations(int_attributes: dict, basic: str, int: str, virtual_int: str = 'gzmtr-virtual-int',
                    bjsubway: bool = False):
    for node in exec_data['nodes'].copy():
        if stations_attributes[node['key'].split('_', 1)[-1]] == 0:
            del exec_data['nodes'][exec_data['nodes'].index(node)]
            del station_data[
                list(station_data.keys())[list(station_data.values()).index(node['key'].split('_', 1)[-1])]]
        if stations_attributes[node['key'].split('_', 1)[-1]] > 1 and int:
            if bjsubway:
                int_attributes['outOfStation'] = False
            exec_data['nodes'][exec_data['nodes'].index(node)] = {'key': node['key'],
                                                                  'attributes': {'visible': True, 'zIndex': 0,
                                                                                 'x': node['attributes']['x'],
                                                                                 'y': node['attributes']['y'],
                                                                                 'type': int, int: {
                                                                          'names': node['attributes'][basic]['names'],
                                                                          'nameOffsetX': 'middle',
                                                                          'nameOffsetY': 'bottom', **int_attributes}}}
    for connection in virtual_int_exec:
        if ((*connection, 'virtual-int') in invalid_routes) or (
                (connection[1], connection[0], 'virtual-int') in invalid_routes):
            continue
        line_id = uuid4().hex[:10]
        while line_id in line_ids:
            line_id = uuid4().hex[:10]
        line_ids.add(line_id)
        try:
            yield {
                'key': f'line_{line_id}',
                'source': f'stn_{station_data[connection[0]]}',
                'target': f'stn_{station_data[connection[1]]}',
                'attributes': {
                    'visible': True,
                    'zIndex': 0,
                    'type': 'simple',
                    'simple': {
                        'offset': 0
                    },
                    'style': virtual_int,
                    'reconcileId': '',
                    virtual_int: {}
                }
            }
            invalid_routes.add((*connection, 'virtual-int'))
        except KeyError:
            print('Invalid ID: Connection (ID1: {}, ID2: {})'.format(*connection))


# 处理信息
def convert_data_3() -> None:
    global routes, stations, data
    data = data[WORLD]
    del data['types']
    del data['positions']
    # 处理线路信息
    routes = data['routes']
    for route in routes:
        del route['durations']
        del route['densities']
        del route['circular']
        route['name'] = [route['number'], *route['name'].split('|')[:2]]
        route['color'] = '#' + hex(route['color'])[2:].rjust(6, '0')
    # 处理车站信息
    stations = data['stations']
    for key, station in stations.items():
        del station['color']
        del station['zone']
        station['name'] = station['name'].split('|')[:2]
        if len(station['name']) < 2:
            station['name'].append('')


def convert_data_4() -> None:
    global routes, stations, data
    data = data['data']
    # 处理线路信息
    stations = {}
    routes = data['routes']
    convert_stations = data['stations']
    for route in routes:
        del route['circularState']
        route['name'] = [route['number'], *route['name'].split('|')[:2]]
        route['color'] = '#' + route['color']
        for station in route['stations']:
            stations[station['id']] = {'x': station['x'], 'z': station['z']}
            route['stations'][route['stations'].index(station)] = station['id']
    for station in convert_stations:
        try:
            stations[station['id']]['name'] = station['name'].split('|')[:2]
            stations[station['id']]['connections'] = station['connections']
            if len(stations[station['id']]['name']) < 2:
                stations[station['id']]['name'].append('')
        except KeyError:
            print('Invalid ID: Station {}, Name: {}'.format(station['id'], station['name']))


if __name__ == '__main__':
    # 开始转换
    data = fetch_data(DATA_LINK)
    convert_data_4() if USE_MTR_400 else convert_data_3()
    exec_data['nodes'] = list(convert_stations(*STYLES[STYLE][0]))
    exec_data['edges'] = list(convert_routes(*STYLES[STYLE][1]))
    exec_data['edges'].extend(list(update_stations(*STYLES[STYLE][2])))

    if exists('RMP_MTR.json'):
        if input('文件已存在，是否覆盖？(y/n) ') not in ['y', 'Y']:
            exit(0)
    with open('RMP_MTR.json', 'w', encoding='UTF-8') as file:
        json.dump({'svgViewBoxZoom': 50, 'svgViewBoxMin': {'x': 0.1, 'y': 0.1}, 'graph': exec_data, 'version': 30},
                  ensure_ascii=False, fp=file)