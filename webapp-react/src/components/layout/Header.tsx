export function Header() {
  return (
    <header className="flex flex-col items-center gap-2 pt-6 pb-4">
      <div className="flex items-center gap-2 flex-wrap justify-center">
        <h1 className="text-[28px] sm:text-[32px] leading-[1.1] tracking-tight" style={{ fontFamily: "'Instrument Serif', serif", fontStyle: 'italic' }}>
          SkinTag
        </h1>
        <div className="flex items-center gap-1.5 px-2 py-1 rounded-full bg-[var(--color-surface)] border text-[11px] text-[var(--color-text-muted)]">
          <div className="w-1 h-1 rounded-full bg-[var(--color-green)]" />
          <span className="hidden sm:inline">Clinical AI</span>
          <span className="inline sm:hidden">AI</span>
        </div>
      </div>
      <p className="text-[13px] sm:text-[14px] text-[var(--color-text-secondary)] text-center max-w-md px-4">
        AI-powered skin lesion risk assessment
      </p>
    </header>
  )
}
