from random import randint
import copy


class Map():
    def cpoy_word(self, word):
        new_word = {}
        new_word['key'] = word['key']
        new_word['pos'] = []
        for i in word['pos']:
            new_word['pos'].append(i)

        new_word['posiable'] = []
        for i in word['posiable']:
            new_word['posiable'].append(i)

        new_word['way'] = word['way']

        return new_word

    def check_pos(self, result, pos, max=9):
        '''
            检查坐标是否可用,可用返回True,否则返回False
            argv{
                result: 结果字典
                pos: 要检查的坐标
                max:横纵坐标最大值
            }
        '''
        if pos[0] < 0 or pos[1] < 0 or pos[0] >= max or pos[1] >= max:
            return False
        for default in result:
            if default['pos'][0] == pos[0] and default['pos'][1] == pos[1]:
                return False
        return True

    def change_pos(self, pos, way):
        '''
            改变坐标,并返回改变后的坐标
            argv{
                pos:坐标
                way:方向{-2:y-1, -1:x-1, 1:x+1, 2:y+1}
            }
        '''
        if way == -2:
            pos[1] -= 1
        elif way == -1:
            pos[0] -= 1
        elif way == 1:
            pos[0] += 1
        elif way == 2:
            pos[1] += 1

        return pos

    def create_maze(self, content, max):
        '''
            生成地图
            argv{
                content: 地图内容
                max: 地图行列数
            }
        '''
        # 初始化
        content_1 = list(content)
        content = list(content)
        maze = [[0 for i in range(max)] for i in range(max)]
        word = {}
        result = []
        pop_result = False  # 用来标识上一次循环是否成功选出坐标
        while True:
            if len(content) == 0:
                # 生成成功 结束循环
                break
            if pop_result:
                # 上一次不成功 跳回上上次
                pop_result = False
                if len(result) <= 0:
                    return False
                word = result.pop()
                if len(word['posiable']) > 0:
                    # 还可以改变
                    word['way'] = word['posiable'].pop(
                        randint(0, len(word['posiable']) - 1))
                    word['pos'] = result[-1]['pos'].copy()
                else:
                    # 不可以改变
                    pop_result = True
                    continue
            else:
                # 否则为下一个文字寻找坐标
                word['key'] = content[0]
                content.pop(0)
                word['posiable'] = list((-2, -1, 1, 2))

                if len(result) == 0 and not pop_result:
                    # 第一次为第一个字找坐标
                    word["pos"] = list((0, 0))
                    word["way"] = 0
                    word["posiable"] = list()
                elif len(result) == 0 and pop_result:
                    # 结果为空 并且上次失败 说明生成地图失败
                    return False
                else:
                    word['way'] = word['posiable'].pop(
                        randint(0, len(word['posiable']) - 1))
                    word['pos'] = result[-1]['pos'].copy()

            word['pos'] = self.change_pos(word['pos'], word['way'])

            while (not self.check_pos(result, word['pos'], max)) and (len(word['posiable']) > 0):
                word['pos'] = self.change_pos(word['pos'], (-1) * word['way'])
                word['way'] = word['posiable'].pop(
                    randint(0, len(word['posiable']) - 1))
                word['pos'] = self.change_pos(word['pos'], word['way'])

            if self.check_pos(result, word['pos'], max):
                # 生成成功
                result.append(copy.deepcopy(word))
                pop_result = False
            else:
                content.insert(0, word['key'])
                # 生成失败
                pop_result = True
        true_way = []
        for word in result:
            true_way.append(word['pos'])
            #print(word, maze)
            maze[word['pos'][0]][word['pos'][1]] = word['key']
        for x in range(len(maze)):
            for y in range(len(maze[x])):
                if maze[x][y] == 0:
                    maze[x][y] = content_1[randint(0, len(content_1) - 1)]

        return maze, true_way

    def CreateMaze(self, content, max):
        while True:
            result = ''
            maze, true_way = self.create_maze(content, 9)
            for pos in true_way:
                result += maze[pos[0]][pos[1]]
            if result == content:
                return maze, true_way


if __name__ == "__main__":
    content = "一动不动二话不说三言两语"
    for i in Map().CreateMaze(content, 9):
        print(i)
