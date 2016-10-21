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

from gcloud import datastore
import os, time

board_size = 10
project_id = os.environ.get('PROJECT_ID')
ds_client = datastore.Client(project_id)
backend_url = 'http://backend-service.default.svc.cluster.local:8081/api/v1'

## for non-GKE environment
backend_ip = os.environ.get('BACKEND_PORT_8081_TCP_ADDR')
backend_port = os.environ.get('BACKEND_PORT_8081_TCP_PORT')
if backend_ip and backend_port:
    backend_url = 'http://' + backend_ip + ':' + backend_port + '/api/v1'
####

def _deserialize_face(face_string):
    result = []
    for y in range(board_size):
        raw = []
        for x in range(board_size):
            raw.append(int(face_string[0]))
            face_string = face_string[1:]
        result.append(raw)
    return result

def _serialize_face(face):
    face_string = ""
    for y in range(board_size):
        for x in range(board_size):
            face_string += str(face[y][x])
    return face_string

def _get_board_entity(board_id):
    key = ds_client.key('GameBoards', int(board_id))
    board = ds_client.get(key)
    return board

def new_board():
    with ds_client.transaction():
        key = ds_client.key('GameBoards')
        board = datastore.Entity(key)
        board.update({
            'face_string': "0"*(board_size**2),
        })
        ds_client.put(board)
    return board.key.id

def get_board(board_id):
    board = _get_board_entity(board_id)
    if not board:
        return None
    return _deserialize_face(board['face_string'])

def delete_board(board_id):
    try:
        with ds_client.transaction():
            key = ds_client.key('GameBoards', int(board_id))
            ds_client.delete(key)
        return 0
    except:
        return -1

def update_board(board_id, x, y, player):
    with ds_client.transaction():
        board = _get_board_entity(board_id)
        face = _deserialize_face(board['face_string'])
        face[y][x] = player
        board['face_string'] = _serialize_face(face)
        ds_client.put(board)

