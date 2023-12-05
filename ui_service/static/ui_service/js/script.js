

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