// script.js

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
  
  // Get all like buttons
  const likeButtons = document.querySelectorAll('.like-button');
  
  // Attach event listener to each like button
  likeButtons.forEach((button) => {
    button.addEventListener('click', (event) => {
      event.stopPropagation(); // Prevent click event propagation
  
      const postId = button.dataset.postId;
      const likeCountElement = document.querySelector(`#like-count-${postId}`);
  
      // Send a POST request to the like URL
      fetch(`/posts/${postId}/like/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': '{{ csrf_token }}', // Include the CSRF token
        },
      })
        .then((response) => response.json())
        .then((data) => {
          // Update the like count on the page
          likeCountElement.textContent = data.like_count;
  
          // Update the button text based on the like status
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
  