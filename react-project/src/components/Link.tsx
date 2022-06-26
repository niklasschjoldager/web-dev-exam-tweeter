type linkProps = {
  children: React.ReactNode
  to: string
}

export default function Link(props: linkProps) {
  const { children, to } = props
  return (
    <a href={to} className="text-primary-200 hover:underline">
      {children}
    </a>
  )
}
