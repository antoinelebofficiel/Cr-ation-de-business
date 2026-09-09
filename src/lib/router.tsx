import { type MouseEvent, type ReactNode } from 'react'
import { navigate } from './path'

export function Link({
  href,
  children,
  className,
}: {
  href: string
  children: ReactNode
  className?: string
}) {
  const onClick = (event: MouseEvent<HTMLAnchorElement>) => {
    if (
      event.defaultPrevented ||
      event.button !== 0 ||
      event.metaKey ||
      event.ctrlKey ||
      event.shiftKey ||
      event.altKey
    ) {
      return
    }
    event.preventDefault()
    navigate(href)
  }

  return (
    <a href={href} className={className} onClick={onClick}>
      {children}
    </a>
  )
}
