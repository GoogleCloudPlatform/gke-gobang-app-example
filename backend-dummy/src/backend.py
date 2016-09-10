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

def _dummy_brain(board_id, player):
    board = get_board(board_id)
    candidates = []
    for y in range(len(board)):
        for x in range(len(board)):
            if board[y][x] == 0:
                candidates.append((x,y))
    if len(candidates) == 0:
        return None
    return choice(candidates)

@app.route('/api/v1/brain/<int:id>/<int:player>', methods=['GET'])
def get_move_api(id, player):
    x, y = _dummy_brain(id, player)
    response = jsonify({'x': x, 'y': y})
    response.status_code = 200
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)

