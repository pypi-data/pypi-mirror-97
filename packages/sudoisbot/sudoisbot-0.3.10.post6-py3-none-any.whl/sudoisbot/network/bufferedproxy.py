#!/usr/bin/python3 -u

from collections import deque, defaultdict
import os
import json
import time

from loguru import logger
import zmq


def proxy_buffering(frontend_addr, backend_addr, capture_addr=None):
    context = zmq.Context()

    # facing publishers
    frontend = context.socket(zmq.SUB)
    frontend.setsockopt(zmq.SUBSCRIBE, b'')
    frontend.bind(frontend_addr)

    # facing services (sinks/subsribers)
    backend = context.socket(zmq.XPUB)
    backend.bind(backend_addr)
    # infrom publishers of a new sink
    #backend.setsockopt(ZMQ_XPUB_VERBOSE, 1)

    logger.info(f"zmq pubsub proxy: {frontend_addr} -> {backend_addr}")
    if capture_addr:
        capture = context.socket(zmq.PUB)
        capture.bind(capture_addr)
        logger.info(f"zmq capture: {capture_addr}")
    else:
        capture = None


    poller = zmq.Poller()
    poller.register(frontend, zmq.POLLIN)
    poller.register(backend, zmq.POLLIN)
    if capture:
        poller.register(backend, zmq.POLLIN)


    # send \x01 to all publishers when they connect

    lvc = dict()
    cache = defaultdict(deque)
    cache_topics = set()

    incount = 0
    outcount = 0

    for topic in cache.keys():
        csize  = len(cache[topic])
        if csize > 0:
            logger.warning(f"{topic} - {csize} cached items loaded")

    while True:
        try:
            events = dict(poller.poll(1000))
        except KeyboardInterrupt:
            logger.info("im leaving")
            break


        now = int(time.time())

        if capture:
            stats = {
                'cache_size': {
                    k.decode(): len(v) for (k, v) in cache.items()
                },
                'topics': [a.decode() for a in lvc.keys()],
                'cache_topics': [a.decode() for a in  cache_topics],
                'incount': incount,
                'outcout': outcount
            }
            capture.send_multipart([b"meta:stats", json.dumps(stats).encode()])

        if frontend in events:
            msg = frontend.recv_multipart()
            topic = msg[0]
            incount++

            #frontend.send_multipart([b"\x00rain"])

            if topic not in lvc:
                logger.info(f"caching topic {topic} that hasnt seen a listener yet")
                cache_topics.add(topic)
            lvc[topic] = msg

            if topic in cache_topics:
                #logger.debug(f"[o] cached {msg}")
                cache[topic].append(msg)
            else:
                backend.send_multipart(msg)

            if capture:
                capture.send_multipart(msg)


        if backend in events:

            msg = backend.recv_multipart()
            outcount++
            #logger.warning(f"[x] backend: {msg}")
            if msg[0][0] == 0:
                topic = msg[0][1:]
                cache_topics.add(topic)
                logger.info(f"[o] now caching {topic}")

            if msg[0][0] == 1: #'\x01'
                topic = msg[0][1:]
                if topic not in lvc:
                    # the keys of the topic dir are also a list of "known topics"
                    logger.success(f"registered {topic}")
                    lvc[topic] = None

                if topic in cache_topics:
                    csize = len(cache[topic])
                    if csize > 0:
                        logger.info(f"draning {csize} messages for {topic}")

                        while len(cache[topic]) > 0:
                            buffered = cache[topic].popleft()
                            backend.send_multipart(buffered)



                    logger.success(f"stopped caching {topic}")
                    cache_topics.discard(topic)


                elif topic in lvc and lvc[topic] is not None:
                    cached = lvc[topic]
                    backend.send_multipart(cached + [b"cached"])
                    logger.success(f"[>] lvc sent for {topic}")


                #frontend.send(msg)
                #logger.success(f"[>] backend: {msg}")


        if capture in events:
            logger.warning(f"capture: {capture.recv_mutlipart(msg)}")


    frontend.close()
    backend.close()
    context.close()


def capture(capture_addr):
    capture_port = capture_addr.split(":")[-1]
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.setsockopt(zmq.SUBSCRIBE, b'')
    addr = f"tcp://127.0.0.1:{capture_port}"
    socket.connect(addr)
    logger.info("connecting to " + addr)

    import pprint
    import sys
    while True:

        r = socket.recv_multipart()
        #pprint.pprint(r[1].decode())
        #print(r)
        jdata = json.loads(r[1].decode())

        if "cache_size" in jdata:
            print(r[1].decode(), end="\n")
        sys.stdout.flush()
        #print("")


def main(args, config):
    capture_addr = config.get('capture_addr')
    if args.capture:
        return capture(capture_addr)

    return proxy_buffering(
        config['frontend_addr'], config['backend_addr'], capture_addr)
