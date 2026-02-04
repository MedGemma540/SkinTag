import { Info } from 'lucide-react'
import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Sheet, SheetContent } from '@/components/ui/sheet'

export function Header() {
  const [showInfo, setShowInfo] = useState(false)

  return (
    <>
      <header className="flex flex-col items-center gap-3 pt-8 pb-6 relative">
        <Button
          onClick={() => setShowInfo(true)}
          variant="ghost"
          size="icon"
          className="absolute right-0 top-8 rounded-full"
          aria-label="About"
        >
          <Info className="w-5 h-5" />
        </Button>

        <h1 className="text-[40px] leading-[1.1] tracking-tight" style={{ fontFamily: "'Instrument Serif', serif" }}>
          Skin<span className="text-[var(--color-accent-warm)]" style={{ fontStyle: 'italic' }}>Tag</span>
        </h1>
        <p className="text-[15px] text-[var(--color-text-secondary)] text-center max-w-md">
          AI-powered skin lesion risk assessment
        </p>
      </header>

      <Sheet open={showInfo} onOpenChange={setShowInfo}>
        <SheetContent>
          <div className="space-y-6 pt-4">
            <div>
              <h2 className="text-[28px] leading-tight font-semibold mb-2" style={{ fontFamily: "'Instrument Serif', serif" }}>
                About SkinTag
              </h2>
              <p className="text-[15px] text-[var(--color-text-secondary)] leading-relaxed">
                Advanced AI technology for evaluating skin lesion risk.
              </p>
            </div>

            <div>
              <h3 className="text-[17px] font-semibold mb-2">Training Data</h3>
              <p className="text-[15px] text-[var(--color-text-secondary)] leading-relaxed">
                Trained on 10,015 clinical dermoscopy images from multiple medical institutions.
              </p>
            </div>

            <div className="bg-[var(--color-red-bg)] border border-[var(--color-red)] rounded-[var(--radius-lg)] p-4">
              <h3 className="text-[15px] font-semibold text-[var(--color-red)] mb-2">
                Medical Disclaimer
              </h3>
              <p className="text-[13px] text-[var(--color-text-secondary)] leading-relaxed">
                This tool is for educational purposes only and should not replace professional medical advice.
                Always consult a healthcare provider for skin concerns.
              </p>
            </div>

            <div>
              <h3 className="text-[17px] font-semibold mb-2">How It Works</h3>
              <ul className="space-y-2 text-[15px] text-[var(--color-text-secondary)]">
                <li>• Upload or capture a photo of your skin lesion</li>
                <li>• AI analyzes the image for melanoma risk</li>
                <li>• Receive risk assessment and recommendations</li>
                <li>• History saved locally for tracking changes</li>
              </ul>
            </div>
          </div>
        </SheetContent>
      </Sheet>
    </>
  )
}
