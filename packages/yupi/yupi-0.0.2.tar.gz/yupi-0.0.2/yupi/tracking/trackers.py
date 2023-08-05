import cv2
import json
import numpy as np
from yupi.tracking.algorithms import Algorithm, resize_frame
from yupi.tracking.affine_estimator import get_affine


class ROI():
    """
    Region of interest.

    Region that can be tracked by the algorithms throughout the sequence of
    image frames.

    Parameters
    ----------
    size : tuple of float
        Size of the region of interest.

        If both tuple's values are grater than 1 then they are rounded and
        taken as pixels. Otherwise, if both values are less than 1, the
        size is taken relative to the video frame size.
    init_mode : str, optional
        ROI's initialization mode. (Default is 'manual').

        Defines the way ROI initial position is setted.

        The ``init_mode`` parameter can be manual or center. These modes are
        stored in ``ROI.MANUAL_INIT_MODE`` and ``ROI.CENTER_INIT_MODE``.
    scale : float, optional
        Scale of the sample frame to set ROI initial position if
        ``init_method`` is set to ``'manual'``. (Default is 0.5).

    Attributes
    ----------
    width : float
        Width of the ROI.

        If the width value is between 0 and 1 then this is taken relative
        to the frames. Otherwise it is a rounded value and taken as pixels.
    height : float
        Height of the ROI.

        If the height value is between 0 and 1 then this is taken relative
        to the frames. Otherwise it is a rounded value and taken as pixels.
    init_mode : str
        ROI's initialization mode.
    scale : float
        Scale of the sample frame to set ROI initial position if
        ``init_method`` is set to ``'manual'``.

    Examples
    --------
    >>> ROI((120, 120), ROI.MANUAL_INIT_MODE)
    ROI: size=(120, 120) init_mode=manual scale=0.5

    Raises
    ------
    ValueError
        If any size value is negative.
    ValueError
        If one of the size value is grater than 1 and the other is less than 1.
    ValueError
        If ROI initialization mode is neither ``'manual'`` or ``'center'``.
    """

    MANUAL_INIT_MODE = 'manual'
    """Manual initialization mode for the ROI"""
    CENTER_INIT_MODE = 'center'
    """Center initialization mode for the ROI"""

    def __init__(self, size: tuple, init_mode: str = MANUAL_INIT_MODE,
                 scale: float = 0.5):

        if size[0] <= 0 or size[1] <= 0:
            raise ValueError("ROI's size values must be positives")

        # TODO: check for a more pythonic way to do this comprobation
        if (size[0] < 1 and size[1] > 1) or \
           (size[0] > 1 and size[1] < 1):
            raise ValueError(size)  # TODO: write error message here

        if init_mode != ROI.CENTER_INIT_MODE and \
           init_mode != ROI.MANUAL_INIT_MODE:
            raise ValueError(f"ROI '{init_mode}' initialization mode unknown")

        self.width, self.heigh = size
        self.init_mode = init_mode
        self.scale = scale
        self.__prev_cXY = None, None
        self.__cXY = None, None
        self.__global_heigh, self.__global_width = None, None

    # this repr could change
    def __repr__(self):
        return 'ROI: size=({}, {}) init_mode={} scale={}' \
            .format(self.width, self.heigh, self.init_mode, self.scale)

    def _recenter(self, centroid: tuple) -> tuple:
        """
        Recenters ROI position.

        Parameters
        ----------
        centroid : tuple of int
            New center of the ROI.

        Returns
        -------
        cX, cY : int
            Center of the ROI.
        """

        # get the centroid refered to the roi
        cX_roi, cY_roi = centroid

        # get the centroid refered to the full image
        cX = self.__prev_cXY[0] - int(self.width/2) + cX_roi
        cY = self.__prev_cXY[1] - int(self.heigh/2) + cY_roi

        self.__cXY = cX, cY

    def __get_bounds(self) -> tuple:
        """
        ROI's bounds.

        Calculates the ROI's bounds according to its center, width, height and
        the global bounds.

        Returns
        -------
        xmin : int
            Mnimum bound on X axis.
        xmax : int
            Maximun bound on X axis.
        ymin : int
            Mnimum bound on Y axis.
        ymax : int
            Maximum bound on Y axis.
        """

        cX, cY = self.__cXY
        half_width, half_height = int(self.width/2), int(self.heigh/2)
        xmin = max(cX - half_width, 0)
        xmax = min(cX + half_width, self.__global_width)
        ymin = max(cY - half_height, 0)
        ymax = min(cY + half_height, self.__global_heigh)
        return xmin, xmax, ymin, ymax

    def __center_init(self, frame: np.ndarray) -> tuple:
        """
        Initialize ROI using center initialization mode.

        Parameters:
        frame : np.ndarray
            Frame used as reference to initialize ROI position at its center.

        Returns
        -------
        tuple of int
            Center of the ROI.
        """

        self.__global_heigh, self.__global_width = frame.shape[:2]
        self.__cXY = int(self.__global_width/2), int(self.__global_heigh/2)
        return self.__cXY

    # TODO: check for 'win2_name' utility. Maybe it it should be 'ROI' as
    # default so there is no need to pass it as a parameter
    def __manual_init(self, frame: np.ndarray, name: str,
                      win2_name: str = 'ROI') -> tuple:
        """
        Initialize ROI using manual initialization mode.

        Parameter
        ---------
        frame : np.ndarray
            Frame used as reference to initialize ROI position manually.
        name : str
            Name of the tracking object.

        Returns
        -------
        tuple of int
            Center of the ROI.
        """

        win1_name = 'Click on the center of {} to init roi'.format(name)

        self.__global_heigh, self.__global_width = frame.shape[:2]

        frame_ = resize_frame(frame, scale=self.scale)
        cv2.imshow(win1_name, frame_)

        # callback handler to manually set the roi
        def on_click(event, x, y, flags, param):

            if event == cv2.EVENT_LBUTTONDOWN:
                # global roi center coordinates
                self.__cXY = int(x / self.scale), int(y / self.scale)

                # copy of true frame and its resized version
                img = frame.copy()
                img_ = frame_.copy()

                # draw a circle in the selected pixel
                cv2.circle(img_, (x, y), 3, (0, 255, 255), 1)
                cv2.imshow(win1_name, img_)

                # get roi in the full size frame
                cv2.circle(img, self.__cXY, 3, (0, 255, 255), 1)
                roi = self.__crop(img)

                # roi padding just to display the new window
                padL, padR = np.hsplit(np.zeros_like(roi), 2)
                roi_ = np.hstack([padL, roi, padR])
                cv2.imshow(win2_name, roi_)

                print('ROI Initialized, now press any key to continue')

        cv2.setMouseCallback(win1_name, on_click)
        cv2.waitKey(0)
        return self.__cXY

    # TODO: check for 'name' utility. It is only use for the return message
    # I think this method should only return True/False and then handle the
    # error in the tracking scenario
    def __check_roi_init(self, name: str) -> tuple:
        """
        Checks for ROI initialization.

        Parameter
        ---------
        name : str
            Name of the tracking object.

        Returns
        -------
        bool
            Whether or not the ROI is initialized.
        str
            Information message.
        """

        if not self.__prev_cXY[0]:
            return False, "[ERROR] ROI was not Initialized " \
                            "(in {})".format(name)
        else:
            cv2.destroyAllWindows()
            return True, '[INFO] ROI was Initialized (in {})'.format(name)

    def __initialize(self, name: str, first_frame: np.ndarray) -> tuple:
        """
        Initialize ROI.

        Parameters
        ----------
        name : str
            Name of the tracking object.
        first_frame : np.ndarray
            First frame of the video.

            If ROI's initialization mode is set to ``'manual'`` this frame
            will be shown to select the tracking object center.

        Returns
        -------
        bool
            Whether or not the ROI was initialized.
        str
            Information message.
        """

        h, w = first_frame.shape[:2]
        if self.width <= 1:
            self.width *= w
        if self.heigh <= 1:
            self.heigh *= h

        # Initialize ROI coordinates manually by user input
        if self.init_mode == ROI.MANUAL_INIT_MODE:
            self.__cXY = self.__manual_init(first_frame, name)
            self.__prev_cXY = self.__cXY
        else:
            self.__cXY = self.__center_init(first_frame)
            self.__prev_cXY = self.__cXY

        return self.__check_roi_init(name)

    def __crop(self, frame: np.ndarray) -> np.ndarray:
        """
        Crops a frame according to the ROI's bounds.

        Parameters
        ----------
        frame : np.ndarray
            Frame that will be cropped.

        Returns
        -------
        window : np.ndarray
            Cropped part of the frame.
        """

        self.__global_heigh, self.__global_width = frame.shape[:2]
        # bounds of the roi
        xmin, xmax, ymin, ymax = self.__get_bounds()
        window = frame[ymin:ymax, xmin:xmax, :]
        return window


class ObjectTracker():
    """
    Tracks an object inside a ROI according to an algorithm.

    Parameters
    ----------
    name : str
        Name of the tracked object.
    algorithm : Algorithm
        Algorithm used to track the object.
    roi : ROI
        Region of interest where the object will be tracked.

    Attributes
    ----------
    name : str
        Name of the tracked object.
    algorithm : Algorithm
        Algorithm used to track the object.
    roi : ROI
        Region of interest where the object will be tracked.
    history : list of tuple
        ROI's position in every frame of the video.

    See Also
    --------
    tracking.algorithms
    """

    def __init__(self, name: str, algorithm: Algorithm, roi: ROI):
        self.name = name
        self.roi = roi
        self.history = []
        self.algorithm = algorithm

    def __init_roi__(self, frame: np.ndarray) -> tuple:
        """
        Initialize the ROI.

        Parameters
        ----------
        frame : np.ndarray
            Sample frame for ROI initialization.

            This frame will be shown for selecting the tracking object center
            if ROI's initialization mode is ``'manual'``.

        Returns
        -------
        tuple
            ROI's center position.
        """

        return self.roi._ROI__initialize(self.name, frame)

    def __track(self, frame: np.ndarray) -> tuple:
        """
        Tracks the center of the object.

        Given a new frame, the center of the object inside the ROI is
        recalculated using the selected algorithm.

        Parameters
        ----------
        frame : np.ndarray
            Frame used by the algorithm to detect the tracked object's new
            center.
        """

        # get only the ROI from the current frame
        window = self.roi._ROI__crop(frame)

        # detect the object using the tracking algorithm
        self.mask, centroid = self.algorithm.detect(window)

        # update the roi center using current ant coordinates
        self.roi._recenter(centroid)

        # update data
        self.history.append(self.roi._ROI__cXY)
        self.roi._ROI__prev_cXY = self.roi._ROI__cXY


class CameraTracker():
    """docstring for CameraTracker"""
    def __init__(self, roi):
        self.history = []
        self.mse = []
        self.roi = roi

    def __init_roi__(self, prev_frame):
        return self.roi._ROI__initialize('Camera', prev_frame)

    # track the floor
    def track(self, prev_frame, frame, ignored_regions):
        # Initialize a mask of what to track
        h, w = frame.shape[:2]
        mask = 255 * np.ones((h, w), dtype=np.uint8)

        # mask pixeles inside every ROIs
        for x0, xf, y0, yf in ignored_regions:
            mask[y0:yf, x0:xf] = 0

        p_good, aff_params, err = get_affine(prev_frame, frame,
                                             self.roi._ROI__get_bounds(),
                                             mask)
        self.features = p_good[1:]

        if err is None:
            return False, 'No matrix was estimated'

        self.history.append(aff_params)
        self.mse.append(err)

        return True, 'Camera Tracked'


class TrackingScenario():
    """docstring for TrackingScenario"""
    def __init__(self, object_trackers, camera_tracker=None, undistorter=None):
        self.object_trackers = object_trackers
        self.camera_tracker = camera_tracker
        self.iteration_counter = 0
        self.auto_mode = True
        self.undistorter = undistorter
        self.enabled = True

    def __digest_video_path(self, video_path):
        # TODO: Validate the path
        self.video_path = video_path

        # create capture object
        self.cap = cv2.VideoCapture(video_path)

        # total number of frames in the video file
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # frames per seconds
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)

        # frame width
        self.w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))

        # frame height
        self.h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.dim = (self.w, self.h)

        self.first_frame = 0

    def __undistort__(self, frame):
        if self.undistorter:
            frame = self.undistorter.fix(frame)
        return frame

    def show_frame(self, frame, show_frame_id=True):
        # cXY, region, features, frame_numb, mask
        frame = frame.copy()

        # draw region in which features are detected
        if self.camera_tracker:
            x0, xf, y0, yf = self.camera_tracker.roi._ROI__get_bounds()

            cv2.putText(frame, 'Camera Tracking region', (x0+5, yf-5),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.2, (0, 0, 255), 1,
                        cv2.LINE_AA)

            cv2.rectangle(frame, (x0, y0), (xf, yf), (0, 0, 255), 2)
            p2, p3 = self.camera_tracker.features
            # draw detected and estimated features
            for p2_, p3_ in zip(p2, p3):
                x2, y2 = np.rint(p2_).astype(np.int32)
                x3, y3 = np.rint(p3_).astype(np.int32)

                cv2.circle(frame, (x2, y2), 3, (0, 0, 0), -1)
                cv2.circle(frame, (x3, y3), 3, (0, 255, 0), -1)

        for otrack in self.object_trackers:
            # TODO: Do this better:
            # alter the blue channel in ant-related pixels
            window = otrack.roi._ROI__crop(frame)
            window[:, :, 0] = otrack.mask

            # draw a point over the roi center and draw bounds
            x1, x2, y1, y2 = otrack.roi._ROI__get_bounds()
            cv2.circle(frame, otrack.roi._ROI__cXY, 5, (255, 255, 255), -1)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
            cv2.putText(frame, otrack.name, (x1+5, y2-5),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.2, (0, 255, 255), 1,
                        cv2.LINE_AA)

        if show_frame_id:
            h, w = frame.shape[:2]
            frame_id = self.iteration_counter + self.first_frame
            x_, y_ = .02, .05
            x, y = int(x_ * w), int(y_ * h)
            cv2.putText(frame, str(frame_id), (x, y),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.2, (0, 255, 255), 1,
                        cv2.LINE_AA)

        frame = resize_frame(frame)
        cv2.imshow('PYTANAL processing window', frame)
        # return frame

    def __first_iteration__(self, start_in_frame):
        # Start processing frams at the given index
        if start_in_frame:
            self.first_frame = start_in_frame
            self.cap.set(cv2.CAP_PROP_P_FRAMES, start_in_frame)

        # Capture the first frame to process
        ret, prev_frame = self.cap.read()

        # correct spherical distortion
        self.prev_frame = self.__undistort__(prev_frame)

        # Initialize the roi of all the trackers
        for otrack in self.object_trackers:
            retval, message = otrack.__init_roi__(self.prev_frame)
            if not retval:
                return retval, message

        # Initialize the region of the camera tracker
        if self.camera_tracker:
            self.camera_tracker.__init_roi__(self.prev_frame)

        # Increase the iteration counter
        self.iteration_counter += 1

        return True, '[INFO] All trackers were initialized'

    def keyboard_controller(self):
        # keyboard events
        wait_key = 0 if not self.auto_mode else 10

        k = cv2.waitKey(wait_key) & 0xff
        if k == ord('m'):
            self.auto_mode = not self.auto_mode

        if k == ord('s'):
            self.__export_data__()

        elif k == ord('q'):
            self.enabled = False

        elif k == ord('e'):
            exit()

    def __regular_iteration__(self):
        # get current frame and ends the processing when no more frames are
        # detected
        ret, frame = self.cap.read()
        if not ret:
            return False, '[INFO] All frames were processed.'

        # correct spherical distortion
        frame = self.__undistort__(frame)

        # ROI Arrays of tracking objects
        roi_array = []

        # Track every object and save past and current ROIs
        for otrack in self.object_trackers:
            roi_array.append(otrack.roi._ROI__get_bounds())
            otrack._ObjectTracker__track(frame)
            roi_array.append(otrack.roi._ROI__get_bounds())

        ret, message = self.camera_tracker.track(self.prev_frame, frame,
                                                 roi_array)
        frame_id = self.iteration_counter + self.first_frame

        if not ret:
            return False, '[Error] {} (Frame {})'.format(message, frame_id)

        # display the full image with the ant in blue (TODO: Refactor this to
        # make more general)
        self.show_frame(frame)

        # save current frame and ROI center as previous for next iteration
        self.prev_frame = frame.copy()

        # Call the keyboard controller to handle key interruptions
        self.keyboard_controller()

        # Increase the iteration counter
        self.iteration_counter += 1

        return True, '[INFO] Frame {} was processed'.format(frame_id)

    def __release_cap__(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def __export_data__(self):
        # TODO: This function needs to be rewritten to be able to handle more
        # than 1 object tracker and also to provide more general purpe semantic
        # information
        last_frame = self.first_frame + self.iteration_counter
        percent_video = 100 * last_frame / self.frame_count
        minutes_video = last_frame / self.fps / 60

        data = {
            'fps': self.fps,
            'first_frame': self.first_frame,
            'last_frame': last_frame,
            'percent': percent_video,
            'r_ac': self.object_trackers[0].history,
            'affine_params': self.camera_tracker.history,
            'mse': self.camera_tracker.mse
        }
        self.__save_data__(data, minutes_video, percent_video)

    def __save_data__(self, data, minutes=None, percent=None):
        if not (minutes or percent):
            progress = ''
        else:
            summary = f'{minutes:.1f}min' if minutes else ''
            summary += '-' if (minutes and percent) else ''
            summary += f'{percent:.1f}%' if percent else ''
            progress = '_[{}]'.format(summary)

        data_file_dir = '{}{}.json'.format(self.video_path[:-4], progress)

        with open(data_file_dir, 'w') as json_file:
            json.dump(data, json_file)

    def track(self, video_path, start_in_frame=0):
        self.__digest_video_path(video_path)

        if self.iteration_counter == 0:
            retval, message = self.__first_iteration__(start_in_frame)
            if not retval:
                return retval, message

        while self.enabled:
            retval, message = self.__regular_iteration__()
            if not retval:
                break

        if message == '[INFO] All frames were processed.':
            retval = True

        self.__release_cap__()
        self.__export_data__()
        return retval, message
