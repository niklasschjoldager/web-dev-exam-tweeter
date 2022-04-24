export default function setupForms(selector) {
  const forms = Array.from(document.querySelectorAll(selector)).filter((form) => form.hasAttribute("data-validate"))
  forms.forEach(prepareForm)
}

export function prepareForm(form) {
  form.setAttribute("novalidate", "")

  const fields = Array.from(form.elements).filter(
    (element) => element.tagName == "INPUT" || element.tagName == "TEXTAREA"
  )
  const fieldsWithCounters = fields.filter((element) =>
    form.querySelector(`[data-counter="${element.getAttribute("id")}"]`)
  )
  fields.forEach((field) => {
    const id = field.getAttribute("id")
    const label = form.querySelector(`label[for="${id}"]`)
    const error = form.querySelector(`[data-error="${id}"]`)

    field.addEventListener("blur", () => {
      checkFieldValidity(field, label, error)
      validateField(field, label, error)
    })
    field.addEventListener("input", () => {
      checkFieldValidity(field, label, error)
      validateForm(form)
    })
  })

  fieldsWithCounters.forEach((field) => {
    handleFieldCounter(field, form)
    field.addEventListener("input", () => handleFieldCounter(field, form))
    field.addEventListener("change", () => handleFieldCounter(field, form))
    form.addEventListener("submit", () => resetFieldCounter(field, form))
  })

  validateForm(form)
}

function handleFieldCounter(field, form) {
  const maxLength = field.getAttribute("maxlength")
  if (!maxLength) return

  const currentLength = field.value.length
  const id = field.getAttribute("id")

  const counterCurrent = form.querySelector(`[data-current="${id}"]`)
  const counterMax = form.querySelector(`[data-max="${id}"]`)

  counterCurrent.textContent = currentLength
  counterMax.textContent = maxLength
}

function resetFieldCounter(field, form) {
  const maxLength = field.getAttribute("maxlength")
  if (!maxLength) return
  const id = field.getAttribute("id")

  const counterCurrent = form.querySelector(`[data-current="${id}"]`)

  counterCurrent.textContent = "0"
}

function validateForm(form) {
  const submitButton = form.querySelector('button[type="submit"]')

  if (!form.checkValidity()) {
    submitButton.setAttribute("disabled", "")
    return
  }

  submitButton.removeAttribute("disabled")
}

function validateField(field, label, error) {
  if (!field.value) {
    label && label.classList.remove("is-invalid")
    field.classList.remove("is-invalid")
    error && error.classList.add("hidden")
    return
  }

  for (const key in field.validity) {
    if (field.validity[key] && key != "valid") {
      const formattedKey = uppercaseToDashesAndLowercase(key)
      const errorMessage = field.getAttribute(`data-error-${formattedKey}`)
      if (error) {
        error.textContent = errorMessage
        error.classList.remove("hidden")
      }
      field.classList.add("is-invalid")
      label && label.classList.add("is-invalid")
      break
    }
  }
}

function uppercaseToDashesAndLowercase(string) {
  return string
    .split(/(?=[A-Z])/)
    .join("-")
    .toLowerCase()
}

function checkFieldValidity(field, label, error) {
  if (field.checkValidity()) {
    field.classList.remove("is-invalid")
    label && label.classList.remove("is-invalid")
    if (error) {
      error.classList.add("hidden")
      error.textContent = ""
    }
  }
}
