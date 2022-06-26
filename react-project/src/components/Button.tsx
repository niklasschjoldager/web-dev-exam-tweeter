import classNames from "classnames"

type buttonProps = {
  as?: "button" | "a"
  children: React.ReactNode
  className?: string
  size?: "sm" | "base" | "lg"
  variant?: "primary" | "primary-outlined" | "outlined" | "dark" | "danger"
}

const sizes = {
  sm: "px-4 h-[2rem] min-w-[2rem] text-sm",
  base: "px-8 h-[2.75rem] min-w-[2.75rem] text-base",
  lg: "px-8 h-[3.25rem] min-w-[3.25rem] text-base",
}
const variants = {
  primary: "text-white bg-primary-200 border-primary-200 hover:bg-primary-100 focus:bg-primary-100",
  "primary-outlined": "text-primary-200 border-gray-300 hover:bg-primary-200/10 focus:bg-primary-200/10",
  outlined: "text-black-200 border-gray-300 focus:bg-black-200/10 hover:bg-black-200/10",
  dark: "bg-black-200 border-black-200 focus:bg-opacity-90 hover:bg-opacity-90 text-white",
  danger: "bg-danger-200 border-danger-200 focus:bg-danger-100 hover:bg-danger-100 text-white",
}
const baseStyles =
  "flex items-center justify-center font-semibold transition-colors border rounded-full outline-none cursor-pointer"

export default function Button(props: buttonProps) {
  const { as = "button", children, className: restClasses, size = "base", variant = "outlined" } = props
  const Element = as

  return <Element className={classNames(baseStyles, sizes[size], variants[variant], restClasses)}>{children}</Element>
}
