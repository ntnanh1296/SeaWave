

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
        button.addEventListener('click', (event) => {
            event.preventDefault();
            event.stopPropagation();
    
            const postId = button.dataset.postId;
            const commentSection = document.getElementById(`comment-section-${postId}`);
            const isCommentSectionVisible = commentSection.style.display !== 'none';
    
            if (isCommentSectionVisible) {
                commentSection.style.display = 'none';
            } else {
                fetch(`/posts/${postId}/get_comments/`)
                    .then((response) => response.json())
                    .then((comments) => {
                        commentSection.innerHTML = '';
    
                        comments.forEach((comment) => {
                            const commentElement = document.createElement('div');
                            commentElement.classList.add('comment');
                            commentElement.innerHTML = `
                            <div class="comment-header">
                                <div>
                                    <p class="comment-author">${comment.user}</p>
                                    <p class="comment-timestamp">${comment.created_at}</p>
                                </div>
                                <hr>
                                {% if user.is_authenticated and comment.author == user %}
                                    <div class="comment-actions-dropdown">
                                        <button class="comment-actions-btn">&#x2026;</button>
                                        <div class="comment-actions-content">
                                            <a href="{% url 'edit-comment' ${comment.id} %}" class="comment-action">Edit</a>
                                            <a href="{% url 'delete-comment' ${comment.id} %}" class="comment-action">Delete</a>
                                        </div>
                                    </div>
                                {% endif %}
                            </div>
                            <p>${comment.text}</p>
                            <button class="like-comment-button" data-comment-id="${comment.id}">Like</button>
                            <span id="like-count-comment-${comment.id}">${comment.like_count}</span>
                            `;
                            commentSection.appendChild(commentElement);
                        });

                        commentSection.style.display = 'block';
                        likeCommentEvent();
                    })
                    .catch((error) => {
                        console.log(error);
                    });
            }
        });
    });

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