export function Header() {
  return (
    <header className="flex flex-col items-center gap-2.5 pt-6 pb-5">
      <h1 className="text-[36px] sm:text-[42px] leading-[1.1] tracking-tight" style={{ fontFamily: "'Instrument Serif', serif", fontStyle: 'italic' }}>
        SkinTag
      </h1>
      <p className="text-[14px] sm:text-[15px] text-[var(--color-text-secondary)] text-center max-w-md px-4">
        AI-powered skin lesion risk assessment
      </p>
      <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-[var(--color-surface)] border text-[12px] text-[var(--color-text-muted)]">
        <div className="w-1.5 h-1.5 rounded-full bg-[var(--color-green)]" />
        Trained on clinical dermoscopy images
      </div>
    </header>
  )
}
