import cv2
import argparse


def main(image_path):
    image = cv2.imread(image_path)
    while True:
        cv2.imshow("demo", image)
        cv2.waitKey(1)
        k = cv2.waitKey(1) & 0xFF
        # press 'q' to exit
        if k == ord('q'):
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Display image.')
    parser.add_argument('--image_path', type=str, default='./image.jpg',
                        help='path of the image to be displayed.')
    args = parser.parse_args()
    main(args.image_path)
