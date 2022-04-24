import { handleAddImage } from "../utils.js"
import { prepareForm } from "../forms/forms.js"

export default async function handleEditUser(id) {
  const template = document.querySelector("[data-template=modal-edit-user]").content.cloneNode(true)
  const modal = template.querySelector("[data-modal=edit-user")
  const form = template.querySelector("[data-form]")
  const saveButton = template.querySelector("[data-modal-action=save-user]")
  const dismissButtons = template.querySelectorAll("[data-modal-dismiss]")

  const removeCoverImageButton = template.querySelector("[data-button=remove-cover-image]")
  const addCoverImageButton = template.querySelector("[data-button=add-cover-image]")
  const coverImageInput = template.querySelector("[data-field=cover-image-input]")
  const coverImageField = template.querySelector("[data-field=cover-image]")

  const profileImageButton = template.querySelector("[data-button=add-profile-image]")
  const profileImageInput = template.querySelector("[data-field=profile-image-input]")
  const profileImageField = template.querySelector("[data-field=profile-image]")

  const user = getUser()
  setUser(modal, user)

  const hasUserCoverImage = coverImageField.getAttribute("src") != "#" ? true : false
  if (hasUserCoverImage) {
    removeCoverImageButton.classList.remove("is-hidden")
  }

  addCoverImageButton.addEventListener("click", () => coverImageInput.click())
  removeCoverImageButton.addEventListener("click", () => {
    coverImageInput.value = ""
    coverImageField.classList.add("is-hidden")
    coverImageField.src = "#"
    removeCoverImageButton.classList.add("is-hidden")
  })
  profileImageButton.addEventListener("click", () => profileImageInput.click())

  coverImageInput.addEventListener("change", () => {
    handleAddImage(coverImageInput, coverImageField)
    coverImageField.classList.remove("is-hidden")
    removeCoverImageButton.classList.remove("is-hidden")
  })
  profileImageInput.addEventListener("change", () => handleAddImage(profileImageInput, profileImageField))

  dismissButtons.forEach((button) =>
    button.addEventListener("click", () => {
      document.body.classList.remove("modal-is-open")
      modal.remove()
    })
  )
  saveButton.addEventListener("click", async function () {
    const user = await requestEditUser(id, modal)
    updateUser(user)
    document.body.classList.remove("modal-is-open")
    modal.remove()
  })

  document.body.classList.add("modal-is-open")
  document.body.append(template)
  prepareForm(form)
}

function updateUser(user) {
  const {
    user_name: name,
    user_bio: bio,
    user_location: location,
    user_website: website,
    user_cover_image: coverImage,
    user_profile_image: profileImage,
  } = user

  const nameField = document.querySelector('[data-field="user-name"]')
  const bioField = document.querySelector('[data-field="user-bio"]')
  const coverImageField = document.querySelector('[data-field="user-cover-image"]')
  const profileImageField = document.querySelector('[data-field="user-profile-image"]')
  const locationField = document.querySelector('[data-field="user-location"]')
  const locationFieldContainer = document.querySelector('[data-field="user-location-container"]')
  const websiteText = document.querySelector('[data-field="user-website-text"]')
  const websiteLink = document.querySelector('[data-field="user-website-link"]')

  nameField.textContent = name

  if (bio) {
    bioField.textContent = bio
    bioField.classList.remove("is-hidden")
  } else {
    bioField.textContent = ""
    bioField.classList.add("is-hidden")
  }

  if (location) {
    locationField.textContent = location
    locationFieldContainer.classList.remove("is-hidden")
  } else {
    locationField.textContent = ""
    locationFieldContainer.classList.add("is-hidden")
  }

  if (website) {
    websiteText.textContent = website
    websiteLink.href = `https://${website}`
    websiteLink.classList.remove("is-hidden")
  } else {
    websiteText.textContent = ""
    websiteLink.href = "#"
    websiteLink.classList.add("is-hidden")
  }

  if (coverImage) {
    coverImageField.src = `/static/users/${coverImage}`
    coverImageField.classList.remove("is-hidden")
  } else if (coverImage === null) {
    coverImageField.src = "#"
    coverImageField.classList.add("is-hidden")
  }

  if (profileImage) {
    profileImageField.src = `/static/users/${profileImage}`
  }
}

function getUser() {
  const name = document.querySelector('[data-field="user-name"]').textContent
  const bio = document.querySelector('[data-field="user-bio"]').textContent
  const location = document.querySelector('[data-field="user-location"]').textContent
  const website = document.querySelector('[data-field="user-website-text"]').textContent
  const coverImage = document.querySelector('[data-field="user-cover-image"]').getAttribute("src")
  const profileImage = document.querySelector('[data-field="user-profile-image"]').getAttribute("src")

  return { name, bio, location, website, coverImage, profileImage }
}

function setUser(modal, user) {
  const { name, bio, location, website, coverImage, profileImage } = user
  const nameField = modal.querySelector("[data-field=edit-user-name]")
  const bioField = modal.querySelector("[data-field=edit-user-bio]")
  const locationField = modal.querySelector("[data-field=edit-user-location]")
  const websiteField = modal.querySelector("[data-field=edit-user-website]")
  const coverImageField = modal.querySelector('[data-field="cover-image"]')
  const profileImageField = modal.querySelector('[data-field="profile-image"]')

  if (coverImage != "#") {
    coverImageField.src = coverImage
    coverImageField.classList.remove("is-hidden")
  } else {
    coverImageField.classList.add("is-hidden")
  }

  if (profileImage != "#") {
    profileImageField.src = profileImage
    profileImageField.classList.remove("is-hidden")
  }

  nameField.value = name
  bioField.value = bio
  locationField.value = location
  websiteField.value = website
}

async function requestEditUser(id, modal) {
  event.preventDefault()
  const form = modal.querySelector("[data-form=edit-user]")
  const formData = new FormData(form)

  const coverImageField = modal.querySelector('[data-field="cover-image"]').getAttribute("src")
  const userCoverImage = document.querySelector('[data-field="user-cover-image"]').getAttribute("src")

  if (coverImageField == userCoverImage) {
    formData.delete("user_cover_image")
  }

  const request = await fetch(`/users/${id}`, {
    method: "PUT",
    body: formData,
  })
  const response = await request
  if (!response.ok) return alert("Could not edit user")

  const data = await response.json()

  return data
}
