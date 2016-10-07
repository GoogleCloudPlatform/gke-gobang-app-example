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
from random import choice
from library import get_board

app = Flask(__name__)

def _score(num_player, num_opponent):
    score = 0
    if num_opponent == 0:
        if num_player == 4:
            score += 1000
        else:
            score += num_player
    if num_player == 0:
        if num_opponent >= 4:
            score += 800
        elif num_opponent >= 3:
            score += 500
        else:
            score += num_opponent
    return score

def scoring_model(board_id, player):
    board = get_board(board_id)
    board_size = len(board)
    score = [[0 for y in range(board_size)]
                for x in range(board_size)]
    if player == 1:
        opponent = 2
    else:
        opponent = 1
    for y in range(board_size):
        for x in range(board_size):
            if board[y][x] != 0:
                score[y][x] = -1

            # check to right
            if x + 4 < board_size:
                num_player = sum(board[y][x+dx] == player for dx in range(5))
                num_opponent = sum(board[y][x+dx] == opponent for dx in range(5))
                for dx in range(5):
                    if board[y][x+dx] == 0:
                        score[y][x+dx] += _score(num_player, num_opponent)

            # check to down
            if y + 4 < board_size:
                num_player = sum(board[y+dy][x] == player for dy in range(5))
                num_opponent = sum(board[y+dy][x] == opponent for dy in range(5))
                for dy in range(5):
                    if board[y+dy][x] == 0:
                        score[y+dy][x] += _score(num_player, num_opponent)

            # check to right-down
            if x + 4 < board_size and y + 4 < board_size:
                num_player = sum(board[y+d][x+d] == player for d in range(5))
                num_opponent = sum(board[y+d][x+d] == opponent for d in range(5))
                for d in range(5):
                    if board[y+d][x+d] == 0:
                        score[y+d][x+d] += _score(num_player, num_opponent)

            # check to left-down
            if x - 4 >= 0 and y + 4 < board_size:
                num_player = sum(board[y+d][x-d] == player for d in range(5))
                num_opponent = sum(board[y+d][x-d] == opponent for d in range(5))
                for d in range(5):
                    if board[y+d][x-d] == 0:
                        score[y+d][x-d] += _score(num_player, num_opponent)

    max_score = max(sum(score, []))
    candidates = []
    for y in range(len(board)):
        for x in range(len(board)):
            if score[y][x] == max_score and board[y][x] == 0:
                candidates.append((x,y))
    if len(candidates) == 0:
        return None

    return choice(candidates)

@app.route('/api/v1/brain/<int:id>/<int:player>', methods=['GET'])
def get_move_api(id, player):
    x, y = scoring_model(id, player)
    response = jsonify({'x': x, 'y': y})
    response.status_code = 200
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)

