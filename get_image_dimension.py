import cv2

# Load the image
image_path = "DALL%C2%B7E%202023-05-08%2015.20.39%20-%20Plastic%20bottle%20on%20top%20of%20a%20car%20in%20a%20forest.png"
image = cv2.imread(image_path)

# Get the dimensions of the image
height, width, channels = image.shape

print("Image Dimensions:")
print("Width:", width)
print("Height:", height)
print("Number of Channels:", channels)
