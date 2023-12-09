

document.addEventListener('DOMContentLoaded', function() {

  function previewMedia(event) {
    const previewContainer = document.getElementById('media-preview');
    previewContainer.innerHTML = '';
  
    const file = event.target.files[0];
  
    if (file) {
        const reader = new FileReader();
  
        reader.onload = function (e) {
            const previewElement = document.createElement('img');
            previewElement.classList.add('post-image');
            previewElement.src = e.target.result;
            previewContainer.appendChild(previewElement);
        };
  
        reader.readAsDataURL(file);
    }
  }
  
    const mediaInput = document.getElementById('id_media');
    mediaInput.addEventListener('change', previewMedia);

  
    const likeButtons = document.querySelectorAll('.like-button');
    const shareButtons = document.querySelectorAll('.share-button');
    const commentButtons = document.querySelectorAll('.comment-button');

    likeButtons.forEach((button) => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            event.stopPropagation();

            const postId = button.dataset.postId;
            const likeCountElement = document.querySelector(`#like-count-${postId}`);

            fetch(`/posts/${postId}/like/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({
                    post_id: postId,
                }),
            })
            .then((response) => response.json())
            .then((data) => {
                likeCountElement.textContent = data.like_count;
                if (data.is_liked) {
                    button.textContent = 'Unlike';
                } else {
                    button.textContent = 'Like';
                }
            })
            .catch((error) => {
                console.log(error);
            });
        });
    });


    shareButtons.forEach((button) => {
        button.addEventListener('click', (event) => {
            event.stopPropagation();

            const postId = button.dataset.postId;
            const shareCountElement = document.querySelector(`#share-count-${postId}`);

            fetch(`/posts/${postId}/share/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
            })
            .then((response) => response.json())
            .then((data) => {
            shareCountElement.textContent = data.share_count;

            button.textContent = 'Shared';
            button.disabled = true;
            })
            .catch((error) => {
            console.log(error);
            });
        });
    });

    commentButtons.forEach((button) => {
        button.addEventListener('click', handleCommentButtonClick);
    });
    
    function handleCommentButtonClick(event) {
        event.preventDefault();
        event.stopPropagation();
    
        const postId = event.target.dataset.postId;
        const commentSection = document.getElementById(`comment-section-${postId}`);
        const isCommentSectionVisible = commentSection.style.display !== 'none';
    
        if (isCommentSectionVisible) {
            commentSection.style.display = 'none';
        } else {
            fetch(`/posts/${postId}/get_comments/`)
                .then((response) => response.json())
                .then((comments) => {
                    renderComments(comments, commentSection);
                    commentSection.style.display = 'block';
                    likeCommentEvent();
                    commentActionDropdownEvent();
                    commentActionButtonEvent();
                })
                .catch((error) => {
                    console.log(error);
                });
        }
    }
    
    function renderComments(comments, container) {
        container.innerHTML = '';
    
        comments.forEach((comment) => {
            const commentElement = document.createElement('div');
            commentElement.classList.add('comment');
    
            commentElement.innerHTML = `
                <div class="comment-detail-container">
                    <img class="comment-avatar" src="${comment.avatar_url}" alt="User Avatar">
                    <div class="comment-detail">
                        <div class="comment-detail-form">
                            <p class="comment-author">${comment.user}</p>
                            <p>${comment.text}</p>
                        </div>    
                        <div class="comment-sub-detail">
                            <p class="comment-timestamp" data-comment-created="${comment.created_at}"></p>
                            <button class="like-comment-button" data-comment-id="${comment.id}">Like</button>
                            <p id="like-count-comment-${comment.id}" style="font-size: 12px;">${comment.like_count}</p>
                        </div>
                    </div>
                    ${comment.is_authenticated && comment.is_comment_author ? `
                        <div class="comment-actions-dropdown">
                            <button class="comment-actions-btn">&#x2026;</button>
                            <div class="comment-actions-content">
                                <a href="{% url 'edit-comment' %}?id=${comment.id}" class="comment-action">Edit</a>
                                <a href="{% url 'delete-comment' %}?id=${comment.id}" class="comment-action">Delete</a>
                            </div>
                        </div>` : ''}
                </div>
            `;
            container.appendChild(commentElement);
        });
    
        updateCommentTimestamps();
    }

    function updateCommentTimestamps() {
        const commentTimestamps = document.querySelectorAll('.comment-timestamp');
    
        commentTimestamps.forEach((timestampElement) => {
            const createdTimestamp = new Date(timestampElement.dataset.commentCreated);
            const currentTimestamp = new Date();
    
            const timeDifferenceInSeconds = Math.floor((currentTimestamp - createdTimestamp) / 1000);
    
            let displayText = '';
    
            if (timeDifferenceInSeconds < 60) {
                displayText = `${timeDifferenceInSeconds} seconds`;
            } else if (timeDifferenceInSeconds < 3600) {
                const minutes = Math.floor(timeDifferenceInSeconds / 60);
                displayText = `${minutes} ${minutes === 1 ? 'minute' : 'minutes'}`;
            } else if (timeDifferenceInSeconds < 86400) {
                const hours = Math.floor(timeDifferenceInSeconds / 3600);
                displayText = `${hours} ${hours === 1 ? 'hour' : 'hours'}`;
            } else if (timeDifferenceInSeconds < 2592000) {
                const days = Math.floor(timeDifferenceInSeconds / 86400);
                displayText = `${days} ${days === 1 ? 'day' : 'days'}`;
            } else {
                const months = Math.floor(timeDifferenceInSeconds / 2592000);
                displayText = `${months} ${months === 1 ? 'month' : 'months'}`;
            }
    
            timestampElement.textContent = displayText;
        });
    }
    

    function likeCommentEvent() {
        const likeCommentButtons = document.querySelectorAll('.like-comment-button');
        likeCommentButtons.forEach((button) => {   
            button.addEventListener('click', (event) => {
                event.preventDefault();
    
                const commentId = button.dataset.commentId;
                const likeCountCommentElement = document.querySelector(`#like-count-comment-${commentId}`);
                
                fetch(`/comments/${commentId}/like/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                })
                .then((response) => response.json())
                .then((data) => {
                    likeCountCommentElement.textContent = data.like_count;
    
                    if (data.is_liked) {
                        button.textContent = 'Unlike';
                    } else {
                        button.textContent = 'Like';
                    }
                })
                .catch((error) => {
                    console.log(error);
                });
            });
        });
    }

    function commentActionDropdownEvent() {
        document.addEventListener("click", function (event) {
            const dropdowns = document.getElementsByClassName("comment-actions-content");
            for (const dropdown of dropdowns) {
                if (!event.target.matches('.comment-actions-btn') && !dropdown.contains(event.target)) {
                    dropdown.style.display = 'none';
                }
            }
        });
    }

    function commentActionButtonEvent() {
        document.addEventListener("click", function (event) {
            const dropdownBtns = document.getElementsByClassName("comment-actions-btn");
            for (const dropdownBtn of dropdownBtns) {
                const dropdown = dropdownBtn.nextElementSibling;
                if (event.target === dropdownBtn) {
                    dropdown.style.display = (dropdown.style.display === 'block') ? 'none' : 'block';
                } else {
                    dropdown.style.display = 'none';
                }
            }
        });
    }
});

document.addEventListener("click", function (event) {
    const dropdowns = document.getElementsByClassName("post-actions-content");
    for (const dropdown of dropdowns) {
        if (!event.target.matches('.post-actions-btn') && !dropdown.contains(event.target)) {
            dropdown.style.display = 'none';
        }
    }
});

document.addEventListener("click", function (event) {
    const dropdownBtns = document.getElementsByClassName("post-actions-btn");
    for (const dropdownBtn of dropdownBtns) {
        const dropdown = dropdownBtn.nextElementSibling;
        if (event.target === dropdownBtn) {
            dropdown.style.display = (dropdown.style.display === 'block') ? 'none' : 'block';
        } else {
            dropdown.style.display = 'none';
        }
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const hidePostButtons = document.querySelectorAll('.hide-post-button');

    hidePostButtons.forEach((button) => {
        button.addEventListener('click', (event) => {
            event.preventDefault();

            const postId = button.dataset.postId;
            const postContainer = document.querySelector(`.post-container[data-post-id="${postId}"]`);

            // Hide the post container
            console.log('Script loaded');
            postContainer.style.display = 'none';
            console.log('Script loaded');

            // TODO: Send an AJAX request to the server to mark the post as hidden for the current user
        });
    });
});