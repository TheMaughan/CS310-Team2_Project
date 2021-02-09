# Asteroids
Under Construction

This is a class project currently, the goal is to have the base elements of the classic Asteroids game.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

BELOW IS THE CS241 BASE REQUIREMENTS FOR THIS PROGRAM (copied and pasted from CS241 assignment requirements):

OO Programming and Data Structures | CS 241
Asteroids Project Description
Overview

For this assignment, we will implement a version of the classic arcade game Asteroids.
Instructions

We will be using the same arcade library as previous projects. Please refer to their instructions for more information about setting up and configuring your development environment.

The following shows the game in action:
Asteroids Game
Game Rules and Specification

    Ship

        The ship obeys the laws of motion. When in motion, the ship will tend to stay in motion.

        Note that the angle or orientation of the ship can be different than the direction it is traveling.

        The right and left arrows rotate the ship 3 degrees to either direction.

        The up arrow will increase the velocity in the direction the ship is pointed by 0.25 pixels/frame.

        For collision detection, you can assume the ship is a circle of radius 30.

    Bullets

        Pressing space bar will shoot a bullet.

        Bullets should start with the same velocity of the ship (speed and direction) plus 10 pixels per frame in the direction the ship is pointed. This means if the ship is traveling straight up, but pointed directly to the right, the bullet will have a velocity that is at an angle up and to the right (starting with an upward velocity from the ship, and adding to it a velocity to the right because of the direction the ship is pointed).

        There is no limit to the number of bullets that can be fired.

        Bullets only live for 60 frames, after which they should "die" and be removed from the game.

        For collision detection, you can assume that bullets have a radius of 30

    Asteroids

        There are 3 types of asteroids in the game:

        Large Asteroids

            Moves at 1.5 pixels per frame, at a random initial direction.

            Rotates at 1 degree per frame.

            For collision detection, can be treated as a circle with radius 15.

            If a large asteroid gets hit, it breaks apart and becomes two medium asteroids and one small one.

            The first medium asteroid has the same velocity as the original large one plus 2 pixel/frame in the up direction.

            The second medium asteroid has the same velocity as the original large one plus 2 pixel/frame in the down direction.

            The small asteroid has the original velocity plus 5 pixels/frame to the right.

        Medium Asteroid

            Rotates at -2 degrees per frame.

            For collision detection, can be treated as a circle with radius 5.

            If hit, it breaks apart and becomes two small asteroids.

            The small asteroid has the same velocity as the original medium one plus 1.5 pixels/frame up and 1.5 pixels/frame to the right.

            The second, 1.5 pixels/frame down and 1.5 to the left.

        Small Asteroid

            Rotates at 5 degrees per frame.

            For collision detection, can be treated as a circle with radius 2.

            If a small asteroid is hit, it is destroyed and removed from the game.

    Other game rules

        The game begins with 5 large asteroids.

        All elements (ship, bullets, asteroids) should "wrap" around the edges of the screen. In other words, if an object goes off the right edge of the screen, it should appear on the left edge.

Architectural Design

The entire program will need to be implemented using the principles of encapsulation. Thus, you need to think about the different components (classes) that you will need in the game, and their various actions (methods) and properties (member variables). Before you start programing, you will need to produce UML class diagrams for each of the classes you will be using. Please pay special attention to the design of these components, so they can be as general-purpose as possible.

In addition, for this project you will be expected to use the principles of inheritance, polymorphism, and abstract methods. You should identify code that is shared among classes and put it in a common base class.
Getting Started

You will use the same framework and classes that you used for Pong and Skeet.

With each project, you have written more of the logic of the game and (hopefully) have become more familiar with the concepts of objects interacting, the game loop, etc. At this point, using the previous projects as a guide, you will start mostly from scratch to create your Asteroids project. A starter program with a few functions to help handle the keystrokes, etc., is a available at: asteroids.py.
Using the Graphics

You can either use your own pictures for the game or the standard ones provided (ship.png, laser.png, big.png, medium.png, small.png). Drawing these in Arcade are a little different from the Skeet game because these pictures have diffent height and widths. The game instructions above identify a radius for each object for the purpose of collision detection only. Use the code sample below to use the height and width of the actual picture:


		# This will load the graphics file into an arcade texture object
		texture = arcade.load_texture("ship.png")
		
		# This will draw the texture object.  The first 2 parameters describe where the 
		# object should be drawn.  The next 2 parameters describe the width and height of
		# the object.  In this program, we want to draw the actual size of the picture.  
		# We can do this by using the width and height member data in the texture object.  
		# The next parameter specifies the texture object we are drawing.  Since we have to 
		# rotate the object during game play, we will specify an additional rotation parameter.
		arcade.draw_texture_rectangle(self.center.x, self.center.y, texture.width, texture.height, texture, self.angle)

Milestones

Starting a large project like this can sometimes seem overwhelming. So to help guide you through this process, a milestone deliverable will be required at the end of each week. More detailed information is contained below, but in short these milestones will require:

    Milestone 1 - Stub functions and floating rocks

    Milestone 2 - Ship and bullets working

    Milestone 3 - Collisions and asteroids breaking apart

    Final Project - Finish the project and add extra features

Assignments

You have four weeks to complete this project, with milestone submissions due along the way. Please note that this is a challenging project that will require you to apply several new and challenging topics. If you wait until the last week, you will not have time to complete the project.

This project will be broken up into the following assignment submissions:

    08 Prove : Milestone 1 - Asteroids -- In the first week you will implement the first part of the game. You will submit a quiz to identify which functionality you have completed. The first milestone should accomlish at least the following:
        Create a draft UML diagram showing the relationships between the classes.
        Create the classes with functions stubbed out (use "pass"). Your code should open the game window.
        Large rocks (asteroids) appear on the screen and move
    09 Prove : Milestone 2 - Asteroids -- In the second week you will implement the second part of the game. You will submit a quiz to identify which functionality you have completed. The second milestone should accomlish at least the following:
        The ship moves correctly on the screen.
        Bullets can be fired based on the angle and velocity of the ship.
        Bullets disappear (die) after 60 frames.
        All objects on the screen (ship, bullets, rocks) wrap around the screen.
        The FlyingObject class is completely implemented (necessary for the above items to work).
    10 Prove : Milestone 3 - Asteroids -- In the third week you will implement the third part of the game. You will submit a quiz to identify which functionality you have completed. The third milestone should accomlish at least the following:
        Large rocks disappear and break into 2 Medium and 1 Small (with correct angle and speed) when hit by a bullet.
        Medium rocks disappear and break into 2 Small (with correct angle and speed) when hit by a bullet.
        Small rocks disappear and do not break apart when hit by a bullet.
        Ship disappears (dies) when hit by a rock.
        Dead rocks and bullets are removed from the lists.
    11 Prove : Project - Asteroids -- In the fourth week you will submit your completed game. You will submit a compressed file (eg. zip, 7z, or rar formats) containing the python file and all image files (e.g. PNG, GIF, JPG) into the assignment dropbox. You must also include a UML diagram (PDF) showing all classes and their relationships. The following requirements will be checked when grading:
        The game starts with 5 large rocks (asteroids) placed randomly on the board that move and rotate.
        Ship thrusts forward with up arrow and and will rotate with left and right arrows.
        Bullets are fired based on the angle and velocity of the ship and will die after 60 frames.
        Large rocks and medium rocks split into correct rocks with correct location and speed.  Small rocks do not split.
        All objects wrap around the screen.
        Clean code with detailed comments included for all functions.
        Appropriate use of inheritance and abstract functions (polymorphism must be used for at least hitting rocks). Remember that the owner of the rocks (i.e. the game class) should not need to determine what kind of rock was hit.
        Appropriate use of lists to store and manipulate objects in the game (e.g. rocks and bullets).
        Appropriate use of constructors (__init__) and the super() function.
        At least one appropriate use of properties for member data that need to be validated (i.e. kept in range).
        UML diagram matches the code delivered.
        Bonus points for creativity will be awarded for projects that add new functionality to the game.

