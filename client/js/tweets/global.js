import handleDeleteTweet from "./deleteTweet.js"
import handleEditTweet from "./editTweet.js"
import handleLikeTweet from "./likeTweet.js"
import handleUnlikeTweet from "./unlikeTweet.js"

export function displayTweet(tweet) {
  const {
    tweet_id: id,
    tweet_image_file_name: image_file_name,
    tweet_text: text,
    user_username: username,
    user_name: name,
  } = tweet

  const hook = document.querySelector("[data-hook=tweets]")
  const template = document.querySelector("[data-template=tweet-item]").content.cloneNode(true)
  const form = template.querySelector("[data-form=tweet]")
  template.querySelector("[data-form=tweet]").setAttribute("data-id", id)
  template.querySelector("[data-field=text]").textContent = text
  template.querySelector("[data-field=username]").href = `/users/${username}`
  template.querySelector("[data-field=username]").textContent = `@${username}`
  template.querySelector("[data-field=name-link]").href = `/users/${username}`
  template.querySelector("[data-field=name]").textContent = name

  if (image_file_name) {
    template.querySelector("[data-field=image]").src = `static/tweets/${image_file_name}`
    template.querySelector("[data-field=image]").classList.remove("is-hidden")
  } else {
    template.querySelector("[data-field=image]").src = "#"
    template.querySelector("[data-field=image]").classList.add("is-hidden")
  }

  prepareTweet(form)
  hook.prepend(template)
}

export function prepareTweet(tweet) {
  const id = tweet.dataset.id

  const deleteButton = tweet.querySelector("[data-button=delete]")
  const editButton = tweet.querySelector("[data-button=edit]")
  const likeButton = tweet.querySelector("[data-button=like]")
  const unlikeButton = tweet.querySelector("[data-button=unlike]")

  deleteButton.addEventListener("click", () => handleDeleteTweet(id, tweet))
  editButton.addEventListener("click", () => handleEditTweet(id, tweet))
  likeButton.addEventListener("click", () => handleLikeTweet(id, tweet))
  unlikeButton.addEventListener("click", () => handleUnlikeTweet(id, tweet))
}

export function resetForm(form) {
  const tweetImageContainer = form.querySelector("[data-hook=tweet-image-container]")
  const tweetImage = form.querySelector("[data-hook=tweet-image]")
  tweetImageContainer.classList.add("is-hidden")
  tweetImage.src = ""

  form.reset()
  form.elements["tweet_text"].style.height = ""

  const isModal = form.closest("[data-modal]")

  if (isModal) {
    document.body.classList.remove("modal-is-open")
    isModal.classList.add("is-hidden")
  }
}

export function handleAddImage(imageInput, image, imageContainer) {
  const selectedFile = imageInput.files[0]

  if (!selectedFile) return imageContainer.classList.add("is-hidden")

  image.src = URL.createObjectURL(selectedFile)
  imageContainer.classList.remove("is-hidden")
}

export function handleRemoveImage(image, imageContainer) {
  image.src = ""
  imageContainer.classList.add("is-hidden")
}
