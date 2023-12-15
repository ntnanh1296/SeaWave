Project Name: SeaWave

Apps:

1. User Service (Django App):

Responsible for user registration, authentication, and profile management.

Communicates with the Redis service to store and retrieve user-post mappings.

API Endpoints:

    /api/users/
        POST: Create a new user. (email, username, password (hashed), gender, birthday)
        GET: Retrieve all user profiles.
        /api/users/{userId}/
        GET: Retrieve a user profile.
        PUT: Update a user profile (token required).
        DELETE: Delete a user (token required).
    /api/users/login/
        POST: Generate JWT token for user.
    Database: PostgreSQL for saving user information.

2. Post Service (Django App):

Manages the creation, retrieval, and update of posts.

Communicates with the Redis service to store and retrieve user-post and post-photo mappings.

    API Endpoints:

        /api/posts/
            POST: Create a new post. (text, photo, author(userId), time_create, time_update) (token required)
            GET: Retrieve all posts.
        /api/posts/{postId}/
            GET: Retrieve a post.
            PUT: Update a post (token required).
            DELETE: Delete a post (token required).
        /api/posts/{postId}/likes/
            POST: Like a post (token required) if user didn't like the post and unlike the post if user already liked the post
        /api/posts/{postId}/comments/
            GET: Retrieve all comments of a post.
            POST: Comment on a post (token required).
            PUT: Edit a comment on a post (token required).
            DELETE: Delete a comment on a post (token required).

    Storage:

        Use Firebase storage to save photos of posts.
        Use Realtime database to save text content of posts.
        
        
3. Follow Service (Django App):

Manages user connections, followers, and following relationships.

    API Endpoints:

    /api/followers/
        GET: Retrieve all users followed by you. count the followers
    /api/following/
        GET: Get all users whom you followed, count the users followed

    /api/following/users/{userID}/
        POST: Follow a userID. if you not follow them and unfollow a userID if you follow them 

    Database: PostgreSQL for managing user connections.

4. Chat Service (Django App):
Manages user chat one to one or group chat
    API Endpoints:
    /api/chat/one-to-one/{userId}: 
        POST: Initiates a one-to-one chat.
    /api/chat/group/{groupId}: 
        POST: Initiates or retrieves a group chat.
    /api/chat/send-message: 
        POST: Sends a message to a user or group.
    /api/chat/messages/{chatId}: Retrieves chat history for a user or group.

5. Notification Service (Django App):

    Handles real-time notifications for activities such as likes, comments, and follows.

    API Endpoints:

    Define WebSocket or long-polling endpoints for real-time notifications.

6. Redis Service:

Responsible for storing and retrieving mappings:
User ID to Post IDs (user_posts:{userId}).
Post ID to Photo IDs (post_photos:{postId}).
Post ID to comment IDs (post_comment:{postID}).
User ID to comment IDs (post_comment:{userID}).
# SeaWave# SeaWave
