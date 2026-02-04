import { AlertTriangle } from 'lucide-react'

export function DisclaimerBanner() {
  return (
    <div className="bg-[var(--color-red-bg)] border border-[var(--color-red)] rounded-[var(--radius)] px-3 py-2 flex gap-2 items-start">
      <AlertTriangle className="w-4 h-4 text-[var(--color-red)] flex-shrink-0 mt-0.5" />
      <p className="text-[13px] leading-snug text-[var(--color-text-secondary)]">
        <strong className="font-semibold text-[var(--color-red)]">Not medical advice.</strong> For educational purposes only. Consult a healthcare provider for diagnosis.
      </p>
    </div>
  )
}
