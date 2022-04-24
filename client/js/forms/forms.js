export default function setupForms(selector) {
  const forms = document.querySelectorAll(selector)
  forms.forEach(prepareForm)
}

function prepareForm(form) {
  form.setAttribute("novalidate", "")

  const inputs = Array.from(form.elements).filter((element) => element.tagName == "INPUT")
  const inputsWithCounters = inputs.filter((element) =>
    form.querySelector(`[data-counter="${element.getAttribute("id")}"]`)
  )
  inputs.forEach((input) => {
    const id = input.getAttribute("id")
    const label = form.querySelector(`label[for="${id}"]`)
    const error = form.querySelector(`[data-error="${id}"]`)
    const type = input.getAttribute("type")
    const counter = form.querySelector(`[data-counter=${id}]`)

    input.addEventListener("blur", () => {
      checkInputValidity(input, label, error)
      validateInput(input, type, label, error)
    })
    input.addEventListener("input", () => {
      checkInputValidity(input, label, counter, error)
      validateForm(form)
    })
  })

  inputsWithCounters.forEach((input) => {
    handleInputCounter(input)
    input.addEventListener("input", () => handleInputCounter(input))
  })

  validateForm(form)
}

function handleInputCounter(input) {
  const maxLength = input.getAttribute("maxlength")
  if (!maxLength) return

  const currentLength = input.value.length
  const id = input.getAttribute("id")

  const counterCurrent = document.querySelector(`[data-current="${id}"]`)
  const counterMax = document.querySelector(`[data-max="${id}"]`)

  counterCurrent.textContent = currentLength
  counterMax.textContent = maxLength
}

function validateForm(form) {
  const submitButton = form.querySelector('button[type="submit"]')

  console.log(form.checkValidity())

  if (!form.checkValidity()) {
    submitButton.setAttribute("disabled", "")
    return false
  }

  submitButton.removeAttribute("disabled")
  return true
}

function validateInput(input, type, label, error) {
  if (!input.value) {
    label.classList.remove("is-invalid")
    input.classList.remove("is-invalid")
    error.classList.add("hidden")
    return
  }

  const errorMessages = {
    email: {
      valueMissing: "What's your e-mail?",
      patternMismatch: "Please enter a valid e-mail.",
      typeMismatch: "Please enter a valid e-mail",
    },
    password: {
      valueMissing: "Please enter a password.",
      patternMismatch:
        "Password must be at least 8 characters long, have 1 uppercase letter, 1 lowercase letter and 1 number or symbol",
      tooShort:
        "Password must be at least 8 characters long, have 1 uppercase letter, 1 lowercase letter and 1 number or symbol",
    },
  }

  for (const key in input.validity) {
    console.log(type)
    if (input.validity[key] && key != "valid") {
      if (errorMessages[type] && errorMessages[type][key]) error.textContent = errorMessages[type][key]
      input.classList.add("is-invalid")
      label.classList.add("is-invalid")
      error.classList.remove("hidden")
      break
    }
  }
}

function checkInputValidity(input, label, error) {
  if (input.checkValidity()) {
    input.classList.remove("is-invalid")
    label.classList.remove("is-invalid")
    error.classList.add("hidden")
    error.textContent = ""
  }
}
