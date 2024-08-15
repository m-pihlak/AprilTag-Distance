import argparse
import video_runner

# Load image from arguments into program
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--family", type=str,
                default="tag36h11",
                help="April Tag family")
ap.add_argument("-d", "--distance", type=int,
                default=300,
                help="April Tag calibration distance in mm")
args = vars(ap.parse_args())

def main():
    video_runner.use_family(args["family"])
    video_runner.create_detector()
    video_runner.calibrate(args["distance"])
    video_runner.stream()

if __name__ == "__main__":
    main()