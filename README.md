The following are code samples of mine from a combination of classes and personal projects. Please don't hesitate to email: lding@pdx.edu for further questions or clarifications. All code should be considered open source, and free to use.

Edit 6/16/19-

Uploaded three projects from Spring 2019 quarter of MS program. All project code & write ups included. 

	Static Shots (OpenCV)- Project was an independenet research project for Professor Feng Liu for Computational Photography. 'Shots' are what one typically thinks of as a scene. Research goal was to get a database of shots where the camera is not moving. Often times, it is difficult to train machine learning algorithms on video because both the camera and environment are changing (Think car cameras). Idea is to get static shots, add artificial motion, then train machine algorithms with a ground control. Heuristics of the project, which I fully developed myself, was to analyze the borders of a shot and see if the frame is moving in unison. If all borders are moving, then shot is non-static. If 3/4 of the borders are still, the shot is classified as static. Program done in OpenCV for Python.
	
	Tesla Database (SQL)- Project I did with my partner Pat Rademacher for Database class. I'm a fan of Tesla vehicles, and we decided to create a Tesla database in SQL. Developed web scrapping tools using Beautiful Soup (Luke), and then automated the upload into SQL (Pat). Both parts done in Python.
	
	Class Polling (Socket Programming)- Project I did with my partner Will Mass for Internetworking Protocols. Created a multi-threaded server that could accept admin and client requests. Clients could then vote on questions, and admins did flow-control for polls and voting. Both partners covered both parts. Project was done in Python. 


A summary of the code folders can be found below:
	Typing Speed- The is a programming assignment done in C to test the user's typing speed. 
	
	Floating Point- The floating point program is done in C, and allows the user to enter a number of bits, fracs, and hex values, and returns the corresponding floating point value (in decimal).
	
	Queue & Stack- This program is written in C++, and was done as a side project. I grew tired of having to write lists and nodes for various Queue/LL/Stack applications. Decided to build a super structure to allow users to push/pop, enqueue/dequeue, in-order-insert, all using one basic code set. Can be run as a program, but really is meant as code base.
	
	Hospital Simulation- This program simulates a priority queue, and is written in C++. 

In-progress/Upcoming:
	Visual Scripting Language (Unreal 4 & C++)- Developing a visual scripting language in 3D/VR, to allow users to connect visual objects for programming, instead of learning to type. Currently have UI, object spawn & connect, and grab functionality built. Actual language interactions between objects comes Q1 2019. 
	
	Edit- Final version compiled. Presentation also loaded.
	
	Copy of latest exe can be downloaded here:
	https://drive.google.com/drive/folders/1Yk3FnhD9mROvRQaU4cRJeRdZ0z00ik1f?usp=sharing 

	Instructions:
		Move Around (WASD)
		Pick-up Objects (Move to, and press F)
		Link two objects (Press left mouse key while pointed at object 1, point at object 2 and release mouse key)
		Spawn Objects (Click 1 key, then mouse click the first or second menu object)
		Type- Hit insert, then enter. 

	
	
