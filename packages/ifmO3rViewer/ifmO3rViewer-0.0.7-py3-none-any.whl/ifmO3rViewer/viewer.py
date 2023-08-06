# %%
import numpy as np
import sys, os
import multiprocessing as mp
import argparse
import logging
import logging.handlers
import time
import signal
from queue import Empty
from pyqtgraph.Qt import QtGui
from ifmO3rViewer.gui import MainWindow

from ifmO3r.pcic import ImageClient

def setup_logger(level=logging.INFO):
    formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    logger = logging.getLogger()
    logger.setLevel(level)

    fileHandler = logging.handlers.WatchedFileHandler('client.log')
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)


def O3DClient(stop, queue, image_height, image_width, address, port, loglevel):
    setup_logger(loglevel)
    logger = logging.getLogger(__file__)
    try:
        while not stop.is_set():
            logger.info('connecting to %s:%s', address, port)
            try:
                pcic = ImageClient(address, port, isO3R=True)
                framecnt = 0
                while not stop.is_set():
                    frame = pcic.readNextFrame()

                    #image_width = frame['im_width']
                    #image_height = frame['im_height']
                    if(len(frame['confidence']) <= 38528):
                        image_width=224
                    else:
                        image_width = 215*2
                    image_height = 172

                    conf = np.frombuffer(frame['confidence'], dtype='uint8').reshape(image_height, image_width)
                    invalid = (np.bitwise_and(conf, 1) == 1)

                    # amplitude image
                    amp = np.frombuffer(frame['amplitude'], dtype='uint16').reshape(image_height, image_width)
                    amp = (amp * 100. / 65535.).astype(np.float)

                    # distance image
                    dist = np.frombuffer(frame['distance'], dtype='uint16').reshape(image_height, image_width)
                    dist = dist.astype(np.float) / 1000.0
                    dist[invalid] = np.nan

                    # point cloud
                    x = np.frombuffer(frame['x'], dtype='int16').reshape(image_height, image_width) / 1000.0
                    y = np.frombuffer(frame['y'], dtype='int16').reshape(image_height, image_width) / 1000.0
                    z = np.frombuffer(frame['z'], dtype='int16').reshape(image_height, image_width) / 1000.0
                    x[invalid] = np.nan
                    y[invalid] = np.nan
                    z[invalid] = np.nan

                    queue.put((framecnt, amp, dist, conf, x, y, z), timeout=0.001)
                    framecnt += 1
                pcic.close()
                while queue.qsize() > 0:
                    try:
                        queue.get(timeout=0.001)
                    except Empty:
                        pass
            except ConnectionRefusedError as ex:
                logger.debug('error while connecting to server at %s:%s', address, port)
                time.sleep(1)
            except KeyboardInterrupt:
                raise
            except Exception as ex:
                logger.exception('unexpected exception caught in viewer.')
                time.sleep(1)
    except KeyboardInterrupt:
        logger.info("stopping data source")
        queue.put(None)

def startGUI(ip='127.0.0.1',port=50012,loglevel='INFO',image_width=224,image_height=172):
    mp.freeze_support()
    stop = mp.Event()
    queue = mp.Queue()
    p = mp.Process(target=O3DClient, args=(stop, queue, image_height, image_width, ip, port, loglevel))
    p.start()

    app = QtGui.QApplication(sys.argv)
    window = MainWindow(stop, queue)
    window.show()
    # the process p will catch the keyboard interrupt and afterwards the gui is shutdown
    # kindly over DataSource.queueClosed
    # we don't want KeyboardInterrupts in the Qt slots
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    sys.exit(app.exec_())

def main():
    parser = argparse.ArgumentParser(description='ifm PCIC Viewer', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-ip', type=str, default='127.0.0.1', help='listen address')
    parser.add_argument('-port', type=int, default=50012, help='listen port')
    parser.add_argument('-loglevel', type=str, default='INFO', help='log level to use')
    parser.add_argument('-width', type=int, default=224, help='image width')
    parser.add_argument('-height', type=int, default=172, help='image height')

    args = parser.parse_args()

    startGUI(args.ip, args.port, args.loglevel, args.width, args.height)

if __name__ == "__main__":
    mp.freeze_support()
    main()

# %%
