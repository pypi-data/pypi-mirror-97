#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2021 Baidu.com, Inc. All Rights Reserved
This module provide configure file management service in i18n environment.

Authors: machen02(machen02@baidu.com)
Date: 2021/01/25 14:55:00
"""

import socket
import zlib
import os
import time
import sys
import json
import logging
import traceback
from pathlib import Path

#log level and format
# logging.basicConfig(level=logging.DEBUG,
#                     format="[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s] %(message)s",
#                     datefmt = '%Y-%m-%d %H:%M:%S %a'
#                     )

KEY_ERRCODE = "errcode"
KEY_ERRDESC = "errdesc"
SERVER_IP = "10.138.35.34"
SERVER_PORT = 8100
CONNECTION_TIMEOUT = 10
RETRY_LIMIT = 3

def __merge_data_in_chunk(data_array):
    merged_data = None
    for index in range(len(data_array)):
        data = data_array[index]
        if merged_data is None:
            merged_data = len(data).to_bytes(4, byteorder='little', signed=False)
        else:
            merged_data += len(data).to_bytes(4, byteorder='little', signed=False)
        merged_data += data

    return merged_data


def __recv_data_all(conn, expected_size):
    response_buf = conn.recv(expected_size)
    while True:
        received_len = len(response_buf)
        if received_len < expected_size:
            response_buf += conn.recv(expected_size - received_len)
        else:
            break
        
    return response_buf


def __send_data_in_chunk(conn, data):
    if data is None:
        conn.sendall(int(0).to_bytes(4, byteorder='little', signed=False))
        return

    conn.sendall(len(data).to_bytes(4, byteorder='little', signed=False))
    conn.sendall(data)


def __normalize_path(path):
    if Path(path).exists():
        return path
    
    return os.path.join(os.getcwd(), path)


def wer(answer_file_path, recognition_file_path, wer_result_path, wer_console_output_path, wer_config_file_path=None):
    """ WER RPC """
    config_file_data = None
    if not wer_config_file_path is None:
        wer_config_file_path = __normalize_path(wer_config_file_path)
        try:
            with open(wer_config_file_path, 'r') as f:
                config_file_data = f.read()
        except:
            logging.error("open wer config file for reading failed: %s", wer_config_file_path)
            return 2, "open wer config file for reading failed"

    # answer file
    answer_file_path = __normalize_path(answer_file_path)
    try:
        with open(answer_file_path, 'rb') as f:
            answer_file_data = f.read()
    except:
        logging.error("open answer file for reading failed: %s", answer_file_path)
        return 2, "open answer file for reading failed"

    # recognition result
    recognition_file_path = __normalize_path(recognition_file_path)
    try:
        with open(recognition_file_path, 'rb') as f:
            result_file_data = f.read()
    except:
        logging.error("open recognition result file for reading failed: %s", recognition_file_path)
        return 2, "open recognition result file for reading failed"

    net_start = time.time() * 1000
    retry_counter = 0
    while retry_counter < RETRY_LIMIT:
        retry_counter += 1
        try:
            # Create a socket (SOCK_STREAM means a TCP socket)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
                # Connect to server and send data
                conn.settimeout(CONNECTION_TIMEOUT)
                conn.connect((SERVER_IP, SERVER_PORT))

                # prepare data
                # 4B | 4B | zipped answer data | 4B | zipped result data | 4B | zipped conf data
                logging.debug("answer file data length: %d", len(answer_file_data))
                zipped_answer_file_data = zlib.compress(answer_file_data, 9)
                logging.debug("answer file data after compressed length: %d", len(zipped_answer_file_data))
                logging.debug("result file data length: %d", len(result_file_data))
                zipped_result_file_data = zlib.compress(result_file_data, 9)
                logging.debug("result file data after compressed length: %d", len(zipped_result_file_data))

                if config_file_data is None:
                    merged_data = __merge_data_in_chunk([zipped_answer_file_data, zipped_result_file_data])
                else:
                    logging.debug("config file data length: %d", len(config_file_data))
                    zipped_config_file_data = zlib.compress(config_file_data, 9)
                    logging.debug("config file data after compressed length: %d", len(zipped_config_file_data))
                    merged_data = __merge_data_in_chunk(\
                        [zipped_answer_file_data, zipped_result_file_data, zipped_config_file_data])
                    
                __send_data_in_chunk(conn, merged_data)

                # parse response
                # 4B | 4B | json object(errcode, errdesc) | 4B | zipped wer result | 4B | zipped wer output
                response_buf = __recv_data_all(conn, 4)
                response_len = int.from_bytes(response_buf, byteorder='little', signed=False)
                logging.debug("response data length: %d", response_len)
                response_data = __recv_data_all(conn, response_len)

                byte_offset = 0
                status_info_len = int.from_bytes(\
                    response_data[byte_offset: byte_offset + 4], byteorder='little', signed=False)
                logging.debug("status json length: %d", status_info_len)
                byte_offset += 4
                status_info_data = response_data[byte_offset: byte_offset + status_info_len]
                status_info_dict = json.loads(status_info_data)
                if status_info_dict[KEY_ERRCODE] != 0:
                    logging.error("WER request error: %d - %s", \
                        status_info_dict[KEY_ERRCODE], status_info_dict[KEY_ERRDESC])
                    return 3, "WER request error"

                byte_offset += status_info_len
                zipped_wer_result_len = int.from_bytes(\
                    response_data[byte_offset: byte_offset + 4], byteorder='little', signed=False)
                logging.debug("zipped wer result length: %d", zipped_wer_result_len)
                byte_offset += 4
                zipped_wer_result_data = response_data[byte_offset: byte_offset + zipped_wer_result_len]
                wer_result_data = zlib.decompress(zipped_wer_result_data)
                logging.debug("unzipped wer result length: %d", len(wer_result_data))
                try:
                    with open(wer_result_path, 'wb') as f:
                        f.write(wer_result_data)
                except:
                    logging.error("open WER result file for writing failed: %s", wer_result_path)
                    return 3, "open WER result file for writing failed"
                logging.debug("wrote WER result file: %s", wer_result_path)

                byte_offset += zipped_wer_result_len
                zipped_wer_output_len = int.from_bytes(\
                    response_data[byte_offset: byte_offset + 4], byteorder='little', signed=False)
                logging.debug("zipped wer output length: %d", zipped_wer_output_len)
                byte_offset += 4
                if zipped_wer_output_len > 0:
                    zipped_wer_output_data = response_data[byte_offset: byte_offset + zipped_wer_output_len]
                    wer_output_data = zlib.decompress(zipped_wer_output_data)
                    logging.debug("unzipped wer output length: %d", len(wer_output_data))
                    try:
                        with open(wer_console_output_path, 'wb') as f:
                            f.write(wer_output_data)
                    except:
                        logging.error("open WER console output file for writing failed: %s", wer_console_output_path)
                        return 3, "open WER console output file for writing failed"
                    logging.debug("wrote WER console output file: %s", wer_console_output_path)
                else:
                    logging.debug("WER console output is empty")
                    
            break

        except socket.timeout:
            traceback.print_exc()
            conn.close()
            if retry_counter != RETRY_LIMIT:
                logging.error("network connection timeout out, retry: %d", retry_counter)
            continue

    net_end = time.time() * 1000
    logging.debug("network related process time: %f ms", net_end - net_start)

    return 0, "OK"

if __name__ == "__main__":
    if len(sys.argv) < 5:
        logging.error("usage: python3 %s answer_file_path recognition_result_path wer_result_path wer_console_output \
wer_config_file[OPTIONAL]", sys.argv[0])
        exit(1)
    
    logging.info("WER parameters:")
    logging.info("answer file path: %s", sys.argv[1])
    logging.info("recognition result path: %s", sys.argv[2])
    logging.info("wer result path: %s", sys.argv[3])
    logging.info("wer console output path: %s", sys.argv[4])
        
    start_time = time.time() * 1000
    if len(sys.argv) == 6:
        logging.info("wer config path: %s", sys.argv[5])
        status, info = wer(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    else:
        status, info = wer(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

    end_time = time.time() * 1000
    logging.info("total process time: %f ms", end_time - start_time)

    exit(status)