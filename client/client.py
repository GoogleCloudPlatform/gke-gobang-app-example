#!/usr/bin/env python

# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

import requests, json, os, sys
api_url = os.environ.get("API_URL")
if not api_url:
    print "You need to set environment variable API_URL"
    sys.exit()

def new_game():
    headers = {'content-type': 'application/json'}
    response = requests.post(api_url + '/games',
                             headers=headers)
    return response.json()['id']

def get_board(id):
    headers = {'content-type': 'application/json'}
    response = requests.get(api_url + '/games/' + str(id),
                            headers=headers)
    return response.json()['board']

def delete_game(id):
    headers = {'content-type': 'application/json'}
    response = requests.delete(api_url + '/games/' +str(id),
                               headers=headers)
    return response.json()['id']

def put_stone(id, x, y, player, auto):
    headers = {'content-type': 'application/json'}
    body = {'x': x, 'y': y, 'player': player, 'auto': auto}
    response = requests.put(api_url + '/games/' + str(id),
                            json.dumps(body), headers=headers)
    return response.json()['result']

def show_board(id):
    board = get_board(id)
    board_size = len(board)
    marks = {0: '-', 1: 'o', 2: 'x'}
    print '  ' + ' '.join(map(str,range(board_size)))
    for y in range(board_size):
        print y,
        for x in range(board_size):
            print marks[board[y][x]],
        print ''


if __name__ == '__main__':
    print "Welcome to Gobang (Five in a Row) game."
    while True:
        print "Game ID (0:new game)?",
        input = raw_input()
        try:
            id = int(input)
        except:
            print "Bad input."
            continue
        if id == 0:
            id = new_game()
        board = get_board(id)
        if not board:
            print "Bad input."
            continue
        break
    print "Your game ID is %d" % id

    while True:
        print ''
        show_board(id)

        board = get_board(id)
        board_size = len(board) #int(board['board_size'])
        print "(q:quit) x(0-%d), y(0-%d)?" % (board_size-1, board_size-1),
        input = raw_input()
        if input == 'q':
            print "Your game ID is %d" % id
            print "See you again."
            break
        try:
            x, y = map(int, input.split(','))
        except:
            print "Bad input."
            continue

        result = put_stone(id, x, y, player=1, auto=False)
        if result == 'error':
            print "Bad input."
            continue
        if result != 'next':
            print ''
            show_board(id)
            if result == 'win':
                print 'You won!'
            if result == 'end':
                print 'Tie game.'
            delete_game(id)
            break

        result = put_stone(id, 0, 0, player=2, auto=True)
        if result != 'next':
            print ''
            show_board(id)
            if result == 'win':
                print 'You lost!'
            if result == 'end':
                print 'Tie game.'
            delete_game(id)
            break

