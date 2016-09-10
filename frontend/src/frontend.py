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

from flask import Flask, jsonify, request, Response
import requests, json
from library import new_board, get_board, update_board, delete_board
from library import backend_url

def _board_full(board_id):
    board = get_board(board_id)
    if any(item == 0 for item in sum(board, [])):
        return False
    return True

def _judge(board_id, player):
    board = get_board(board_id)
    board_size = len(board)
    for y in range(board_size):
        for x in range(board_size):
            # check to right
            if x + 4 < board_size:
                if all(board[y][x+dx] == player for dx in range(5)):
                    return True
            # check to down
            if y + 4 < board_size:
                if all(board[y+dy][x] == player for dy in range(5)):
                    return True
            # check to right-down
            if x + 4 < board_size and y + 4 < board_size:
                if all(board[y+d][x+d] == player for d in range(5)):
                    return True
            # check to left-down
            if x - 4 > 0 and y + 4 < board_size:
                if all(board[y+d][x-d] == player for d in range(5)):
                    return True
    return False

def _get_move(board_id, player):
    headers = {'content-type': 'application/json'}
    response = requests.get(
        backend_url + '/brain/' + str(board_id) + '/' + str(player),
        headers=headers)
    result = response.json()
    return (result['x'], result['y'])

def _put_stone(board_id, x, y, player, auto):
    board = get_board(board_id)
    board_size = len(board)
    if not player in [1,2]:
        return -1
    if auto:
        x, y = _get_move(board_id, player)
    if x < 0 or x >= board_size or y < 0 or y >= board_size:
        return -1
    if board[y][x] != 0:
        return -1

    update_board(board_id, x, y, player)

    if _judge(board_id, player):
        return 1 # win

    if _board_full(board_id):
        return 99 # end

    return 0

app = Flask(__name__)

@app.route('/api/v1/games', methods=['POST'])
def new_game_api():
    id = new_board()
    if id == -1:
        response = jsonify({'id': None})
        response.status_code = 500
    else:
        response = jsonify({'id': id})
        response.status_code = 200
    return response

@app.route('/api/v1/games/<int:id>', methods=['GET'])
def get_board_api(id):
    board = get_board(id)
    if board == -1:
        response = jsonify({'board': None})
        response.status_code = 500
    else:
        response = jsonify({'board': board})
        response.status_code = 200
    return response

@app.route('/api/v1/games/<int:id>', methods=['DELETE'])
def delete_board_api(id):
    result = delete_board(id)
    if result == -1:
        response = jsonify({'id': None})
        response.status_code = 500
    else:
        response = jsonify({'id': id})
        response.status_code = 200
    return response

@app.route('/api/v1/games/<int:id>', methods=['PUT'])
def put_stone_api(id):
    request_body = json.loads(request.data)
    try:
        x, y = int(request_body['x']), int(request_body['y'])
        player = int(request_body['player'])
        auto = int(request_body['auto'])
    except:
        response = jsonify({'result': 'error'})
        response.status_code = 500
        return response

    result = _put_stone(id, x, y, player, auto)
    if result == -1:
        response = jsonify({'result': 'error'})
        response.status_code = 500
    elif result == 1:
        response = jsonify({'result': 'win'})
        response.status_code = 200
    elif result == 99:
        response = jsonify({'result': 'end'})
        response.status_code = 200
    else:
        response = jsonify({'result': 'next'})
        response.status_code = 200
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

