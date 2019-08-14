# Face-and-Hand-Detection

This program detects Face and Hand. For the face I used HaardCascade. It's simple and works pretty well.
For the hand the HaardCascade method is not very reliable. That's why I used a different method.
When you run the code you will see a square on the right of your window. Your hand is only detected in it.
The way it works is the following: when there are no objects in the square you hit the SPACE key and the code
will take a picture of the square. When something new appears in it (that when wasn't there before when
taking the background picture) it will be processed by several filters to get a clean outline of it.
Those filters can be seen on the additional windows that will open upon running the code. This means that
it will capture objects other than your hand. Also a change in the background will be seen as a new object,
therefore it will be shown as one. If your background changes you can easily remove your hand and hit the
SPACE key again to capture a new background. You exit the program by hitting the ESCAPE key.
