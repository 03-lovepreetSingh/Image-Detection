import cv2
import numpy as np
from sklearn.cluster import KMeans

def detect_tampering(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply K-means clustering to the grayscale image
    kmeans = KMeans(n_clusters=2)
    labels = kmeans.fit_predict(gray.reshape(-1, 1))

    # Reshape the labels array to the shape of the gray image
    labels = labels.reshape(gray.shape)

    # Create a binary mask based on the cluster labels
    mask = np.where(labels == 1, 255, 0).astype(np.uint8)

    # Find contours in the binary mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If there are any contours, the image has been tampered with
    if len(contours) > 0:
        return True, mask
    else:
        return False, mask

if __name__ == "__main__":
    image_path = "test01.jpg"  #### UPDATE THIS PATH WITH THE PATH IN FRONT-END
    is_tampered, mask = detect_tampering(image_path)
    if is_tampered:
        print("The image has been tampered with.")
        # Display the binary mask for visualization
        cv2.imshow("Mask", mask)
        cv2.waitKey(5000)  # Wait for 5 seconds (5000 milliseconds)
        cv2.destroyAllWindows()
    else:
        print("The image has not been tampered with.")
